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
from pathlib import Path

class config:
    # utilitzarem https://semver.org/ d'una manera bastant laxa
    versio = '0.1.2'

    usuari = ''
    url_captures = 'https://farside.link/nitter/'
    # usuaris als que s'enviaran notificacions en cas de ser necessari
    # ha de ser una llista/tupla de les ids dels usuaris
    admins = []


    ruta_captures = Path('./captures')

    nom_arxiu_imatge = 'captura.png'
    nom_arxiu_alt = 'ALT.txt'

    class Keys:
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''
