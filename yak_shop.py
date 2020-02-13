import sys
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from yak import Yak, Sex
import herd
from herd import Herd
import xml.etree.ElementTree as XMLParser
import json


app = Flask(__name__)
CORS(app)


def get_herd(input_xml):
    yaks_list = list()
    root_element = XMLParser.fromstring(input_xml)
    if root_element.tag != 'herd':
        raise Exception('The root element must be "herd".')
    for element in root_element.iter('labyak'):
        yak_name = element.get('name')
        if yak_name is None:
            raise Exception('The "name" is not in labyak.')

        yak_age = element.get('age')
        if yak_age is None:
            raise Exception('The "age" is not in labyak.')
        yak_age = float(yak_age) * 100

        yak_sex = element.get('sex')
        if yak_sex is None or yak_sex not in ['f', 'm']:
            raise Exception('The "sex" is not in labyak or is not m/f.')
        yak_sex = Sex.FEMALE if yak_sex == 'f' else Sex.MALE

        yaks_list.append(Yak(name=yak_name, age=yak_age, sex=yak_sex))
    if len(yaks_list) == 0:
        raise Exception('No labyak in XML file.')
    return Herd(yaks_list)


def generate_in_stock_report(_herd, elapsed_time):
    total_milk = _herd.total_milk(elapsed_time)
    total_skins = _herd.total_skins(elapsed_time)

    in_stock = '''In Stock:
    {:.3f} liters of milk    
    {} skins of wool\n'''.format(total_milk, total_skins)

    herd_status = 'Herd:\n'
    for yak in _herd.get_yaks_list():
        herd_status += '    ' + yak.name + ' ' + str((yak.age + elapsed_time) / 100) + ' years old.\n'

    return in_stock + herd_status


@app.route('/yak-shop/load', methods=['POST'])
def load_new_herd():
    try:
        herd.global_herd = get_herd(request.data)
        response = Response("new herd loaded", status=205)
    except Exception as _ex:
        error_msg = "XML parse error: {}".format(_ex)
        print(error_msg)
        response = Response(error_msg, status=400)
    return response


@app.route('/yak-shop/stock/<int:elapsed_time>', methods=['GET'])
def stock_in_elapsed_time(elapsed_time):
    stock = dict()
    total_milk = herd.global_herd.total_milk(elapsed_time)
    total_skins = herd.global_herd.total_skins(elapsed_time)
    stock['milk'] = total_milk
    stock['skins'] = total_skins
    return json.dumps(stock)


@app.route('/yak-shop/herd/<int:elapsed_time>', methods=['GET'])
def herd_in_elapsed_time(elapsed_time):
    herd_list = list()
    for yak in herd.global_herd.get_yaks_list():
        yak_details = {'name': yak.name,
                       'age': (yak.age + elapsed_time) / 100,
                       'age-last-shaved': yak.age / 100}
        herd_list.append(yak_details)
    return json.dumps(herd_list)


@app.route('/yak-shop/order/<int:ordered_time>', methods=['POST'])
def handle_the_order(ordered_time):
    try:
        # user_name = request.json["customer"]
        ordered_milk = float(request.json["order"]["milk"])
        ordered_skins = int(request.json["order"]["skins"])
        elapsed_time = ordered_time
        total_milk = herd.global_herd.total_milk(elapsed_time)
        total_skins = herd.global_herd.total_skins(elapsed_time)
        output = {}
        if ordered_milk <= total_milk:
            output["milk"] = ordered_milk
        if ordered_skins <= total_skins:
            output["skins"] = ordered_skins

        status_code = 404
        if len(output) == 2:
            status_code = 201
        elif len(output) == 1:
            status_code = 206

        response = jsonify(output)
        response.status_code = status_code
    except KeyError as _ex:
        error_msg = "json format is not correct. {}".format(_ex)
        response = Response(error_msg, status=400)
        response.status_code = 404
    return response


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python yak_shop.py <input_file_path> <elapsed_time>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    try:
        with open(input_file_path, 'r') as input_file:
            herd.global_herd = get_herd(input_file.read())
    except FileNotFoundError as ex:
        print(ex)
        sys.exit(2)
    except Exception as ex:
        print("XML parse error: {}".format(ex))
        sys.exit(2)

    try:
        _elapsed_time = int(sys.argv[2])
        assert(_elapsed_time >= 0)
    except (ValueError, AssertionError) as ex:
        print("elapsed_time must be non negative integer.")
        sys.exit(3)

    report = generate_in_stock_report(herd.global_herd, _elapsed_time)
    print(report)

    app.run(debug=True)
