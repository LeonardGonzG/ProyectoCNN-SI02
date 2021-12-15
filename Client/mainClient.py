import requests
import base64
import cv2
import numpy as np
from Objects.Image import Image


classPred = ['Cuchara', 'Tenedor', 'Cuchillo', 'Molinillo', 'Cacerola']

cap = cv2.VideoCapture('http://192.168.1.82:4747/video')

"""azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)"""

rojoBajo = np.array([170,100,100],np.uint8)
rojoAlto = np.array([179,255,255],np.uint8)

json_data = {}
imgs = []
models = []

ansServer = 'Success'

def addImage(id, content):
    data = Image(id, content)
    imgs.append(data.__dict__)

def addModel(name):
    models.append(name)

def makeJson():
    json_data['id_client'] = '001'
    json_data['images'] = imgs
    json_data['models'] = models

    return json_data


def initDialogUser():
    initDialog = True
    while initDialog:
        print('-------------------------------------------------------')
        print("Inicio de procesamiento. \n********* Seleccione los modelos de predicción *********")
        print("CNN 1 layer (y/n)")
        cnn1 = input()
        print("CNN 2 layers (y/n)")
        cnn2 = input()
        print("VGG16 (y/n)")
        vgg16 = input()
        print("VGG19 (y/n)")
        vgg19 = input()

        if cnn1 in 'n' and cnn2 in 'n' and vgg16 in 'n' and vgg19 in 'n':
            print('###### Por favor seleccione al menos un modelo ######')
            initDialog = True
        else:

            print('###### Modelos seleccionados ######')
            if cnn1 in 'y':
                # add model
                print('CNN 1 layer')
                addModel('CNN_1_layer')
            if cnn2 in 'y':
                # add model
                print('CNN 2 layers')
                addModel('CNN_2_layers')
            if vgg16 in 'y':
                print('VGG16')
                addModel('VGG16')
            if vgg19 in 'y':
                print('VGG19')
                addModel('VGG19')

            print('###### Confirmar envio (y/n) ######')
            proces = input()
            if proces in 'y':
                print('Iniciando procesamiento...')

                resp = requests.post('http://127.0.0.1:5000/predict', json= makeJson())
                f = open('./Information/summaryAnswer.txt', 'w')
                f.write("")
                f.close()
                #print(resp)
                dataA = resp.json()
                #print(dataA)
                if dataA['state'] in 'success':
                    msg = 'Se han realizado las predicciones satisfactoriamente\n'

                    for n in dataA['results']:
                        msg+= 'Modelo: '+ str(n['model_id'])+'\n'

                        for c in n['results']:
                            msg += 'Id imagen: '+ str(c['id_image'])+' Clase: '+ classPred[c['clase']] + ' \n'

                    f = open('./Information/summaryAnswer.txt', 'w')
                    f.write(msg)
                    f.close()

                    print('Puedes revisar el informe en el archivo summaryAnswer.txt :)')
                    msg=""
                if dataA['state'] in 'error':
                    msg = 'Error al realizar las predicciones'
                    f = open('./Information/summaryAnswer.txt', 'w')
                    f.write(msg)
                    f.close()
                    print('Fallas al realizar las predicciones. :(')

                print('#####################################')
                initDialog = False
            else:
                print('Proceso finalizado')
                initDialog = True  # Change

                print('-------------------------------------------------------')
                models = []
                imgs = []

                # Clear data to answer


#addImage('01', 'akjllk')
#addImage('02', 'oiuoioo')

#addModel('KNN')
#addModel('CNN')

#dataSend = makeJson()
#print(dataSend)

#resp = requests.post('http://127.0.0.1:5000/predict', json= makeJson())

#dataA =resp.json()
#print(dataA['results'])


def detectForm(frame, imgClient):
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(frameHSV, rojoBajo, rojoAlto)

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contornos:
        vertices = cv2.approxPolyDP(c, 0.05 * cv2.arcLength(c, True), True)

        area = cv2.contourArea(c)
        if (len(vertices) == 4 and area > 2000):
            imgClient = vertices
            mensaje = "ROI detectado"
            cv2.putText(frame, mensaje, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.drawContours(frame, [c], -1, (0, 0, 255), 3)

    return (frame, imgClient)


pathImg= './ImgROI/'
c_counter = 0

while True:

    ret ,frame = cap.read()
    origFrame = frame
    imgClient =[]

    if ret==True:

        frame = detectForm(frame, imgClient)
        cv2.imshow('frame', frame[0])

        if cv2.waitKey(1) & 0xFF == ord('c'):

            try:
                bord = -30
                x, y, w, h = cv2.boundingRect(frame[1])
                cutImg = origFrame[y - bord:y + h + bord, x - bord:x + w + bord]
                cutImg = cv2.resize(cutImg, (256, 256))

                cv2.imshow("ROI One", cutImg)
                img_name = str(c_counter) + '.tiff'

                cv2.imwrite(str(pathImg) + img_name, cutImg)
                image = open(str(pathImg) + img_name, 'rb')
                image_read = image.read()

                image_64_encode = base64.encodebytes(image_read)

                addImage(img_name, image_64_encode)

                print(img_name)
                c_counter += 1
            except:
                print('Problemas al captura la imagen')


        if cv2.waitKey(1) & 0xFF == ord('p'):
            initDialogUser()
            break



cap.release()
cv2.destroyAllWindows()