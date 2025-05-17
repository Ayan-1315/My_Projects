import cv2
import os
import numpy as np

def facebox(faceNet, frame):
    blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), [104, 117, 123], swapRB=False)
    faceNet.setInput(blob)
    detection = faceNet.forward()
    bboxs = []
    for i in range(detection.shape[2]):
        confidence = detection[0, 0, i, 2]
        if confidence > 0.7:
            x1 = int(detection[0, 0, i, 3] * frame.shape[1])
            y1 = int(detection[0, 0, i, 4] * frame.shape[0])
            x2 = int(detection[0, 0, i, 5] * frame.shape[1])
            y2 = int(detection[0, 0, i, 6] * frame.shape[0])
            bboxs.append([x1, y1, x2, y2])
    return bboxs

def predict_age_gender(ageNet, genderNet, face):
    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
    
    # Predict gender
    genderNet.setInput(blob)
    gender_preds = genderNet.forward()
    gender = genderList[gender_preds[0].argmax()]
    
    # Predict age
    ageNet.setInput(blob)
    age_preds = ageNet.forward()
    age = ageList[age_preds[0].argmax()]
    
    return age, gender

cap = cv2.VideoCapture(0)

# Paths to the face detection model files
faceProto = os.path.join("C:\\Users\\91786\\Desktop\\PROGRAMS\\Machine_Learning\\01_Age_detection", "opencv_face_detector.pbtxt")
faceModel = os.path.join("C:\\Users\\91786\\Desktop\\PROGRAMS\\Machine_Learning\\01_Age_detection", "opencv_face_detector_uint8.pb")

# Paths to the age and gender prediction model files
ageProto = os.path.join("C:\\Users\\91786\\Desktop\\PROGRAMS\\Machine_Learning\\01_Age_detection", "age_deploy.prototxt")
ageModel = os.path.join("C:\\Users\\91786\\Desktop\\PROGRAMS\\Machine_Learning\\01_Age_detection", "age_net.caffemodel")

genderProto = os.path.join("C:\\Users\\91786\\Desktop\\PROGRAMS\\Machine_Learning\\01_Age_detection", "gender_deploy.prototxt")
genderModel = os.path.join("C:\\Users\\91786\\Desktop\\PROGRAMS\\Machine_Learning\\01_Age_detection", "gender_net.caffemodel")

# Ensure the paths are correct
assert os.path.isfile(faceProto), f"{faceProto} does not exist"
assert os.path.isfile(faceModel), f"{faceModel} does not exist"
assert os.path.isfile(ageProto), f"{ageProto} does not exist"
assert os.path.isfile(ageModel), f"{ageModel} does not exist"
assert os.path.isfile(genderProto), f"{genderProto} does not exist"
assert os.path.isfile(genderModel), f"{genderModel} does not exist"

# Load models
faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

# Lists of age categories and genders
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# Set properties for the video capture
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.41)  # Adjusted brightness value
cap.set(cv2.CAP_PROP_CONTRAST, 0.31)    # Adjusted contrast value
cap.set(cv2.CAP_PROP_SHARPNESS, 1)
cap.set(cv2.CAP_PROP_SATURATION, 0.66)  # Adjusted saturation value
cap.set(cv2.CAP_PROP_GAMMA, 1.0)
cap.set(cv2.CAP_PROP_BACKLIGHT, 1)
cap.set(cv2.CAP_PROP_GAIN, 1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    bboxs = facebox(faceNet, frame)
    for bbox in bboxs:
        face = frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        age, gender = predict_age_gender(ageNet, genderNet, face)

        # Draw bounding box and label on the frame
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        label = f"{gender}, Age: {age}"
        cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Age and Gender Prediction", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()