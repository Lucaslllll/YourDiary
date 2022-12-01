from connection import AccessDB
import random
import sys


class TestCrudInTable(object):

    # for post and put
    def load(self):

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

        self.image = images[x]
        name = names[x]

        self.dados = {
            "name": name,
            "text": "LOREM LOREM",
            "date": "2022-11-25T00:07:46Z",
            "category": [],
            "author": 1,
            "public": False,
            "edit": False,
            
        }

    def execute(self, method, name_url="annotations/"):

        try:  
            # se não for post nem put, então AssertionError será método inválido
            assert method == "PUT" or method == "POST" or method == "GET" or method == "DELETE", "método inválido"
            if method == "POST":
                annotations = AccessDB(name_url=name_url, tag="ANNOTATIONS")
                annotations.post(data=self.dados, files=self.image)
            elif method == "PUT":
                annotations = AccessDB(name_url=name_url, tag="ANNOTATIONS")
                annotations.put(data=self.dados, files=self.image)

        except AssertionError as msg:
            print(msg)


test = TestCrudInTable()
test.load()

if len(sys.argv) > 1:
    if len(sys.argv) == 2:
        test.execute(method=sys.argv[1], name_url=sys.argv[2])

    test.execute(method=sys.argv[1])


