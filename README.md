# OWDC
OW Datacase - Equipe Mines Paristech 

# TODO 

- ranger un peu les files du git | ======================> (0%) |
- check comment faire des diagramme de voronoï lisible | > (0%) |
- tracer les graphes de parking-carac-basique  | ========> (0%) |
- map avec les caractéristiques de chaque parking  | ====> (0%) |
- tracer x/y pour toutes les data  | ====================> (0%) |

# Remarques


# AIDES

- préalablement installer Panda, numpy, et si autre error du type : 
```python
Traceback (most recent call last):                                                                                                             
  File "script.py", line 21, in <module>                                                                                                
     import pandas as pd                                                                                                                        
 ImportError: No module named pandas
 ```
 
 Vérifier que pip est installé par :
 
 ```python
 pip --version
 ```
 sinon, go sur : https://pip.pypa.io/en/stable/installing/
 
 et : 
 
 pour tout les modules : 
 
 ```python
pip install pandas
 ```
 
- 3 fichiers de data : le principal en contient 24millions. Il y en 2 samples sur le drive, sinon le fichier Data_tuto permet de les extraire en .npy et les utiliser en matrice numpy ensuite via 

```python
dataset = np.load("/path/name_file.npy")
```

- le fichier .html : première visio d'une map avec les différents parkings du dataset dessus (réalisé avec map-2.py). Dispo en image aussi.

- le fichier parking-basique.py permet d'extraire des premières data par parking en .npy : les graphes liés arrivent soon. Pour le lire, suffit de lacher un bon 
```
python parking-caracteristiques-basique-1.py
```

# Autres

