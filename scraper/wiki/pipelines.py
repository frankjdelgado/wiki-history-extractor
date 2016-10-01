# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import json

# Clean item data
class WikiPipeline(object):
    def process_item(self, item, spider):

        if item['comment'] is not None:
            item['comment'] = re.sub('<[^>]*>', '', item['comment'])

        return item

# Export items to file
class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('revision.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)

        return item

