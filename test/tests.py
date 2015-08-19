import csv
import os
import datetime
import mock
from io import StringIO
import unittest

from helpers import csv_parser
from helpers import tresurydirect_parser as td
from helpers import formula
import get_values as gv

class CSVParser_TestCases(unittest.TestCase):

    def test_of_loading_single(self):
        file_path = os.getcwd() + "/test/" + 'test_one.csv'
        self.assertEqual(csv_parser.load_from_csv(file_path, header = True), [{'Series': 'EE', 'SerialNumber': 'R11111111', 'IssueDate': '12/2222', 'Denomination': '4000'}])

    def test_of_loading_multi(self):
        file_path = os.getcwd() + "/test/" + 'test_data.csv'
        self.assertEqual(csv_parser.load_from_csv(file_path, header = True), [{'Series': 'EE', 'SerialNumber': 'C777535063EE', 'IssueDate': '08/1989', 'Denomination': '100'}, {'Series': 'EE', 'SerialNumber': 'R114463707EE', 'IssueDate': '08/1994', 'Denomination': '200'}])


class TresDirectParse_TestCases(unittest.TestCase):
    @unittest.skip("skipping live request")
    def test_treasurydirect_parsing_current_valuation_live(self):
        test_params = {'Series': 'EE', 'SerialNumber': 'C777535063EE', 'IssueDate': '08/1989', 'Denomination': '100'}
        test_valuation_date = '08/2015'

        self.assertEqual(td.parse_url(params = test_params, valuation_date = test_valuation_date), ['C777535063EE', '08/2015', 'EE', '$100', '08/1989', '02/2016', '08/2019', '$50.00', '$127.00', '4.00%', '$6.88', '$177.00', 0.049789363935413666])

    @unittest.skip("skipping live request")
    def test_treasurydirect_parsing_past_valuation_live(self):
        test_params = {'Series': 'EE', 'SerialNumber': 'R114463707EE', 'IssueDate': '08/1994', 'Denomination': '200'}
        test_valuation_date = '07/2015'

        self.assertEqual(td.parse_url(params = test_params, valuation_date = test_valuation_date), ['R114463707EE', '07/2015', 'EE', '$200', '08/1994', '08/2015', '08/2024', '$100.00', '$129.04', '4.00%', '$5.28', '$229.04', 0.04039191319543778])

    file_attr = {'text.return_value': 'test_response'}
    mock_requests = mock.Mock(spec = td.requests.Response, **file_attr)

    tree_attr = {'xpath.return_value': ['dropped', 'EE', '$200', '08/1994', '08/2015', '08/2024', '$100.00', '$129.04', '4.00%', '$229.04']}
    mock_tree = mock.Mock(**tree_attr)

    @mock.patch('lxml.html.fromstring', return_value = mock_tree)
    @mock.patch('requests.post', return_value = mock_requests)
    def test_treasurydirect_parsing_past_valuation_w_mock(self, mock_response, mock_page):
        test_params = {'Series': 'EE', 'SerialNumber': 'R114463707EE', 'IssueDate': '08/1994', 'Denomination': '200'}
        test_valuation_date = '07/2015'

        self.assertEqual(td.parse_url(params = test_params, valuation_date = test_valuation_date), ['R114463707EE', '07/2015', 'EE', '$200', '08/1994', '08/2015', '08/2024', '$100.00', '$129.04', '4.00%', '08/1994', '$229.04', 0.04039191319543778])

        mock_response.assert_called_once_with('http://www.treasurydirect.gov/BC/SBCPrice', data={'RedemptionDate': '07/2015', 'Series': 'EE', 'SerialNumber': 'R114463707EE', 'Denomination': '200', 'IssueDate': '08/1994', 'btnAdd.x': 'CALCULATE'})

        self.assertEqual(mock_page.called, True)


class formula_TestCases(unittest.TestCase):

    def test_cagr_calculation(self):

        initial_price = 50.0
        current_value = 177.00
        issue_date = '08/1989'
        valuation_date = '08/2015'

        self.assertEqual(formula.calc_CAGR(initial_price, current_value, issue_date, valuation_date),0.049789363935413666)


class cmdline_argparse_TestCases(unittest.TestCase):

    def test_cmdline_default_args(self):
        parsed = gv.parse_cmdline(['/path/to/file.csv'])
        expected = {'delimeter': ',', 'header': True, 'input_csv_filepath': '/path/to/file.csv', 'output': 'Bond_Valuations.csv', 'v': False}
        expected['valuation_date'] = datetime.datetime.strftime(datetime.datetime.now(), "%m/%Y")

        self.assertEqual(parsed.__dict__, expected)

    def test_cmdline_input_args(self):
        parsed = gv.parse_cmdline(['something.csv', '-v', '07/2011', '-hd', False, '-o', 'outputfile.csv', '-d', ':', '--v'])
        expected = {'delimeter': ':', 'header': False, 'input_csv_filepath': 'something.csv', 'output': 'outputfile.csv', 'v': True, 'valuation_date': '07/2011'}

        self.assertEqual(parsed.__dict__, expected)

    def test_invalid_valuation_date(self):
        valuation_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days = 60), "%m/%Y")

        self.assertRaises(AssertionError, lambda: gv.parse_cmdline(['/path/to/file.csv', '-v', valuation_date]))


class get_values_TestCases(unittest.TestCase):

    from_csv =[{'Series': 'EE', 'SerialNumber': 'C777535063EE', 'IssueDate': '08/1989', 'Denomination': '100'}]

    file_attr = {'tell.return_value': 0, 'name': 'file_test'}
    mock_file = mock.Mock(spec = file, **file_attr)

    mock_csv = mock.Mock(spec = csv.writer(mock_file))

    @mock.patch('get_values.td.parse_url', return_value = ["test_row"])
    @mock.patch('get_values.csv.writer')
    @mock.patch('get_values.open', return_value = mock_file)
    @mock.patch('get_values.csv_parser.load_from_csv', return_value = from_csv)
    def test_write_to_file(self, mock_load_from_csv, mock_open, mock_writer, mock_parse_url):

        attrs = {'delimeter': ':', 'header': False, 'input_csv_filepath': 'something.csv', 'output': 'outputfile.csv', 'v': True, 'valuation_date': '07/2011'}
        options = mock.Mock(**attrs)

        gv.main(options)
        mock_load_from_csv.assert_called_once_with(delim=':', filepath='something.csv', header=False)
        mock_open.assert_called_once_with('outputfile.csv', 'a')

        mock_writer_calls = mock_writer.mock_calls
        self.assertEqual(len(mock_writer_calls), 3)
        self.assertRegexpMatches(str(mock_writer_calls[0]), "('file_test')")
        self.assertRegexpMatches(str(mock_writer_calls[1]), "('Number', 'SerialNum', 'ValuationDate', 'SeriesType', 'Denomination', 'IssueDate', 'NextAccrualDate', 'FinalMaturity', 'IssuePrice', 'TotalInterest', 'InterestRate', 'YtdInterest', 'Value', 'CAGR')")
        self.assertRegexpMatches(str(mock_writer_calls[2]), "(1, 'test_row')")


        mock_parse_url.assert_called_once_with(params={'Series': 'EE', 'SerialNumber': 'C777535063EE', 'IssueDate': '08/1989', 'Denomination': '100'}, valuation_date='07/2011')



if __name__ == '__main__':
    unittest.main()
