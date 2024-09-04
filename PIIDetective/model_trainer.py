import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras._tf_keras.keras.preprocessing.image import load_img, img_to_array
import numpy as np
# Create a sample dataset
positive_samples = [
    "C:/object_detection/imgs/img1.png",
    "C:/object_detection/imgs/img2.png",
    "C:/object_detection/imgs/img3.png",
    "C:/object_detection/imgs/img4.png",
    "C:/object_detection/imgs/img5.png",
    "C:/object_detection/imgs/img6.jpg",
    "C:/object_detection/imgs/img7.jpg",
    "C:/object_detection/imgs/img8.jpg",
    "C:/object_detection/imgs/img9.jpg",
]
negative_samples = [
    'C:/object_detection/negative_imgs/img1.jpg',
    "C:/object_detection/negative_imgs/img2.jpg",
    "C:/object_detection/negative_imgs/img3.jpg",
    "C:/object_detection/negative_imgs/img4.jpg",
    "C:/object_detection/negative_imgs/img5.jpg",
    "C:/object_detection/negative_imgs/img6.jpg",
    "C:/object_detection/negative_imgs/img7.jpg",
    "C:/object_detection/negative_imgs/img8.jpg",
    "C:/object_detection/negative_imgs/img9.jpg"
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
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(2, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(dataset, epochs=30)
model.save('aadhar_card_model.keras')
