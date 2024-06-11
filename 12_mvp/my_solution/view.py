import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

class View:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Data Processing GUI")

        # Create a Text widget to display the data
        self.text_widget = tk.Text(self.root)
        self.text_widget.pack(side=tk.BOTTOM)

        self.selected_option = None

    def add_option_menu(self, options: list[str], index_of_selected_option: int):
        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set(options[index_of_selected_option])
        option_menu = tk.OptionMenu(self.root, self.selected_option, *options)
        option_menu.pack(side=tk.LEFT)

    def add_button(self, text: str, handler: callable):
        button = tk.Button(self.root, text=text, command=handler)
        button.pack(side=tk.LEFT)

    def get_selected_option(self) -> str:
        return self.selected_option.get()

    def display(self):
        self.root.mainloop()
    
    def ask_for_path_to_load_csv(self) -> str:
        return fd.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    def ask_for_path_to_save_csv(self) -> str:
        return fd.asksaveasfile(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

    def show_info(self, title: str, msg: str) -> None:
        mb.showinfo(title, msg)

    def show_error(self, title:str, msg: str) -> None:
        mb.showerror(title, msg)

    def display_on_widget(self, text: str) -> None:
        # Clear widget from previous data
        self.text_widget.delete("1.0", tk.END)
        # set the text of the widget to the data
        self.text_widget.insert(tk.END, text)