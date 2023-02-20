import joblib
import base64
import os
import numpy as np
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from flask import Flask
from flask import request
from flask import json
from tensorflow import keras
from keras import models
from werkzeug.utils import secure_filename

BUCKET_NAME = 'soybeanpredictor'
MODEL_FILE_NAME = '404Soybeans.h5'
MODEL_LOCAL_PATH = '/Users/mwhug/CapstoneProject/' + MODEL_FILE_NAME

app = Flask(__name__)

def model_predict(model_input):
    #load the image, make sure it is the target size (specified by model code)
    #img = keras.preprocessing.image.load_img(img_path, target_size=(256,256))
    #convert the image to an array
    #img = img.img_to_array(img)
    #normalize array size
    #img /= 255           
    #expand image dimensions for keras convention
    #img = np.expenad_dims(img, axis = 0)

    #call model for prediction
    opt = keras.optimizers.RMSprop(learning_rate = 0.01)
    keras.models.loaded_model.compile(optimizer = opt, loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
    model = load_model()
    pred = model.predict(model_input)

def output_statement(pred):
    if pred == 0:
        #output this range of days
        return 'Model Prediction: Your plant is at Day 9 of the growth cycle.'
    elif pred == 1:
        #output this range
        return 'Model Prediction: Your plant is at Day 10 of the growth cycle.'
    elif pred == 2:
        #output this range
        return 'Model Prediction: Your plant is at Day 11 of the growth cycle.'
    elif pred == 3:
        #output this range
        return 'Model Prediction: Your plant is at Day 12 of the growth cycle.'
    elif pred == 4:
        #output this range
        return 'Model Prediction: Your plant is at Day 13 of the growth cycle.'
    elif pred == 5:
        #output this range
        return 'Model Prediction: Your plant is at Day 14 of the growth cycle.'
    elif pred == 6:
        #output this range
        return 'Model Prediction: Your plant is at Day 15 of the growth cycle.'
    elif pred == 7:
        #output this range
        return 'Model Prediction: Your plant is at Day 16 of the growth cycle.'
    elif pred == 8:
        #output this range
        return 'Model Prediction: Your plant is at Day 17 of the growth cycle.'
    elif pred == 9:
        #output this range
        return 'Model Prediction: Your plant is at Day 18 of the growth cycle.'
    elif pred == 10:
        #output this range
        return 'Model Prediction: Your plant is at Day 19 of the growth cycle.'
    elif pred == 11:
        #output this range
        return 'Model Prediction: Your plant is at Day 20 of the growth cycle.'
    elif pred == 12:
        #output this range
        return 'Model Prediction: Your plant is at Day 21 of the growth cycle.'
    elif pred == 13:
        #output this range
        return 'Model Prediction: Your plant is at Day 22 of the growth cycle.'
    elif pred == 14:
        #output this range
        return 'Model Prediction: Your plant is at Day 23 of the growth cycle.'
    elif pred == 15:
        #output this range
        return 'Model Prediction: Your plant is at Day 24 of the growth cycle.'
    elif pred == 16:
        #output this range
        return 'Model Prediction: Your plant is at Day 25 of the growth cycle.'
    elif pred == 17:
        #output this range
        return 'Model Prediction: Your plant is at Day 26 of the growth cycle.'
    elif pred == 18:
        #output this range
        return 'Model Prediction: Your plant is at Day 27 of the growth cycle.'
    elif pred == 19:
        #output this range
        return 'Model Prediction: Your plant is at Day 28 of the growth cycle.'
    else:
        return 'Error: Model sent prediction out of the prescribed range. Please try again.'

@app.route('/', methods=['POST'])
def index():
    payload = json.loads(request.get_data().decode('base64'))
    input = payload['payload']  #variable input is a dictionary.
    prediction = predict(input)
    data = {}
    data['data'] = prediction[-1]
    return json.dumps(data)

def load_model():
    print('Loading model from S3')
    connection = S3Connection()
    s3bucket = connection.create_bucket(BUCKET_NAME)
    keyobject = Key(s3bucket)
    keyobject.key = MODEL_FILE_NAME

    contents = keyobject.get_contents_to_filename(MODEL_LOCAL_PATH)
    model = joblib.load(MODEL_LOCAL_PATH)
    return model

def predict(input):
    print('Making predictions')
    #data coming in as json. Need to convert to numpy array (normal array might work, not sure which is most ideal yet)
    model_input = np.asarray(input)

    pred = model_predict(model_input)
    output = output_statement(pred)
    return output

if __name__ == "__main__":
    app.run()