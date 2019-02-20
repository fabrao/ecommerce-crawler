from contextlib import closing
from selenium.webdriver import Firefox
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
print('opening first url...') #abre html inicial das buscas do submarino no firefox-agent
driver.get("https://www.submarino.com.br/categoria/celulares-e-smartphones/smartphone/f/preco-5000.0:9000.0")

#r: abre o arquivo para leitura e escrita. O stream é posicionado no início do arquivo.
#w: abre o arquivo para leitura e escrita. O stream é posicionado no início do arquivo e o arquivo será criado caso não exista.
#a: abre o arquivo para leitura e escrita. O arquivo será criado caso não exista e o stream é posicionado no final do arquivo.
#limpa arquivo
open('product_code_list.txt','w').close()

while True:
    #cria lista com o html dos 24 itens exibidos na busca
    list_itens = driver.find_elements_by_css_selector("div.main-grid div.product-grid-item")

    file = open("product_code_list.txt","a") 
    #percorre a lista de itens
    for item in list_itens:
        item_srce = item.get_attribute("outerHTML")
        item_html = parser.fromstring(item_srce)
        item_href = item_html.xpath("//a/@href")
        #faz o split do conteudo do href aprovaitando apenas a parte da string anterior a '?' (/produto/133453126)
        item_link = item_href[0].split("?")[0].replace('/produto/','') #DE:/produto/133453126 PARA:133453126
        print(item_link)
        file.write(item_link)
        file.write('\n')

    #define o botao next-page
    button_next = driver.find_elements_by_xpath("//div[@class='card card-pagination']/ul/li[last()]/a")[0]
    source_next = button_next.get_attribute("outerHTML")
    
    if 'href="#"' not in source_next: 
        button_next.click() #clica no botao prox.pagina
        time.sleep(5) #sleep para carregar novos itens
    else:
        break

    file.close()
'''
page_source = driver.page_source
soup = BeautifulSoup(page_source, "lxml")
print(soup.prettify())
'''
driver.quit()