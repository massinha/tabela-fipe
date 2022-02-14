
def extract_option(dataframe, choosed_option):
    return dataframe.query('Label == @choosed_option')['Value'].item()


def extract_prices_series(raw_price_series):
    price_series = raw_price_series.str[3:]
    price_series = price_series.str.replace('\.', '')
    price_series = price_series.str.replace(',00', '')
    price_series = price_series.str.replace(' ', '')
    price_series = price_series.astype(float)

    return price_series
