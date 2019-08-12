from iexfinance.stocks import Stock

iex_token='sk_8a855bd5a63f4966a734af05765d3d08'


if __name__ == '__main__':
    a = Stock("AAPL", token=iex_token)
    a.get_quote()