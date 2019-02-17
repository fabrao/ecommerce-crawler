from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from urllib.parse import urlsplit, urljoin
import lxml.html as parser
import time

options = Options()
options.headless = True

print('firefox-agent starting...') #executa firefox-agent
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
print('opening start-url...') #abre html inicial das buscas do submarino no firefox-agent
driver.get("https://www.submarino.com.br/categoria/celulares-e-smartphones/smartphone/f/preco-500.0:9000.0")


for x in range(3):
    print('\nLOOP: %s' % x)
    #define o botao next-page
    buttonNext = driver.find_elements_by_xpath("//div[@class='card card-pagination']/ul/li[last()]/a")
    buttonNext = buttonNext[0]

    #cria lista com o html dos 24 itens exibidos na busca
    listItens = driver.find_elements_by_css_selector("div.main-grid div.product-grid-item")

    #percorre a lista de itens
    for item in listItens:
        item_srce = item.get_attribute("outerHTML")
        item_html = parser.fromstring(item_srce)
        item_href = item_html.xpath("//a/@href")
        #faz o split do conteudo do href aprovaitando apenas a parte da string anterior a '?' (/produto/133453126)
        item_link = item_href[0].split("?")[0]
        print(item_link)

    buttonNext.click() # Clica no botao prox.pagina
    time.sleep(10) #sleep para carregar novos itens
    page_source = driver.page_source

#soup = BeautifulSoup(page_source, "lxml")
#print(soup.prettify())
driver.quit()