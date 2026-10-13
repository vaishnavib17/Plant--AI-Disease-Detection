"""
PlantCare AI - Custom CNN Baseline Training Pipeline
A lightweight convolutional neural network built from scratch for comparison against EfficientNetB0.
"""

import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization

NUM_CLASSES = 16
MODEL_SAVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models/custom_cnn_baseline.h5"))

def build_custom_cnn():
    print("Building Custom CNN Baseline Model...")
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Conv2D(256, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(NUM_CLASSES, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(name='precision'), tf.keras.metrics.Recall(name='recall')]
    )
    return model

if __name__ == "__main__":
    model = build_custom_cnn()
    model.summary()
    print("Custom CNN baseline script ready.")
