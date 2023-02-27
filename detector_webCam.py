import cv2

detector_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

captura = cv2.VideoCapture(0)

while True:
    ret, img = captura.read()
    img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_detectada = detector_face.detectMultiScale(img_cinza)
    for (x, y, l, a) in face_detectada:
        cv2.rectangle(img, (x, y), (x + l, y + a), (0, 0, 255), 2)
    cv2.imshow('Face Detectada', img)
    if cv2.waitKey(1) == ord('x'):
        break
        
captura.release()

cv2.destroyAllWindows()
