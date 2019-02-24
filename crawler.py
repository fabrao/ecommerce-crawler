from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import lxml.html as parser
import time
import sys
import os
import shoplist

store=sys.argv[1]
category=sys.argv[2]

print ('### BEGIN: %s ###' % str(datetime.now()))

options = Options()
options.headless = True

print('firefox-agent starting...') #executa firefox-agent
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
print('opening main url...') #abre html inicial das buscas do submarino no firefox-agent

url_base = 'https://'+store+'.com.br/categoria/'+eval('shoplist.'+category)
driver.get(url_base)
#driver.get("https://www.submarino.com.br/categoria/celulares-e-smartphones/smartphone/f/preco-500.0:9000.0")

products_filepath = 'products/'+category+'.txt'
products_filepath_tmp = products_filepath.replace('.txt', '_tmp.txt')

open(products_filepath_tmp,'w').close() #limpa arquivo
#r: abre o arquivo para leitura e escrita. O stream é posicionado no início do arquivo.
#w: abre o arquivo para leitura e escrita. O stream é posicionado no início do arquivo e o arquivo será criado caso não exista.
#a: abre o arquivo para leitura e escrita. O arquivo será criado caso não exista e o stream é posicionado no final do arquivo.

page_num = 0;
while True:
    page_num += 1
    print ('PAGE: %d' % page_num)
    
    products_file_tmp = open(products_filepath_tmp,"a")
    find_success = False
    count_except = 0
    while find_success == False and count_except < 5 :
        try:
            #cria lista com o html dos 24 itens exibidos na busca
            list_itens = driver.find_elements_by_css_selector("div.main-grid div.product-grid-item")
            for item in list_itens:
                item_srce = item.get_attribute("outerHTML")
                item_html = parser.fromstring(item_srce)
                item_href = item_html.xpath("//a/@href")
                #faz o split do conteudo do href aprovaitando apenas a parte da string anterior a '?' (/produto/133453126)
                item_code = item_href[0].split("?")[0].replace('/produto/','') #DE:/produto/133453126 PARA:133453126
                products_file_tmp.write(item_code)
                products_file_tmp.write('\n')
                find_success = True
        except:
            find_success = False
            count_except += 1
            time.sleep(1)

    #define o botao next-page
    button_next = driver.find_elements_by_xpath("//div[@class='card card-pagination']/ul/li[last()]/a")[0]
    source_next_button = button_next.get_attribute("outerHTML")
    
    if 'href="#"' not in source_next_button: 
        button_next.click() #clica no botao prox.pagina
        time.sleep(2)
        source_next_button_new = driver.find_elements_by_xpath("//div[@class='card card-pagination']/ul/li[last()]/a")[0].get_attribute("outerHTML")
        count_loop = 0
        while source_next_button_new == source_next_button and count_loop < 12:
            count_loop += 1
            #if count_loop % 5 == 0:
            #    button_next.click()
            time.sleep(2)
            source_next_button_new = driver.find_elements_by_xpath("//div[@class='card card-pagination']/ul/li[last()]/a")[0].get_attribute("outerHTML")
    else: #ultima pagina de produtos
        break
    products_file_tmp.close()
driver.quit()


#Remove codigos duplicados
list_not_duplicate = set()
products_file  = open(products_filepath, "w")
products_file_tmp = open(products_filepath_tmp, "r")

for code in products_file_tmp:
    if code not in list_not_duplicate:
        products_file.write(code)
        list_not_duplicate.add(code)

products_file.close()
products_file_tmp.close()
os.remove(products_filepath_tmp)

print ('#### END: %s ####' % str(datetime.now()))
