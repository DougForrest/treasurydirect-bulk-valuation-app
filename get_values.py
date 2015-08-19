import argparse
import csv
import datetime
import logging
import os
import sys

from helpers import csv_parser
from helpers import tresurydirect_parser as td


"""
Project: bulk update Government Series EE Bond values

Take Series EE bond information from a csv file, query the treasurydirect.gov
pricing service, then return a csv file with the current bond valuations.

"""

def main(opts):

    """
    This function handles the execution of the script
    opts:  Namespace(delimeter=',', header=True, input_csv_filepath='somefilepath', output='Bond_Valuations.cvs', v=False, valuation_date='08/2015')
    """

    if opts.v:
        logging.basicConfig(level=logging.INFO)

    bonds_list = csv_parser.load_from_csv(filepath = opts.input_csv_filepath, header = opts.header, delim = opts.delimeter)

    f = open(opts.output, 'a')

    logging.info("Opening output file:  %s", opts.output)

    writer = csv.writer(f)

    headers = ['Number', 'SerialNum', 'ValuationDate', 'SeriesType', 'Denomination', 'IssueDate', 'NextAccrualDate', 'FinalMaturity', 'IssuePrice', 'TotalInterest', 'InterestRate', 'YtdInterest', 'Value', 'CAGR']

    for n, bond in enumerate(bonds_list, 1):
        try:
            valuation_results = td.parse_url(params = bond, valuation_date = opts.valuation_date)


            if n == 1 and f.tell() == 0:
                writer.writerow(headers)

            output = [n] + valuation_results

            logging.info('Writing to file:  %s', output)
            writer.writerow(output)

        except Exception as e:
            logging.warning("Issue writing row: %s", n, bond)
            logging.warning("Exception: %s", e)
            raise

    f.close()
    logging.info("Completed output to file: %s", opts.output)

def parse_cmdline(args):

    parser = argparse.ArgumentParser(description = "Get valuation of U.S. Government Bond Series EE, I, E, and Savings Notes")
    parser.add_argument('input_csv_filepath', type = str,
                        help = 'filepath (str) to local csv file containing input variables in the format of: SeriesType, Denomination, SerialNumber, IssueDate/n EE,200,R11111111,01/2000')
    parser.add_argument('-o', '--output', type = str, required = False,
                        default = os.path.join(os.path.dirname(__file__),
                            'Bond_Valuations.csv'),
                        help = 'File path for output, defaults to Bond_Valuations.csv in working directory')
    parser.add_argument('-v', '--valuation_date', type = str, required = False,
                        default = datetime.datetime.strftime(datetime.datetime.now(), "%m/%Y"),
                        help =  "Desired valuation date, must be in the form 'MM/YYYY', date defaults to current month")
    parser.add_argument('-hd', '--header', type = bool, required = False,
                        default = True,
                        help = 'Does the input csv file have a header? Defaults to True')
    parser.add_argument('-d', '--delimeter', type = str, required = False,
                        default = ',',
                        help = "Indicate the delimeter of the input file. Defaults to ','")
    parser.add_argument('--v', '--verbose', action = "store_true",
                        help = 'Print output to terminal as parsed, default is False')
    opts = parser.parse_args(args)

    assert datetime.date.today() >= datetime.date(int(opts.valuation_date[3:]), int(opts.valuation_date[:2]), 01), "Valuation date must be less than or equal to the current date"

    return opts


if __name__ == '__main__':
    print sys.argv[1:]

    opts = parse_cmdline(sys.argv[1:])
    main(opts)
