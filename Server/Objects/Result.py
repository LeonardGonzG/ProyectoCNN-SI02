
class Result:
    def __init__(self, id):
        self.model_id = id
        self.results = []

class Inference:
    def __init__(self, clase, id_image):
        self.clase = clase
        self.id_image = id_image

"""resp = Result(1)
a = Inference(0, 88)
b = Inference(1, 33)
resp.results.append(a.__dict__)

print(resp.__dict__)"""