from connection import AccessDB
import random




names = ["dummyB", "dummyC", "dummyD", "dummyE", "dummyF", "dummyG"]
images = [
            {'thumb': open("/home/Lucas/Downloads/motivacional-adao-negro.png", 'rb')}, 
            {'thumb': open("/home/Lucas/Downloads/light-bulb-with-drawing-graph.jpg", 'rb')},
            {'thumb': open("/home/Lucas/Downloads/close-up-organic-tomato-with-copy-space.jpg", 'rb')},
            {'thumb': open("/home/Lucas/Downloads/beneficios-matruz-dicas(1).png", 'rb')},
            {'thumb': open("/home/Lucas/Downloads/tired-femalel.jpg", 'rb')},
            {'thumb': open("/home/Lucas/Downloads/cyclist-on-the-finish-line.jpg", 'rb')},
        ]

x = random.randint(0,5)

image = images[x]
name = names[x]

dados = {
    "name": name,
    "text": "LOREM LOREM",
    "date": "2022-11-25T00:07:46Z",
    "category": [],
    "author": 1,
    "public": False,
    "edit": False,
    
}


annotations = AccessDB(name_url="annotations/", tag="ANNOTATIONS")
annotations.post(data=dados, files=image)


 
