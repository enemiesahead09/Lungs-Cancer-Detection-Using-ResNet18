# 🫁 PulmoScan AI - Lung Disease & Cancer Detection System

An end-to-end Deep Learning system with **Explainable AI (Grad-CAM)** for automated detection and multi-class classification of lung disease and neoplasms from thoracic Computed Tomography (CT) scans.

---

## 🚀 How to Run the Web Application

### Method 1: One-Click Launcher (Easiest)
Simply double-click the **`start_ui.bat`** file in this folder. It will automatically activate your environment and launch the UI in your default web browser at **`http://localhost:8501`**.

### Method 2: Via Terminal / PowerShell
Open your terminal in this project directory and run:
```bash
conda activate spam-detection
streamlit run app.py
```

---

## 🌟 Key Features for Your Class Presentation

1. **🔬 Interactive Diagnostic Scanner**:
   - **Quick Demo Scans (1-Click)**: Instant test buttons for *Normal*, *Benign*, and *Malignant* cases—no need to search for files during your live presentation!
   - **Custom Upload**: Drag and drop any `.jpg` or `.png` thoracic CT scan.
   - **Multi-Class Confidence Scores**: Real-time probabilities for all 3 classes (*Normal*, *Benign Nodule*, *Malignant Neoplasm*).

2. **🔥 Explainable AI (Grad-CAM Heatmaps)**:
   - Visual localization showing exactly which lung nodules or tissue anomalies the CNN focused on to make its diagnosis.
   - Interactive opacity slider and colormap switcher (`jet`, `inferno`, `magma`, `viridis`).

3. **📋 Automated Clinical Radiology Report**:
   - Generates a clinical summary with unique Scan ID, timestamp, risk tier, histological characteristics, and medical follow-up recommendation.
   - Includes a one-click **"Download Diagnostic Report (.txt)"** button.

4. **📊 Dataset Explorer**:
   - Visual breakdown of the **14,819 CT scans** (5,019 Benign, 5,640 Malignant, 4,160 Normal).
   - Side-by-side radiological comparison of pathology types.

5. **🧠 Model Architecture & Evaluation**:
   - Deep Residual CNN (ResNet-18) transfer learning pipeline.
   - Confusion matrix, training/validation loss & accuracy dynamics, precision, recall, and F1-score.

6. **🎓 Built-In Presentation Guide & Viva Q&A**:
   - A dedicated tab with a ready-to-use 5-minute speaking script and the top professor questions with answers.

---

## 📁 Project Directory Structure
```
Lungs Disease Detection/
│
├── app.py                      # Main Streamlit web application
├── gradcam.py                  # PyTorch Grad-CAM explainable AI engine
├── train_classifier.py         # Deep learning training script
├── start_ui.bat                # 1-click Windows launcher
├── sample_scans/               # Pre-staged high-res test scans for live demo
│   ├── Normal_Case_Sample1.jpg
│   ├── Benign_Case_Sample1.jpg
│   └── Malignant_Case_Sample1.jpg
├── models/
│   ├── lung_cancer_resnet18.pth # Trained model weights
│   ├── metrics.json             # Test set accuracy & performance metrics
│   └── confusion_matrix.png     # Evaluation confusion matrix plot
├── TheLungCancerDataset/       # Original dataset (14,819 CT scans)
│   ├── Bengin cases/           # 5,019 scans
│   ├── Malignant cases/        # 5,640 scans
│   └── Normal cases/           # 4,160 scans
└── lung-cancer-cnn-classifier-main/ # Original project repository files
```

---

## 👨‍🏫 Viva Q&A Quick Reference

- **Q: Why use Transfer Learning?**
  *A:* Pre-trained weights from ImageNet give the convolutional layers strong feature extraction capabilities for edges, gradients, and textures, which prevents overfitting and accelerates convergence on medical imaging datasets.
- **Q: What does Grad-CAM do?**
  *A:* It calculates the gradients of the target class score with respect to the final convolutional feature maps, highlighting the spatial regions of the CT scan that contributed most to the prediction.
- **Q: How are Benign and Malignant nodules differentiated on CT?**
  *A:* Benign nodules typically display circumscribed, smooth borders and stable attenuation, whereas malignant lesions feature spiculated/lobulated margins, infiltrative growth, and architectural distortion.
