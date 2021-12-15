from flask import Flask, jsonify, request
import base64
from Objects.Result import Result
from Objects.Result import Inference
import cv2
from Prediccion import  Prediccion

app = Flask(__name__)

clases=[0,1,2,3,4]
ancho=256
alto=256

results=[]

def imgDecode(listIm, models):
    for n in listIm:
        image_64_decode = base64.decodebytes(n['content'].encode())
        image_result = open('./Img/'+n['id'], 'wb')
        image_result.write(image_64_decode)

    for x in models:

        if x in 'CNN_1_layer':
            miModeloCNN = Prediccion("./Models/CNN_1_layer.h5", ancho, alto)
            resp = Result(1)
            for n in listIm:
                imagen = cv2.imread("./Img/"+n['id'])
                claseResultado = miModeloCNN.predecir(imagen)
                clase = clases[claseResultado]
                a = Inference(clase, n['id'])
                resp.results.append(a.__dict__)

            results.append(resp.__dict__)

        if x in 'CNN_2_layers':
            miModeloCNN = Prediccion("./Models/CNN_2_layers.h5", ancho, alto)
            resp = Result(2)
            for n in listIm:
                imagen = cv2.imread("./Img/"+n['id'])
                claseResultado = miModeloCNN.predecir(imagen)
                clase = clases[claseResultado]
                a = Inference(clase, n['id'])
                resp.results.append(a.__dict__)

            results.append(resp.__dict__)

        if x in 'VGG16':
            miModeloVGG16 = Prediccion("./Models/VGG16.h5", 224, 224)
            resp = Result(3)
            for n in listIm:
                imagen = cv2.imread("./Img/" + n['id'])
                claseResultado = miModeloVGG16.predecir(imagen)
                clase = clases[claseResultado]
                a = Inference(clase, n['id'])
                resp.results.append(a.__dict__)

            results.append(resp.__dict__)

        if x in 'VGG19':
            miModeloVGG19 = Prediccion("./Models/VGG19.h5", 224, 224)
            resp = Result(4)
            for n in listIm:
                imagen = cv2.imread("./Img/" + n['id'])
                claseResultado = miModeloVGG19.predecir(imagen)
                clase = clases[claseResultado]
                a = Inference(clase, n['id'])
                resp.results.append(a.__dict__)

            results.append(resp.__dict__)

    return True

@app.route('/data', methods=['POST'])
def returnData():
    name = request.json['name']+'Ups'
    return jsonify({'nameFull': name})

@app.route('/predict', methods=['POST'])
def returnHi():

    try:

        id_client = request.json['id_client']
        images = request.json['images']
        models = request.json['models']

        print('Imagenes recibidas')
        print(len(images))

        print('Cliente: '+id_client)

        if(imgDecode(images, models)):
            return jsonify({'state': 'success',
                            'message': 'Predictions made satisfactorily',
                            'results': results
                            })

    except:
        return jsonify({'state': 'error',
                        'message': 'Error making predictions'
                        })

@app.errorhandler(404)
def error_404_handler(e):
    return jsonify({'state': 'error',
                    'message': 'Error making predictions'
                    })

if __name__ == "__main__":
    #Debug/Development
    app.run(debug=True, port="5000")