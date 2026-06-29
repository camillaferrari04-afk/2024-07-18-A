import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._min = None
        self._max = None

    def fillDD(self):
        self._view.dd_min_ch.options.clear()
        self._view.dd_max_ch.options.clear()
        for r in self._model.chromosome():
            self._view.dd_min_ch.options.append(ft.dropdown.Option(text=r, data=r, on_click=self.memomin))
            self._view.dd_max_ch.options.append(ft.dropdown.Option(text=r, data=r, on_click=self.memomax))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        if self._min is None or self._max is None:
            self._view.txt_result1.controls.append(ft.Text("Devi selezionare un cromosoma minimo e massimo", color="red", size=18))
            self._view.update_page()
            return
        if self._min > self._max:
            self._view.txt_result1.controls.append(ft.Text("Il cromosoma massimo deve essere più grande del minimo", color="red", size=18))
            self._view.update_page()
            return

        self.caricamentopagina1()

        nodi, archi = self._model.creategraph(self._min, self._max)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text("Grafo correttamente creato", color="green", size=18))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi: {nodi}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {archi}"))
        self._view.txt_result1.controls.append(ft.Text(f""))

        self._view.txt_result1.controls.append(ft.Text(f"I 5 nodi con il maggior numero di archi uscenti sono:"))
        for nodo in self._model.getnodimaggiori():
            self._view.txt_result1.controls.append(ft.Text(f"{nodo["nodo"]} | num. archi uscenti: {nodo["outed"]} | peso tot.: {nodo["weight"]}"))

        self._view.btn_path.disabled = False

        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()

        self.caricamentopagina2()
        costo, percorso = self._model.percorsoottimo()

        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Percorso piu lungo trovato(costo: {costo}, lunghezza {len(percorso)}", color="green", size=18))
        for i in percorso:
            self._view.txt_result2.controls.append(ft.Text(f"{i}"))
        self._view.update_page()


    def memomin(self, e):
        self._min = e.control.data
    def memomax(self, e):
        self._max = e.control.data

    def caricamentopagina1(self):
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text("Caricamento..."))
        self._view.update_page()

    def caricamentopagina2(self):
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text("Caricamento..."))
        self._view.update_page()
