import os
import customtkinter
from MyFrame import MyFrame
from PIL import Image, ImageTk


class Window(customtkinter.CTk):
   def __init__(self):
       super().__init__()
       self.geometry("720x720")
       self.title("Monte Carlo Simulator")

       icon_path = 'Benchmark/logo-cnrs.png'
       if os.path.exists(icon_path):
           self.icon_image = ImageTk.PhotoImage(Image.open(icon_path))
           self.wm_iconphoto(True, self.icon_image)
           #self.iconphoto(True, self.icon_image)
       else:
           print(f"Icon file not found: {icon_path}")

       self.grid_rowconfigure(0, weight=1)  # configure grid system
       self.grid_columnconfigure(0, weight=1)

       self.my_frame = MyFrame(master=self)
       self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
