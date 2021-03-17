import webbrowser
import os
import lxml.etree as ET


def crawl():
    try:
        os.remove("results/zvetsad.xml")
    except OSError:
        print("results/zvetsad.xml not found")
    os.system('scrapy crawl zvetsad -o results/zvetsad.xml -t xml')


def xslt_parse():
    dom = ET.parse('results/zvetsad.xml')
    xslt = ET.parse('zvetsad.xslt')
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    with open('results/zvetsad.html', 'wb') as f:
        f.write(ET.tostring(newdom, pretty_print=True))
    webbrowser.open('file://' + os.path.realpath("results/zvetsad.html"))


crawl()
xslt_parse()
