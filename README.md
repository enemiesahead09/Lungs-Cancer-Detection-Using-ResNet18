# 🫁 PulmoScan AI - Lung Disease & Cancer Detection System

An end-to-end Deep Learning system with **Explainable AI (Grad-CAM)** for automated detection and multi-class classification of lung disease and neoplasms from thoracic Computed Tomography (CT) scans.

---

## 📊 Dataset

The model is trained and evaluated on the **IQ-OTH/NCCD Lung Cancer Dataset** comprising **14,819 axial thoracic CT scan slices** categorized into three classes:
- **Malignant Cases**: 5,640 scans (Invasive malignant neoplasms, irregular borders, spiculation)
- **Benign Cases**: 5,019 scans (Circumscribed nodules, smooth margins, non-invasive granulomas)
- **Normal Cases**: 4,160 scans (Clear lung parenchyma without pathological lesions)

🔗 **Kaggle Dataset Link:** [https://www.kaggle.com/datasets/sangemjayaprakash/lung-cancer-14k](https://www.kaggle.com/datasets/sangemjayaprakash/lung-cancer-14k)

---

## 🚀 How to Run the Web Application

### Method 1: One-Click Launcher (Windows)
Double-click the **`start_ui.bat`** file in this folder. It will activate the conda environment and launch the UI at **`http://localhost:8501`**.

### Method 2: Via Terminal / PowerShell
Open your terminal in this project directory and run:
```bash
conda activate spam-detection
streamlit run app.py
```

---

## 🌟 Key Features

1. **🔬 Interactive Diagnostic Scanner**:
   - **Quick Demo Scans (1-Click)**: Instant test buttons for *Normal*, *Benign*, and *Malignant* cases for instantaneous testing.
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

---

## 📁 Project Directory Structure

```
Lungs Disease Detection/
│
├── app.py                      # Main Streamlit web application
├── gradcam.py                  # PyTorch Grad-CAM explainable AI engine
├── train_classifier.py         # Deep learning training script
├── start_ui.bat                # 1-click Windows launcher
├── requirements.txt            # Python dependencies
├── sample_scans/               # Pre-staged high-res test scans for live demo
│   ├── Normal_Case_Sample1.jpg
│   ├── Benign_Case_Sample1.jpg
│   └── Malignant_Case_Sample1.jpg
├── models/
│   ├── lung_cancer_resnet18.pth # Trained ResNet-18 model weights
│   ├── metrics.json             # Test set accuracy & performance metrics
│   └── confusion_matrix.png     # Evaluation confusion matrix plot
└── lung-cancer-cnn-classifier-main/ # Reference baseline models & notebooks
```

---

## 🔬 Model Performance & Results

- **Validation Accuracy (Peak)**: 91.90%
- **Test Accuracy**: 88.10%
- **Malignant Recall (Sensitivity)**: 100.0% (Zero false negatives)
- **Benign Precision**: 98.00%
- **Macro F1-Score**: 87.79%

---

## 📄 License

This project is licensed under the [MIT License](lung-cancer-cnn-classifier-main/LICENSE).
