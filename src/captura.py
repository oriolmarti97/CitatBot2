from src import memoria_captures
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import io
from PIL import Image
from pathlib import Path
from config import config

def desar_imatge(img, ruta):
    stream = io.BytesIO(img)
    im = Image.open(stream)
    im.save(ruta)

def get_driver():
    options = Options()
    options.add_argument('--headless')

    driver = selenium.webdriver.Firefox(options=options)
    driver.set_window_size(500, 600)
    return driver

def captura(user, tweet):
    driver = get_driver()
    def _captura(user, tweet):
        if user is None:
            user='_'
        #driver = get_driver()
        driver.get(f"{config.url_captures}/{user}/status/{tweet}")
        t = driver.find_element(By.CLASS_NAME,'main-tweet')
        t = t.find_element(By.CLASS_NAME,'timeline-item')
        img = t.screenshot_as_png
        desar_imatge(img, memoria_captures.get_ruta_img(user, tweet))

        with open(memoria_captures.get_ruta_alt(user, tweet),'w') as f:
            nom = t.find_element(By.CLASS_NAME, 'fullname').text
            usuari = t.find_element(By.CLASS_NAME, 'username').text
            txt = t.find_element(By.CLASS_NAME,'tweet-content').text
            data = t.find_element(By.CLASS_NAME, 'tweet-published').text
            # num_rt = t.find_element(By.CLASS_NAME, 'icon-retweet').text
            # num_likes = t.find_element(By.CLASS_NAME, 'icon').text

            alt = f"Tweet de l'usuari {nom} ({usuari}) a data {data}: {txt}"
            f.write(alt)

    try:
        _captura(user, tweet)
    except Exception as e:
        try:
            _captura(user, tweet)
        except Exception as ee:
            print(repr(e))
            print(repr(ee))
            return False
    finally:
        driver.quit()
    return True

if __name__ == '__main__':
    if captura(None, '1544925927074848768'):
        print(':D')
    else:
        print(':(')
