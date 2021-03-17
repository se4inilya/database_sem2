import os
from lxml import etree

print("start")
os.system('scrapy crawl uahotels')
print("scrapy is ended")
print('\n'*3)
root = None
with open('results/uahotels.xml', 'r', encoding="utf-8") as file:
    root = etree.parse(file)

pagesCount = root.xpath('count(//page)')
textFragmentsCount = root.xpath('count(//fragment[@type="text"])')
print('Average count of text fragments per page %f' % (textFragmentsCount / pagesCount))