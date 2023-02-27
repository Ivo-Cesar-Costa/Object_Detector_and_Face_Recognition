import cv2
import sys
from random import randint

(vmax, vmin, vsub) = (cv2.__version__).split('.')

rastreadores = ['BOOSTING', 
                'MIL',
                'KCF',
                'TLD',
                'MEDIANFLOW',
                'MOSSE',
                'CSRT']

rastreador = rastreadores[6]
#print(rastreador)

if int(vmin) < 3:
    rx = rastreador
else:
    if rastreador == 'BOOSTING':
        rx = cv2.TrackerBoosting_create()
    if rastreador == 'MIL':
        rx = cv2.TrackerMIL_create()
    if rastreador == 'KCF':
        rx = cv2.TrackerKCF_create()
    if rastreador == 'TLD':
        rx = cv2.TrackerTLD_create()
    if rastreador == 'MEDIANFLOW':
        rx = cv2.TrackerMedianFlow_create()
    if rastreador == 'MOSSE':
        rx = cv2.TrackerMOSSE_create()
    if rastreador == 'CSRT':
        rx = cv2.TrackerCSRT_create()
        
video = cv2.VideoCapture('estrada.mp4')
if not video.isOpened():
    print('ERRO: Não foi possível carregar o vídeo!!!')
    sys.exit()
    
ok, frame = video.read()
if not ok:
    print('ERRO: Não foi possível ler o arquivo de vídeo!!!')
    sys.exit()
    
bbox = cv2.selectROI(frame, False)
ok = rx.init(frame, bbox)
colors = (randint(0, 255), randint(0, 255), randint(0, 255))

while True:
    ok, frame = video.read()
    if not ok:
        break
        
    timer = cv2.getTickCount()
    ok, bbox = rx.update(frame)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    
    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), colors, 2, 1)
    else:
        cv2.putText(frame, 'Falha no Rastreamento!!!', (100, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)
        
    cv2.putText(frame, rastreador + 'Rastreador', (100, 20),
               cv2.FONT_HERSHEY_SIMPLEX, .75, (50, 170, 50), 2)
    cv2.putText(frame, 'FPS: ' + str(int(fps)), (100, 50),
               cv2.FONT_HERSHEY_SIMPLEX, .75, (50, 170, 50), 2)
    
    cv2.imshow('Rastreamento', frame)
    #if cv2.waitKey(1) == ord('x'): # tecla x
    if cv2.waitKey(1) & 0XFF == 27: # tecla ESC
        cv2.destroyAllWindows()
        break