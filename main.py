import sys

from app.consola import menu
from interfaz.gui import iniciar_gui


if __name__ == "__main__":
    if "--cli" in sys.argv:
        menu()
    else:
        iniciar_gui()