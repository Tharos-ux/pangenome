from sys import path
from os.path import exists

odgi_path: str = "./.env/bin"
if exists(odgi_path):
    path.append(odgi_path)
    import odgi
else:
    exit(1)

g = odgi.graph()
print("Ooooof.")
