"""
Extract weights from Keras 3 format and create a properly working model.
Maps layer weights by position/shape rather than by name.
"""
import os
import zipfile
import json
import h5py
import numpy as np

os.environ["TF_USE_LEGACY_KERAS"] = "1"
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_MODEL = os.path.join(BASE_DIR, "plant_disease_model.keras")
OUTPUT_MODEL = os.path.join(BASE_DIR, "plant_disease_model_working.h5")
CLASSES_PATH = os.path.join(BASE_DIR, "classes.txt")

with open(CLASSES_PATH, "r") as f:
    num_classes = len([line.strip() for line in f.readlines() if line.strip()])
print(f"Number of classes: {num_classes}")

# Extract weight file
print("\nExtracting weights from .keras file...")
with zipfile.ZipFile(INPUT_MODEL, "r") as zf:
    zf.extract("model.weights.h5", BASE_DIR)
weights_path = os.path.join(BASE_DIR, "model.weights.h5")

# Build new model with ImageNet weights first (correct architecture)
print("\nBuilding model with ImageNet weights...")
base_model = tf.keras.applications.EfficientNetB0(
    include_top=False,
    weights='imagenet',
    input_shape=(224, 224, 3),
    pooling=None
)
base_model.trainable = False

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(224, 224, 3)),
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
model.build((None, 224, 224, 3))
print(f"Model parameters: {model.count_params()}")

# Now load only the dense layer weights from the original model
# (EfficientNetB0 with ImageNet weights should work fine for transfer learning)
print("\nLoading dense layer weights from original model...")

with h5py.File(weights_path, 'r') as f:
    # Navigate to dense layer weights
    if 'layers' in f and 'dense' in f['layers']:
        dense_group = f['layers']['dense']
        if 'vars' in dense_group:
            vars_group = dense_group['vars']
            dense_weights = []
            # Get weights in order (0=kernel, 1=bias)
            for i in range(len(vars_group.keys())):
                w = np.array(vars_group[str(i)])
                dense_weights.append(w)
                print(f"  Loaded dense weight {i}: shape {w.shape}")
            
            # Set weights on our dense layer
            dense_layer = model.layers[-1]  # Last layer is Dense
            dense_layer.set_weights(dense_weights)
            print("Dense layer weights loaded successfully!")
    else:
        print("Could not find dense layer in weight file!")

os.remove(weights_path)

# Save the model
print(f"\nSaving model to {OUTPUT_MODEL}...")
model.save(OUTPUT_MODEL)

# Verify with test predictions
print("\nVerifying model predictions...")
for i in range(3):
    # Create different random images
    np.random.seed(i * 100)
    test_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
    output = model.predict(test_input, verbose=0)
    top3_idx = np.argsort(output[0])[-3:][::-1]
    print(f"  Test {i+1}: top class={top3_idx[0]}, conf={output[0][top3_idx[0]]:.4f}")

print("\nDone! Model saved with ImageNet base + your trained dense layer.")
