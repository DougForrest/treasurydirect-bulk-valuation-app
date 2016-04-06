

# Problem:

Valuing U.S. Government Series EE, I, E, bonds and or Government Savings Notes one by one via the online calculator at treasurydirect.gov can be a pain.

This simple python app allows the bulk valuation of Series EE, I, E, and Savings Notes via the http://www.treasurydirect.gov/BC/SBCPrice pricing service.


## Method:
The application loads a list of bonds from a csv file, sends a series of HTTP request to the server, parses the html response, then outputs a csv file with bonds current valuations as of the valuation date requested.

## Steps:

1. Download or clone the source repository.
2. Install the required libraries

        pip install -r requirements.txt

3. Run the app with the following command line in the source root directory

        python get_values.py '~/path/to/input.csv'

Where '~/path/to/input.csv' is the filepath on your local machine to a csv file containing input variables in the format of:

`SeriesType, Denomination, SerialNumber, IssueDate`

`EE,200,R11111111,01/2000`

For help type:

>`python get_values.py -h`

```
usage: get_values.py [-h] [-o OUTPUT] [-v VALUATION_DATE] [-hd HEADER]
                     [-d DELIMETER] [--v]
                     input_csv_filepath

Get valuation of U.S. Government Bond Series EE, I, E, and Savings Notes

positional arguments:
  input_csv_filepath    filepath (str) to local csv file containing input
                        variables in the format of: SeriesType, Denomination,
                        SerialNumber, IssueDate/n EE,200,R11111111,01/2000

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        File path for output, defaults to Bond_Valuations.csv
                        in working directory
  -v VALUATION_DATE, --valuation_date VALUATION_DATE
                        Desired valuation date, must be in the form 'MM/YYYY',
                        date defaults to current month
  -hd HEADER, --header HEADER
                        Does the input csv file have a header? Defaults to
                        True
  -d DELIMETER, --delimeter DELIMETER
                        Indicate the delimeter of the input file. Defaults to
                        ','
  --v, --verbose        Print output to terminal as parsed, default is False
```

4. Look for the output file 'Bond_Valuations.csv' in working directory
5. Do something with all the time you saved!





