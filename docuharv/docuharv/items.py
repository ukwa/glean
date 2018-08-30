# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DocumentItem(scrapy.Item):
    # Document Title
    title = scrapy.Field()
    # Original URL for the document:
    document_url = scrapy.Field()
    # Wayback timestamp of the document:
    wayback_timestamp = scrapy.Field()
    # The filename of the Document:
    filename = scrapy.Field()
    # The size of the Document in bytes:
    size = scrapy.Field()
    # The ISBN of this Document (if known):
    isbn = scrapy.Field()
    # The DOI of this Document (if known):
    doi = scrapy.Field()
    # Command or Act paper reference (if any, UK GOV only):
    command_paper_number = scrapy.Field()
    house_of_commons_paper_number = scrapy.Field()


class LandingPageItem(scrapy.Item):
    # Landing page title:
    title = scrapy.Field()
    # The Document's Landing Page:
    landing_page_url = scrapy.Field()
    # Wayback timestamp of the landing page:
    wayback_timestamp = scrapy.Field()
    # The most recent publication date of this Document:
    publication_date = scrapy.Field()
    # The first publication date of this Document (if known):
    first_publication_date = scrapy.Field()
    # An array of authors for the document:
    authors = scrapy.Field()
    # An array of publishers for this document:
    publishers = scrapy.Field()

    # The array of resource documents associated with this landing page:
    documents = scrapy.Field()

    # The original metadata payload from the publisher (if any, JSON encoded):
    publisher_metadata = scrapy.Field()

    # The ID of the Target this Document should be associated with (if any):
    target_id = scrapy.Field()
