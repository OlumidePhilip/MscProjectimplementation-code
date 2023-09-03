import cv2
import numpy as np
import requests
import json
import os

def crop_out_face(img, T = True, name = ''):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
    if len(face) >= 1:
        print('here')
        print(len(face))
        for (x, y, w, h) in face:
            face_roi = img[y:y + h, x:x + w]
        if T == True:
            cv2.imwrite(name, face_roi)
        return face_roi
    else:
        return "no-img"
   


def hist_classify(img1, img2):
    img1 = cv2.imread(img1)
    bw1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    cropped_bw1 = crop_out_face(bw1, False, "crp0.jpg")
    bw2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    cropped_bw2 = crop_out_face(bw2, False, "crp1.jpg")
    if type(cropped_bw1) == str or type(cropped_bw2) == str:
        print("No face somewhere")
        return False
    
    hist1 = cv2.calcHist([cropped_bw1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([cropped_bw2], [0], None, [256], [0, 256])

    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
    print(similarity)

    if similarity > 15000:
        return True
    else:
        return False
    
def sift_classify(img1, img2):
    sift = cv2.SIFT_create()
    img1 = cv2.imread(img1)
    bw1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    cropped_bw1 = crop_out_face(bw1, False, "crp0.jpg")
    bw2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    cropped_bw2 = crop_out_face(bw2, False, "crp1.jpg")
    if type(cropped_bw1) == str or type(cropped_bw2) == str:
        print("No face somewhere")
        return False

    _, descriptors1 = sift.detectAndCompute(cropped_bw1, None)
    _, descriptors2 = sift.detectAndCompute(cropped_bw2, None)

    bf = cv2.BFMatcher()

    matches = bf.match(descriptors1, descriptors2)

    matches = sorted(matches, key=lambda x: x.distance)

    if matches[0].distance < 183:
        return True
    else:
        return False
    
url = os.environ.get("MODEL_URL", "http://localhost:80/predict")

def siamese_classify(img1, img2):
    img1 = cv2.imread(img1)
    bw1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    cropped_bw1 = crop_out_face(bw1, True, "crp0.jpg")
    bw2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    cropped_bw2 = crop_out_face(bw2, True, "crp1.jpg")
    if type(cropped_bw1) == str or type(cropped_bw2) == str:
        print("No face somewhere")
        return False
    else:
        im1 = cv2.resize(bw1, (64,64)) / 225
        im2 = cv2.resize(bw2, (64, 64)) / 225
        img1E = np.expand_dims(np.expand_dims(im1, axis = -1), axis = 0)
        img2E = np.expand_dims(np.expand_dims(im2, axis = -1), axis = 0)
        print(img1E.shape)
        print(img2E.shape)
        form_data = {
            'img1': json.dumps(img1E.tolist()),
            'img2': json.dumps(img2E.tolist())
        }
        response = requests.post(url, data=form_data)
        print(response.text)
        if response.text == "True":
            return True
        return False

