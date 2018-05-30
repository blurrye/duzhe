# -*- coding: utf-8 -*-
import scrapy
from duzhe.items import DuzheItem


class DuzheSpiderSpider(scrapy.Spider):
    name = 'dz'
    allowed_domains = ['52duzhe.com']
    start_urls = ['http://www.52duzhe.com/']

    def parse(self, response):
        """
        获取每期书的url

        http://www.52duzhe.com/ -->
        http://www.52duzhe.com/2017_24/index.html
        """

        book_urls = response.xpath('/html/body/div[2]/div/div[1]/table').xpath('.//a/@href').extract()

        for url in book_urls:
            url_book = response.urljoin(url)
            yield scrapy.Request(url=url_book, callback=self.parse_book)

    def parse_book(self, response):
        """
        某期书url --> 获取每篇文章url

        http://www.52duzhe.com/2017_24/index.html -->
        http://www.52duzhe.com/2017_24/duzh20172401.html
        """

        article_urls = response.xpath('/html/body/div[2]/div/div[1]/div/div[1]/table').xpath('.//a/@href').extract()

        for url in article_urls:
            url_article = response.urljoin(url)
            yield scrapy.Request(url=url_article, callback=self.parse_article)

    def parse_article(self, response):
        """
        某篇文章url --> 文章信息
        """

        item = DuzheItem()

        item['url'] = response.url
        item['title'] = response.xpath('/html/body/div[2]/div/div[1]/div/h1/text()').extract_first(default='').strip()
        item['author'] = response.xpath('//*[@id="pub_date"]/text()').extract_first(default='').strip()

        # 正文内容是由多个<p>标签内容组成
        content = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/p/text()').extract()
        item['content'] = ''.join(content)

        yield item
