from lxml import html
import requests

def parse_url(params, valuation_date, url = 'http://www.treasurydirect.gov/BC/SBCPrice'):
    """
    Sends an http post request to the given url with the provided paramaters and parses the response from the server.

    Args:
    url (str): default 'http://www.treasurydirect.gov/BC/SBCPrice'
    params (dict)

    Returns: bond_results (list)
    """

    # # Set valuation to current month if not specified
    # if valuation_date == None:
    #     valuation_date = datetime.strftime(datetime.now(), "%m/%Y")

    bond_results = [params['SerialNumber'], valuation_date]


    # Additional parameters
    params['RedemptionDate'] = valuation_date
    params['btnAdd.x'] = 'CALCULATE'

    page = requests.post(url, data = params)
    tree = html.fromstring(page.text)

    tres_results = tree.xpath('//table[@class = "bnddata"]//tr[@class = "altrow1"]/td//text()')[1:10]

    return bond_results + tres_results
