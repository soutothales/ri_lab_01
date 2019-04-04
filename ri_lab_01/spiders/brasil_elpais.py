# -*- coding: utf-8 -*-
import scrapy
import json

import pdb
from datetime import datetime

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    # Essa é uma variável de controle para gerar apenas 100 documentos
    count = 0 

    def aux_parse(self, response):

        for articulo__interior in response.css('div.articulo__interior'):
            url = articulo__interior.css('h2.articulo-titulo a::attr(href)').get()
            url = 'https:' + str(url)

            yield response.follow(url, callback=self.new_parse)



    def parse(self, response):

        yield response.follow(response.url, callback=self.aux_parse)
            

        
        # page = response.url.split("/")[-2]
        # filename = 'quotes-page-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        #
        #
        #


   
    # Função para fazer o parse das informações
    def new_parse(self, response):

        
        for item in response.css('div.contenedor'):

            # Formatação para resgatar título
            title = str(item.css('h1.articulo-titulo::text').get().encode('utf-8'))

            # Formatação para resgatar author
            author = str(item.css('div.firma div.autor div.autor-texto span.autor-nombre a::text').get())
            
            # Formatação para o formato desejado de date
            date = item.css('div.articulo-datos time::attr(datetime)').get()
            date = date[:-6]
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            date = datetime.strftime(date,'%d/%m/%Y %H:%M:%S')

            # Formatação para resgatar sub titulo
            sub_title = item.css('div.articulo-subtitulos h2.articulo-subtitulo::text').get()

            # Formatação para resgatar texto
            text = item.css('div.articulo__contenedor p::text').getall()
            text = "".join(text)


            # Formatação para resgatar url
            url = response.request.url
            

            # Formatação para resgatar section
            section = str(url.split("/")[-2])

            # pdb.set_trace()

            
            yield {
                'title': title,
                'sub_title': sub_title,
                'author': author,
                'date': date,
                'section': section,
                'text': text,
                'url': url                  
            }
                
                
        
        

            
