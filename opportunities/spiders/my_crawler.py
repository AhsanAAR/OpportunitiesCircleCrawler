from datetime import datetime as dt

import scrapy


class MyCrawlerSpider(scrapy.Spider):
    name = 'my_crawler'
    allowed_domains = ['opportunitiescircle.com']
    start_urls = ['https://www.opportunitiescircle.com/explore-opportunities/']

    def parse(self, response, **kwargs):
        opportunity_links = response.css("article div.elementor-image a::attr(href)").getall()

        for url in opportunity_links:
            yield response.follow(url, callback=self.parse_opportunity_page)

        next_link = response.css(".next::attr(href)").get()
        yield response.follow(next_link, callback=self.parse)

    def parse_opportunity_page(self, response):
        deadline = response.css(".elementor-inline-item "
                                ".elementor-post-info__item--type-custom::text").get()

        data = {
            "url": response.url,
            "name": response.css("h1.elementor-heading-title.elementor-size-default::text").get(),
            "funding_type": response.css(".elementor-repeater-item-fac2e97 "
                                         ".elementor-post-info__terms-list-item::text").get(),
            "deadline": str(dt.strptime(deadline[11:-1], '%B %d, %Y')) if deadline else None,
            "description": '\n'.join(response.css(".elementor-element.elementor-element-1a6770f."
                                                  "elementor-widget.elementor-widget-theme-post-content p::text").getall()),
            "region": response.css(".elementor-repeater-item-21b526f "
                                   ".elementor-post-info__terms-list-item::text").get(),
            "eligibility": response.css(".elementor-element-d78a9e1 li::text").getall(),
            "benefits": response.css(".elementor-element-004e374 li::text").getall(),
            "other_details": response.css(".elementor-element-bbc908a li::text").getall(),
            "apply_link": response.css(".elementor-element-0cb5de2 "
                                       "a.elementor-animation-shrink::attr(href)").get(),
        }

        return data
