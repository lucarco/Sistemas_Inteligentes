
#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver

    def GetPlan(self):
        findGoal = False
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        self.open.clear()
        self.precessed.clear()
        # se configura el nodo inicial con valor 0 
        # _ConfigureNode(self, node, parent, newG)
        self._ConfigureNode(self.problem.Initial(), None, 0)
        self.open.append(self.problem.Initial())
        path = []
        #mientras no encontremos la meta y haya elementos en open....
        #TODO implementar el bucle de búsqueda del algoritmo A*

        while len(self.open) > 0 and findGoal == False:
            
            # 1. Ordenamos la lista abierta por el coste total F = G + H de menor a mayor
            self.open.sort(key = lambda n: n.g + n.h)

            # 2. Extraemos el nodo más prometedor (el primero de la lista)
            current = self.open.pop(0)

            # 3. Comprobamos si hemos llegado a la meta
            if current == self.problem.goal:
                findGoal = True
                path = self.ReconstructPath(current)
                break

            # 4. Metemos el nodo actual en la lista de cerrados (procesados)
            self.precessed.add(current)

            # 5. Generamos sus sucesores
            successors = self.problem.GetSucessors(current)

            for sucesor in successors:
                # Si el sucesor ya ha sido explorado (está en cerrados), lo ignoramos
                if sucesor in self.precessed:
                    continue
                
                # Calculamos el nuevo coste G (coste acumulado del actual + el coste de ir a la casilla sucesora)
                nuevo_G = current.g + self.problem.GetGCost(sucesor)
                
                # Buscamos si el sucesor ya está en la lista abierta esperando a ser explorado
                nodo_en_abierta = self.GetSucesorInOpen(sucesor)
                
                if nodo_en_abierta is not None:
                    # Ya estaba en ABIERTA. Miramos si este nuevo camino es más barato (G menor)
                    if nuevo_G < nodo_en_abierta.g:
                        self._ConfigureNode(nodo_en_abierta, current, nuevo_G)
                else:
                    # Es un nodo totalmente nuevo. Lo configuramos y lo metemos en ABIERTA
                    self._ConfigureNode(sucesor, current, nuevo_G)
                    self.ApendInOpen(sucesor)


        return path

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)
        node.SetH(self.problem.Heuristic(node))


    def ApendInOpen(self, node):
        if node.g == None:
            print("ApendInOpen ", node.x, node.y)
        self.open.append(node)

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found

    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        #TODO: devuelve el path invertido desde la meta hasta que el padre sea None.

        path = []
        current = goal

        # se reconstruye hasta el nodo inicial
        while current.parent != None:
            path.append(current)
            current = current.parent
        
        # con [::-1] se invierte
        return path[::-1]



