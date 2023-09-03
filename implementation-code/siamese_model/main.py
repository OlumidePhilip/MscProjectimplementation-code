from flask import Flask, request
from tensorflow.keras.models import load_model
import numpy as np
import json
import os

app = Flask(__name__)


@app.route("/")
def index():
    print(model.summary())
    sum_l = []
    model.summary(print_fn=lambda x: sum_l.append(x))
    return "\n".join(sum_l)

@app.route("/predict", methods = ["POST"])
def predict():
    img1_b = request.form['img1']
    img2_b = request.form['img2']

    img1 = np.array(json.loads(img1_b))
    img2 = np.array(json.loads(img2_b))

    print(img1.shape)
    print(img2.shape)
    p = model.predict([img1, img2])[0][0]
    print(p)
    if round(p, 2) > 0.5:
        print("Similar")
        return "True"
    else:
      print("Not Similar")
      return "false"
    

if __name__ == "__main__":
    model = load_model('final_model.h5')
    app.run(host = '0.0.0.0', port=os.environ.get("PORT", 80))


