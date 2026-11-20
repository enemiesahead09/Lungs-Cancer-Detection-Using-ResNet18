import os
import random
import json
import time
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Fix seeds for reproducibility
torch.manual_seed(42)
np.random.seed(42)
random.seed(42)

CLASSES = ["Bengin cases", "Malignant cases", "Normal cases"]
DATA_DIR = "TheLungCancerDataset"
OUTPUT_DIR = "models"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class LungCTDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        image = Image.open(path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, self.labels[idx]

def get_data_splits(samples_per_class=700):
    train_paths, train_labels = [], []
    val_paths, val_labels = [], []
    test_paths, test_labels = [], []

    for idx, c in enumerate(CLASSES):
        c_dir = os.path.join(DATA_DIR, c)
        all_imgs = [os.path.join(c_dir, f) for f in os.listdir(c_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(all_imgs)
        selected = all_imgs[:samples_per_class]

        n_train = int(len(selected) * 0.8)
        n_val = int(len(selected) * 0.1)

        train_paths.extend(selected[:n_train])
        train_labels.extend([idx] * n_train)

        val_paths.extend(selected[n_train:n_train+n_val])
        val_labels.extend([idx] * n_val)

        test_paths.extend(selected[n_train+n_val:])
        test_labels.extend([idx] * (len(selected) - (n_train + n_val)))

    return (train_paths, train_labels), (val_paths, val_labels), (test_paths, test_labels)

def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Transforms
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    eval_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    print("Splitting dataset...")
    (train_p, train_l), (val_p, val_l), (test_p, test_l) = get_data_splits(samples_per_class=700)
    print(f"Train samples: {len(train_p)}, Val samples: {len(val_p)}, Test samples: {len(test_p)}")

    train_ds = LungCTDataset(train_p, train_l, transform=train_transform)
    val_ds = LungCTDataset(val_p, val_l, transform=eval_transform)
    test_ds = LungCTDataset(test_p, test_l, transform=eval_transform)

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=32, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_ds, batch_size=32, shuffle=False, num_workers=0)

    print("Building ResNet18 model...")
    model = resnet18(weights=ResNet18_Weights.DEFAULT)

    # Freeze earlier layers, fine-tune layer3, layer4 and custom head
    for name, param in model.named_parameters():
        if "layer3" in name or "layer4" in name or "fc" in name:
            param.requires_grad = True
        else:
            param.requires_grad = False

    num_ftrs = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(num_ftrs, 128),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(128, len(CLASSES))
    )

    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=6)

    epochs = 6
    best_val_acc = 0.0
    best_model_path = os.path.join(OUTPUT_DIR, "lung_cancer_resnet18.pth")

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    print("Starting training...")
    start_time = time.time()
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        scheduler.step()
        train_loss = running_loss / total
        train_acc = correct / total

        # Validation
        model.eval()
        v_loss = 0.0
        v_correct = 0
        v_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                v_loss += loss.item() * images.size(0)
                _, predicted = outputs.max(1)
                v_total += labels.size(0)
                v_correct += predicted.eq(labels).sum().item()

        val_loss = v_loss / v_total
        val_acc = v_correct / v_total

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)

        print(f"Epoch [{epoch+1}/{epochs}] - Train Loss: {train_loss:.4f}, Train Acc: {train_acc*100:.2f}% | Val Loss: {val_loss:.4f}, Val Acc: {val_acc*100:.2f}%")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), best_model_path)
            print(f"  -> Model saved with Val Acc: {val_acc*100:.2f}%")

    total_time = time.time() - start_time
    print(f"Training completed in {total_time:.2f} seconds.")

    # Load best model for evaluation on test set
    model.load_state_dict(torch.load(best_model_path, map_location=device))
    model.eval()

    all_preds, all_labels, all_probs = [], [], []
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            probs = torch.softmax(outputs, dim=1)
            _, predicted = outputs.max(1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())
            all_probs.extend(probs.cpu().numpy())

    test_acc = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='weighted')
    cm = confusion_matrix(all_labels, all_preds)
    report = classification_report(all_labels, all_preds, target_names=CLASSES, output_dict=True)

    print(f"--- TEST SET EVALUATION ---")
    print(f"Test Accuracy: {test_acc*100:.2f}%")
    print(f"Test Precision: {precision*100:.2f}%")
    print(f"Test Recall: {recall*100:.2f}%")
    print(f"Test F1-Score: {f1*100:.2f}%")

    # Plot and save confusion matrix
    plt.figure(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=CLASSES, yticklabels=CLASSES)
    plt.title(f"Test Confusion Matrix (Accuracy: {test_acc*100:.1f}%)")
    plt.xlabel("Predicted Class")
    plt.ylabel("Actual Class")
    plt.tight_layout()
    cm_path = os.path.join(OUTPUT_DIR, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=200)
    plt.close()

    # Save metrics JSON
    metrics_data = {
        "test_accuracy": float(test_acc),
        "test_precision": float(precision),
        "test_recall": float(recall),
        "test_f1": float(f1),
        "best_val_accuracy": float(best_val_acc),
        "history": history,
        "classification_report": report,
        "classes": CLASSES,
        "total_dataset_counts": {
            "Bengin cases": len(os.listdir(os.path.join(DATA_DIR, "Bengin cases"))),
            "Malignant cases": len(os.listdir(os.path.join(DATA_DIR, "Malignant cases"))),
            "Normal cases": len(os.listdir(os.path.join(DATA_DIR, "Normal cases"))),
        }
    }
    with open(os.path.join(OUTPUT_DIR, "metrics.json"), "w") as f:
        json.dump(metrics_data, f, indent=4)

    print("Metrics and artifacts saved in models/")

if __name__ == "__main__":
    train()
