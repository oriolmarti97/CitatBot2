import tweepy
import re
from src import memoria, memoria_captures, captura
from config import config
import traceback

# per no fer variables globals
# No són constants com a tal, però assumim que sí
class Constants:
    #REGEXCMD = re.compile('\/\w*')
    REGEXCMD = re.compile('\/[a-zA-Z]*')

class Interpretador:
    COMANDES_EXCLOENTS = [('/rankingon','/rankingoff'), ('/citat','/resposta'), ('/citat','/rankingon'), ('/citat', '/rankingoff'), ('/resposta','/rankingon'), ('/resposta','/rankingoff')]
    def es_mencio_explicita(self):
        # Si no s'ha definit usuari el bot no pot saber si la menció és explícita
        if config.usuari == '' or config.usuari is None:
            return True
        return config.usuari.lower() in self._get_contingut_tweet().lower()
    def es_rt(self):
        return hasattr(self.tweet, 'retweeted_status')
    def get_cmd(self):
        return [x.lower() for x in Constants.REGEXCMD.findall(self.tweet.text)]
    def _get_contingut_tweet(self):
        if not hasattr(self.tweet, 'display_text_range'):
            print('display_text_range no existeix :(')
            return self.tweet.text
        return self.tweet.text[self.tweet.display_text_range[0]:self.tweet.display_text_range[1]]
    def __init__(self, tweet):
        # Això estaria millor com a variable de classe, però aleshores no podem accedir a self
        self.switch_cmd = {
                '/rankingon': self._ranking_on,
                '/rankingoff': self._ranking_off,
                '/citat': self._set_citat,
                '/resposta': self._set_resposta,
                '/report': self._reporta,
        }
        self.tweet = tweet
        self.tweet_a_respondre = None
        self.id_usuari = None
        self.es_captura = True
        self.citat = True
        self.usuari_captura = None
        self.id_captura = None
        self.report = False
        self.alt = ''
        self.es_canvi_ranking = False
        self.em_segueix=None
        self.es_tweet_sensible=False
        self.msg_error=''

        self.memoria = memoria.Memoria()

        self._interpreta()

    def _comprova_follow(self):
        try:
            f = api.get_friendship(source_id=self.id_usuari, target_id=config.id_usuari)
            return f[1].followed_by
        except Exception as e:
            traceback.print_exc()
        # si ha fallat, assumim que ens segueix
        return True

    def _interpreta(self):
        self.id_usuari = self.tweet.user.id_str
        comandes = self.get_cmd()
        if self._comandes_excloents(comandes):
            self.msg_error = f'Les comandes {"".join(self._comandes_excloents)} no es poden utilitzar juntes'
            return
        for cmd in self.get_cmd():
            if cmd in self.switch_cmd:
                self.switch_cmd[cmd]()
        if self.es_captura:
            if not self.es_mencio_explicita():
                self.es_captura=False
                return
            api.create_favorite(self.tweet.id)
            self.usuari_captura, self.id_captura = self._obte_tweet_a_capturar()
            if not captura.captura(self.usuari_captura, self.id_captura):
                self.msg_err = 'Em sap greu, no he pogut obtenir la captura'
                self.es_captura=False
                return
            else:
                self.img = memoria_captures.get_ruta_img(self.usuari_captura, self.id_captura)
            with open(memoria_captures.get_ruta_alt(self.usuari_captura, self.id_captura)) as f:
                self.alt = f.read()
            self.em_segueix = self._comprova_follow()

    def _comandes_excloents(self, comandes):
        for grupcmd in self.COMANDES_EXCLOENTS:
            if all(x in comandes for x in grupcmd):
                self.comandes_excloents = grupcmd
                return True
        return False

    def _ranking_on(self):
        self.memoria.actualitza_config_ranking(self.id_usuari,True)
        self.es_canvi_ranking = True
        self.es_captura = False
    def _ranking_off(self):
        self.memoria.actualitza_config_ranking(self.id_usuari,False)
        self.es_canvi_ranking = True
        self.es_captura = False
    def _set_citat(self):
        # redundant, però així queda explícit
        self.citat = True
    def _set_resposta(self):
        self.citat = False
    def _reporta(self):
        self.report = True
        self.es_captura = False

    @staticmethod
    def _te_tweet_citat(tweet):
        return tweet.is_quote_status
    @staticmethod
    def _get_id_tweet_citat(tweet):
        return tweet.quoted_status_id

    @staticmethod
    def _respon_a_tweet(tweet):
        return hasattr(tweet, 'in_reply_to_status_id') and tweet.in_reply_to_status_id is not None
    @staticmethod
    def _get_id_tweet_respost(tweet):
        return tweet.in_reply_to_status_id
    def _obte_tweet_a_capturar(self):
        def obte_tweet_tweepy():
            id1 = self._get_id_tweet_respost(self.tweet)
            tw1 = api.get_status(id1)

            if self.citat:
                if self._te_tweet_citat(tw1):
                    id2 = self._get_id_tweet_citat(tw1)
                else:
                    id2 = self._get_id_tweet_respost(tw1)
            else:
                id2 = self._get_id_tweet_respost(tw1)
            tw2 = api.get_status(id2)
            usr2 = tw2.user.screen_name

            print(usr2, id2)
            return usr2, str(id2)
        # si no podem amb el tweepy, pot ser culpa d'algun bloqueig
        # intentem obtenir-lo per una altra banda
        def obte_tweet_no_tweepy():
            pass


        try:
            return obte_tweet_tweepy()
        except Exception as e:
            traceback.print_exc()
            # TODO: comprovar quina excepció retorna el tweepy i posar-la
            try:
                return obte_tweet_no_tweepy()
            except Exception as ee:
                print(repr(e))
                print(repr(ee))
                self.es_captura = False
                return None


