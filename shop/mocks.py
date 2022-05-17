import requests

#l'ecoscore est stocké dans une constante et sera réutilisé dans nos tests
ECOSCORE_GRADE = 'd'

def mock_openfoodfact_success(self, method, url):
    #Notre mock doit avoir la même signature que la méhode à mocker
    #A savoir les mêmes paramètres d'entrée et le type de sortie
    def monker_json():
        #Nous créeons une méthode qui servira à mockey patcher response.json()
        return {
            'product':{
                'ecoscore_grade':ECOSCORE_GRADE
            }
        }
    #Créons la réponse et modifions ses valeurs pour que le status code et les
    # données correspondent à nos attendus"
    response = requests.Response()
    response.status_code = 200
    #Nous "mocker pastons" notre response.json
    # Attention à ne pas metttre les (), nous n'appelons pas la méthode,
    # mais on la remplace afin de tester en local
    response.json = monker_json
    return response
