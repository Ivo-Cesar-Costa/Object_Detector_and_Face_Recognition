import cv2
import sys
from random import randint


rastreadores = ['BOOSTING', 
                'MIL',
                'KCF',
                'TLD',
                'MEDIANFLOW',
                'MOSSE',
                'CSRT']

def escolhe_rastreador(rastreador):
    
    if rastreador == rastreadores[0]:
        rx = cv2.legacy.TrackerBoosting_create()
    if rastreador == rastreadores[1]:
        rx = cv2.legacy.TrackerMIL_create()
    if rastreador == rastreadores[2]:
        rx = cv2.legacy.TrackerKCF_create()
    if rastreador == rastreadores[3]:
        rx = cv2.legacy.TrackerTLD_create()
    if rastreador == rastreadores[4]:
        rx = cv2.legacy.TrackerMedianFlow_create()
    if rastreador == rastreadores[5]:
        rx = cv2.legacy.TrackerMOSSE_create()
    if rastreador == rastreadores[6]:
        rx = cv2.legacy.TrackerCSRT_create()
    else:
        rx = None
        print('ERRO: Rastreador Inválido !!!')
    return rx


video = cv2.VideoCapture('estrada.mp4')

ok, frame = video.read()
if not ok:
    print('ERRO: Não foi possível ler o arquivo de vídeo!!!')
    sys.exit(1)  
    
    
bboxes = [] 
colors = []

while True:
    bbox = cv2.selectROI('MultitTracker', frame)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))   
    print('Selecione os objetos a serem rastreados e pressione ENTER duas vezes em cada objeto.')
    print('Selecione o ultimo objeto a ser rastreado e pressione ENTER uma vez.')
    print('Pressione Q para sair da seleção e começar a rastrear.')
    print('Pressione C para cancelar a seleção.')
    print('Pressione ESC para sair.')
    k = cv2.waitKey(0) & 0XFF  # tecla ESC
    if (k == 113):
        break
        
reastreador_escolhido = 'CSRT'
multi_rastreador = cv2.legacy.MultiTracker_create()

for bbox in bboxes:
    multi_rastreador.add(escolhe_rastreador(reastreador_escolhido), frame, bbox)
    
while video.isOpened():
    ok, frame = video.read()
    
    if not ok:
        break
        
    ok, boxes = multi_rastreador.update(frame)
    for i, newbox in enumerate(boxes):
        
        (x, y, w, h) = [int(v) for v in newbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), colors[i], 2, 1)
        
    cv2.imshow('Rastreamento Multiplo', frame)
    if cv2.waitKey(1) & 0XFF == 27: # tecla esc
        cv2.destroyAllWindows()
        break
    # if cv2.waitKey(1) == ord('x'):  # tecla X
    #     cv2.destroyAllWindows()
    #     break