import customtkinter
import customtkinter as ctk
import openmc
import os
import numpy as np
import tkinter as tk
import openmc.plotter
import openmc.stats
import openmc.source
import matplotlib.pyplot as plt
import openmc.config
import matplotlib.colors as mcolors
import glob
import openmc.data


def configure_openmc():
    cross_sections_path = "my_custom_nuclear_data_dir/cross_sections.xml"
    openmc.config['cross_sections'] = cross_sections_path

class MyFrame(customtkinter.CTkFrame):
   def __init__(self, master, **kwargs):
       super().__init__(master, **kwargs)
       os.system('rm *.h5')
       os.system('rm *.xml')
       os.system('rm *.png')

       configure_openmc()

       self.energy_filter = openmc.EnergyFilter.from_group_structure('CCFE-709')

       self.poly_surface_spectra_tally = openmc.Tally
       self.fer_poly_surface_spectra_tally = openmc.Tally
       self.fer_surface_spectra_tally = openmc.Tally

       self.my_materials = openmc.Materials()
       self.poly_cell_region = None
       self.results = openmc.StatePoint
       self.results_filename = None
       self.my_source = openmc.IndependentSource()
       self.cell_universe = openmc.Universe()
       self.fer = openmc.Material(name='fer')
       self.air = openmc.Material(name='air')
       self.cristal = openmc.Material(name='cristal')
       self.polyethylen = openmc.Material(name='polyethylen')

       self.mesh = openmc.RegularMesh()
       self.mesh_tally = openmc.Tally()
       self.my_settings = openmc.Settings()
       self.my_tallies = openmc.Tallies([])
       self.my_tally = openmc.Tally()

       self.plot_files = []
       self.current_plot_index = 0

       self.fer_poly_cone = openmc.XCone()
       self.poly_plane = openmc.XPlane()
       self.fer_poly_plane = openmc.XPlane()
       self.fer_plane = openmc.XPlane()

       self.poly_cell = openmc.Cell()

       self.fer_cell = openmc.Cell()

       self.air_cell = openmc.Cell()
       self.cristal_cell = openmc.Cell()

       self.air_cell_cone = openmc.Cell()

       self.root_cell = openmc.Cell()

       self.root_universe = openmc.Universe()
       self.my_geometry = openmc.Geometry()

       self.label = ctk.CTkLabel(master=self, text="Read me ", text_color="Green")
       self.label.grid(row=0, column=1, pady=10, padx=3)
       """self.read_button = customtkinter.CTkButton(master=self, text="Read me", command=self.read_me)
       self.read_button.grid(row=0, column=2, pady=10, padx=5)"""

       """self.label = ctk.CTkLabel(master=self, text="Generate new file")
       self.label.grid(row=2, column=0, pady=10, padx=5)
       self.entry = customtkinter.CTkButton(master=self, text="Generate File", command=self.generate_input_file(data
                                                                                                                =""))
       self.entry.grid(row=2, column=1, pady=10, padx=5)"""

       """self.label = ctk.CTkLabel(master=self, text="Open new file")
       self.label.grid(row=3, column=0, pady=10, padx=5)
       self.open_button = customtkinter.CTkButton(master=self, text="Open file", command=self.open_file)
       self.open_button.grid(row=3, column=1, pady=10, padx=5)


       self.run_file_button = customtkinter.CTkButton(master=self, text="Run file")
       self.run_file_button.grid(row=3, column=2, pady=10, padx=5)"""


       self.label = ctk.CTkLabel(master=self, text="FIll THE SETTINGS :", text_color="Green")
       self.label.grid(row=4, column=2, pady=10, padx=5)


       self.label = ctk.CTkLabel(master=self, text="1) Materials :")
       self.label.grid(row=6, column=0, pady=10, padx=5)
       self.materiau = customtkinter.CTkButton(master=self, text="Materials", command=self.materiau_click_event)
       self.materiau.grid(row=6, column=1, pady=10, padx=5)

       self.label = ctk.CTkLabel(master=self, text="3) Settings :")
       self.label.grid(row=6, column=2, pady=10, padx=5)
       self.settings = customtkinter.CTkButton(master=self, text="Settings", command=self.setting_click_event)
       self.settings.grid(row=6, column=3, pady=10, padx=5)


       self.label = ctk.CTkLabel(master=self, text="2) Geometry :")
       self.label.grid(row=7, column=0, pady=10, padx=5)
       self.geo = customtkinter.CTkButton(master=self, text="Geometry", command=self.geometry_click_event)
       self.geo.grid(row=7, column=1, pady=10, padx=5)


       self.label = ctk.CTkLabel(master=self, text="5) Tally :")
       self.label.grid(row=7, column=2, pady=10, padx=5)
       self.settings = customtkinter.CTkButton(master=self, text="Tally", command=self.tallies_click_event)
       self.settings.grid(row=7, column=3, pady=10, padx=5)

       self.label = ctk.CTkLabel(master=self, text="4) Mesh :")
       self.label.grid(row=8, column=0, pady=10, padx=5)
       self.def_mesh = customtkinter.CTkButton(master=self, text="Mesh", command=self.mesh_click_event)
       self.def_mesh.grid(row=8, column=1, pady=10, padx=5)


       self.label = ctk.CTkLabel(master=self, text="Show geometry :")
       self.label.grid(row=9, column=0, pady=10, padx=5)
       self.show_geo = customtkinter.CTkButton(master=self, text="Show geometry", command=self.afficher_geo)
       self.show_geo.grid(row=9, column=1, pady=10, padx=5)

       """self.canvas = tk.Canvas(master=self, width=500, height=500, bg='white')
       self.canvas.grid(row=9, column=7, pady=20, padx=20, sticky='nsew')"""

       """self.next_button = customtkinter.CTkButton(master=self, text="Next", command=self.show_next_plot)
       self.next_button.grid(row=10, column=7, pady=10)"""

       """self.label = ctk.CTkLabel(master=self, text="Show source:")
       self.label.grid(row=9, column=2, pady=10, padx=5)
       self.show_source = customtkinter.CTkButton(master=self, text="Show source", command=self.afficher_source)
       self.show_source.grid(row=9, column=3, pady=10, padx=5)"""

       self.label = ctk.CTkLabel(master=self, text="Flux 2D:")
       self.label.grid(row=8, column=2, pady=10, padx=5)
       self.show_source = customtkinter.CTkButton(master=self, text="Flux 2D", command=self.afficher_flux_2d)
       self.show_source.grid(row=8, column=3, pady=10, padx=5)

       self.label = ctk.CTkLabel(master=self, text="Neutron current:")
       self.label.grid(row=10, column=0, pady=10, padx=5)
       self.simulation = customtkinter.CTkButton(master=self, text="Show current", command=self.result_flux_neutronique)
       self.simulation.grid(row=10, column=1, pady=10, padx=5)

       """self.label = ctk.CTkLabel(master=self, text="Different current:")
       self.label.grid(row=12, column=0, pady=10, padx=5)
       self.simulation = customtkinter.CTkButton(master=self, text="Current", command=self.show_different_courrant)
       self.simulation.grid(row=12, column=1, pady=10, padx=5)"""

       self.label = ctk.CTkLabel(master=self, text="Run the simulation:")
       self.label.grid(row=13, column=1, pady=10, padx=5)
       self.simulation = customtkinter.CTkButton(master=self, text="RUN", command=self.run_simulation,
                                                 fg_color="red")
       self.simulation.grid(row=13, column=2, pady=10, padx=5)

       self.label = ctk.CTkLabel(master=self, text="Cross section:")
       self.label.grid(row=9, column=2, pady=10, padx=5)
       self.mat = customtkinter.CTkButton(master=self, text="Plots", command=self.mat_graph_click_event)
       self.mat.grid(row=9, column=3, pady=10, padx=5)

       self.label = ctk.CTkLabel(master=self, text="Extract data:")
       self.label.grid(row=10, column=2, pady=10, padx=5)
       self.extract_data = customtkinter.CTkButton(master=self, text="Extract data", command=self.extraction_data)
       self.extract_data.grid(row=10, column=3, pady=10, padx=5)

       self.label = ctk.CTkLabel(master=self, text="Restart simulation:")
       self.label.grid(row=14, column=1, pady=10, padx=5)
       self.extract_data = customtkinter.CTkButton(master=self, text="Restart", command=self.restart_simulation, fg_color="green")
       self.extract_data.grid(row=14, column=2, pady=10, padx=5)

   """def restart_simulation(self):
       os.system('rm *.h5')
       os.system('rm *.xml')
       os.system('rm *.png')"""

   def restart_simulation(self):
       self.master.destroy()  # Ferme la boucle principale de Tkinter
       self.delete_files()
      #window = Window()
      # window.mainloop()

   def delete_files(self):
       main_directory = r'C:\Users\expert\PycharmProjects\Simulator'
       file_extensions = ['*.h5', '*.xml', '*.png']

       for ext in file_extensions:
           # Lister les fichiers avec le pattern spécifié dans le dossier principal uniquement
           pattern = os.path.join(main_directory, ext)
           files = glob.glob(pattern)
           for file in files:
               if os.path.isfile(file):
                   try:
                       os.remove(file)
                       print(f"Deleted file: {file}")
                   except OSError as e:
                       print(f"Error deleting file {file}: {e}")

   #@staticmethod
   """def generate_input_file(data):
       with open("data.txt", 'a', encoding="utf-8") as file:
           file.write(data)"""


   """def open_file(self):
       file_path = filedialog.askopenfilename()  # Demander à l'utilisateur de choisir un fichier
       if file_path:  # Vérifiez si un fichier a été sélectionné
           try:
               with open(file_path, "r", encoding="utf-8") as file:
                   # content = [line.strip() for line in file.readlines()] transformer le fichier en une liste de chaine de caractere
                   for content in file:
                       content = file.readlines()  # Lire le contenu du fichier
                       # content = content.strip() supprimer ces caractères de saut de ligne,
                       print(content)  # Afficher le contenu du fichier
                   openmc.run(file)
           except IOError:
               print("Erreur lors de l'ouverture du fichier.")"""

   def show_temporary_message(self, message, duration=2000):
       # Create a small window to show the message
       message_window = ctk.CTkToplevel(self)
       message_window.title("Save successfully")
       message_window.geometry("300x50")

       # Make the window appear in the center
       x = self.winfo_rootx() + self.winfo_width() // 2 - 150
       y = self.winfo_rooty() + self.winfo_height() // 2 - 50
       message_window.geometry(f'+{x}+{y}')

       label = tk.Label(message_window, text=message, pady=20)
       label.pack()

       # Close the window after the specified duration
       message_window.after(duration, message_window.destroy)

   def materiau_click_event(self):
       # Créer une nouvelle fenêtre pour les paramètres
       materiau_window = ctk.CTkToplevel(self)
       materiau_window.title("Materials")


       self.label = ctk.CTkLabel(materiau_window, text="Materials", text_color="Green")
       self.label.grid(row=0, column=0, pady=5, padx=5)


       self.name_label = ctk.CTkLabel(materiau_window, text="Name:")
       self.name_label.grid(row=1, column=0, pady=5, padx=5)
       self.name_entry = ctk.CTkComboBox(materiau_window,
                                         values=['fer', 'polyethylen', 'air', 'cristal'])
       self.name_entry.grid(row=1, column=1, pady=5, padx=5)


       self.nuclide_label = ctk.CTkLabel(materiau_window, text="nuclide:")
       self.nuclide_label.grid(row=2, column=0, pady=5, padx=5)
       self.nuclide_entry = ctk.CTkComboBox(materiau_window,
                                            values=['', 'Fe56', 'Fe54', 'Fe57', 'B10', 'C12', 'C13', 'H1', 'H2', 'N14',
                                                    'N15', 'O16', 'O17', 'O18', 'F19', 'B10', 'N14', 'O16', 'O17',
                                                    'O18'])
       self.nuclide_entry.grid(row=2, column=1, pady=5, padx=5)


       self.label = ctk.CTkLabel(materiau_window, text="Ou ajouter un element:")
       self.label.grid(row=3, column=0, pady=5, padx=5)
       self.element_entry = ctk.CTkComboBox(materiau_window,
                                            values=['', 'C', 'H', 'N', 'O'])
       self.element_entry.grid(row=3, column=1, pady=5, padx=5)


       self.label = ctk.CTkLabel(materiau_window, text="Pourcentage:")
       self.label.grid(row=4, column=0, pady=5, padx=5)
       self.densite_entry = ctk.CTkComboBox(materiau_window,
                                            values=['', '0.1', '0.917', '0.021', '0.022', '0.1435', '0.2144',
                                                    '0.781154', '0.209476', '0.158671285'])
       self.densite_entry.grid(row=4, column=1, pady=5, padx=5)


       self.densite_total_label = ctk.CTkLabel(materiau_window, text="Densité total:")
       self.densite_total_label.grid(row=6, column=0, pady=5, padx=5)


       self.unit_label = ctk.CTkLabel(materiau_window, text="Unité:")
       self.unit_label.grid(row=7, column=0, pady=5, padx=3)
       self.unit_entry = customtkinter.CTkComboBox(materiau_window,
                                                   values=['g/cm3', 'kg/m3', 'atom/b-cm', 'atom/cm3', 'sum'])
       self.unit_entry.grid(row=7, column=1, pady=5, padx=5)
       self.unit_entry.set('g/cm3')  # Définir la valeur par défaut


       self.material_d_label = ctk.CTkLabel(materiau_window, text="Valeur :")
       self.material_d_label.grid(row=7, column=2, pady=5, padx=5)
       self.material_d_entry = ctk.CTkComboBox(materiau_window,
                                               values=['', '7.87', '0.94', '0.001205'])
       self.material_d_entry.grid(row=7, column=3, pady=5, padx=5)


       self.label = ctk.CTkLabel(materiau_window, text="Delet an element:")
       self.label.grid(row=4, column=2, pady=5, padx=5)
       self.material_delete_entry = ctk.CTkComboBox(materiau_window,
                                                    values=['', 'C', 'H', 'N', 'F19', 'O', 'Fe56', 'Fe54', 'Fe57', 'B10',
                                                            'C12', 'C13', 'H1', 'H2', 'N14',
                                                            'N15', 'O16', 'O17', 'O18', 'N14', 'O16',
                                                            'O17',
                                                            'O18'])
       self.material_delete_entry.grid(row=4, column=3, pady=5, padx=5)


       self.delete_button = ctk.CTkButton(materiau_window, text="Delete", command=self.delete_element_or_nuclide)
       self.delete_button.grid(row=4, column=4, pady=5, padx=5)


       #self.save_densite_button = ctk.CTkButton(materiau_window, text="Save", command=self.set_densite)
       #self.save_densite_button.grid(row=7, column=4, pady=5, padx=5)


       close_button = ctk.CTkButton(materiau_window, text="Close", command=materiau_window.destroy)
       close_button.grid(row=8, column=4, pady=5, padx=5)


       self.add_button = ctk.CTkButton(materiau_window, text="Add", command=self.add_element_or_nuclide)
       self.add_button.grid(row=3, column=4, pady=5, padx=5)


   def add_element_or_nuclide(self):
       #os.system("rm my_custom_nuclear_data_with_materials/*.h5")
       name = self.name_entry.get()
       nuclide = self.nuclide_entry.get()
       element = self.element_entry.get()
       percent = float(self.densite_entry.get())
       # Vérifier si le matériau existe déjà dans la liste
       existing_material = next((material for material in self.my_materials if material.name == name), None)

       if existing_material:
           # Si le matériau existe, ajouter simplement le nucléide ou l'élément à ce matériau
           if nuclide:
               existing_material.add_nuclide(nuclide, percent)
           else:
               existing_material.add_element(element, percent)
               self.set_densite(existing_material)
       else:
           # Si le matériau n'existe pas, créer un nouveau matériau et l'ajouter à la liste
           new_material = openmc.Material(name=name)  # Vous devez adapter cela selon votre implémentation de la classe Material
           if nuclide:
               new_material.add_nuclide(nuclide, percent)
           else:
               new_material.add_element(element, percent)
           self.my_materials.append(new_material)
           self.set_densite(new_material)
       self.my_materials.export_to_xml()
       self.nuclide_entry.set("")
       self.element_entry.set("")
       self.densite_entry.set("")
       # Show the temporary message
       self.show_temporary_message("Element successfully added!")


   def set_densite(self, material):
       unit = self.unit_entry.get()
       value = float(self.material_d_entry.get())
       name = self.name_entry.get()
       # Recherche du matériau dans la liste et définition de la densité si le matériau existe
       for material in self.my_materials:
           if material.name == name:
               material.set_density(unit, value)
      #else:
           #print("Choix invalide")

   def delete_element_or_nuclide(self):
       nuclide = self.nuclide_entry.get()
       element = self.element_entry.get()
       material_delete = self.material_delete_entry.get()
       for material_delete in self.my_materials:
           if material_delete == nuclide or element:
               self.my_materials.remove(material_delete)
               print(f" element has been deleted. {self.my_materials}")
               break
       else:
           print(f"{material_delete} not found.")

   def geometry_click_event(self):
       # Créer une nouvelle fenêtre pour les paramètres
       geometry_window = ctk.CTkToplevel(self)
       geometry_window.title("Geometry")


       self.label = ctk.CTkLabel(geometry_window, text="CHOOSE YOUR GEOMETRY :", text_color="Green")
       self.label.grid(row=0, column=0, pady=5, padx=3)
       self.objet_entry = ctk.CTkComboBox(geometry_window,
                                             values=['Cone', 'Parallelepided','Cylinder','Sphere'])
       self.objet_entry.grid(row=0, column=1, pady=5, padx=5)


       self.label = ctk.CTkLabel(geometry_window, text="CONE", text_color="Green")
       self.label.grid(row=1, column=0, pady=5, padx=3)


       """self.label = ctk.CTkLabel(geometry_window, text="Rayon cone:")
       self.label.grid(row=2, column=0, pady=5, padx=5)
       self.angle_cone_entry = ctk.CTkComboBox(geometry_window,
                                               values=['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8',
                                                       '0.9'])
       self.angle_cone_entry.grid(row=2, column=1, pady=5, padx=5)"""


       self.label = ctk.CTkLabel(geometry_window, text="Plan")
       self.label.grid(row=2, column=0, pady=5, padx=5)
       self.min_plan_entry = ctk.CTkComboBox(geometry_window,
                                             values=['0.0', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.min_plan_entry.grid(row=2, column=1, pady=5, padx=5)


       self.label = ctk.CTkLabel(geometry_window, text="plan du Cone en x ")
       self.label.grid(row=3, column=0, pady=5, padx=5)
       self.x_cone_entry = ctk.CTkComboBox(geometry_window,
                                           values=['0.0', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.x_cone_entry.grid(row=3, column=1, pady=5, padx=5)
       self.label = self.label = ctk.CTkLabel(geometry_window, text="plan du Cone en y")
       self.label.grid(row=3, column=2, pady=5, padx=5)
       self.y_cone_entry = ctk.CTkComboBox(geometry_window,
                                           values=['0.0', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.y_cone_entry.grid(row=3, column=3, pady=5, padx=5)
       self.label = ctk.CTkLabel(geometry_window, text="plan du Cone en z")
       self.label.grid(row=3, column=4, pady=5, padx=5)
       self.z_cone_entry = ctk.CTkComboBox(geometry_window,
                                           values=['0.0', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.z_cone_entry.grid(row=3, column=5, pady=5, padx=5)


       self.label = ctk.CTkLabel(geometry_window, text="PARALLELEPIPED", text_color="Green")
       self.label.grid(row=4, column=0, pady=5, padx=3)


       self.label = ctk.CTkLabel(geometry_window, text="Min_x")
       self.label.grid(row=5, column=0, pady=5, padx=3)
       self.minx_para_entry = ctk.CTkComboBox(geometry_window,
                                              values=['130', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.minx_para_entry.grid(row=5, column=1, pady=5, padx=3)

       self.label = ctk.CTkLabel(geometry_window, text="Max_x")
       self.label.grid(row=6, column=0, pady=5, padx=3)
       self.maxx_para_entry = ctk.CTkComboBox(geometry_window,
                                              values=['0', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.maxx_para_entry.grid(row=6, column=1, pady=5, padx=3)


       self.label = ctk.CTkLabel(geometry_window, text="Min_y")
       self.label.grid(row=5, column=2, pady=5, padx=3)
       self.miny_para_entry = ctk.CTkComboBox(geometry_window,
                                              values=['0.875', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.miny_para_entry.grid(row=5, column=3, pady=5)
       self.label = ctk.CTkLabel(geometry_window, text="Max_y")
       self.label.grid(row=6, column=2, pady=5, padx=3)
       self.maxy_para_entry = ctk.CTkComboBox(geometry_window,
                                              values=['0.875', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.maxy_para_entry.grid(row=6, column=3, pady=5, padx=3)

       self.label = ctk.CTkLabel(geometry_window, text="Min_z")
       self.label.grid(row=5, column=4, pady=5, padx=3)
       self.minz_para_entry = ctk.CTkComboBox(geometry_window,
                                              values=['0.65', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.minz_para_entry.grid(row=5, column=5, pady=5, padx=3)
       self.label = ctk.CTkLabel(geometry_window, text="Max_z")
       self.label.grid(row=6, column=4, pady=5, padx=3)
       self.maxz_para_entry = ctk.CTkComboBox(geometry_window,
                                              values=['0.65', '10', '20', '30', '40', '50', '60', '70', '80'])
       self.maxz_para_entry.grid(row=6, column=5, pady=5, padx=3)

       self.label = ctk.CTkLabel(geometry_window, text="Créer les dimension de votre salle d'éxperience  :", text_color="Green")
       self.label.grid(row=7, column=0, pady=5, padx=3)


       self.label = ctk.CTkLabel(geometry_window, text="Min_x")
       self.label.grid(row=8, column=0, pady=5, padx=3)
       self.minx_bound_entry = ctk.CTkComboBox(geometry_window,
                                               values=['10', '20', '30', '40', '50', '60', '70', '80'])
       self.minx_bound_entry.grid(row=8, column=1, pady=5, padx=3)
       self.label = ctk.CTkLabel(geometry_window, text="Max_x")
       self.label.grid(row=8, column=2, pady=5, padx=3)
       self.maxx_bound_entry = ctk.CTkComboBox(geometry_window,
                                               values=['10', '20', '30', '40', '50', '60', '70', '80'])
       self.maxx_bound_entry.grid(row=8, column=3, pady=5, padx=3)


       self.label = ctk.CTkLabel(geometry_window, text="Min_y")
       self.label.grid(row=9, column=0, pady=5, padx=3)
       self.miny_bound_entry = ctk.CTkComboBox(geometry_window,
                                               values=['10', '20', '30', '40', '50', '60', '70', '80'])
       self.miny_bound_entry.grid(row=9, column=1, pady=5)
       self.label = ctk.CTkLabel(geometry_window, text="Max_y")
       self.label.grid(row=9, column=2, pady=5, padx=3)
       self.maxy_bound_entry = ctk.CTkComboBox(geometry_window,
                                               values=['10', '20', '30', '40', '50', '60', '70', '80'])
       self.maxy_bound_entry.grid(row=9, column=3, pady=5, padx=3)


       self.label = ctk.CTkLabel(geometry_window, text="Min_z")
       self.label.grid(row=10, column=0, pady=5, padx=3)
       self.minz_bound_entry = ctk.CTkComboBox(geometry_window,
                                               values=['10', '20', '30', '40', '50', '60', '70', '80'])
       self.minz_bound_entry.grid(row=10, column=1, pady=5)
       self.label = ctk.CTkLabel(geometry_window, text="Max_z")
       self.label.grid(row=10, column=2, pady=5, padx=3)
       self.maxz_bound_entry = ctk.CTkComboBox(geometry_window,
                                               values=['10', '20', '30', '40', '50', '60', '70', '80'])
       self.maxz_bound_entry.grid(row=10, column=3, pady=5, padx=3)


       self.button = ctk.CTkButton(geometry_window, text="Save", command=self.geometry_retrieve_settings)
       self.button.grid(row=10, column=5, pady=5, padx=3)


       close_button = ctk.CTkButton(geometry_window, text="Close", command=geometry_window.destroy)
       close_button.grid(row=11, column=5, pady=5, padx=5)


   def geometry_retrieve_settings(self):
       objet = self.objet_entry.get()

       self.cell_universe = openmc.Universe(name='experiment')
       self.root_cell = openmc.Cell(name='root cell')
       self.root_universe = openmc.Universe(universe_id=0, name='root universe')
       # Boundary to surround the geometry
       minx_b = float(self.minx_bound_entry.get())
       maxx_b = float(self.maxx_bound_entry.get())
       miny_b = float(self.miny_bound_entry.get())
       maxy_b = float(self.maxy_bound_entry.get())
       minz_b = float(self.minz_bound_entry.get())
       maxz_b = float(self.maxz_bound_entry.get())

       minp_x = float(self.minx_para_entry.get())
       maxp_x = float(self.maxx_para_entry.get())
       minp_y = float(self.miny_para_entry.get())
       maxp_y = float(self.maxy_para_entry.get())
       minp_z = float(self.minz_para_entry.get())
       maxp_z = float(self.maxz_para_entry.get())

       min_x = openmc.XPlane(-minx_b, boundary_type='vacuum')
       max_x = openmc.XPlane(maxx_b, boundary_type='vacuum')
       min_y = openmc.YPlane(-miny_b, boundary_type='vacuum')
       max_y = openmc.YPlane(maxy_b, boundary_type='vacuum')
       min_z = openmc.ZPlane(-minz_b, boundary_type='vacuum')
       max_z = openmc.ZPlane(maxz_b, boundary_type='vacuum')

       for material in self.my_materials:
           if material.name == 'fer':
               self.fer_material = material
           elif material.name == 'polyethylen':
               self.poly_material = material
           elif material.name == 'air':
               self.air_material = material
           elif material.name == 'cristal':
               self.cristal_material = material

       if objet == 'Cone':
           x_cone = float(self.x_cone_entry.get())
           y_cone = float(self.y_cone_entry.get())
           z_cone = float(self.z_cone_entry.get())
           # rayon = float(self.angle_cone_entry.get())
           min_plan = float(self.min_plan_entry.get())

           self.fer_poly_cone = openmc.XCone(x_cone, y_cone, z_cone, 5.59e-4)
           self.poly_plane = openmc.XPlane(-min_plan, boundary_type='transmission')
           self.fer_poly_plane = openmc.XPlane(0.0, boundary_type='transmission')
           self.fer_plane = openmc.XPlane(min_plan, boundary_type='transmission')

           # Create poly Cell
           self.poly_cell = openmc.Cell(name='poly_cell')
           self.poly_cell.fill = self.poly_material
           self.poly_cell.region = -self.fer_poly_cone & + self.poly_plane & - self.fer_poly_plane
           self.cell_universe.add_cell(self.poly_cell)

           # Create a fer Cell
           self.fer_cell = openmc.Cell(name='fer_cell')
           self.fer_cell.fill = self.fer_material
           self.fer_cell.region = -self.fer_poly_cone & + self.fer_poly_plane & - self.fer_plane
           self.cell_universe.add_cell(self.fer_cell)

           # Create an air Cell
           self.air_cell = openmc.Cell(name='air_cell')
           self.air_cell.fill = self.air_material
           self.air_cell.region = +self.fer_poly_cone | - self.poly_plane | + self.fer_plane
           self.cell_universe.add_cell(self.air_cell)

           """# Create the cone of air cell to specify to provenance of neutron for current calculation
           self.air_cell_cone = openmc.Cell(name='air_cell_cone')
           self.air_cell_cone.fill = self.air_material
           self.air_cell_cone.region = -self.fer_poly_cone & + self.fer_plane
           self.cell_universe.add_cell(self.air_cell_cone)"""

       elif objet == 'Parallelepided':

           self.vol_air_crist = openmc.model.RectangularParallelepiped(-minp_x, maxp_x, -minp_y, maxp_y, -minp_z, maxp_z,
                                                                  boundary_type='transmission')
           self.vol_crist = openmc.model.RectangularParallelepiped(0., 3., -minp_y, maxp_y, -minp_z, maxp_z,
                                                              boundary_type='transmission')
           self.cristal_cell = openmc.Cell(name='cristal_cell')
           self.cristal_cell.fill = self.cristal_material
           self.cristal_cell.region = -self.vol_crist
           self.cell_universe.add_cell(self.cristal_cell)

           self.air_cell = openmc.Cell(name='air_cell')
           self.air_cell.fill = self.air_material
           self.air_cell.region = +self.vol_crist
           self.cell_universe.add_cell(self.air_cell)

           air_crist_cell = openmc.Cell(name='air_crist_cell')
           air_crist_cell.fill = self.air_material
           air_crist_cell.region = -self.vol_air_crist
           self.cell_universe.add_cell(air_crist_cell)
       # OpenMC requires that there is a "root" universe.
       # Let us create a root cell that is filled by the pin cell universe and then assign it to the root universe.
       # Create root Cell
       # Add boundary planes
       self.root_cell.fill = self.cell_universe
       self.root_cell.region = +min_x & -max_x & +min_y & -max_y & +min_z & -max_z
       # We now must create a geometry that is assigned a root universe, put the geometry into a geometry file, and export it to XML.
       # Create root Universe
       self.root_universe.add_cell(self.root_cell)
       # Create Geometry and set root Universe
       self.my_geometry = openmc.Geometry(self.root_universe)
       # Show the temporary message
       self.show_temporary_message("Geometry successfully save!")
       self.my_geometry.export_to_xml()

   """def generate_statepoint_files(self, energy_sources):
       # Retrieve settings from user input
       self.retrieve_settings()

       self.statepoint_files = []
       for energy_source in energy_sources:
           # Update the source energy
           self.my_settings.source.energy = openmc.stats.Discrete([energy_source], [1.0])

           # Create and run the OpenMC model
           model = openmc.model.Model(self.my_geometry, self.my_materials, self.my_settings, self.my_tallies)

           # Remove old files and run OpenMC
           os.system("rm *.h5")
           model.run(tracks=True)

           # Rename the statepoint file
           self.statepoint_filename = f"statepoint_{energy_source}.10.h5"
           os.rename("statepoint.10.h5", self.statepoint_filename)
           self.statepoint_files.append(self.statepoint_filename)

       return self.statepoint_files"""


   def setting_click_event(self):
       # Créer une nouvelle fenêtre pour les paramètres
       settings_window = ctk.CTkToplevel(self)
       settings_window.title("Settings")


       # Ajouter des éléments dans la nouvelle fenêtre
       self.label = ctk.CTkLabel(settings_window, text="PARAMETRES:", text_color="Green")
       self.label.grid(row=0, column=0, pady=5, padx=5)


       self.batches_label = ctk.CTkLabel(settings_window, text="Batches (lots):")
       self.batches_label.grid(row=1, column=0, pady=5, padx=5)
       self.batches_entry = ctk.CTkComboBox(settings_window,
                                            values=['10'])
       self.batches_entry.grid(row=1, column=1, pady=5, padx=5)


       self.nbr_particle_label = ctk.CTkLabel(settings_window, text="Particles number:")
       self.nbr_particle_label.grid(row=2, column=0, pady=5, padx=5)
       self.nbr_particle_entry = ctk.CTkComboBox(settings_window,
                                                 values=['10000'])
       self.nbr_particle_entry.grid(row=2, column=1, pady=5, padx=5)


       self.run_mode_label = ctk.CTkLabel(settings_window, text="run mode:")
       self.run_mode_label.grid(row=3, column=0, pady=5, padx=5)
       self.run_mode_entry = ctk.CTkEntry(settings_window)
       self.run_mode_entry.insert(0, 'fixed source')  # Default value
       self.run_mode_entry.grid(row=3, column=1, pady=5, padx=5)


       self.batches_label = ctk.CTkLabel(settings_window, text="ENERGY:", text_color="Green")
       self.batches_label.grid(row=4, column=0, pady=5, padx=5)


       self.discret_label = ctk.CTkLabel(settings_window, text="Discret energy eV:")
       self.discret_label.grid(row=5, column=0, pady=5, padx=5)
       self.discret_entry = ctk.CTkComboBox(settings_window,
                                            values=['1.0e6', '2.0e6', '5.0e6', '144e3', '15e6'])
       self.discret_entry.grid(row=5, column=1, pady=5, padx=5)


       self.normal_label = ctk.CTkLabel(settings_window, text="Normal energy eV:")
       self.normal_label.grid(row=6, column=0, pady=5, padx=5)
       self.normal_entry = ctk.CTkComboBox(settings_window,
                                           values=['1.0e6', '2.0e6', '5.0e6', '144e3', '15e6'])
       self.normal_entry.grid(row=6, column=1, pady=5, padx=5)


       self.localisation_label = ctk.CTkLabel(settings_window, text="Localisation of x:")
       self.localisation_label.grid(row=5, column=2, pady=5, padx=5)
       self.localisation_entry = ctk.CTkComboBox(settings_window,
                                                 values=['40','-120', '80'])
       self.localisation_entry.grid(row=5, column=3, pady=5, padx=5)


       self.angle_label = ctk.CTkLabel(settings_window, text="Angle:")
       self.angle_label.grid(row=6, column=2, pady=5, padx=5)
       self.angle_entry = ctk.CTkComboBox(settings_window,
                                          values=['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'])
       self.angle_entry.grid(row=6, column=3, pady=5, padx=5)


       self.source_particle_label = ctk.CTkLabel(settings_window, text="Type of source:")
       self.source_particle_label.grid(row=7, column=0, pady=5, padx=5)
       self.source_particle_entry = ctk.CTkComboBox(settings_window,
                                                    values=['neutron', 'photon', 'alpha', 'gamma', 'protons',
                                                            'electron'])
       self.source_particle_entry.grid(row=7, column=1, pady=5, padx=5)


       self.direction_label = ctk.CTkLabel(settings_window, text="Direction source (monodirectional):")
       self.direction_label.grid(row=8, column=0, pady=5, padx=5)
       self.direction_entry = ctk.CTkComboBox(settings_window,
                                              values=['-1', '1'])
       self.direction_entry.grid(row=8, column=1, pady=5, padx=5)


       # Ajouter un bouton "save" pour valider les paramètres
       self.save_button = ctk.CTkButton(settings_window, text="Save", command=self.retrieve_settings)
       self.save_button.grid(row=7, column=3, pady=5, padx=5)


       close_button = ctk.CTkButton(settings_window, text="Close", command=settings_window.destroy)
       close_button.grid(row=8, column=3, pady=5, padx=5)


   def retrieve_settings(self):
       discret = float(self.discret_entry.get())
       normal = float(self.normal_entry.get())
       localisation = float(self.localisation_entry.get())
       angle = float(self.angle_entry.get())
       direction = float(self.direction_entry.get())
       batches = self.batches_entry.get()
       particles = self.nbr_particle_entry.get()
       run_mode = self.run_mode_entry.get()
       source_particle = self.source_particle_entry.get()
       #self.energy_source = normal
       #discret = [1.0e6, 2.0e6, 5.0e6]
       #mean = 10.0
       #p = (-4., 2., 10.)
       p = (localisation, 0.0, 0.0)

       self.source_space = openmc.stats.Point(p)
       self.source_particle = source_particle

       self.discrete_energy = openmc.stats.Discrete([discret], [1.0])
       self.normal_energy = openmc.stats.Normal(normal, 3.0)

       self.isotropic = openmc.stats.Isotropic()
       self.monodirectional = openmc.stats.Monodirectional((direction, 0., 0.))


       self.variation_angle = angle * np.pi / 180  # conversion degré -> rad
       self.normal_polar = openmc.stats.Normal(np.cos(np.pi / 2), np.cos(np.pi / 2 - self.variation_angle))  # en cos(rad)
       self.normal_azimutal = openmc.stats.Normal(np.pi, self.variation_angle)  # en rad
       self.distribution_polar_azimutal = openmc.stats.PolarAzimuthal(mu=self.normal_polar, phi=self.normal_azimutal)


       self.my_source = openmc.IndependentSource(space=self.source_space, angle=self.distribution_polar_azimutal,
                                                 energy=self.normal_energy,
                                                 particle=source_particle)


       # Récupérer les valeurs des paramètres et les utiliser comme requis
       self.my_settings = openmc.Settings()
       self.my_settings.batches = int(batches)
       self.my_settings.particles = int(particles)
       self.my_settings.run_mode = run_mode  # Use the value entered
       self.my_settings.source = self.my_source
       self.show_temporary_message("Settings successfully save!")
       self.my_settings.export_to_xml()

   def mesh_click_event(self):
       # Créer une nouvelle fenêtre pour les paramètres
       mesh_window = ctk.CTkToplevel(self)
       mesh_window.title("Mesh")

       self.label = ctk.CTkLabel(mesh_window, text="Define the mesh use for tallies", text_color="Green")
       self.label.grid(row=0, column=0, pady=5, padx=5)

       self.label = ctk.CTkLabel(mesh_window, text="Dimension x:")
       self.label.grid(row=1, column=0, pady=5, padx=5)
       self.x_entry = ctk.CTkComboBox(mesh_window, values=['500', '1000', '1'])
       self.x_entry.grid(row=1, column=1, pady=5, padx=5)

       self.label = ctk.CTkLabel(mesh_window, text="Dimension y:")
       self.label.grid(row=2, column=0, pady=5, padx=5)
       self.y_entry = ctk.CTkComboBox(mesh_window, values=['1', '500', '1000'])
       self.y_entry.grid(row=2, column=1, pady=5, padx=5)

       self.label = ctk.CTkLabel(mesh_window, text="Dimension z:")
       self.label.grid(row=3, column=0, pady=5, padx=5)
       self.z_entry = ctk.CTkComboBox(mesh_window, values=['500', '1000', '1'])
       self.z_entry.grid(row=3, column=1, pady=5, padx=5)

       self.button = ctk.CTkButton(mesh_window, text="Save", command=self.mesh_define)
       self.button.grid(row=4, column=1, pady=5, padx=3)

       close_button = ctk.CTkButton(mesh_window, text="Close", command=mesh_window.destroy)
       close_button.grid(row=4, column=2, pady=5, padx=5)

   def mesh_define(self):
       x = int(self.x_entry.get())
       y = int(self.y_entry.get())
       z = int(self.z_entry.get())

       self.mesh = openmc.RegularMesh().from_domain(
           self.my_geometry,  # the corners of the mesh are being set automatically to surround the geometry
           dimension=[x, y, z]  # Maillage CARRE nécessaire
       )
       self.show_temporary_message("Mesh successfully save!")

   def tallies_click_event(self):
       # Créer une nouvelle fenêtre pour les paramètres
       tallies_window = ctk.CTkToplevel(self)
       tallies_window.title("Tally")

       self.label = ctk.CTkLabel(tallies_window, text="Choose the particule :", text_color="Green")
       self.label.grid(row=0, column=0, pady=5, padx=5)

       self.particule_entry = ctk.CTkComboBox(tallies_window,
                                              values=['neutron', 'photon', 'gamma', 'alpha', 'proton', 'electron'])
       self.particule_entry.grid(row=0, column=1, pady=5, padx=5)

       self.label = ctk.CTkLabel(tallies_window,
                                 text="Create a surface for the elements  click Yes\n"
                                      "(if the elemnts are fer,air,polyethylen):\n")
       self.label.grid(row=2, column=0, pady=5, padx=5)

       self.surface_button = ctk.CTkButton(tallies_window, text="Yes", command=self.tallies_retrieve_settings)
       self.surface_button.grid(row=2, column=1, pady=5, padx=5)

       self.label = ctk.CTkLabel(tallies_window,
                                 text="Click No will creat automatically a Tally :")
       self.label.grid(row=3, column=0, pady=5, padx=5)
       self.surface_no_button = ctk.CTkButton(tallies_window, text="No", command=self.create_mesh_tally)
       self.surface_no_button.grid(row=3, column=1, pady=5, padx=5)

       close_button = ctk.CTkButton(tallies_window, text="Close", command=tallies_window.destroy)
       close_button.grid(row=4, column=1, pady=5, padx=5)

   def tallies_retrieve_settings(self):
       # sets up particle
       particule = self.particule_entry.get()
       self.neutron_particle_filter = openmc.ParticleFilter(particule)
       self.energy_filter = openmc.EnergyFilter.from_group_structure('CCFE-709')

       # setup the surface filters
       self.fer_provenance_filter = openmc.CellFromFilter(self.fer_cell.id)
       self.poly_provenance_filter = openmc.CellFromFilter(self.poly_cell.id)
       self.air_provenance_filter = openmc.CellFromFilter(self.air_cell_cone.id)

       self.poly_surface_filter = openmc.SurfaceFilter(self.poly_plane.id)
       self.fer_poly_surface_filter = openmc.SurfaceFilter(self.fer_poly_plane.id)
       self.fer_surface_filter = openmc.SurfaceFilter(self.fer_plane.id)

       self.poly_surface_spectra_tally = openmc.Tally(tally_id=None, name='poly_surface_spectra_tally')
       self.poly_surface_spectra_tally.scores = ['current']
       self.poly_surface_spectra_tally.filters = [self.poly_surface_filter, self.poly_provenance_filter,
                                                  self.neutron_particle_filter,
                                                  self.energy_filter]
       self.my_tallies.append(self.poly_surface_spectra_tally)

       self.fer_poly_surface_spectra_tally = openmc.Tally(tally_id=None, name='fer_poly_surface_spectra_tally')
       self.fer_poly_surface_spectra_tally.scores = ['current']
       self.fer_poly_surface_spectra_tally.filters = [self.fer_poly_surface_filter, self.fer_provenance_filter,
                                                      self.neutron_particle_filter, self.energy_filter]
       self.my_tallies.append(self.fer_poly_surface_spectra_tally)

       self.fer_surface_spectra_tally = openmc.Tally(tally_id=None, name='fer_surface_spectra_tally')
       self.fer_surface_spectra_tally.scores = ['current']
       self.fer_surface_spectra_tally.filters = [self.fer_surface_filter, self.air_provenance_filter,
                                                 self.neutron_particle_filter,
                                                 self.energy_filter]
       self.my_tallies.append(self.fer_surface_spectra_tally)
       self.show_temporary_message("Tally successfully save!")

       self.my_tallies.export_to_xml()

   def create_mesh_tally(self):
       # create the tallies
       particule = self.particule_entry.get()
       self.neutron_particle_filter = openmc.ParticleFilter(particule)

       #self.my_tallies = openmc.Tallies()

       self.mesh_filter = openmc.MeshFilter(self.mesh)
       # Create a tally
       self.mesh_tally = openmc.Tally(name='tallies_on_mesh')
       self.mesh_tally.filters = [self.mesh_filter, self.neutron_particle_filter]
       self.mesh_tally.scores = ['flux', 'absorption', 'scatter', '(n,2n)']
       self.mesh_tally.estimator = 'analog'  # Ou 'analog' ou 'collision' ou 'tracklength'
       # create the tallies
       #self.my_tallies = openmc.Tallies([self.mesh_tally])
       self.my_tallies.append(self.mesh_tally)
       self.show_temporary_message("Tally successfully save!")

       self.my_tallies.export_to_xml()

       """data4 = f"Tally: {self.my_tallies}\n" \
               f"Particule: {particule}\n"
       #return data4
       self.generate_input_file(data4)"""
   # Enregistrer les données dans le fichier
   # with open("data.txt", 'w', encoding="utf-8") as file:
   #   file.write(data4)

   def afficher_geo(self):

       if self.fer_cell:
           color_assignment = {self.air_cell: 'deepskyblue', self.poly_cell: 'white', self.fer_cell: 'black'}
       else:
           color_assignment = {self.cristal_cell: 'red', self.air_cell: 'blue'}

       plot = self.my_geometry.plot(basis='xz', color_by='cell', colors=color_assignment, pixels=(500, 500))
       plot.figure.savefig('xz-cell.png')
       self.plot_files.append('xz-cell.png')

       plot = self.my_geometry.plot(basis='xy', color_by='cell', colors=color_assignment, pixels=(500, 500))
       plot.figure.savefig('xy-cell.png')
       self.plot_files.append('xy-cell.png')

       plot = self.my_geometry.plot(basis='yz', color_by='cell', colors=color_assignment, pixels=(500, 500),
                                    origin=(0, 0, 0))
       plot.figure.savefig('yz-cell.png')
       self.plot_files.append('yz-cell.png')


   """def afficher_source(self):

       try:
           plot_source_energy(self.my_source)
           plot_source_position(self.my_source)
           plot_source_direction(self.my_source)

           # Combine the plots into one image
           fig, axes = plt.subplots(3, 1, figsize=(10, 15))
           axes[0].imshow(plt.imread('source_energy.png'))
           axes[0].set_title('Source Energy Distribution')
           axes[0].axis('off')

           axes[1].imshow(plt.imread('source_position.png'))
           axes[1].set_title('Source Position')
           axes[1].axis('off')

           axes[2].imshow(plt.imread('source_direction.png'))
           axes[2].set_title('Source Direction Distribution')
           axes[2].axis('off')

           plt.tight_layout()
           plt.savefig('source.png')
           plt.show()

       except Exception as e:
           print(f"Error in afficher_source: {e}")"""


   def run_simulation(self):
       model = openmc.model.Model(self.my_geometry, self.my_materials, self.my_settings, self.my_tallies)
       model.run(tracks=True)

   def afficher_flux_2d(self):

       plot_nb = "flux_2D"

       self.results = openmc.StatePoint('statepoint.10.h5')

       self.my_tally = self.results.get_tally(name=self.mesh_tally.name)
       my_slice = self.my_tally.get_slice(scores=['flux'])
       my_slice.mean.flatten()
       my_slice.mean.shape = (self.mesh.dimension[0], self.mesh.dimension[2])
       # setting the resolution to the mesh dimensions

       # Affichage flux en 2D
       fig = plt.subplot(411)
       im = fig.imshow(my_slice.mean, extent=self.mesh.bounding_box.extent['xy'], norm=mcolors.LogNorm())
       plt.colorbar(im, ax=fig, label='Flux')
       fig.get_figure().set_size_inches(20, 10)

       my_slice1 = self.my_tally.get_slice(scores=['absorption'])
       my_slice1.mean.flatten()
       my_slice1.mean.shape = (self.mesh.dimension[0], self.mesh.dimension[2])
       fig1 = plt.subplot(412)
       im1 = fig1.imshow(my_slice1.mean, extent=self.mesh.bounding_box.extent['xy'], norm=mcolors.LogNorm())
       plt.colorbar(im1, ax=fig1, label='Absorption')
       fig1.get_figure().set_size_inches(20, 10)  # Taille de 20x10 pouces

       my_slice2 = self.my_tally.get_slice(scores=['scatter'])
       my_slice2.mean.flatten()
       my_slice2.mean.shape = (self.mesh.dimension[0], self.mesh.dimension[2])
       fig2 = plt.subplot(413)
       im2 = fig2.imshow(my_slice2.mean, extent=self.mesh.bounding_box.extent['xy'], norm=mcolors.LogNorm())
       plt.colorbar(im2, ax=fig2, label='Scatter')
       fig2.get_figure().set_size_inches(20, 10)  # Taille de 20x10 pouces

       my_slice3 = self.my_tally.get_slice(scores=['scatter'])
       my_slice3.mean.flatten()
       my_slice3.mean.shape = (self.mesh.dimension[0], self.mesh.dimension[2])
       fig3 = plt.subplot(414)
       im3 = fig3.imshow(my_slice3.mean, extent=self.mesh.bounding_box.extent['xy'], norm=mcolors.LogNorm())
       plt.colorbar(im3, ax=fig3, label='(n,2n)')
       fig3.get_figure().set_size_inches(20, 10)  # Taille de 20x10 pouces"""

       plt.savefig(f'{plot_nb}.png')
       plt.show()


   def result_flux_neutronique(self):

       self.energy1 = [144e3, 565e3, 2.5e6, 15e6]
       self.energy2 = ['144keV', '565keV', '2.5MeV', '15MeV']

       for self.energy_source, plot_nb in zip(self.energy1, self.energy2):

           self.results = openmc.StatePoint('statepoint.10.h5')

           print(self.results)

           self.my_tally = self.results.get_tally(scores=['flux'])
           self.my_slice = self.my_tally.get_slice(scores=['flux'])

           self.my_slice.mean.shape = (self.mesh.dimension[0], self.mesh.dimension[2])

           fig1 = plt.subplot(411)
           im1 = fig1.imshow(self.my_slice.mean, extent=self.mesh.bounding_box.extent['xz'], )
           plt.colorbar(im1, ax=fig1, label=['Flux'])
           fig1.get_figure().set_size_inches(20, 10)

           self.my_tally = self.results.get_tally(scores=['absorption'])
           self.my_slice = self.my_tally.get_slice(scores=['absorption'])

           self.my_slice.mean.shape = (self.mesh.dimension[0], self.mesh.dimension[2])

           fig2 = plt.subplot(412)
           im2 = fig2.imshow(self.my_slice.mean, extent=self.mesh.bounding_box.extent['xz'], )
           plt.colorbar(im2, ax=fig2, label=['Absorption'])
           fig2.get_figure().set_size_inches(20, 10)

           self.my_tally = self.results.get_tally(scores=['scatter'])
           self.my_slice = self.my_tally.get_slice(scores=['scatter'])
           self.my_slice.mean.shape = (self.mesh.dimension[0], self.mesh.dimension[2])

           fig3 = plt.subplot(413)
           im3 = fig3.imshow(self.my_slice.mean, extent=self.mesh.bounding_box.extent['xz'], )
           plt.colorbar(im3, ax=fig3, label=['Scatter'])
           fig3.get_figure().set_size_inches(20, 10)

           self.my_tally = self.results.get_tally(scores=['(n,2n)'])
           self.my_slice = self.my_tally.get_slice(scores=['(n,2n)'])

           self.my_slice.mean.shape = (self.mesh.dimension[0], self.mesh.dimension[2])

           fig4 = plt.subplot(414)
           im4 = fig4.imshow(self.my_slice.mean, extent=self.mesh.bounding_box.extent['xz'], )
           plt.colorbar(im4, ax=fig4, label=['(n,2n)'])
           fig4.get_figure().set_size_inches(20, 10)

           plt.savefig(f'{plot_nb}.png')
           plt.show()

   def extraction_data(self):

       #self.results = openmc.StatePoint(self.results_filename)
       self.results = openmc.StatePoint('statepoint.10.h5')

       self.poly_surface_tally = self.results.get_tally(name='poly_surface_spectra_tally')
       self.fer_poly_surface_tally = self.results.get_tally(name='fer_poly_surface_spectra_tally')
       self.fer_surface_tally = self.results.get_tally(name='fer_surface_spectra_tally')

       bin_boundaries = self.energy_filter.lethargy_bin_width

       poly_current = self.poly_surface_tally.mean.flatten()
       fer_poly_current = self.fer_poly_surface_tally.mean.flatten()
       fer_current = self.fer_surface_tally.mean.flatten()

       normalised_poly_current = -1 * poly_current / bin_boundaries
       normalised_fer_poly_current = -1 * fer_poly_current / bin_boundaries
       normalised_fer_current = -1 * fer_current / bin_boundaries

       lengh_array = len(poly_current)
       print(lengh_array)

       sum_current_surface_fer = normalised_fer_current.sum()
       sum_current_surface_poly = normalised_poly_current.sum()
       sum_current_surface_fer_poly = normalised_fer_poly_current.sum()

       normalised_poly_current = -1 * poly_current / bin_boundaries
       normalised_fer_poly_current = -1 * fer_poly_current / bin_boundaries
       normalised_fer_current = -1 * fer_current / bin_boundaries

       lengh_array = len(poly_current)
       print(lengh_array)
       for i in range(lengh_array):
           sum_current_surface_fer = normalised_fer_current.sum()
           sum_current_surface_poly = normalised_poly_current.sum()
           sum_current_surface_fer_poly = normalised_fer_poly_current.sum()

       if sum_current_surface_fer != 0:
           print("% of particle between current entrance of the cone and exit of the cone " +
                 str(sum_current_surface_poly * 100 / sum_current_surface_fer) + "%")
           print("% of particle between current entrance of the cone and middle of the cone " +
                 str(sum_current_surface_fer_poly * 100 / sum_current_surface_fer) + "%")
       else:
           print("Warning: sum_current_surface_fer is zero, cannot perform division.")

       plt.figure()
       plt.step(self.energy_filter.values[:-1], normalised_poly_current, label='poly surface')
       plt.step(self.energy_filter.values[:-1], normalised_fer_poly_current, label='fer poly surface')
       plt.step(self.energy_filter.values[:-1], normalised_fer_current, label='fer surface')
       plt.xscale('log')
       plt.yscale('log')
       plt.legend()
       plt.ylabel('Neutron current [neutron cm per source particle]')
       plt.xlabel('Neutron Energy [eV]')
       plt.savefig('Current.png')
       plt.show()
       # Create a new window to display the plot
       plot_window = ctk.CTkToplevel(self)
       plot_window.title("Plot")


   def mat_graph_click_event(self):
       # Créer une nouvelle fenêtre pour les paramètres
       mat_window = ctk.CTkToplevel(self)
       mat_window.title("Cross section")

       self.label = ctk.CTkLabel(mat_window, text="Cross section graph", text_color="Green")
       self.label.grid(row=0, column=0, pady=5, padx=5)

       self.label = ctk.CTkLabel(mat_window, text="fer:")
       self.label.grid(row=1, column=0, pady=5, padx=5)
       self.fer_mat_entry = ctk.CTkComboBox(mat_window, values=['absorption', 'total', '(n,2n)', '(n,gamma)'])
       self.fer_mat_entry.grid(row=1, column=1, pady=5, padx=5)

       self.label = ctk.CTkLabel(mat_window, text="polyethylen:")
       self.label.grid(row=2, column=0, pady=5, padx=5)
       self.poly_mat_entry = ctk.CTkComboBox(mat_window, values=['absorption', 'total', '(n,2n)', '(n,gamma)'])
       self.poly_mat_entry.grid(row=2, column=1, pady=5, padx=5)

       self.label = ctk.CTkLabel(mat_window, text="air:")
       self.label.grid(row=3, column=0, pady=5, padx=5)
       self.air_mat_entry = ctk.CTkComboBox(mat_window, values=['absorption', 'total', '(n,2n)', '(n,gamma)'])
       self.air_mat_entry.grid(row=3, column=1, pady=5, padx=5)

       self.label = ctk.CTkLabel(mat_window, text="cristal:")
       self.label.grid(row=4, column=0, pady=5, padx=5)
       self.cristal_mat_entry = ctk.CTkComboBox(mat_window, values=['absorption', 'total', '(n,2n)', '(n,gamma)'])
       self.cristal_mat_entry.grid(row=4, column=1, pady=5, padx=5)

       self.button = ctk.CTkButton(mat_window, text="Save", command=self.show_materiau_graph)
       self.button.grid(row=5, column=1, pady=5, padx=3)

       close_button = ctk.CTkButton(mat_window, text="Close", command=mat_window.destroy)
       close_button.grid(row=6, column=2, pady=5, padx=5)



   def show_materiau_graph(self):

       configure_openmc()
       air = self.air_mat_entry.get()
       poly = self.poly_mat_entry.get()
       fer = self.fer_mat_entry.get()
       cristal = self.cristal_mat_entry.get()

       # Trouver les matériaux dans la liste des matériaux
       for material in self.my_materials:
           if material.name == 'fer':
               self.fer_material = material
           if material.name == 'poly':
               self.poly_material = material
           if material.name == 'air':
               self.air_material = material
           if material.name == 'cristal':
               self.cristal_material = material
       # Vérifier les matériaux trouvés et générer les graphiques
       if self.fer_material and self.poly_material and self.air_material:
           fig5, ax = plt.subplots()
           openmc.plotter.plot_xs(
               axis=ax,
               reactions={
                   self.fer_material: [fer],
                   self.poly_material: [poly],
                   self.air_material: [air],
               }
           )
           ax.set_xlim(1e4, 20e6)
           ax.set_xticks([144e3, 565e3, 2.5e6, 15.1e6])
           ax.xaxis.grid(True)
           ax.yaxis.grid(True)
           plt.savefig('graph_fer_poly_air.png')
           plt.show()

       if self.cristal_material and self.air_material:
           fig5, ax = plt.subplots()
           openmc.plotter.plot_xs(
               axis=ax,
               reactions={
                   self.cristal_material: [cristal],
                   self.air_material: [air],
               }
           )
           ax.set_xlim(1e4, 20e6)
           ax.set_xticks([144e3, 565e3, 2.5e6, 15.1e6])
           ax.xaxis.grid(True)
           ax.yaxis.grid(True)
           plt.savefig('graph_cristal_air.png')
           plt.show()


   """def read_me(self):
       # Créer une nouvelle fenêtre pour les paramètres
       read_window = ctk.CTkToplevel(self)
       read_window.title("Instruction")

       try:
           with open("projet/README", "r") as fichier:
               readme_content = fichier.read()
       except FileNotFoundError:
           readme_content = "README file not found."

           # Create a CTkTextbox widget to display the content
       read_textbox = ctk.CTkTextbox(read_window, width=400, height=300)
       read_textbox.pack(padx=20, pady=20)

       # Insert the README content into the textbox
       read_textbox.insert(ctk.END, readme_content)

       # Make the textbox read-only
       read_textbox.configure(state='disabled')"""












