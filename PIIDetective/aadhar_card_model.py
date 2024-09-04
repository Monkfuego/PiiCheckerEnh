import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras._tf_keras.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import pandas as pd

# Create a sample dataset
positive_samples = [
    "C:/CODES/PiiCheckerModels/adh_pos1.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos2.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos3.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos4.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos5.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos6.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos7.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos8.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos9.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos10.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos11.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos12.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos13.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos14.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos15.jpg",
    "C:/CODES/PiiCheckerModels/adh_pos16.jpg",
]
negative_samples = [
    "C:/CODES/PiiCheckerModels/adh_neg1.jpg",
    "C:/CODES/PiiCheckerModels/adh_neg2.jpg",
    "C:/CODES/PiiCheckerModels/adh_neg3.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos1.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos2.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos3.jpg", 
    "C:/CODES/PiiCheckerModels/dl_pos4.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos5.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos6.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos7.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos8.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos9.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos10.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos11.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos12.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos13.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos14.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos15.jpg",
    "C:/CODES/PiiCheckerModels/dl_pos16.jpg",

]

# Function to load images
def load_images(image_paths, label):
    images = []
    labels = []
    for img_path in image_paths:
        img = load_img(img_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0  # Normalize the image to [0, 1]
        images.append(img_array)
        labels.append(label)
    return np.array(images), np.array(labels)

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0  # Normalize the image to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions to match the input shape (1, 224, 224, 3)
    return img_array

# Load positive and negative images
positive_images, positive_labels = load_images(positive_samples, 1)
negative_images, negative_labels = load_images(negative_samples, 0)

# Combine the datasets
images = np.concatenate((positive_images, negative_images), axis=0)
labels = np.concatenate((positive_labels, negative_labels), axis=0)

# Create a TensorFlow dataset
dataset = tf.data.Dataset.from_tensor_slices((images, labels))
dataset = dataset.shuffle(buffer_size=len(images)).batch(32)

# Create a TensorFlow model
model = keras.Sequential([
    layers.Conv2D(32, 3, activation='relu', input_shape=(224, 224, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, 3, activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(2, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(dataset, epochs=20)

input_image_path = "C:/CODES/PiiCheckerModels/adh_pos6.jpg"  # Replace with your input image path
input_image = preprocess_image(input_image_path)

# Make a prediction
prediction = model.predict(input_image)

# Interpret the prediction
predicted_class = np.argmax(prediction)  # Get the index of the highest probability
if predicted_class == 1:
    print("The input image is predicted to be a positive sample.")
else:
    print("The input image is predicted to be a negative sample.")

# Save the model to an HDF5 file
model.save('aadhar_card_model.h5')

print("Model saved to aadhar_card_model.h5")