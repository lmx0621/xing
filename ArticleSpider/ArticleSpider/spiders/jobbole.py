# -*- coding: utf-8 -*-
import re
import scrapy
from  scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1、获取文字列表中的文字url，并交给scrapy下载后并进行解析
        2、获取下一页的url并交给scrapy进行下载，下载后交给parse
        :param response:
        :return:
        """
        #解析列表页中所有文字的url，并交给scrapy下载后并进行解析
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse_detail)
        #获取下一页的url并交给scrapy进行下载，下载后交给parse
        next_urls = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_urls:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse)

    def parse_detail(self, response):
        #提取文字的具体字段
        re_selector = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace("·","").strip()
        praise_nums = int(response.xpath('//div[@class="post-adds"]/span[1]/h10/text()').extract()[0])
        tag_list = response.xpath('//div[@class="entry-meta"]/p/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = "，".join(tag_list)


        bookmark = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract()[0]
        match_re = re.match(".*?(\d+).*",bookmark)
        if match_re:
            bookmark = int(match_re.group(1))
        else:
            comment = 0
        comment = response.xpath('//div[@class="post-adds"]/a/span/text()').extract()[0]
        match_re = re.match(".*?(\d+).*",comment)
        if match_re:
            comment = int(match_re.group(1))
        else:
            comment = 0
        content = response.xpath('//*[@id="post-111845"]/div[@class="entry"]').extract()[0]
        pass
