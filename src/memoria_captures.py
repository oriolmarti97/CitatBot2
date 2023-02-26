#    Copyright 2022 Oriol Martí i Rodríguez
#
#    This file is part of CitatBot.
#
#    CitatBot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CitatBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CitatBot.  If not, see <https://www.gnu.org/licenses/>.
#


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
