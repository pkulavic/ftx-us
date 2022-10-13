from ftx import FTX

def main():
    ftx = FTX()
    for bc in ftx._baseCurrencies:
        if ftx.compute_profit_USD(bc):
            print(bc + ': ', ftx.compute_profit_USD(bc))
        if ftx.compute_profit_USDT(bc):
            print(bc + ': ', ftx.compute_profit_USDT(bc))
        


if __name__ == "__main__":
    main()
