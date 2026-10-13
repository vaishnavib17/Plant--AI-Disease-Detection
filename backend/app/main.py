"""PlantCare AI: FastAPI backend using the trained EfficientNetB0 model."""

import io
import json
import time
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

BACKEND_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BACKEND_DIR / "models"

# Initially use the model from the successful small training test.
MODEL_PATH = MODEL_DIR / "efficientnetb0_plantcare_smoke.h5"
LABELS_PATH = MODEL_DIR / "class_indices_smoke.json"

# Human-readable information for the actual PlantVillage folder names.
CLASS_DETAILS = {
    "Pepper__bell___Bacterial_spot": ("Pepper", "Bacterial Spot", "Diseased"),
    "Pepper__bell___healthy": ("Pepper", "Healthy", "Healthy"),
    "Potato___Early_blight": ("Potato", "Early Blight", "Diseased"),
    "Potato___Late_blight": ("Potato", "Late Blight", "Diseased"),
    "Potato___healthy": ("Potato", "Healthy", "Healthy"),
    "Tomato_Bacterial_spot": ("Tomato", "Bacterial Spot", "Diseased"),
    "Tomato_Early_blight": ("Tomato", "Early Blight", "Diseased"),
    "Tomato_Late_blight": ("Tomato", "Late Blight", "Diseased"),
    "Tomato_Leaf_Mold": ("Tomato", "Leaf Mold", "Diseased"),
    "Tomato_Septoria_leaf_spot": ("Tomato", "Septoria Leaf Spot", "Diseased"),
    "Tomato_Spider_mites_Two_spotted_spider_mite": (
        "Tomato", "Spider Mites (Two-Spotted Spider Mite)", "Diseased"
    ),
    "Tomato__Target_Spot": ("Tomato", "Target Spot", "Diseased"),
    "Tomato__Tomato_YellowLeaf__Curl_Virus": (
        "Tomato", "Tomato Yellow Leaf Curl Virus", "Diseased"
    ),
    "Tomato__Tomato_mosaic_virus": (
        "Tomato", "Tomato Mosaic Virus", "Diseased"
    ),
    "Tomato_healthy": ("Tomato", "Healthy", "Healthy"),
}

