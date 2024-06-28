from Window import Window
from MyFrame import configure_openmc


class Main:
    configure_openmc()
    window = Window()
    window.mainloop()