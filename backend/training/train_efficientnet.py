import json
import os
import random
import tempfile
from pathlib import Path

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Dataset and training settings
DATASET_DIR = Path.home() / "Downloads/archive/PlantVillage/PlantVillage"
PROJECT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_DIR / "models"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 8
EPOCHS = int(os.getenv("EPOCHS", "3"))
MAX_IMAGES_PER_CLASS = int(os.getenv("MAX_IMAGES_PER_CLASS", "100"))
SEED = 42
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

random.seed(SEED)
tf.random.set_seed(SEED)


def main():
    if not DATASET_DIR.is_dir():
        raise FileNotFoundError(f"Dataset folder not found: {DATASET_DIR}")

    class_dirs = sorted(
        p for p in DATASET_DIR.iterdir()
        if p.is_dir() and any(
            f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
            for f in p.iterdir()
        )
    )

    if len(class_dirs) < 2:
        raise RuntimeError("Expected at least two class folders with images.")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    smoke_test = MAX_IMAGES_PER_CLASS > 0

    print(f"Dataset: {DATASET_DIR}")
    print(f"Classes found: {len(class_dirs)}")
    print(f"Epochs: {EPOCHS}")
    print(
        f"Image limit per class: {MAX_IMAGES_PER_CLASS}"
        if smoke_test else "Using all available images"
    )

    # Build a temporary, small dataset using links to the original images.
    # This avoids copying thousands of files.
    with tempfile.TemporaryDirectory(prefix="plantcare_sample_") as temp:
        sample_root = Path(temp)

        for class_dir in class_dirs:
            files = sorted(
                f for f in class_dir.iterdir()
                if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
            )
            random.shuffle(files)

            if smoke_test:
                files = files[:MAX_IMAGES_PER_CLASS]

            destination = sample_root / class_dir.name
            destination.mkdir()

            for i, source in enumerate(files):
                os.symlink(source, destination / f"{i}{source.suffix.lower()}")

            print(f"  {class_dir.name}: {len(files)} images")

        generator = ImageDataGenerator(validation_split=0.2)

        train_data = generator.flow_from_directory(
            str(sample_root),
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            class_mode="categorical",
            subset="training",
            shuffle=True,
            seed=SEED,
        )

        val_data = generator.flow_from_directory(
            str(sample_root),
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            class_mode="categorical",
            subset="validation",
            shuffle=False,
            seed=SEED,
        )

        num_classes = train_data.num_classes
        class_indices = train_data.class_indices

        print(f"\nTraining images: {train_data.samples}")
        print(f"Validation images: {val_data.samples}")
        print(f"Detected output classes: {num_classes}")

        # Start with a frozen pretrained feature extractor.
        # The classification head learns to distinguish these plant classes.
        base_model = EfficientNetB0(
            weights="imagenet",
            include_top=False,
            input_shape=(224, 224, 3),
        )
        base_model.trainable = False

        inputs = layers.Input(shape=(224, 224, 3))
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.25)(x)
        outputs = layers.Dense(num_classes, activation="softmax")(x)

        model = models.Model(inputs, outputs)
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )

        model.summary()

        history = model.fit(
            train_data,
            validation_data=val_data,
            epochs=EPOCHS,
        )

        if smoke_test:
            model_path = MODEL_DIR / "efficientnetb0_plantcare_smoke.h5"
            labels_path = MODEL_DIR / "class_indices_smoke.json"
            history_path = MODEL_DIR / "training_history_smoke.json"
        else:
            model_path = MODEL_DIR / "efficientnetb0_plantcare.h5"
            labels_path = MODEL_DIR / "class_indices.json"
            history_path = MODEL_DIR / "training_history.json"

        model.save(str(model_path))

        with open(labels_path, "w") as f:
            json.dump(class_indices, f, indent=2)

        with open(history_path, "w") as f:
            json.dump(
                {
                    key: [float(v) for v in values]
                    for key, values in history.history.items()
                },
                f,
                indent=2,
            )

        print("\nTRAINING FINISHED")
        print(f"Model saved: {model_path}")
        print(f"Class labels saved: {labels_path}")
        print(f"Training history saved: {history_path}")
        print(
            "Final validation accuracy: "
            f"{history.history['val_accuracy'][-1]:.4f}"
        )
        print(
            "This is a small smoke-test model, not yet the final model."
            if smoke_test else "Full-dataset training run completed."
        )


if __name__ == "__main__":
    main()
