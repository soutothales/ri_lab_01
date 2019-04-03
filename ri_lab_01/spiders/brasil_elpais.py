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

    # Utilizei esta função auxiliar para minerar o texto do artículo
    def get_text(self, page):

        yield scrapy.Request(url='https:'+page, callback=self.parse)


    def parse(self, response):

        ########## Meu código se encaixa aqui ###############


        for articulo__interior in response.css('div.articulos__interior'):
            # meta content="2019-04-01T14:48:12" itemprop="datePublished"
            # 'title'	String	
            # 'sub_title'	String	
            # 'author'	String	
            # 'date'	Datetime	dd/mm/yyyy hh:mi:ss
            # 'section'	String	Esportes, Saúde, Política, etc
            # 'text'	String	
            # 'url'

            

            # Formatação para resgatar título
            title = articulo__interior.xpath('string(.//h2)').get().encode('utf-8')

            # Formatação para resgatar section
            section = articulo__interior.css('h2 a::attr(href)').get().split('/')[-2]

            # Formatação para resgatar author
            author = articulo__interior.css('div.articulo-metadatos div.firma div.autor div.autor-texto span.autor-nombre a::text').get()
            
            # Formatação para o formato desejado de date
            date = articulo__interior.css('time::attr(datetime)').get()
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            date = datetime.strftime(date,'%d/%m/%Y %H:%M:%S')

            # Formatação para resgatar sub titulo
            sub_title = articulo__interior.css('p.articulo-entradilla::text').get()

            # Formatação para resgatar o texto
            # text

            # Formatação para resgatar url
            url = articulo__interior.css('h2 a::attr(href)').get().encode('utf-8')



            # article_page = articulo__interior.css('h2 a::attr(href)').get()

            # article_text = self.get_text(article_page)

            
            yield {
                'title': title,
                'sub_title': sub_title,
                'author': author,
                'date': date,
                'section': section,
                'url': url                  
            }

            # articulo__interior.css('h2 a::attr(href)').get()

            pdb.set_trace()

            # scrapy.Request(articulo__interior.css('h2 a::attr(href)').get(), callback=self.parse)

            # next_page = response.css('li.paginacion-siguiente a::attr(href)').get()
            # counter = 0
            # if next_page is not None and counter < 3:
            #     yield response.follow(next_page)



        
        ##################################################

        
        # page = response.url.split("/")[-2]
        # filename = 'quotes-page-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        #
        #
        #
