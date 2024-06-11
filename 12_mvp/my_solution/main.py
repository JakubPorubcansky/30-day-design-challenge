from view import View
from model import Model
from presenter import Presenter

def main() -> None:
    view = View()
    model = Model()
    presenter = Presenter(view, model)
    presenter.run()

if __name__ == "__main__":
    main()
