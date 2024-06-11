from view import View
from model import Model

class Presenter:
    def __init__(self, view: View, model: Model):
        self.model = model
        self.view = view
        self._add_widgets_to_view()
    
    def run(self):
        self.view.display()

    def _add_widgets_to_view(self):
        self.view.add_button("Load CSV", self.load_csv)
        self.view.add_button("Show input data", self.show_input_data)
        self.view.add_button("Analyze Data", self.analyze_data)
        self.view.add_option_menu(["All", "Temperature", "Humidity", "CO2"], index_of_selected_option=0)
        self.view.add_button("Export Data", self.export_data)
    
    def load_csv(self):
        file_path = self.view.ask_for_path_to_load_csv()
        self.model.load_data(file_path)
        self.view.show_info("Import", "Data successfully loaded!")

    def show_input_data(self):
        try:
            self.view.display_on_widget(str(self.model.data))
        except NameError:
            self.view.show_error("Error", "No data to show!")

    def analyze_data(self):
        if self.model.data is None:
            self.view.show_error("Error", "Please load data first!")
            return
        self.model.process_data(self.view.get_selected_option())
        self.view.display_on_widget(str(self.model.processed_data))

    def export_data(self):
        file_path = self.view.ask_for_path_to_save_csv()
        if file_path is not None:
            self.model.processed_data.to_csv(file_path, index=False)
            self.view.show_info("Export", "Data exported successfully!")
