from selenium.webdriver.firefox.options import Options
from selenium import webdriver
#from contextlib import closing
#from selenium.webdriver import Firefox
#from selenium.webdriver.support.ui import WebDriverWait
#from bs4 import BeautifulSoup
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC
#from urllib.parse import urlsplit, urljoin
#import lxml.html as parser
#import time

options = Options()
options.headless = True

url_loja = 'https://www.submarino.com.br/produto/'
lista_code = open('product_code_list.txt')

#limpa arquivo
open('result_products.txt','w').close()

for cod_produto in lista_code:

	cod_produto = cod_produto.replace('\n','')
	driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
	driver.get(url_loja + cod_produto.replace('\n',''))

	file = open("result_products.txt","a") 

	try:
		print('%s' % cod_produto)

		nome_produto = driver.find_elements_by_xpath("//h1[@id='product-name-default']")[0].text
		#print ("NOME_PRODUTO: %s" % nome_produto)

		html_preco = driver.find_elements_by_xpath("//p[@class='sales-price']")
		preco_produto = float(html_preco[0].text.replace('R$ ','').replace('.','').replace(',','.'))
		#print ('PRECO_PRODUTO: R$%s' % preco_produto)

		html_cb_ame = driver.find_elements_by_xpath("//section[@class='buy-box']/div/div[1]/div/div[2]/span/span[3]/span")
		cashback_ame = float(html_cb_ame[0].text.replace('R$ ','').replace('.','').replace(',','.'))
		#print ("CASHBACK_AME: %s" % cashback_ame)

		desconto_ame = int((cashback_ame*100)/preco_produto)
		#print ("DESCONTO_AME: %s%%" % desconto_ame)

		html_ccloja = driver.find_elements_by_xpath("//section[@class='buy-box']/div/div[@id='brandCard']/div[2]/span/span/span[1]/span[1]")
		preco_ccloja = float(html_ccloja[0].text.replace('R$ ','').replace('.','').replace(',','.'))
		#print ("PRECO_CCLOJA: %s" % preco_ccloja)

		desconto_ccloja = (100 - int((preco_ccloja*100) / preco_produto ) ) 
		#print ("DESCONTO_CCLOJA: %s%%" % desconto_ccloja)

		file.write("%r,%r,%r,%r,%r,\n" % (desconto_ame, desconto_ccloja, preco_produto, cod_produto, nome_produto))
	except:
		print('%s (exception)' % cod_produto)

	file.close()
	driver.quit()

lista_code.close()