app = FastAPI(
    title="PlantCare AI API",
    description="Plant disease classification using a trained EfficientNetB0 model.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
class_names = []
prediction_history = []


class Candidate(BaseModel):
    class_name: str
    species: str
    condition: str
    confidence: float


class PredictionResponse(BaseModel):
    success: bool
    predicted_class: str
    species: str
    condition: str
    status: str
    confidence: float
    top_candidates: List[Candidate]
    uncertainty_flag: bool
    uncertainty_reason: Optional[str] = None
    inference_time_ms: float
    model_used: str


def load_artifacts():
    global model, class_names

    if not MODEL_PATH.is_file() or not LABELS_PATH.is_file():
        print("PlantCare model or class-label file is missing.")
        model = None
        class_names = []
        return

    with open(LABELS_PATH, "r") as f:
        class_indices = json.load(f)

    class_names = [
        name for name, index in
        sorted(class_indices.items(), key=lambda item: item[1])
    ]

    loaded_model = tf.keras.models.load_model(str(MODEL_PATH), compile=False)

    if loaded_model.output_shape[-1] != len(class_names):
        raise ValueError(
            "Model output count does not match the saved class-label count."
        )

    model = loaded_model
    print(f"Loaded model: {MODEL_PATH.name}")
    print(f"Loaded {len(class_names)} class labels.")


load_artifacts()


def class_metadata(class_name):
    species, condition, status = CLASS_DETAILS.get(
        class_name,
        ("Unknown", class_name.replace("_", " "), "Diseased"),
    )
    return {
        "id": class_names.index(class_name),
        "name": class_name,
        "species": species,
        "condition": condition,
        "status": status,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model is not None else "degraded",
        "model_loaded": model is not None,
        "model_name": MODEL_PATH.name if model is not None else None,
        "framework": "TensorFlow / Keras",
        "device": "CPU",
        "total_classes": len(class_names),
        "model_stage": "smoke_test" if model is not None else "not_loaded",
    }


@app.get("/classes")
def get_classes():
    return {
        "classes": [class_metadata(name) for name in class_names],
        "total_classes": len(class_names),
    }


@app.get("/metrics")
def get_metrics():
    history_path = MODEL_DIR / "training_history_smoke.json"
    history = {}

    if history_path.is_file():
        with open(history_path, "r") as f:
            history = json.load(f)

    validation_accuracy = history.get("val_accuracy", [])
    training_accuracy = history.get("accuracy", [])

    return {
        "models": {
            "EfficientNetB0": {
                "model_loaded": model is not None,
                "model_stage": "smoke_test",
                "validation_accuracy": (
                    validation_accuracy[-1] if validation_accuracy else None
                ),
                "training_accuracy": (
                    training_accuracy[-1] if training_accuracy else None
                ),
                "epochs_completed": len(training_accuracy),
                "test_accuracy": None,
            }
        },
        "dataset_stats": {
            "total_classes": len(class_names),
            "image_resolution": [224, 224],
            "note": (
                "Smoke-test validation metrics only; no independent test "
                "set has been evaluated."
            ),
        },
    }


@app.get("/history")
def get_history():
    return {"history": prediction_history, "count": len(prediction_history)}


@app.post("/predict", response_model=PredictionResponse)
async def predict_image(
    file: UploadFile = File(...),
    model_choice: str = Query("EfficientNetB0"),
):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="The trained model is not loaded. Check backend/models.",
        )

    if model_choice not in ("EfficientNetB0", "TransferModel"):
        raise HTTPException(
            status_code=400,
            detail=(
                "The Custom CNN model has not been trained yet. "
                "Choose Transfer Model to use the trained EfficientNetB0."
            ),
        )

    if not file.filename or Path(file.filename).suffix.lower() not in (
        ".jpg", ".jpeg", ".png", ".webp"
    ):
        raise HTTPException(
            status_code=400,
            detail="Upload a JPG, JPEG, PNG, or WebP image.",
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Maximum image size is 10MB.")

    start = time.perf_counter()

    try:
        with Image.open(io.BytesIO(contents)) as image:
            image = image.convert("RGB").resize((224, 224))
            pixels = np.asarray(image, dtype=np.float32)
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file could not be decoded as an image.",
        )

    # EfficientNetB0 includes its own input rescaling layer.
    batch = np.expand_dims(pixels, axis=0)
    probabilities = model.predict(batch, verbose=0)[0]

    if not np.all(np.isfinite(probabilities)):
        raise HTTPException(
            status_code=500, detail="The model returned invalid probabilities."
        )

    best_indices = np.argsort(probabilities)[::-1][:3]
    predicted_index = int(best_indices[0])
    predicted_name = class_names[predicted_index]
    predicted_info = class_metadata(predicted_name)
    confidence = float(probabilities[predicted_index])

    candidates = []
    for index in best_indices:
        name = class_names[int(index)]
        details = class_metadata(name)
        candidates.append({
            "class_name": name,
            "species": details["species"],
            "condition": details["condition"],
            "confidence": float(probabilities[int(index)]),
        })

    uncertain = confidence < 0.55
    elapsed_ms = (time.perf_counter() - start) * 1000

    result = {
        "success": True,
        "predicted_class": predicted_name,
        "species": predicted_info["species"],
        "condition": predicted_info["condition"],
        "status": predicted_info["status"],
        "confidence": confidence,
        "top_candidates": candidates,
        "uncertainty_flag": uncertain,
        "uncertainty_reason": (
            "The model confidence is low. Try a clear, well-lit image of a "
            "single leaf." if uncertain else None
        ),
        "inference_time_ms": round(elapsed_ms, 2),
        "model_used": "EfficientNetB0-smoke-test",
    }

    prediction_history.insert(0, {
        "filename": file.filename,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        **result,
    })
    del prediction_history[50:]

    return result


