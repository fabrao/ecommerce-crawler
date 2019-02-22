from lxml.cssselect import CSSSelector
from lxml import html
import requests
import traceback
import sys

loja=sys.argv[1]
url_loja = 'https://www.'+loja+'.com.br/produto/'

lista_produtos = open(sys.argv[2])

open(sys.argv[3],'w').close() #limpar arquivo
lista_resultados = open(sys.argv[3],'a')

for cod_produto in lista_produtos:

	page = html.fromstring(requests.get(url_loja + cod_produto).content)
	cod_produto = cod_produto.replace('\n','')
	
	try:
		nome_produto = page.cssselect("#product-name-default")[0].text

		html_preco = page.xpath("//p[@class='sales-price']/text()")[0]
		preco_produto = float(html_preco.replace('R$ ','').replace('.','').replace(',','.'))

		#//span[contains(text(),"com Ame e receba")]/span[3]/span
		'''
		if loja == 'americanas':
			html_cb_ame = page.xpath("//div[@class='buybox-b-panel']/div/div[3]/div/div/div[1]/div/div[2]/span/span[3]/span/text()")[0]
		else:
			html_cb_ame = page.xpath("//section[@class='buy-box']/div/div[1]/div/div[2]/span/span[3]/span/text()")[0]
		'''
		html_cb_ame = page.xpath("//span[contains(text(),'com Ame e receba')]/span[3]/span/text()")[0]
		cashback_ame = float(html_cb_ame.replace('R$ ','').replace('.','').replace(',','.'))

		desconto_ame = int((cashback_ame*100)/preco_produto)

		html_ccloja = page.xpath("//div/div[@id='brandCard']/div[2]/span/span/span[1]/span[1]/text()")[0]
		preco_ccloja = float(html_ccloja.replace('R$ ','').replace('.','').replace(',','.'))

		desconto_ccloja = int(100-((preco_ccloja*100)/preco_produto))

		lista_resultados.write("%r,%r,%r,%r,%r,\n" % (desconto_ame, desconto_ccloja, preco_produto, cod_produto, nome_produto))
		print (cod_produto)
	except:
		try:
			out_of_stock = page.xpath("//span[@id='title-stock']")[0]
			print ('%s: fora de estoque' % cod_produto)
		except:
			try:
				is_not_product = page.xpath("//div[@data-component='aggregations']")[0]
				print ('%s: galeria de produtos' % cod_produto)
			except:
				try:
					card_variations = page.xpath("//div[@class='variations-wrapper']/span[@class='variations-message']")[0]
					print ('%s: card_variations' % cod_produto)
				except:
					try:
						not_found = page.xpath("//div[@data-component='notfound']")[0]
						print ('%s: nao encontrado' % cod_produto)
					except Exception as e:
						print ('%s: exception' % cod_produto)
						traceback.print_exc()
				
lista_resultados.close()
lista_produtos.close()