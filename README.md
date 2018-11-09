# OWDC
OW Datacase - Equipe Mines Paristech 


## Pour l'équipe : 

# AIDES

- Pour les fichiers .html : ouvrir, cliquer sur "Raw", copier-coller le texte :
```html
<!DOCTYPE html>
<head>    
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" /> .......
 ```
dans un éditeur de texte (atom, visual studio code,...) et changer l'extension de .txt en .html (sur votre ordinateur) : plus qu'à l'ouvrir. 
Sur la droite : un filtre pour afficher les différentes data, les légendes sont en haut.

- préalablement installer Panda, numpy, et si autre errors du type : 
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
 
 pour tout les modules (exemple avec pandas) : 
 
 ```python
pip install pandas
 ```
 
- 3 fichiers de data : le principal en contient 24millions. Il y en 2 samples sur le drive, sinon le fichier Data_tuto permet de les extraire en .npy et les utiliser en matrice numpy ensuite via 

```python
dataset = np.load("/path/name_file.npy")
```



