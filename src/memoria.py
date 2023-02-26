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

from datetime import datetime, timedelta
import json
from pathlib import Path
import copy

# La memòria serà un json
# Aspecte de la memòria:
#    {
#        config_usuaris:{
#            id1:{
#                ranking: True,
#            },
#            id2:{}},
#        estadistiques_setmanals:{
#            // Any, i número de setmana
#            YYYY_W:{
#                usuaris:{
#                    id1:{
#                        usos_bot:N
#                    },
#                    id2:{},
#                },
#                tweets:{
#                    id1:{
#                        num_captures:N
#                    },
#                    id2:{},
#                }
#            }
#        },
#        estadistiques_globals:{
#            usuaris:{
#                id1:{
#                    usos_bot:N
#                }
#            }
#        }
#    }
class Memoria:
    json = 'memoria.json'
    PLANTILLA={
        'config_usuaris':{},
        'estadistiques_setmanals':{},
        'estadistiques_globals':{
            'usuaris':{}
        }
    }
    PLANTILLA_SETMANA={
        'usuaris':{},
        'tweets':{}
    }
    def _setmana_actual(self):
        # retorna el dilluns de la setmana actual
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        monday = now-timedelta(days = now.weekday())
        return monday

    def _setmana_anterior(self):
        # retorna el dilluns de la setmana anterior
        return self._setmana_actual()-timedelta(days=7)

    def _datetime_a_str(self, data):
        return data.strftime('%Y_%W')

    def setmana_actual(self):
        return self._datetime_a_str(self._setmana_actual())

    def setmana_anterior(self):
        return self._datetime_a_str(self._setmana_anterior())

    def _get_json(self):
        with open(self.json) as f:
            cont = f.read()
        return json.loads(cont)
    def _escriu_json(self, js):
        with open(self.json,'w') as f:
            json.dump(js, f, indent=4)
    def __init__(self):
        if not Path(self.json).exists():
            self._escriu_json(self.PLANTILLA)
        pass
    def actualitza_config_ranking(self, usuari, ranking_permes=True):
        js = self._get_json()
        config = js['config_usuaris']
        if usuari not in config:
            config[usuari]={}
        config[usuari]['ranking']=ranking_permes
        self._escriu_json(js)

    def _estadistiques_setmanals(self, js, anterior=False):
        if anterior:
            setmana = self.setmana_anterior()
        else:
            setmana = self.setmana_actual()
        estadistiques_setmanals = js['estadistiques_setmanals']
        if setmana not in estadistiques_setmanals:
            # es podria hardcodejar la plantilla i ens evitaríem la còpia, però intento evitar hardcodejar coses
            estadistiques_setmanals[setmana]=copy.deepcopy(self.PLANTILLA_SETMANA)
        return estadistiques_setmanals[setmana]
    def nova_captura_usuari(self, id_usuari):
        def actualitza_captures_setmanals():
            estadistiques_setmana_actual=self._estadistiques_setmanals(js)
            usuaris = estadistiques_setmana_actual['usuaris']
            if id_usuari not in usuaris:
                usuaris[id_usuari] = {'usos_bot':0}
            usuaris[id_usuari]['usos_bot']+=1
        def actualitza_captures_globals():
            usuaris = js['estadistiques_globals']['usuaris']
            if id_usuari not in usuaris:
                usuaris[id_usuari]={'usos_bot':0}
            usuaris[id_usuari]['usos_bot']+=1
        
        js = self._get_json()
        actualitza_captures_setmanals()
        actualitza_captures_globals()
        self._escriu_json(js)

    def nova_captura_tweet(self, id_tweet):
        js = self._get_json()
        estadistiques_setmana_actual = self._estadistiques_setmanals(js)
        tweets = estadistiques_setmana_actual['tweets']
        if id_tweet not in tweets:
            tweets[id_tweet]={'num_captures':0}
        tweets[id_tweet]['num_captures']+=1
        self._escriu_json(js)

    def _X_mes_frequents_setmana_anterior(self,clau1, clau2):
        js = self._get_json()
        estadistiques_setmanals = self._estadistiques_setmanals(js, anterior=True)
        d = estadistiques_setmanals[clau1]
        aux = [(x,y[clau2]) for (x,y) in d.items()]
        return sorted(aux, key=lambda x: x[1], reverse=True)
    def usuaris_mes_frequents_setmana_anterior(self):
        return self._X_mes_frequents_setmana_anterior('usuaris','usos_bot')
    def tweets_mes_capturats_setmana_anterior(self):
        return self._X_mes_frequents_setmana_anterior('tweets','num_captures')

    def ranking_activat(self, usuari):
        js = self._get_json()
        config = js['config_usuaris']
        return usuari not in config or config[usuari]['ranking']

