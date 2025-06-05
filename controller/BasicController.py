from flask import Flask, jsonify, request
import subprocess


app = Flask(__name__)


@app.route('/date', methods=['GET'])
def get_date():
    result = subprocess.check_output(['date']).decode('utf-8')
    return jsonify({'date': result.strip()})


@app.route('/parameter', methods=['GET'])
def get_param():
    symbol = request.args.get('symbol')
    return jsonify({'symbol': symbol})


if __name__ == '__main__':
    app.run()

