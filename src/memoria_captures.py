# Arxiu que engloba la gestió de memòria dels arxius generats a partir de la captura d'un cert tweet
from pathlib import Path
from config import config


def __get_ruta(usuari, id_tweet):
    ruta = Path(config.ruta_captures,usuari,id_tweet)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta

def get_ruta_alt(usuari, id_tweet):
    return Path(__get_ruta(usuari, id_tweet), config.nom_arxiu_alt)

def get_ruta_img(usuari, id_tweet):
    return Path(__get_ruta(usuari, id_tweet), config.nom_arxiu_imatge)
