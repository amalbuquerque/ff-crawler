import ipdb
import pycurl
import re
from lxml import etree
from lxml.cssselect import CSSSelector
from StringIO import StringIO

CURRENCY_CODES = {
        'EUR': 814,
        'USD': 333,
        'GBP': 402,
        'CHF': 1,
        'CNY': 220,
        'JPY': 534
        }

class Curler(object):
    """ classe que abstrai o acesso 'a ff boerse """
    def __init__(self, currency, user = None, password = None, \
             print_debug = False):
        print('Debug: ' + str(print_debug))
        self.user = user
        self.password = password
        self.currency = currency
        self.debug = print_debug
        self.curl = None
        self.raw_response = None
        self.response_buffer = StringIO()

    def prt(self, msg):
        if (self.debug):
            print(msg)

    def set_URL(self, curl, page):
        url = str.format('http://en.boerse-frankfurt.de/Ajax/BondSearchResults?borrower=&marketsegment=&bondtype=&maturity=&yield=&rating=&exchange=&coupon=&currency={0}&count=100&p={1}', CURRENCY_CODES[self.currency], page)
        curl.setopt(curl.URL, url)
        return curl

    def init_ajax_curl(self, page, init=True):
        self.prt('Igniting the Curl')
        c = pycurl.Curl()
        c = self.set_URL(c, page)
        referer = str.format('http://en.boerse-frankfurt.de/bonds/bonds-finder?borrower=&marketsegment=&bondtype=&maturity=&yield=&rating=&exchange=&coupon=&currency={0}&count=100', CURRENCY_CODES[self.currency])
        c.setopt(c.REFERER, referer)
        c.setopt(c.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2464.0 Safari/537.36')

        c.setopt(c.HTTPHEADER,
                 ['Host: en.boerse-frankfurt.de',
                  'Proxy-Connection: keep-alive',
                  'Accept: */*',
                  'X-Requested-With: XMLHttpRequest',
                  'Accept-Language: en-US,en;q=0.8,pt;q=0.6'])

        if (self.user != None and self.password != None):
            c.setopt(c.USERPWD, self.user + ':' + self.password)
            c.setopt(c.HTTPAUTH, c.HTTPAUTH_NTLM)

        c.setopt(c.NOPROGRESS, 1)
        c.setopt(c.WRITEFUNCTION, self.response_buffer.write)
        if (init):
            self.curl = c
        return c

    def change_page_URL(self, page):
        if (self.curl != None):
            self.curl = self.set_URL(self.curl, page)

    def perform(self, page):
        if (self.curl == None):
            self.init_ajax_curl(page)
        else:
            self.change_page_URL(page)

        if (self.curl != None):
            url = self.curl.getinfo(self.curl.EFFECTIVE_URL)
            self.prt('I will now perform the Curl request. URL=' + url)
            self.curl.perform()
            self.raw_response = self.response_buffer.getvalue()
        self.prt('Content obtained:')
        self.prt(self.raw_response)
        return self.raw_response

