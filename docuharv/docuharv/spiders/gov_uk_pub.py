import scrapy
from scrapy.selector import HtmlXPathSelector
import json
from urllib.parse import urlsplit, urlunsplit


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
        # Just return it all
        md = json.loads(response.body)
        resp = response.copy()
        for doc in md['details']['documents']:
            resp._set_body(doc)
            frag = HtmlXPathSelector(resp)
            yield { 'title': resp.css('.title ::text').extract_first() }

