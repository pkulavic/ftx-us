import requests
import apikeys


class FTX:
    """A class for making requests to the FTX API."""
    endpoint = 'https://ftx.us/api'
    apikey = apikeys.apikey
    secret_key = apikeys.secret
    foreign_currencies = ['AUD', 'BRZ', 'CAD', 'EUR']
    def __init__(self) -> None:
        self._baseCurrencies = self._get_base_currencies()
    def _get_base_currencies(self):
        return sorted(list({market['baseCurrency'] for market in requests.get(self.endpoint + '/markets').json()['result']}))
    def _get_market_names(self):
        return [market['name'] for market in self.get_all_markets()] 
    def get_latest_price(self, symbol: str):
        return requests.get(self.endpoint + '/markets/' + symbol).json()['result']['last']
    def get_all_markets(self):
        """Returns a json object containing all markets."""
        return requests.get(self.endpoint + '/markets').json()['result']
    def get_triangularly_tradable_assets(self):
        """Returns a json object of assets that are tradable for both BTC and/or 
        USDT, USDC."""
        triangle_assets = []
        markets = self.get_all_markets()
        market_names = self._get_market_names()
        for asset in self._baseCurrencies:
            triangle_assets.append([market['name'] for market in markets if market['baseCurrency'] == asset])

        def domestic(markets):
            for name in markets:
                if name[-3:] in self.foreign_currencies or name[:3] in self.foreign_currencies:
                    return False
            return True

        return filter(domestic, filter(lambda x: len(x) > 1, triangle_assets))
    def compute_triangle_profit(self, symbol):
        markets = self.get_all_markets()
        triangle_markets = []

    def compute_profit_USD(self, symbol: str) -> float:
        # A dict with name as key and market as value
        markets = {m['name']: m for m in filter(lambda market: market['baseCurrency'] == symbol, self.get_all_markets())} 
        quote_currencies: list[float] = [markets[name]['quoteCurrency'] for name in markets]
        if 'BTC' in quote_currencies and 'USD' in quote_currencies:
            # BTC/USD
            a: float = list(filter(lambda x: x['name'] == 'BTC/USD', self.get_all_markets()))[0]['ask']
            # symbol/BTC
            b: float = markets[symbol + '/BTC']['ask']
            # 1 / [symbol/USD]
            c: float = 1 / markets[symbol + '/USD']['ask']
            return a * b * c     
    def compute_profit_USDT(self, symbol: str) -> float:
        # A dict with name as key and market as value
        markets = {m['name']: m for m in filter(lambda market: market['baseCurrency'] == symbol, self.get_all_markets())} 
        quote_currencies: list[float] = [markets[name]['quoteCurrency'] for name in markets]
        if 'BTC' in quote_currencies and 'USDT' in quote_currencies:
            # BTC/USD
            a: float = list(filter(lambda x: x['name'] == 'BTC/USDT', self.get_all_markets()))[0]['ask']
            # symbol/BTC
            b: float = markets[symbol + '/BTC']['ask']
            # 1 / [symbol/USDT]
            c: float = 1 / markets[symbol + '/USDT']['ask']
            return a * b * c   



def main():
    ftx = FTX()
    print(ftx._baseCurrencies)
    for asset in ftx.get_triangularly_tradable_assets():
        print(asset)



if __name__ == "__main__":
    main()
