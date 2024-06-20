from model.model import Model

myModel = Model()
myModel._creaGrafo("Relax", "2015")
print(myModel.getGraphDetails())
myModel.archiPesanti()
cammino = myModel.percorso(125110)
print(len(cammino))
for c in cammino:
    print(c)

