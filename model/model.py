import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._brands = DAO.getAllBrands()

    def _creaGrafo(self, brand, anno):
        self._grafo.clear()
        self._nodes = DAO.getAllNodes(brand)
        self._grafo.add_nodes_from(self._nodes)
        nodi = self._nodes
        for u in nodi:
            for v in nodi:
                if u != v:
                    arco = DAO.getEdge(u, v, anno)
                    if arco[0][0] != None:
                        self._grafo.add_edge(arco[0][0], arco[0][1], weight=arco[0][2])

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def archiPesanti(self):
        archi = list(self._grafo.edges(data=True))
        archi.sort(key=lambda x: x[2]["weight"], reverse=True)
        top3 = archi[:3]
        nodiDuplicati = []
        nodiUnici = []
        for a in top3:
            u = a[0]
            v = a[1]
            if u not in nodiUnici:
                nodiUnici.append(u)
            elif u not in nodiDuplicati:
                nodiDuplicati.append(u)

            if v not in nodiUnici:
                nodiUnici.append(v)
            elif v not in nodiDuplicati:
                nodiDuplicati.append(v)

        return top3, nodiDuplicati

    def percorso(self, partenza):
        self._bestPath = []
        self._ricorsione(partenza, [])
        return self._bestPath

    def _ricorsione(self, nodo, parziale):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        # ordino la lista dei vicini così taglia delle soluzioni prima
        vicini = self._grafo.neighbors(nodo)
        lista_vicini = []
        for v in vicini:
            edgeW = self._grafo[nodo][v]["weight"]
            lista_vicini.append((v, edgeW))
        lista_vicini.sort(key=lambda x: x[1], reverse=True)

        for v in lista_vicini:
            peso_arco = v[1]
            peso_ultimo = 0
            if len(parziale) > 0:
                peso_ultimo = parziale[-1][2]
            if peso_arco >= peso_ultimo and self.filtroArchi(nodo, v[0], parziale):
                parziale.append((nodo, v[0], peso_arco))
                self._ricorsione(v[0], parziale)
                parziale.pop()

    def filtroNodi(self, v, parziale):      # no percorso semplice, non serve
        pass

    def filtroArchi(self, n, v, parziale):
        for a in parziale:
            if a[:2] == (n, v) or a[:2] == (v, n):
                return False
        return True