@app.post("/explain")
async def explain_prediction(
    file: UploadFile = File(...),
    class_name: str = Query(""),
):
    """Generate a Grad-CAM heatmap from the trained EfficientNetB0."""
    import base64

    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded.")

    if not file.filename or Path(file.filename).suffix.lower() not in (
        ".jpg", ".jpeg", ".png", ".webp"
    ):
        raise HTTPException(
            status_code=400, detail="Upload a JPG, JPEG, PNG, or WebP image."
        )

    contents = await file.read()
    if not contents or len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400, detail="Image is empty or exceeds 10MB."
        )

    try:
        with Image.open(io.BytesIO(contents)) as source:
            original = source.convert("RGB")
            original_size = original.size
            resized = original.resize((224, 224))
            pixels = np.asarray(resized, dtype=np.float32)
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400, detail="The uploaded file is not a valid image."
        )

    try:
        # The nested EfficientNetB0 produces the spatial feature maps.
        feature_extractor = model.get_layer("efficientnetb0")
        feature_maps = feature_extractor(
            tf.convert_to_tensor(pixels[None, ...]), training=False
        )

        with tf.GradientTape() as tape:
            tape.watch(feature_maps)
            pooled = model.get_layer("global_average_pooling2d")(
                feature_maps, training=False
            )
            dropped = model.get_layer("dropout")(pooled, training=False)
            scores = model.get_layer("dense")(dropped)
            probabilities = tf.nn.softmax(scores, axis=-1)

            if class_name:
                if class_name not in class_names:
                    raise HTTPException(
                        status_code=400,
                        detail="Requested class is not supported by this model."
                    )
                target_index = class_names.index(class_name)
            else:
                target_index = int(tf.argmax(probabilities[0]).numpy())

            target_score = scores[:, target_index]

        gradients = tape.gradient(target_score, feature_maps)
        if gradients is None:
            raise RuntimeError("Could not calculate gradients for Grad-CAM.")

        # Average gradients over spatial dimensions to weight each channel.
        weights = tf.reduce_mean(gradients, axis=(1, 2), keepdims=True)
        cam = tf.reduce_sum(weights * feature_maps, axis=-1)[0]
        cam = tf.nn.relu(cam)
        maximum = tf.reduce_max(cam)
        cam = tf.where(
            maximum > 0,
            cam / (maximum + tf.keras.backend.epsilon()),
            tf.zeros_like(cam)
        )
        heatmap = cam.numpy()

        heatmap_image = Image.fromarray(
            np.uint8(np.clip(heatmap, 0, 1) * 255)
        ).resize(original_size, Image.Resampling.BILINEAR)

        # Apply a color map to make the activation easier to inspect.
        heat_array = np.asarray(heatmap_image, dtype=np.float32) / 255.0
        colored = np.zeros((*heat_array.shape, 3), dtype=np.uint8)
        colored[..., 0] = np.uint8(
            np.clip(1.5 - np.abs(4 * heat_array - 3), 0, 1) * 255
        )
        colored[..., 1] = np.uint8(
            np.clip(1.5 - np.abs(4 * heat_array - 2), 0, 1) * 255
        )
        colored[..., 2] = np.uint8(
            np.clip(1.5 - np.abs(4 * heat_array - 1), 0, 1) * 255
        )

        overlay_array = (
            0.55 * np.asarray(original, dtype=np.float32)
            + 0.45 * colored.astype(np.float32)
        )
        overlay = Image.fromarray(
            np.uint8(np.clip(overlay_array, 0, 255))
        )

        def png_base64(image):
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode("ascii")

        predicted_index = int(tf.argmax(probabilities[0]).numpy())
        return {
            "success": True,
            "method": "Grad-CAM",
            "target_class": class_names[target_index],
            "predicted_class": class_names[predicted_index],
            "target_probability": float(probabilities[0, target_index].numpy()),
            "heatmap_base64": png_base64(heatmap_image.convert("RGB")),
            "overlay_base64": png_base64(overlay),
            "image_width": original_size[0],
            "image_height": original_size[1],
            "note": (
                "Grad-CAM highlights image regions influencing this class score; "
                "it does not establish disease causation."
            ),
        }
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Grad-CAM generation failed: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Grad-CAM generation failed. Check the backend terminal."
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
