# Crear entorn virtual (venv)
Nota: la comanda "python" farà referència a Python 3. En alguns sistemes la comanda ha de ser "python3", o alguna variant. Es pot comprovar fent "python --version"
```python -m pip install venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Instal·lar geckodriver
```wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
tar xzvf geckodriver\*
mv geckodriver /usr/bin
```

# Posar en execució
Per desenvolupar es pot utilitzar qualsevol sistema operatiu, i si es vol provar executar amb l'entorn activat ("source venv/bin/activate"). No obstant, si volem deixar el bot corrent, cal fer els passos següents en un servidor (aquí s'assumeix que és en un servidor GNU/Linux).
## systemd: 
Si el sistema on estem utilitza systemd, podem seguir els passos descrits [aquí](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267). En particular, però, a l'apartat *ExecStart* cal posar com a intèrpret del python la ruta (absoluta) on tenim el venv. Si estigués a /home/oriol/CitatBot2 hauríem de posar /home/oriol/CitatBot2/venv/bin/python.

Això, però, requereix tenir accés a l'usuari root o ser part dels sudoers, i no sempre és possible

## pm2
Podem utilitzar [pm2](https://pm2.io/blog/2018/09/19/Manage-Python-Processes), un gestor de processos utilitzat principalment a NodeJS, però que es pot utilitzar també en Python.
Només cal tenir en compte que, igual que abans, cal utilitzar l'entorn virtual, i no el Python per defecte

## Altres opcions
Existeixen moltes opcions. Us convido a ampliar aquest arxiu amb altres idees.
