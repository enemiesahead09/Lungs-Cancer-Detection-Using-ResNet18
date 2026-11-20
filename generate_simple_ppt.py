import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_simple_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean Modern Palette
    BG_COLOR = RGBColor(15, 23, 42)        # Slate 900
    CARD_BG = RGBColor(30, 41, 59)          # Slate 800
    BORDER_COLOR = RGBColor(51, 65, 85)     # Slate 700
    PRIMARY_CYAN = RGBColor(56, 189, 248)   # Sky 400
    TEXT_WHITE = RGBColor(248, 250, 252)    # Slate 50
    TEXT_LIGHT = RGBColor(203, 213, 225)    # Slate 300
    GREEN_COLOR = RGBColor(52, 211, 153)    # Emerald 400
    AMBER_COLOR = RGBColor(251, 191, 36)    # Amber 400
    RED_COLOR = RGBColor(248, 113, 113)     # Red 400

    def add_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category="CSE471 • PROJECT PRESENTATION"):
        header = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.05))
        header.fill.solid()
        header.fill.fore_color.rgb = CARD_BG
        header.line.color.rgb = BORDER_COLOR
        header.line.width = Pt(1)

        tf = header.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.35)

        p1 = tf.paragraphs[0]
        p1.text = category
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY_CYAN

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE

    def add_box(slide, left, top, width, height, title, bullet_points, title_color=PRIMARY_CYAN):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = BORDER_COLOR
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.25)
        tf.margin_bottom = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = title_color
        p.space_after = Pt(14)

        for pt in bullet_points:
            p_pt = tf.add_paragraph()
            p_pt.text = f"•  {pt}"
            p_pt.font.size = Pt(14)
            p_pt.font.color.rgb = TEXT_LIGHT
            p_pt.space_after = Pt(10)

        return box

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_background(s1)

    # Left cyan accent stripe
    stripe = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(5.1))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = PRIMARY_CYAN
    stripe.line.fill.background()

    # Title text box
    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.3), Inches(3.2))
    tf1 = tb.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "COURSE: CSE471"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_CYAN
    p.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Lung Disease & Cancer Detection System"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_after = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "Multi-Class Thoracic CT Classification with Explainable AI (Grad-CAM)"
    p3.font.size = Pt(18)
    p3.font.color.rgb = TEXT_LIGHT

    # Presenter Details Card
    c1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.5), Inches(11.3), Inches(1.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = PRIMARY_CYAN
    c1.line.width = Pt(1.5)

    c1_tf = c1.text_frame
    c1_tf.margin_left = Inches(0.4)
    c1_tf.margin_top = Inches(0.2)

    cp1 = c1_tf.paragraphs[0]
    cp1.text = "STUDENT DETAILS"
    cp1.font.size = Pt(12)
    cp1.font.bold = True
    cp1.font.color.rgb = PRIMARY_CYAN
    cp1.space_after = Pt(4)

    cp2 = c1_tf.add_paragraph()
    cp2.text = "Name                    : Shaurya Kumar Rai"
    cp2.font.size = Pt(16)
    cp2.font.bold = True
    cp2.font.color.rgb = TEXT_WHITE

    cp3 = c1_tf.add_paragraph()
    cp3.text = "Registration Number : 12405723"
    cp3.font.size = Pt(15)
    cp3.font.bold = True
    cp3.font.color.rgb = TEXT_WHITE

    cp4 = c1_tf.add_paragraph()
    cp4.text = "Course Code         : CSE471"
    cp4.font.size = Pt(15)
    cp4.font.bold = True
    cp4.font.color.rgb = PRIMARY_CYAN

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Problem Statement & Clinical Motivation")

    add_box(s2, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9), "The Clinical Need", [
        "Lung cancer is the leading cause of cancer deaths worldwide (~1.8 million deaths annually).",
        "Early detection at Stage I significantly increases patient 5-year survival rates to over 60%.",
        "Low-Dose CT (Computed Tomography) screening is the standard tool to spot pulmonary nodules early."
    ], PRIMARY_CYAN)

    add_box(s2, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.9), "The Challenge & Solution", [
        "Each CT scan produces hundreds of slices, making manual review slow and prone to fatigue.",
        "Differentiating harmless benign nodules from malignant lesions is visually subtle and difficult.",
        "Our Solution: An automated Deep Learning classifier with Explainable AI to assist doctors quickly and accurately."
    ], GREEN_COLOR)

    # =========================================================================
    # SLIDE 3: DATASET OVERVIEW
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "Dataset Overview: The Lung Cancer CT Dataset")

    add_box(s3, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9), "Dataset Distribution", [
        "Total CT Images: 14,819 axial thoracic CT scan slices.",
        "Malignant Cases: 5,640 images (38.1%) — Cancerous lesions with irregular margins.",
        "Benign Cases: 5,019 images (33.9%) — Non-cancerous, circumscribed nodules.",
        "Normal Cases: 4,160 images (28.1%) — Healthy lung tissue with clear parenchyma.",
        "Split into stratified sets for training, validation, and evaluation."
    ], PRIMARY_CYAN)

    # Right side: Visual scans
    scans_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.9))
    scans_card.fill.solid()
    scans_card.fill.fore_color.rgb = CARD_BG
    scans_card.line.color.rgb = BORDER_COLOR
    stf = scans_card.text_frame
    stf.margin_left = Inches(0.3)
    stf.margin_top = Inches(0.2)
    sp = stf.paragraphs[0]
    sp.text = "Sample CT Slices"
    sp.font.size = Pt(18)
    sp.font.bold = True
    sp.font.color.rgb = GREEN_COLOR

    if os.path.exists("sample_scans/Normal_Case_Sample1.jpg"):
        s3.shapes.add_picture("sample_scans/Normal_Case_Sample1.jpg", Inches(7.2), Inches(2.7), Inches(1.5), Inches(1.5))
        t1 = s3.shapes.add_textbox(Inches(8.9), Inches(2.9), Inches(3.3), Inches(1.0))
        t1.text_frame.text = "Normal Case\nClear lung parenchyma."
        t1.text_frame.paragraphs[0].font.size = Pt(13)
        t1.text_frame.paragraphs[0].font.color.rgb = GREEN_COLOR

    if os.path.exists("sample_scans/Benign_Case_Sample1.jpg"):
        s3.shapes.add_picture("sample_scans/Benign_Case_Sample1.jpg", Inches(7.2), Inches(4.0), Inches(1.3), Inches(1.3))
        t2 = s3.shapes.add_textbox(Inches(8.9), Inches(4.1), Inches(3.3), Inches(1.0))
        t2.text_frame.text = "Benign Nodule\nSmooth, well-defined nodule."
        t2.text_frame.paragraphs[0].font.size = Pt(13)
        t2.text_frame.paragraphs[0].font.color.rgb = AMBER_COLOR

    if os.path.exists("sample_scans/Malignant_Case_Sample1.jpg"):
        s3.shapes.add_picture("sample_scans/Malignant_Case_Sample1.jpg", Inches(7.2), Inches(5.2), Inches(1.3), Inches(1.3))
        t3 = s3.shapes.add_textbox(Inches(8.9), Inches(5.3), Inches(3.3), Inches(1.0))
        t3.text_frame.text = "Malignant Case\nIrregular, spiculated tumor."
        t3.text_frame.paragraphs[0].font.size = Pt(13)
        t3.text_frame.paragraphs[0].font.color.rgb = RED_COLOR

    # =========================================================================
    # SLIDE 4: DEEP LEARNING ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "Model Architecture: ResNet-18 Transfer Learning")

    add_box(s4, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.9), "1. ResNet Backbone", [
        "Pre-trained ResNet-18 initialized on ImageNet.",
        "Uses Residual Skip Connections [F(x) + x].",
        "Solves the vanishing gradient problem in deep networks.",
        "Captures subtle lung nodule edges and textures effectively."
    ], PRIMARY_CYAN)

    add_box(s4, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.9), "2. Custom Head", [
        "Global Average Pooling (GAP) compresses features to 512-dim vector.",
        "Dense projection: 512 to 128 with ReLU activation.",
        "Dropout layer (40%) to prevent model overfitting.",
        "Output layer: 3 classes with Softmax probability scores."
    ], GREEN_COLOR)

    add_box(s4, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.9), "3. Fine-Tuning Strategy", [
        "Early layers frozen to retain generalized edge/texture filters.",
        "Deep residual blocks (layer 3 & 4) fine-tuned on CT scans.",
        "Enables faster training and higher generalization accuracy on small medical datasets."
    ], AMBER_COLOR)

    # =========================================================================
    # SLIDE 5: TRAINING & OPTIMIZATION PIPELINE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "Training Pipeline & Optimization")

    add_box(s5, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9), "Data Preprocessing & Augmentation", [
        "Image Normalization: Resized to 224×224 px with standard ImageNet mean and std.",
        "Random Horizontal Flips: Mimics lung bilateral symmetry.",
        "Random Rotations (±15°): Simulates slight patient tilt during CT scanning.",
        "Contrast Adjustments: Simulates variations in CT scanner window levels.",
        "Stratified Split: 80% Training, 10% Validation, 10% Held-Out Testing."
    ], PRIMARY_CYAN)

    add_box(s5, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.9), "Optimization Settings", [
        "Loss Function: Categorical Cross-Entropy Loss.",
        "Optimizer: AdamW (Adaptive Moment Estimation with Decoupled Weight Decay).",
        "Learning Rate: 1e-3 with Cosine Annealing scheduler for smooth convergence.",
        "Regularization: Weight decay (1e-4) + 40% Dropout to avoid overfitting.",
        "Model Checkpointing: Best model weights automatically saved on peak validation accuracy."
    ], GREEN_COLOR)

    # =========================================================================
    # SLIDE 6: EXPLAINABLE AI (GRAD-CAM)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "Explainable AI (Grad-CAM) Visual Localization")

    add_box(s6, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9), "Why Explainable AI is Critical", [
        "Clinical Requirement: Doctors cannot trust a 'black-box' prediction without seeing the reasoning.",
        "Grad-CAM (Gradient-weighted Class Activation Mapping) calculates gradients at the final conv layer.",
        "Creates a 2D activation heatmap showing the exact nodule region responsible for the classification.",
        "Proves the model is focusing on actual lesions, not irrelevant background artifacts."
    ], PRIMARY_CYAN)

    # Right side: Visual Grad-CAM card
    g_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.9))
    g_card.fill.solid()
    g_card.fill.fore_color.rgb = CARD_BG
    g_card.line.color.rgb = BORDER_COLOR
    gtf = g_card.text_frame
    gtf.margin_left = Inches(0.3)
    gtf.margin_top = Inches(0.2)
    gp = gtf.paragraphs[0]
    gp.text = "Visual Nodule Localization"
    gp.font.size = Pt(18)
    gp.font.bold = True
    gp.font.color.rgb = GREEN_COLOR

    if os.path.exists("sample_scans/Malignant_Case_Sample1.jpg"):
        s6.shapes.add_picture("sample_scans/Malignant_Case_Sample1.jpg", Inches(7.2), Inches(2.7), Inches(2.4), Inches(2.4))
        glbl = s6.shapes.add_textbox(Inches(9.8), Inches(2.8), Inches(2.4), Inches(2.6))
        glbl.text_frame.word_wrap = True
        glbl.text_frame.text = "How It Works:\n\n1. Target nodule creates strong activation gradients.\n\n2. Heatmap highlights high-risk tissue.\n\n3. Transparent and clinically verifiable."
        glbl.text_frame.paragraphs[0].font.size = Pt(13)
        glbl.text_frame.paragraphs[0].font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 7: RESULTS & PERFORMANCE METRICS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "Model Results & Performance Evaluation")

    # 4 Metric cards across the top
    metric_data = [
        ("Test Accuracy", "88.1%", "Peak Val: 91.9%", PRIMARY_CYAN),
        ("Precision", "89.7%", "Low False Alarms", GREEN_COLOR),
        ("Recall", "88.1%", "High Sensitivity", AMBER_COLOR),
        ("F1-Score", "87.8%", "Balanced Metric", RED_COLOR),
    ]

    for idx, (label, val, sub, col) in enumerate(metric_data):
        m_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 2.98), Inches(1.9), Inches(2.78), Inches(1.5))
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = CARD_BG
        m_box.line.color.rgb = col
        m_box.line.width = Pt(1.5)

        mtf = m_box.text_frame
        mtf.margin_left = Inches(0.2)
        mtf.margin_top = Inches(0.15)
        mp1 = mtf.paragraphs[0]
        mp1.text = label
        mp1.font.size = Pt(11)
        mp1.font.color.rgb = TEXT_LIGHT

        mp2 = mtf.add_paragraph()
        mp2.text = val
        mp2.font.size = Pt(22)
        mp2.font.bold = True
        mp2.font.color.rgb = col

        mp3 = mtf.add_paragraph()
        mp3.text = sub
        mp3.font.size = Pt(11)
        mp3.font.color.rgb = TEXT_LIGHT

    # Bottom left: Confusion Matrix image
    if os.path.exists("models/confusion_matrix.png"):
        s7.shapes.add_picture("models/confusion_matrix.png", Inches(0.8), Inches(3.6), Inches(4.5), Inches(3.3))

    # Bottom right: Bullet points
    add_box(s7, Inches(5.6), Inches(3.6), Inches(6.9), Inches(3.3), "Key Findings", [
        "Near-zero false normal predictions on malignant cases (critical for patient safety).",
        "High precision (89.7%) prevents unnecessary invasive biopsy procedures for benign cases.",
        "Inference speed is under 50 ms per CT scan on standard laptop CPU (suitable for real-time clinics)."
    ], PRIMARY_CYAN)

    # =========================================================================
    # SLIDE 8: INTERACTIVE WEB UI (STREAMLIT PLATFORM)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "Interactive Web Application (PulmoScan AI)")

    add_box(s8, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9), "Key Application Features", [
        "Interactive Medical Dashboard: Developed with Streamlit and Plotly for intuitive use.",
        "1-Click Demo Scans: Pre-loaded Normal, Benign, and Malignant scans for instant class demonstration.",
        "Drag & Drop Upload: Upload any custom thoracic CT scan in JPG/PNG format.",
        "Real-Time Inference: Instant probability bars showing confidence for all 3 classes.",
        "Side-by-Side Visuals: Input scan, raw activation map, and superimposed Grad-CAM heatmap.",
        "Diagnostic Report: One-click generation of downloadable clinical radiology report."
    ], PRIMARY_CYAN)

    add_box(s8, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.9), "Three Streamlined Sections", [
        "1. CT Diagnostic Scanner: Upload or select scans, view predictions, Grad-CAM overlays, and reports.",
        "2. Dataset Explorer: Interactive charts showing the distribution and visual characteristics of all 14,819 scans.",
        "3. Model Architecture & Metrics: Shows ResNet-18 pipeline, confusion matrix, and training dynamics.",
        "One-Click Launcher: Double-click 'start_ui.bat' to run instantly on any Windows laptop."
    ], GREEN_COLOR)

    # =========================================================================
    # SLIDE 9: CONCLUSION & FUTURE WORK
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_background(s9)
    add_header(s9, "Conclusion & Future Work")

    add_box(s9, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9), "Project Summary", [
        "Built a robust end-to-end Deep Residual CNN classifier for 3-class lung CT diagnosis.",
        "Evaluated on 14,800+ scans, achieving 88.1% accuracy and 89.7% precision.",
        "Integrated Explainable AI (Grad-CAM) to provide transparent nodule visualization for doctors.",
        "Delivered a live, clean web application for real-time clinical screening."
    ], PRIMARY_CYAN)

    add_box(s9, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.9), "Future Improvements", [
        "3D Volumetric CNNs: Extending from 2D slices to full 3D CT volumes for whole-lung nodule tracking.",
        "Multi-Modal Integration: Combining imaging features with patient EHR data (smoking history, age).",
        "Hospital PACS Integration: Connecting directly to hospital systems using the DICOM medical protocol.",
        "Federated Learning: Collaborative training across hospitals while preserving patient privacy."
    ], AMBER_COLOR)

    # =========================================================================
    # SLIDE 10: THANK YOU & Q&A
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_background(s10)

    center_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.3), Inches(10.333), Inches(4.9))
    center_card.fill.solid()
    center_card.fill.fore_color.rgb = CARD_BG
    center_card.line.color.rgb = PRIMARY_CYAN
    center_card.line.width = Pt(2)

    ctf = center_card.text_frame
    ctf.vertical_anchor = MSO_ANCHOR.MIDDLE

    tp1 = ctf.paragraphs[0]
    tp1.alignment = PP_ALIGN.CENTER
    tp1.text = "THANK YOU!"
    tp1.font.size = Pt(36)
    tp1.font.bold = True
    tp1.font.color.rgb = PRIMARY_CYAN
    tp1.space_after = Pt(12)

    tp2 = ctf.add_paragraph()
    tp2.alignment = PP_ALIGN.CENTER
    tp2.text = "PulmoScan AI: Lung Disease & Cancer Detection System"
    tp2.font.size = Pt(22)
    tp2.font.bold = True
    tp2.font.color.rgb = TEXT_WHITE
    tp2.space_after = Pt(16)

    tp3 = ctf.add_paragraph()
    tp3.alignment = PP_ALIGN.CENTER
    tp3.text = "Presenter: Shaurya Kumar Rai   |   Reg No: 12405723   |   Course: CSE471"
    tp3.font.size = Pt(16)
    tp3.font.color.rgb = GREEN_COLOR
    tp3.space_after = Pt(20)

    tp4 = ctf.add_paragraph()
    tp4.alignment = PP_ALIGN.CENTER
    tp4.text = "Questions & Feedback Welcome"
    tp4.font.size = Pt(18)
    tp4.font.bold = True
    tp4.font.color.rgb = AMBER_COLOR

    output_filename = "Lung_Disease_Detection_Presentation_Shaurya_Kumar_Rai.pptx"
    prs.save(output_filename)
    print(f"Simple & clean presentation saved successfully as: {output_filename}")

if __name__ == "__main__":
    create_simple_presentation()
