from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import json

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service = servico)

acao = ActionChains(navegador)

navegador.get('https://www.nba.com/stats/players/traditional?CF=MIN*GE*100&PerMode=Totals&dir=-1&sort=PTS')

aceitar_cookies = navegador.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
aceitar_cookies.click()
sleep(2)
seletor = navegador.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[4]/div/label/div/select')
seletor.click()
acao.send_keys('a' + Keys.ENTER).perform()

lista = [{}]
time = {}
total = tentativas = 1


while True:
    if total > 30:
        break        
    existe = False
    team = navegador.find_element(By.XPATH, f'//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{tentativas}]/td[3]/a')
    url = team.get_attribute('href')
    url = url.replace('https://www.nba.com/stats/team/', '')
    img_url = f'https://cdn.nba.com/logos/nba/{url}/global/L/logo.svg'
    for item in lista:
        if team.text in item.values():
            existe = True
            break
    if not existe:
        time = {"TName": team.text, "team_img": img_url} 
        lista.append(time.copy())
        total +=1
    tentativas +=1

j = json.dumps(lista)

#creating a json file in the desired path
with open ("desired_path\\Teams_List.json", "w") as f:
     f.write(j)
