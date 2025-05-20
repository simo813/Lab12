import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        listNationsCO = self._model.passNations()
        for nation in listNationsCO:
            self.view.ddcountry.options.append(ft.dropdown.Option(key=nation, text=nation))
        self.view.ddyear.options.append(ft.dropdown.Option(key="2015", text="2015"))
        self.view.ddyear.options.append(ft.dropdown.Option(key="2016", text="2016"))
        self.view.ddyear.options.append(ft.dropdown.Option(key="2017", text="2017"))
        self.view.ddyear.options.append(ft.dropdown.Option(key="2018", text="2018"))
        self.view.update_page()



    def handle_graph(self, e):
        self._model.createGraph(self.view.ddcountryValue, self.view.ddyearValue)
        graph = self._model.graphMO
        nNodes = graph.number_of_nodes()
        nEdges = graph.number_of_edges()
        self.view.txt_result.controls.append(
                ft.Text(f"Numero di vertici: {nNodes} Numero di archi: {nEdges}"))
        self.view.update_page()




    def handle_volume(self, e):
        pass


    def handle_path(self, e):
        pass
