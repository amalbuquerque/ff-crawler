# coding: latin-1
import argparse
import ipdb
import sys
import exceptions
from curler import Curler

def main(*args):
    try:
        parser = argparse.ArgumentParser(description='FF Boerse Bond Crawler')

        parser.add_argument('--currency', nargs='?', default='EUR', help='Currency to search for (default=EUR). Possible values: EUR, USD, GBP, CHF, CNY, JPY')
        parser.add_argument('resultfile', nargs='?', default='resultBonds.csv', help='Result file (default=result<timestamp>.csv).')
        parser.add_argument('--user', nargs='?', default = None, help='User to send if behind a proxy')
        parser.add_argument('--password', nargs='?', default = None, help='Password to send if behind a proxy')
        parser.add_argument('--debug', action='store_true', default = False, help='If True, prints everything (both content and debug messages)')
        prog_args = parser.parse_args()
        # Use as: prog_args.currency and prog_args.resultfile
        # Use as: prog_args.user and prog_args.password
        # ipdb.set_trace()
        print('Init ended')
    except:
        raise Exception('Problem parsing the options passed')

    curler = Curler(prog_args.currency, prog_args.user, prog_args.password, prog_args.debug)
    # Page=1
    curler.perform(1)
    # Page=2
    curler.perform(2)

if __name__ == '__main__':
    sys.exit(main(*sys.argv))