class Escoltador(tweepy.Stream):
    def respon(self, interpretador):
        txt = f'@{interpretador.tweet.user.screen_name} '
        if interpretador.em_segueix:
            pass
        else:
            txt += 'Recorda seguir-me per donar suport al bot!'

        m = api.media_upload(interpretador.img)
        api.create_media_metadata(m.media_id, interpretador.alt)
        api.update_status(txt, in_reply_to_status_id=interpretador.tweet.id, media_ids=[m.media_id])
    def on_status(self, tweet):
        def gestiona_tweet():
            interpretador = Interpretador(tweet)
            if interpretador.es_captura:
                self.respon(interpretador)
                interpretador.memoria.nova_captura_usuari(interpretador.id_usuari)
                interpretador.memoria.nova_captura_tweet(interpretador.id_captura)


            elif interpretador.es_canvi_ranking:
                api.update_status(f'@{interpretador.tweet.user.screen_name} Configuració actualitzada!', in_reply_to_tweet_id=interpretador.tweet.id)
                pass
            elif interpretador.msg_error != '':
                api.update_status(f'@{interpretador.tweet.user.screen_name} {interpretador.msg_error}', in_reply_to_tweet_id=interpretador.tweet.id)

            if interpretador.report:
                text=f'https://twitter.com/tweet/{interpretador.tweet.user.screen_name}/{interpretador.tweet.id}'
                for user in config.admins:
                    api.send_direct_message(recipient_id=user, text=text)

        try:
            gestiona_tweet()
        except Exception as e:
            traceback.print_exc()


if __name__=='__main__':
    auth = tweepy.OAuthHandler(config.Keys.consumer_key,config.Keys.consumer_secret)
    auth.set_access_token(config.Keys.access_token,config.Keys.access_token_secret)
    api=tweepy.API(auth, wait_on_rate_limit=True)

    escoltador=Escoltador(*config.keys)
    escoltador.filter(track=[config.usuari])

