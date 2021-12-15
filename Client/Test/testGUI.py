import requests
from Objects.Image import Image
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading


cap = cv2.VideoCapture('http://192.168.1.1:4747/video')

azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)

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

#addImage('01', 'akjllk')
#addImage('02', 'oiuoioo')

#addModel('KNN')
#addModel('CNN')

#dataSend = makeJson()
#print(dataSend)

#resp = requests.post('http://127.0.0.1:5000/predict', json= makeJson())

#dataA =resp.json()
#print(dataA['results'])
moveDown = 20
moveRight = 20

root = Tk(className='Cliente')
root.geometry("1300x400")

lb01 = ttk.Label(root, text="Modelos - Redes neuronales")
lb01.place(x=0+moveRight, y=0+moveDown)

fonttitle = tkFont.Font(family="Arial", size=16, weight="bold")
lb01.configure(font=fonttitle)


def click_me():
    print("CNN",t.get())
    print("RestNet50", m.get())
    print("MobileNet", n.get())

    ansServer = 'Nop '
    lb07.config(text = ansServer)
    modelCnn.insert(parent='', index='end', iid=4, text='',
                    values=('5', 'Cacerola pequeña', '105'))



t = IntVar()
cnn = Checkbutton(root, text="CNN",  variable=t)
# cnn.pack()
cnn.place(x=0+moveRight, y=30+moveDown)

m = IntVar()
restnet = Checkbutton(root, text="RestNet50",  variable=m)
#restnet.pack()
restnet.place(x=80+moveRight, y=30+moveDown)

n = IntVar()
mobilenet = Checkbutton(root, text="MobileNet",  variable=n)
#mobilenet.pack()
mobilenet.place(x=180+moveRight, y=30+moveDown)


lb06 = ttk.Label(root, text="Respuesta servidor")
lb06.place(x=0+moveRight, y=80+moveDown)

lb07 = ttk.Label(root, text=ansServer)
lb07.place(x=0+moveRight, y=100+moveDown)

b = Button(root, text="Enviar", command=click_me, bg='#82E1F4')
b.pack()
b.place(x=200+moveRight, y=60+moveDown)

##############Cerrar app######################################
btnCancel = ttk.Button(root, text="Salir", command=root.destroy)
btnCancel.place(x=1100,y=360)

########################### Información predicción - modelo CNN ###########################
lb02 = ttk.Label(root, text="CNN")
lb02.place(x=350+moveRight, y=0+moveDown)

fonttitle2 = tkFont.Font(family="Arial", size=16, weight="bold")
lb02.configure(font=fonttitle2)

modelCnn = ttk.Treeview(root)

def makeCNN():
    modelCnn['columns'] = ('id', 'Clase', '% Predicción')

    modelCnn.column("#0", width=0,  stretch=NO)
    modelCnn.column("id",anchor=CENTER, width=80)
    modelCnn.column("Clase", anchor=CENTER, width=120)
    modelCnn.column("% Predicción",anchor=CENTER, width=80)

    modelCnn.heading("#0",text="",anchor=CENTER)
    modelCnn.heading("id", text="ID",anchor=CENTER)
    modelCnn.heading("Clase",text="Clase",anchor=CENTER)
    modelCnn.heading("% Predicción",text="% Predicción",anchor=CENTER)


    modelCnn.pack()
    modelCnn.place (x=350, y=50+moveDown)

""" modelCnn.insert(parent='',index='end',iid=0,text='',
    values=('1','Cuchara','101'))
    modelCnn.insert(parent='',index='end',iid=1,text='',
    values=('2','Tenedor','102'))
    modelCnn.insert(parent='',index='end',iid=2,text='',
    values=('3','Cuchillo','103'))
    modelCnn.insert(parent='',index='end',iid=3,text='',
    values=('4','Molinillo','104'))
    modelCnn.insert(parent='',index='end',iid=4,text='',
    values=('5','Cacerola pequeña','105'))"""



makeCNN()
#########################################################################

########################### Información predicción - modelo RestNet50 ###########################
lb03 = ttk.Label(root, text="RestNet50")
lb03.place(x=650+moveRight, y=0+moveDown)

fonttitle3 = tkFont.Font(family="Arial", size=16, weight="bold")
lb03.configure(font=fonttitle3)

modelRest = ttk.Treeview(root)
modelRest['columns'] = ('id', 'Clase', '% Predicción')

modelRest.column("#0", width=0,  stretch=NO)
modelRest.column("id",anchor=CENTER, width=80)
modelRest.column("Clase", anchor=CENTER, width=120)
modelRest.column("% Predicción",anchor=CENTER, width=80)

modelRest.heading("#0",text="",anchor=CENTER)
modelRest.heading("id", text="ID",anchor=CENTER)
modelRest.heading("Clase",text="Clase",anchor=CENTER)
modelRest.heading("% Predicción",text="% Predicción",anchor=CENTER)

modelRest.insert(parent='',index='end',iid=0,text='',
values=('1','Cuchara','101'))
modelRest.insert(parent='',index='end',iid=1,text='',
values=('2','Tenedor','102'))
modelRest.insert(parent='',index='end',iid=2,text='',
values=('3','Cuchillo','103'))
modelRest.insert(parent='',index='end',iid=3,text='',
values=('4','Molinillo','104'))
modelRest.insert(parent='',index='end',iid=4,text='',
values=('5','Cacerola pequeña','105'))
modelRest.pack()
modelRest.place (x=650, y=50+moveDown)

#########################################################################

########################### Información predicción - modelo MobileNet ###########################
lb04 = ttk.Label(root, text="MobileNet")
lb04.place(x=950+moveRight, y=0+moveDown)

fonttitle4 = tkFont.Font(family="Arial", size=16, weight="bold")
lb04.configure(font=fonttitle4)

modelMobile = ttk.Treeview(root)
modelMobile['columns'] = ('id', 'Clase', '% Predicción')

modelMobile.column("#0", width=0,  stretch=NO)
modelMobile.column("id",anchor=CENTER, width=80)
modelMobile.column("Clase", anchor=CENTER, width=120)
modelMobile.column("% Predicción",anchor=CENTER, width=80)

modelMobile.heading("#0",text="",anchor=CENTER)
modelMobile.heading("id", text="ID",anchor=CENTER)
modelMobile.heading("Clase",text="Clase",anchor=CENTER)
modelMobile.heading("% Predicción",text="% Predicción",anchor=CENTER)

modelMobile.insert(parent='',index='end',iid=0,text='',
values=('1','Cuchara','101'))
modelMobile.insert(parent='',index='end',iid=1,text='',
values=('2','Tenedor','102'))
modelMobile.insert(parent='',index='end',iid=2,text='',
values=('3','Cuchillo','103'))
modelMobile.insert(parent='',index='end',iid=3,text='',
values=('4','Molinillo','104'))
modelMobile.insert(parent='',index='end',iid=4,text='',
values=('5','Cacerola pequeña','105'))
modelMobile.pack()
modelMobile.place (x=950, y=50+moveDown)

#########################################################################

def beginApp():
    while True:

      ret,frame = cap.read()

      if ret==True:
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(frameHSV,azulBajo,azulAlto)

        contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame, contornos, -1, (255,0,0), 3)
        for c in contornos:
          vertices = cv2.approxPolyDP(c, 0.05 * cv2.arcLength(c, True), True)

          if (len(vertices) == 4):
            #imgClient = vertices
            mensaje = "ROI detectado"
            cv2.putText(frame, mensaje, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.drawContours(frame, [c], 0, (0, 0, 255), 2)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            root.mainloop()
            break


beginApp()
cap.release()
cv2.destroyAllWindows()




