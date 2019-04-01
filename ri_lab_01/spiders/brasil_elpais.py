# -*- coding: utf-8 -*-
import scrapy
import json
# import scrapy_useragents
# import scrapy-rotating-proxies

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('frontier/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):

        ########## Meu código se encaixa aqui ###############


        for articulo__interior in response.css('div.articulos__interior'):
            # meta content="2019-04-01T14:48:12" itemprop="datePublished"
            # 'title'	String	
            #     'sub_title'	String	
            #     'author'	String	
            #     'date'	Datetime	dd/mm/yyyy hh:mi:ss
            #     'section'	String	Esportes, Saúde, Política, etc
            #     'text'	String	
            #     'url'
            yield {
                'title': articulo__interior.xpath('string(.//h2)').get(),
            }

            next_page = response.css('li.paginacion-siguiente a::attr(href)').get()
            counter = 0
            if next_page is not None and counter < 3:
                yield response.follow(next_page)



        
        ##################################################
        # page = response.url.split("/")[-2]
        # filename = 'quotes-page-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        #
        #
        #
