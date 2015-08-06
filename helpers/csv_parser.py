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
        A dictionary of {'label': 'value', ...}
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

class TestCases(unittest.TestCase):

    def test_of_loading_one(self):
        self.assertEqual(load_from_csv('test_one.csv', header = True), [{'Series': 'EE', 'SerialNumber': 'R11111111', 'IssueDate': '12/2222', 'Denomination': '4000'}])

    def test_of_loading_two(self):
        self.assertEqual(load_from_csv('test_two.csv', header = True), [{'Series': 'EE', 'SerialNumber': 'R11111111', 'IssueDate': '12/2222', 'Denomination': '4000'}, {'Series': 'E', 'SerialNumber': 'NZZZZZZZZ', 'IssueDate': '01/0000', 'Denomination': '100'}])


if __name__ == '__main__':
    unittest.main()



