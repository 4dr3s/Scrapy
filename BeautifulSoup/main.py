import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dictionari_insta_list = []

def get_account_name(soup, dictionari_insta):
    account_name = soup.find('a',
                             class_='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp xqnirrm xj34u2y x568u83')
    if account_name:
        link = account_name.get('href')
        dictionari_insta["account_name"] = account_name.text
        dictionari_insta["profile_link"] = f"https://www.instagram.com{link}"

def get_date(soup, dictionari_insta):
    date = soup.find('time', class_='_a9ze _a9zf')
    if date:
        fecha = date.get('datetime')
        dictionari_insta["post_date"] = fecha

def get_description(soup, dictionari_insta):
    description = soup.find('h1', class_='_ap3a _aaco _aacu _aacx _aad7 _aade')
    if description:
        dictionari_insta["description"] = description.get_text(strip=True)

def get_comment(soup, dictionari_insta):
    comments = soup.find_all('span', class_='_ap3a _aaco _aacu _aacx _aad7 _aade')
    comment_array = []
    for comment in comments:
        comment_array.append(comment.get_text(strip=True))
    dictionari_insta["comments"] = comment_array

def img_vdo(soup, multimedia_list):
    img = soup.find('img', class_='x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3')
    if img:
        image = img.get('src')
        multimedia_list.append(image)
    vdo = soup.find('video', class_='x1lliihq x5yr21d xh8yej3')
    if vdo:
        video = vdo.get('src')
        multimedia_list.append(video)

def multimedia(soup, drive, dictionari_insta):
    multimedia_list = []
    img_vdo(soup, multimedia_list)
    while True:
        try:
            btn_next = WebDriverWait(drive, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='Siguiente' and contains(@class, '_afxw _al46 _al47')]"))
            )
            time.sleep(5)
            btn_next.click()
            time.sleep(2)
            img_vdo(soup, multimedia_list)
        except Exception as e:
            print("Ya no se encontró botón 'Siguiente'")
            break
    dictionari_insta["multimedia_link"] = multimedia_list


def get_info(drive, posts_list):
    for link in posts_list:
        drive.get(link)
        time.sleep(5)
        dictionari_insta = {"link": link}
        print(f'Visitando la publicación: {link}')
        html = drive.page_source
        soup = BeautifulSoup(html, 'html.parser')
        get_account_name(soup, dictionari_insta)
        get_date(soup, dictionari_insta)
        get_description(soup, dictionari_insta)
        get_comment(soup, dictionari_insta)
        time.sleep(3)
        multimedia(soup, drive, dictionari_insta)
        dictionari_insta_list.append(dictionari_insta)

archivo_resultados = open('C:/Users/andre/Downloads/resultados_instagram.txt', 'w', encoding='utf-8')
drive = webdriver.Firefox()
drive.get('https://www.instagram.com/explore/tags/ver%C3%B3nicaabad/')
posts_list = []
time.sleep(5)
article = drive.find_element(By.TAG_NAME, 'article')
posts = article.find_elements(By.TAG_NAME, 'div')
for post in posts:
    if 'x1lliihq x1n2onr6 xh8yej3 x4gyw5p x2pgyrj x56m6dy x1ntc13c xn45foy x9i3mqj' == post.get_attribute('class'):
        link = post.find_element(By.XPATH, './a')
        posts_list.append(link.get_attribute('href'))
get_info(drive, posts_list)

for post in dictionari_insta_list:
    archivo_resultados.write(str(post) + '\n')

archivo_resultados.close()

with open('C:/Users/andre/Downloads/datos_instagram.json', 'w', encoding='utf-8') as json_file:
    json.dump(dictionari_insta_list, json_file, ensure_ascii=False, indent=4)

drive.close()
