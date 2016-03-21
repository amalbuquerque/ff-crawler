# coding: latin-1
import argparse
import csv
# import ipdb
import sys
import exceptions
from curler import Curler
from bondparser import BondParser
from unicodestuff import UnicodeWriter

def main(*args):
    try:
        parser = argparse.ArgumentParser(description='FF Boerse Bond Crawler')

        parser.add_argument('--currency', nargs='?', default='EUR', help='Currency to search for (default=EUR). Possible values: EUR, USD, GBP, CHF, CNY, JPY')
        parser.add_argument('resultfile', nargs='?', default='resultBonds', help='Result file (default=resultBonds_CURRENCY.csv).')
        parser.add_argument('--pagelimit', nargs='?', default = 100, type=int, help='To avoid getting many pages')
        parser.add_argument('--user', nargs='?', default = None, help='User to send if behind a proxy')
        parser.add_argument('--password', nargs='?', default = None, help='Password to send if behind a proxy')
        parser.add_argument('--debug', action='store_true', default = False, help='If True, prints everything (both content and debug messages)')
        prog_args = parser.parse_args()
        # Use as: prog_args.currency and prog_args.resultfile
        # Use as: prog_args.user and prog_args.password
        # ipdb.set_trace()
    except:
        raise Exception('Problem parsing the options passed')

    curler = Curler(prog_args.currency, prog_args.user, prog_args.password, prog_args.debug)
    parser = BondParser(prog_args.debug)
    page = 1

    with open(prog_args.resultfile + '_' + prog_args.currency + '.csv', 'wb') as output:
        # 2016/02/24 17:18:59, AA: Normal CSV writer can't handle UTF-8
        # writer = csv.writer(output, quoting=csv.QUOTE_ALL)
        writer = UnicodeWriter(output)
        print('Obtained first page exclusively for headers')
        content = curler.perform(page)
        # ipdb.set_trace()
        headers = parser.get_headers(content)
        writer.writerow(headers)

        print('Will start to parse each page...')
        while True:
            # ipdb.set_trace()
            content = curler.perform(page)
            # rows is a list of lists
            rows = parser.get_bonds(content)
            # ipdb.set_trace()
            print('Page ' + str(page) + ' has ' + str(len(rows)) + ' bonds.')
            if (len(rows) <= 0) or (page > prog_args.pagelimit):
                print('No bonds to parse or reached page limit. Ending!')
                break

            writer.writerows(rows)
            page = page + 1

    print('Ended obtaining all the available pages')

if __name__ == '__main__':
    sys.exit(main(*sys.argv))
