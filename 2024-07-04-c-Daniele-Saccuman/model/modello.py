from database.DAO import DAO
import networkx as nx
#from geopy import distance

class Model:
    def __init__(self):
        self._listSighting = []
        self._listShapes = []
        self._listYears = []
        self._listShapes = []

        self._grafo = nx.DiGraph()
        self._nodi = []
        self._archi = []
        self._idMap = {}


    def getYears(self):
        self._listYears = DAO.getAllYears()
        return self._listYears

    def getShape(self, anno):
        self._listShape = DAO.getAllShapes(anno)
        return self._listShape

    @property
    def listSighting(self):
        return self._listSighting

    def buildGraph(self, anno, shape):
        self._grafo.clear()
        self._nodi = DAO.get_all_sightings(anno, shape)
        for s in self._nodi:
            self._idMap[s.id] = s

        self._grafo.add_nodes_from(self._nodi)
        self._archi = DAO.getAllEdges(anno, shape)

        for e in self._archi:
            if e[1] < e[3]:
                peso = e[3] - e[1]
                self._grafo.add_edge(self._idMap[e[0]], self._idMap[e[2]], weight = peso)
            elif e[1] > e[3]:
                peso = e[1] - e[3]
                self._grafo.add_edge(self._idMap[e[2]], self._idMap[e[0]], weight=peso)

    def archiPesiMaggiori(self):
        listaArchi = []
        listaBest = []
        for uscente, entrante in self._grafo.edges():
            pesoArco = self._grafo[uscente][entrante]["weight"]
            listaArchi.append((uscente, entrante, pesoArco))
        listaArchi.sort(key=lambda x: x[2], reverse=True)
        conta = 0
        for a in range(0, len(listaArchi)):
            if conta <= 4:
                listaBest.append(listaArchi[a])
                conta = conta + 1
        return listaBest

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getEdges(self):
        return list(self._grafo.edges())

    def getNodes(self):
        return list(self._grafo.nodes())
