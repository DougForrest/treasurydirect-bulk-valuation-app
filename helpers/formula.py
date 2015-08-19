import datetime

def calc_CAGR(initial_price, current_value, issue_date, valuation_date):
    """
    Calculate the compound annual growth rate of the investment (CAGR).

    Args:
    initial_price (float)
    current_value (float)
    issue_date (str) 'MM/YYYY' ex '01/1990'
    valuation_date (str) 'MM/YYYY'  ex '08/2015'

    Returns: CAGR (float)
    """
    issue_date = datetime.date(int(issue_date[3:]), int(issue_date[:2]), 01)
    valuation_date = datetime.date(int(valuation_date[3:]), int(valuation_date[:2]), 01)

    delta = valuation_date - issue_date

    return ((current_value/ float(initial_price)) ** (1 / (delta.days / 365.0))) - 1


