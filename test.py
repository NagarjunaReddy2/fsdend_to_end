import os

path="notebooks/research.ipynb"

dir,file=(os.path.split(path))

os.makedirs(dir,exist_ok=True)

with open(file,"w") as f:
     pass