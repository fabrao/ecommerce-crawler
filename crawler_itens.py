from lxml.cssselect import CSSSelector
from datetime import datetime
from lxml import html
from shutil import copyfile
import requests
import traceback
import sys
import os

store = sys.argv[1]
category = sys.argv[2]

products_filepath = 'products/'+category+'.txt'
results_filepath = 'results/'+category+'-'+store+'.txt'

products_filepath_tmp = products_filepath.replace('.txt', '_tmp.txt')
url_base = 'https://www.'+store+'.com.br/produto/'

print ('### BEGIN: %s ###' % str(datetime.now()))

list_gallery_codes = set()
products_file = open(products_filepath)
#r: abre o arquivo para leitura e escrita. O stream é posicionado no início do arquivo.
#w: abre o arquivo para leitura e escrita. O stream é posicionado no início do arquivo e o arquivo será criado caso não exista.
#a: abre o arquivo para leitura e escrita. O arquivo será criado caso não exista e o stream é posicionado no final do arquivo.

open(results_filepath,'w').close() #limpar arquivo

for product_code in products_file:

	page = html.fromstring(requests.get(url_base + product_code).content)
	product_code = product_code.replace('\n','')
	
	try:
		full_price_html = page.xpath("//p[@class='sales-price']/text()")[0]
		full_price_result = float(full_price_html.replace('R$ ','').replace('.','').replace(',','.'))

		#AME CASH-BACK
		ame_html = page.xpath("//span[contains(text(),'com Ame e receba')]/span[3]/span/text()")[0]
		ame_result = float(ame_html.replace('R$ ','').replace('.','').replace(',','.'))
		ame_off = int((ame_result*100)/full_price_result)

		#CARTAO CREDITO LOJA
		scc_html = page.xpath("//div/div[@id='brandCard']/div[2]/span/span/span[1]/span[1]/text()")[0]
		scc_result = float(scc_html.replace('R$ ','').replace('.','').replace(',','.'))
		scc_off = int(100-((scc_result*100)/full_price_result))

		if ame_off < 15 and scc_off < 15:
			continue

		product_name = page.cssselect("#product-name-default")[0].text
		results_file = open(results_filepath,'a')
		results_file.write("%d,%d,%.2f,%s,%s\n" % (ame_off, scc_off, full_price_result, product_code, product_name))
		results_file.close()
	except:
		try:
			card_variations = page.xpath("//div[@class='variations-wrapper']/span[@class='variations-message']")[0]
			print ('%s: card_variations' % product_code)
		except:
			try:
				out_of_stock = page.xpath("//span[@id='title-stock']")[0]
				print ('%s: fora de estoque' % product_code)
			except:
				try:
					its_gallery = page.xpath("//div[@data-component='aggregations']")[0]
					print ('%s: galeria de produtos' % product_code)
					list_gallery_codes.add(product_code+'\n')
				except:
					try:
						not_found = page.xpath("//div[@data-component='notfound']")[0]
						print ('%s: nao encontrado' % product_code)
					except Exception as e:
						print ('%s: exception' % product_code)
						error_file = open('logs/crawler_itens_error.log','a')
						error_file.write('##### %s - %s - %s #####\n' % (str(datetime.now()), loja, product_code))
						traceback.print_exc(file = error_file)
						error_file.write('\n\n')
						error_file.close()

products_file.close()

#Remove codigo de galerias da lista de produtos
if list_gallery_codes:
	copyfile(products_filepath, products_filepath_tmp)
	products_file  = open(products_filepath, "w")
	products_file_tmp = open(products_filepath_tmp, "r")
	for code in products_file_tmp:
		if code not in list_gallery_codes:
			products_file.write(code)
	products_file.close()
	products_file_tmp.close()
	os.remove(products_filepath_tmp)

print ('#### END: %s ####' % str(datetime.now()))
