import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_account_name(soup, archivo_resultados):
    account_name = soup.find('a', class_='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp xqnirrm xj34u2y x568u83')
    if account_name:
        link = account_name.get('href')
        archivo_resultados.write(f'Publicación de: {account_name.text}\n')
        archivo_resultados.write(f'Link de perfil: https://www.instagram.com{link}\n')


def get_date(soup, archivo_resultados):
    date = soup.find('time', class_='_a9ze _a9zf')
    fecha = date.get('datetime')
    if date:
        archivo_resultados.write(f'Fecha de publicación: {fecha}\n')


def get_description(soup, archivo_resultados):
    description = soup.find('h1', class_='_ap3a _aaco _aacu _aacx _aad7 _aade')
    if description:
        archivo_resultados.write(f'Descripción de la publicación: {description.get_text(strip=True)}\n')


def get_comment(soup, archivo_resultados):
    comments = soup.find_all('span', class_='_ap3a _aaco _aacu _aacx _aad7 _aade')
    for comment in comments:
        archivo_resultados.write(f'Comentario de la publicación: {comment.get_text(strip=True)}\n')


def img_vdo(soup, multimedia_list):
    img = soup.find('img', class_='x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3')
    if img:
        image = img.get('src')
        multimedia_list.append(image)
    vdo = soup.find('video', class_='x1lliihq x5yr21d xh8yej3')
    if vdo:
        video = vdo.get('src')
        multimedia_list.append(video)


def multimedia(soup, drive, archivo_resultados):
    multimedia_list = []
    img_vdo(soup, multimedia_list)
    btn_next = drive.find_elements(By.TAG_NAME, 'button')
    for btn in btn_next:
        if ' _afxw _al46 _al47' == btn.get_attribute('class') and 'Siguiente' == btn.get_attribute('Siguiente'):
            btn.click()
            time.sleep(5)
            img_vdo(soup, multimedia_list)
    time.sleep(3)
    archivo_resultados.write(f'Multimedia de la publicación: {multimedia_list}\n\n')


def get_info(drive, posts_list, archivo_resultados):
    for link in posts_list:
        drive.get(link)
        time.sleep(5)
        archivo_resultados.write(f'Publicación: {link}\n')
        print(f'Visitando la publicación :{link}')
        html = drive.page_source
        soup = BeautifulSoup(html, 'html.parser')
        get_account_name(soup, archivo_resultados)
        get_date(soup, archivo_resultados)
        get_description(soup, archivo_resultados)
        get_comment(soup, archivo_resultados)
        time.sleep(3)
        multimedia(soup, drive, archivo_resultados)


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
get_info(drive, posts_list, archivo_resultados)
archivo_resultados.close()
drive.close()
