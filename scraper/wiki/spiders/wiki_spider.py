import re
import time
import scrapy

from wiki.items import WikiItem


class WikiSpider(scrapy.Spider):
    name = "wikis"
    start_urls = [
        'https://en.wikipedia.org/w/index.php?title=Malazan_Book_of_the_Fallen&action=history',
    ]

    def parse(self, response):

        # Extract current revisions
        for revision in response.css('ul#pagehistory li'):

            comment = revision.css('span.comment').extract_first()
            date = revision.css('a.mw-changeslist-date::text').extract_first()
            ip = revision.css('a.mw-anonuserlink bdi::text').extract_first()
            user = revision.css('a.mw-userlink bdi::text').extract_first()
            size = revision.css('span.history-size::text').extract_first()
            tags = revision.css('span.mw-tag-marker::text').extract()

            item = WikiItem(
                comment=comment,
                date=date,
                ip=ip,
                user=user,
                size=size,
                tags=tags,
            )

            yield item

        # Get next revision history page
        next_page = response.css('a.mw-nextlink::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            # Be kind and treat wikimedia with care
            # time.sleep(1)
            yield scrapy.Request(next_page, callback=self.parse)