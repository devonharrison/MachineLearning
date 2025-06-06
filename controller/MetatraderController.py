from flask import Flask, jsonify, request
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import atexit


app = Flask(__name__)

# MetaTrader 5 client is always defaulted to GMT+3
# Connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()


@app.route('/all', methods=['GET'])
def get_all_symbols():
    symbols = mt5.symbols_get()
    symbol_names = [s.name for s in symbols]
    return jsonify({'symbols': symbol_names})


@app.route('/tick-data', methods=['GET'])
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
    return jsonify({'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'bid': bid,
                    'ask': ask,
                    'last': last
                    })


@app.route('/candle-stick-data', methods=['GET'])
def get_candle_stick_data():
    symbol = request.args.get('symbol')
    # set time zone to UTC
    timeframe = mt5.TIMEFRAME_M5

    count = int(request.args.get('count', 50))  # default to 50 candles

    # Get candles ending "now"
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)

    if rates is None or len(rates) == 0:
        return jsonify({'error': f'No candlestick data found for {symbol}'}), 404

        # Convert structured array to JSON-serializable list
    candle_data = []
    for rate in rates:
        candle_data.append({
            'time': datetime.fromtimestamp(int(rate['time'])).strftime('%Y-%m-%d %H:%M:%S'),
            'open': float(rate['open']),
            'high': float(rate['high']),
            'low': float(rate['low']),
            'close': float(rate['close']),
            'tick_volume': int(rate['tick_volume']),
            'spread': int(rate['spread']),
            'real_volume': int(rate['real_volume']),
        })

    return jsonify({'symbol': symbol, 'candles': candle_data})


if __name__ == '__main__':
    app.run(port=5000)

# Shutdown MT5 connection
atexit.register(mt5.shutdown)
