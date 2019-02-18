from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time

# use firefox to get page with javascript generated content
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')

print("### driver.get...")
driver.get("https://www.submarino.com.br/categoria/celulares-e-smartphones/smartphone/f/preco-500.0:9000.0")

print("\n### buttons.find...")
buttonNext = driver.find_elements_by_xpath("//div[@class='card card-pagination']/ul/li[10]/a")
buttonNext = buttonNext[0]

print("# BUTTON NEXT \n %s" % buttonNext)

source_codeNext = buttonNext.get_attribute("outerHTML")
print("# SOURCE NEXT \n %s" % source_codeNext)

buttonNext.click() # Clica no botao prox.pagina
time.sleep(5)
page_source = driver.page_source
soup = BeautifulSoup(page_source, "lxml")
print(soup.prettify())
driver.quit()