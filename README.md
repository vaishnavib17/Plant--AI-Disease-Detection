# PlantCare AI — Deep Learning-Based Plant Disease Detection System

An academic deep learning project developed for CSE Artificial Intelligence and Machine Learning students. PlantCare AI leverages **EfficientNetB0** (with transfer learning), a **Custom CNN baseline**, **Grad-CAM explainability**, and **uncertainty handling** to classify plant leaf health and diseases with high accuracy.

---

## 1. Project Overview & Architecture

PlantCare AI consists of:
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, and Lucide icons.
- **Backend**: Python FastAPI with TensorFlow/Keras inference pipeline.
- **Explainability**: Grad-CAM heatmaps highlighting influential leaf regions.
- **Dataset**: PlantVillage dataset (16 disease and healthy classes across Tomato, Potato, Corn, Apple, Grape, and Pepper).

---

## 2. Project Structure

```text
plantcare-ai/
  frontend/                  # React + TypeScript + Vite frontend
  backend/
    app/
      main.py                # FastAPI endpoints (/health, /predict, /explain, /metrics, /history)
      routes/
      services/
    models/                  # Saved model weights (.h5)
    dataset/                 # PlantVillage dataset directory
    training/
      train_efficientnet.py  # EfficientNetB0 transfer learning pipeline
      train_cnn.py           # Custom CNN baseline training pipeline
      evaluate.py            # Evaluation & metrics comparison script
    explainability/
      gradcam.py             # Grad-CAM heatmap generation module
    tests/
      test_api.py            # pytest automated backend tests
    requirements.txt
  README.md
  .gitignore
```

---

## 3. Prerequisites & Mac Setup

- Python 3.10+
- Node.js 18+ & npm
- macOS (Apple Silicon M1/M2/M3 or Intel)

### Python Virtual Environment Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Running Model Training & Evaluation

### Train EfficientNetB0 Transfer Learning Model
```bash
python training/train_efficientnet.py
```

### Train Custom CNN Baseline
```bash
python training/train_cnn.py
```

### Run Model Evaluation
```bash
python training/evaluate.py
```

### Run Automated Backend Tests
```bash
pytest tests/test_api.py
```

---

## 5. Starting the Application

### Start FastAPI Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Start React Frontend
```bash
# In project root directory
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000` and communicate with the FastAPI backend at `http://localhost:8000`.

---

## 6. API Documentation

- `GET /health` - Backend status and model load check.
- `GET /classes` - List of configured crop classes and diseases.
- `POST /predict` - Upload leaf image for disease classification and confidence scoring.
- `POST /explain` - Generate Grad-CAM explainability heatmaps.
- `GET /metrics` - Model performance comparison (EfficientNetB0 vs Custom CNN).
- `GET /history` - Session prediction history.

---

## 7. Academic Disclaimer

PlantCare AI is an educational project created for CSE Artificial Intelligence and Machine Learning coursework. It is intended for research and demonstration purposes. Always consult professional agronomists or agricultural extension officers before applying treatments or chemical controls.
