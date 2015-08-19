import csv
import logging
import unittest

def load_from_csv(filepath, header = True, delim = ','):
    """
    Parse a CSV file to extract paramaters

    Args:
        filepath (str) to local csv file containing
            SeriesType, Denomination, SerialNumber, IssueDate

            Data is expected in the following format:
            EE,200,R11111111,01/2000

        header (boolean): Defaults to true, headers are ignored

    Returns:
        A list of dictionaries of [{'label': 'value', ...}, ...]
    """
    logging.info('Loading data from:  %s', filepath)
    # Set up labels
    labels = ['Series', 'Denomination','SerialNumber', 'IssueDate']

    # Setup empty list
    data = []

    with open(filepath, 'rU') as csvfile:
        csv_data = csv.reader(csvfile, delimiter = delim, dialect=csv.excel_tab)

        if header:
            csv_data.next()

        for row in csv_data:
            logging.info('Parsing row:  %s', row)
            data.append(dict(zip(labels, row)))

    return data
