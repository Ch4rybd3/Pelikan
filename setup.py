from distutils.core import setup
import py2exe

setup(
    windows=['main.py'],  # Si ton script utilise Tkinter (GUI)
    options={
        'py2exe': {
            'packages': ['tkinter', 'PIL'],
            'includes': ['tkinter', 'PIL'],
            'bundle_files': 1,  # Tout inclure dans un seul fichier exécutable
            'compressed': True,  # Compresser l'exécutable
        }
    },
    zipfile=None  # Ne pas créer de fichier ZIP séparé
)
