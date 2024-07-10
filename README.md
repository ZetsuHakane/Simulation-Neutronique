# Simulation-Neutronique
Pour commencer le test il faudra installer different module via votre invite de commande 

1 - Premieres etapes : allez dans votre invite de commande et taper les commande dans cette ordre pour installer openmc.
telecharger le repertoire dans votre terminal faite taper :

git clone https://github.com/ZetsuHakane/Simulation-Neutronique.git

Une fois le dossier telecharge aller dans le dossier via cd lien vers le repertoire 

cd Simulation-Neutronique/

2 - Deuxieme etapes telecharger OpenMc dans le dossier Simulation-Neutroniaue:

- chmod u+x *.py
- sudo apt-get install python3-pil.imagetk  python3-tk
- sudo apt install g++ cmake libhdf5-dev libpng-dev hdf5-helpers
- git clone --recurse-submodules https://github.com/openmc-dev/openmc.git
- cd openmc
- mkdir build && cd build
- cmake ..
- make
- sudo make install
- cd ..
- python -m pip install .

3 - Troisieme etape 
Lancer l'applicatio via :
run main 

####### PS N'oublliez pas d'appuier sur le bouton 'Save' pour tous les onglets

_ Instruction pour faire une simulation avec un cone : 

- Pressez le boutton "Materiaux" Entrez vos eleemnts pour la simulation pour simuler un cone utiliser 3 elements le fer, le polyethylene, et l'air entrer a chaque fois un nouveau pourcentage ppour chaque muclide mais entrer une fois la densite pour chaque elements
- Pressez le boutton "Geometry" Creer votre geometrie choisir le type de geometrie ici le cone est par defaut entrer les dimensions de votre cone, et entrer les dimensions de votre salle d'experience
- Pressez le boutton "Settings" Entrez vos settings, l'energie de la soucre, le nombre de particule par lots, l'angle du cone
- Pressez le boutton "Tally" Creer un Tally entrer Oui si votre simulation est pour un cone ainsi vous pourrez visualiser le courant en 2D et extraire les donnes.
  
_ Instruction pour une simulation cristal 

- Pressez le boutton "Materiaux"
- Pressez le boutton "Geometry" pour un parallelepiped choisir via l'o=nglet en haut a gauche paralleliped, puis entrer les diension de votre cristal et votre salle d'expereince 
- Pressez le boutton "Settings" entrez les parametres de la simulation, l'energie etc...
- Pressez le boutton "Mseh" pour creer un maillage
- Pressez le boutton "Tally" appuier sur non pour creer un tally automatiquement.
- Pour visualiser le flux clicker sur 2D, pour visualiser les sections efficace clicker sur cross section et choisir le type de graphique en pour les materiaux ici le cristal contient tout les materiaux donc vous devez juste choisir le type de graphique pour le cristal

Pour fermet la fenetre clicker sur 'Restart' la fenetre va se fermer et pour relancer une fois la simulation sur votre terminal relancer la commande 
run main 
