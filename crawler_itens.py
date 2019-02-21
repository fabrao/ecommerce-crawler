from lxml import html
import requests
import traceback


url_loja = 'https://www.submarino.com.br/produto/'

lista_code = open('product_code_list.txt')
open('result_products.txt','w').close() #limpar arquivo

for cod_produto in lista_code:

	page = html.fromstring(requests.get(url_loja + cod_produto).content)
	cod_produto = cod_produto.replace('\n','')
	
	try:
		nome_produto = page.xpath("//h1[@id='product-name-default']/text()")[0]

		html_preco = page.xpath("//p[@class='sales-price']/text()")[0]
		preco_produto = float(html_preco.replace('R$ ','').replace('.','').replace(',','.'))

		html_cb_ame = page.xpath("//section[@class='buy-box']/div/div[1]/div/div[2]/span/span[3]/span/text()")[0]
		cashback_ame = float(html_cb_ame.replace('R$ ','').replace('.','').replace(',','.'))

		desconto_ame = int((cashback_ame*100)/preco_produto)

		html_ccloja = page.xpath("//section[@class='buy-box']/div/div[@id='brandCard']/div[2]/span/span/span[1]/span[1]/text()")[0]
		preco_ccloja = float(html_ccloja.replace('R$ ','').replace('.','').replace(',','.'))

		desconto_ccloja = (100 - int((preco_ccloja*100) / preco_produto ) ) 

		file = open("result_products.txt","a")
		file.write("%r,%r,%r,%r,%r,\n" % (desconto_ame, desconto_ccloja, preco_produto, cod_produto, nome_produto))
		file.close()
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
				except Exception as e:
					print ('%s: exception' % cod_produto)
					traceback.print_exc()

lista_code.close()