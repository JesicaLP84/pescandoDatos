from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine # crear la conexion con la BBDD
import pandas as pd

#levantamos el servicio
s = Service('Users/Usuario/pescandodatos/chromedriver')

busqueda = input('Que quieres buscar?.')
busqueda = busqueda.replace(" ", "+")

if busqueda != "":
    driver = webdriver.Chrome(service=s)
    link = f'https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={busqueda}&_sacat=0'
    driver.get(link)
    
    product_title =[]
    product_price = []
    
    page = BeautifulSoup(driver.page_source, 'html.parser') # Hacer studio previo para que lo identifique correctamente, 
    

for product in page.findAll('li', attrs={'class', 's-item'}):
    title = product.find('div', attrs={'class', 's-item__title'})
    if title:
        product_title.append(title.text)
    else: 
        product_title.append('')
    
    price = product.find('span', attrs={'class', 's-item__price'})
    
    if price:
        product_price.append(price.text.replace('EUR', ''))
    else:
        product_price.append('')
        
    product_list = pd.DataFrame({ 'title': product_title, 'price' : product_price }) # Se utiliza par ameter datos a la BBdd
    
    print(product_list)
    

# mete la creacion de un csv
product_list.to_csv(r'lista_productos.csv')

# leemos el fichero que acabamos de crear para importarlo a MySQL

data = pd.read_csv('lista_productos.csv')

#Eliminas la columna Unnamed del DataFrame
data = data.drop(columns=['Unnamed: 0'])

# conecta con la BBDD  e insertar los datos en la tabla que crado productos
conexion = create_engine('mysql+mysqlconnector://root:MySQL2022@localhost:3306/wr_python')

data.to_sql('products', con=conexion, if_exists='append', index=False)
