from flask import Flask, jsonify, request
import MetaTrader5 as mt5
from datetime import datetime


app = Flask(__name__)

# Connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()


@app.route('/all', methods=['GET'])
def get_all_symbols():
    symbols = mt5.symbols_get()
    for s in symbols:
        print(s.name)
    return jsonify({'result': 'success'})


@app.route('/realtime', methods=['GET'])
def get_tick_info():
    symbol = request.args.get('symbol')

    # Ensure the symbol is visible in the Market Watch
    if not mt5.symbol_select(symbol, True):
        mt5.shutdown()
        return jsonify({'result': 'Failed to select symbol: ' + symbol})

    # Request the latest tick (real-time) data
    tick = mt5.symbol_info_tick(symbol)
    if tick:
        time = datetime.fromtimestamp(tick.time)
        bid = tick.bid
        ask = tick.ask
        last = tick.last

    else:
        return jsonify({'result': 'Failed to retrieve tick data: ' + symbol})
    return jsonify({'time': time,
                    'bid': bid,
                    'ask': ask,
                    'last': last
                    })


if __name__ == '__main__':
    app.run()

# Shutdown MT5 connection
mt5.shutdown()
