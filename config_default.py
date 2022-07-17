from pathlib import Path

class config:
    # utilitzarem https://semver.org/ d'una manera bastant laxa
    versio = '0.1.1'

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
