import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._grafo = None
        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        countries = self._model.getAllCountries()
        for country in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(country))

        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(str(i)))
        self._view.update_page()


    def handle_graph(self, e):
        country = self._view.ddcountry.value
        anno = self._view.ddyear.value
        if country is None or anno is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("selezionare un anno e una country correttamente"))
            self._view.update_page()
            return
        else:
            annoInt = int(anno)
            self._grafo = self._model.build_Graph(country, annoInt)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"numero di vertici: {len(self._grafo.nodes)} numero di archi: {len(self._grafo.edges)}"))
            self._view.btn_volume.disabled=False
            self._view.update_page()





    def handle_volume(self, e):
        mappa = self._model.calcola_Volumi()
        self._view.txtOut2.controls.clear()
        for key in mappa:
            self._view.txtOut2.controls.append(ft.Text(f"{key[0].Retailer_name} --> {key[1]}"))
        self._view.update_page()



    def handle_path(self, e):
        pass
