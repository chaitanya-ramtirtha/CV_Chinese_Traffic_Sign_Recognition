import os
import io
import numpy as np
from PIL import Image
import tensorflow as tf
from flask import Flask, request, jsonify, render_template

# Defining the Flask app
app = Flask(__name__)

# Loading the model
model = tf.keras.models.load_model('traffic_classifier.h5')

category_dict = {0: "Speed limit - 5", 1: "Speed limit - 15", 2: "Speed limit - 30", 3: "Speed limit - 40",
                 4: "Speed limit - 50", 5: "Speed limit - 60",
                 6: "Speed limit - 70", 7: "Speed limit - 80", 8: "Only right turn is allowed",
                 9: "Only left turn is allowed",
                 10: "No entry, One way", 11: "No left turn allowed", 12: "No left or right turn allowed",
                 13: "No right turn allowed"
    , 14: "Cannot change lanes", 15: "No U-turn allowed", 16: "No thoroughfare for vehicles", 17: "No honking"
    , 18: "End speed limit 40", 19: "End speed limit 50", 20: "Allowed to go only right or straight",
                 21: "No turn allowed",
                 22: "Only left turn allowed", 23: "Cannot go straight", 24: "Only right turn allowed", 25: "Keep left",
                 26: "Keep right", 27: "Roundabout", 28: "Only cars allowed", 29: "Honking allowed",
                 30: "Cycle lane", 31: "U-turn allowed", 32: "Warning for an obstacle, pass either side",
                 33: "Traffic signal warning",
                 34: "Warning for a danger with no specific traffic sign.",
                 35: "Warning for a crossing for pedestrians.", 36: "Warning for cyclists.",
                 37: "Warning for children.", 38: "Warning for a curve to the right.",
                 39: "Warning for a curve to the left."
    , 40: "Warning for steep descent", 41: "Warning for steep ascent", 42: "Slow",
                 43: "Side road junction ahead on the right", 44: "Side road junction ahead on the left",
                 45: "Cross-village road", 46: "Double curve, with turn right first, then left",
                 47: "Locomotive railroad crossing ahead - without safety barriers", 48: "Roadworks ahead",
                 49: "Multiple curves", 50: "Railroad head - with safety barriers",
                 51: "Accident area", 52: "Stop", 53: "No entry for vehicular and pedestrians", 54: "No stopping",
                 55: "No entry for vehicular traffic", 56: "Give way", 57: "Control"}

# Function to preprocess the image
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image)
    image = image.astype('float32')
    image /= 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Using model to make predictions
@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':

        file = request.files['file']

        image = Image.open(io.BytesIO(file.read()))

        image = preprocess_image(image)

        prediction = model.predict(image)

        category = np.argmax(prediction)

        if category in category_dict.keys():
            category_text = category_dict[category]
        else:
            category_text = "Image does not belong to the pre-defined 58 categories. Please search online."

        warning_text = 'Warning: This machine learning model may have chance of mis classification. Please verify the output once'

        return jsonify({'warning': warning_text, 'category': category_text})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
