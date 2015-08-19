from lxml import html
import requests
import formula

def parse_url(params, valuation_date, url = 'http://www.treasurydirect.gov/BC/SBCPrice'):
    """
    Sends an http post request to the given url with the provided paramaters and parses the response from the server.

    Args:
    url (str): default 'http://www.treasurydirect.gov/BC/SBCPrice'
    params (dict)

    Returns: bond_results (list)
    """

    bond_results = [params['SerialNumber'], valuation_date]

    # Additional parameters
    params['RedemptionDate'] = valuation_date
    params['btnAdd.x'] = 'CALCULATE'

    page = requests.post(url, data = params)

    tree = html.fromstring(page.text)

    tres_results = tree.xpath('//table[@class = "bnddata"]//tr[@class = "altrow1"]/td//text()')[1:10]
    ytd_int = tree.xpath('//table[@id = "ta1"]//td/text()')[3]
    tres_results.insert(8,ytd_int)

    initial_price = float(tres_results[5][1:])
    current_value = float(tres_results[9][1:])
    issue_date = tres_results[2]

    cagr = formula.calc_CAGR(initial_price, current_value, issue_date, valuation_date)


    return bond_results + tres_results + [cagr]
