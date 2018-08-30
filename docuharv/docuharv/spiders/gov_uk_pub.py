import json
import scrapy
from scrapy.selector import HtmlXPathSelector
from urllib.parse import urlsplit, urlunsplit
from ..items import LandingPageItem, DocumentItem


class GovUkSpider(scrapy.Spider):
    name = 'govukpub'
    start_urls = ['https://www.gov.uk/government/publications']

    def parse(self, response: scrapy.http.Response):

        # Extract every link to a landing page:
        for title in response.css('.document-row > h3 > a'):
            yield response.follow(title, self.parse_landing_page)

        # Extract the link to the next page of results:
        for next_page in response.css('.next > a'):
            yield response.follow(next_page, self.parse)

    def parse_landing_page(self, response: scrapy.http.Response):
        # On a landing page, we can extract all the documents, or infer the JSON link and use that.
        #    yield {'title': pub.css('h1 ::text').extract_first().strip()}
        for pub in response.css('.publication'):
            # This is a publication, so let's infer the API link:
            lp_url = list(urlsplit(response.url))
            lp_url[2] = "/api/content%s" % lp_url[2]
            api_json_url = urlunsplit(lp_url)
            yield response.follow(api_json_url, self.parse_content_api_json)

    def parse_content_api_json(self, response: scrapy.http.Response):
        # Build up an item
        md = json.loads(response.body)
        item = LandingPageItem()
        item['landing_page_url'] = response.url
        item['title'] = md['title']
        item['first_publication_date'] = md['first_published_at']
        item['publication_date'] = md['first_published_at']
        # Pick up the 'public updated' date instead, if present:
        if 'public_updated_at' in md:
            item['publication_date'] = md['public_updated_at']
        item['publishers'] = []
        for org in md['links']['organisations']:
            item['publishers'].append(org['title'])
        # item['publisher_metadata'] = md

        # Make a response object to make it easy to parse the HTML fragments in the API:
        resp = response.copy()

        # Go through the documents:
        item['documents'] = []
        for doc in md['details']['documents']:
            resp._set_body(doc)
            doc_item = DocumentItem()
            doc_item['title'] = resp.css('.title ::text').extract_first()
            doc_item['document_url'] = response.urljoin(resp.css('.attachment-details a::attr(href)  ').extract_first())
            doc_item['isbn'] = resp.css('span[class=isbn] ::text').extract_first()
            doc_item['command_paper_number'] = resp.css('span[class=command_paper_number] ::text').extract_first()
            doc_item['house_of_commons_paper_number'] = resp.css('span[class=house_of_commons_paper_number] ::text').extract_first()
            item['documents'].append(dict(doc_item))

        # Return the composite ite:
        yield item

