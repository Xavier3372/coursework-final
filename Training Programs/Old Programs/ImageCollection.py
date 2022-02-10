# Program has been deprecated, use programs in folder "New Programs instead"

# Written by Xavier Koh
import time
import uuid
import cv2
import os
os.system('pip install opencv-python')

labels = ['h']


num_img = 50 #CHANGE THIS TY
# If u reading this, use the commented one on top
IMAGES_PATH = os.path.join('Tensorflow', 'workspace',
                           'images', 'collectedimages')

if not os.path.exists(IMAGES_PATH):
    if os.name == 'posix':
        os.system('mkdir -p {IMAGES_PATH}')
    if os.name == 'nt':
        os.system('mkdir {IMAGES_PATH}')
for label in labels:
    path = os.path.join(IMAGES_PATH, label)
    if not os.path.exists(path):
        os.system("mkdir {path}")

for i in labels:
    cap = cv2.VideoCapture(0)
    print(('collecting images for {}').format(i))
    time.sleep(5)
    for img_no in range(num_img):
        print(('collecting image {} no.{}').format(i,img_no+100)) #change to 0/50/100
        img_name = os.path.join(
            IMAGES_PATH, i, '{}.jpg'.format(i+str(img_no+100)))
        while True:
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k % 256 == 32:
                cv2.imwrite(img_name, frame)
                break
            elif k % 256 == 27:
                cv2.destroyAllWindows()
                break

cap.release()
cv2.destroyAllWindows()
