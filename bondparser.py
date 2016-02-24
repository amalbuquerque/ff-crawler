# import ipdb
import re
from lxml import html
from lxml.cssselect import CSSSelector

class BondParser(object):
    """ classe que implementa o parsing do html obtido """
    def __init__(self, print_debug = False):
        self.debug = print_debug

    def sanitize(self, content):
        # copied from other project, to confirm that all of this is needed
        content = content.replace('\\r\\n','\n')
        content = content.replace('\\t','\t')
        content = content.replace('\\"','\"')
        content = content.replace('&nbsp;',' ')

        # retirar os separadores para que a regex funcione
        content = content.replace('\t','')
        content = content.replace('\n','')
        content = content.replace('\r','')

        return content

    def remove_scripts(self, content):
        content = re.sub('<script .*>.*</script>', '', content)
        return content

    def get_last_page(self, content):
        content = self.sanitize(content)
        content = self.remove_scripts(content)

        toparse = html.fromstring(content)
        span_lastpage_selector = CSSSelector('span.icon-page-forward-stop')
        span = span_lastpage_selector(toparse)[0]
        # span is inside the <a> with the onclick we want
        anchor_parent = span.getparent()
        onclick_action = anchor_parent.attrib.get('onclick')

        match = re.search('\((\d+)\)', onclick_action)
        # match.group(0) refers to the match to all regex (in our case, e.g. (61))
        return match.group(1)

    def get_bonds(self, content):
        content = self.sanitize(content)
        content = self.remove_scripts(content)

        toparse = html.fromstring(content)
        row_selector = CSSSelector('table > tr')
        tr_list = row_selector(toparse)
        td_selector = CSSSelector('td')
        rows = []

        for tr in tr_list:
            temp_tds = [td.text_content() for td in td_selector(tr)]
            rows.append(temp_tds)
        return rows

    def get_headers(self, content):
        content = self.sanitize(content)
        content = self.remove_scripts(content)

        toparse = html.fromstring(content)
        headers_row_selector = CSSSelector('table > thead > tr')
        headers_row = headers_row_selector(toparse)[0]

        header_selector = CSSSelector('th > div > a')
        headers_elements = header_selector(headers_row)
        headers = [e.text for e in headers_elements]
        return headers

    def debug_toparse(self):
        raw = open('C:\\dados\\projectos\\ffcrawler\\resultsimple.txt', 'r').read()
        raw = self.sanitize(raw)
        raw = self.remove_scripts(raw)

        toparse = html.fromstring(raw)
        return toparse

    def debug_headers_rows(self):
        raw = open('C:\\dados\\projectos\\ffcrawler\\resultsimple.txt', 'r').read()
        headers = self.get_headers(raw)
        rows = self.get_bonds(raw)

        toreturn = { 'headers': headers, 'rows': rows, 'content': raw }
        return toreturn
