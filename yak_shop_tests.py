import unittest
import requests
import json
from yak_shop import get_herd
from yak import Sex


class YakShopTestCases(unittest.TestCase):
    def test_load_herd_correct(self):
        xml = '''<herd>
        <labyak name="Betty-1" age="4" sex="f"/>
        <labyak name="Betty-2" age="8" sex="f"/>
        <labyak name="Betty-3" age="9.5" sex="f"/>
        </herd>'''
        response = requests.post('http://127.0.0.1:5000/yak-shop/load', data=xml)
        self.assertEqual(response.status_code, 205)

    def test_load_herd_with_incorrect_key(self):
        xml = '''<herd>
        <lab_yak name="Betty-1" age="4" sex="f"/>
        <lab_yak name="Betty-2" age="8" sex="f"/>
        <lab_yak name="Betty-3" age="9.5" sex="f"/>
        </herd>'''
        response = requests.post('http://127.0.0.1:5000/yak-shop/load', data=xml)
        self.assertEqual(response.status_code, 400)

    def test_load_herd_with_incorrect_format(self):
        xml = '''<labyak name="Betty-1" age="4" sex="f"/>
        <labyak name="Betty-2" age="8" sex="f"/>
        <labyak name="Betty-3" age="9.5" sex="f"/>'''
        response = requests.post('http://127.0.0.1:5000/yak-shop/load', data=xml)
        self.assertEqual(response.status_code, 400)

    def test_load_herd_in_list_format(self):
        xml = '''[{name:"Betty-1", age:"4", sex:"f"},
        {name:"Betty-2", age:"8", sex:"f"},
        {name:"Betty-3", age:"9.5", sex:"f"}'''
        response = requests.post('http://127.0.0.1:5000/yak-shop/load', data=xml)
        self.assertEqual(response.status_code, 400)

    def test_get_stuck(self):
        response = requests.get('http://127.0.0.1:5000/yak-shop/stock/13')
        self.assertEqual(response.json(), {"milk": 1104.48, "skins": 3})

    def test_get_stuck_incorrect_url(self):
        response = requests.get('http://127.0.0.1:5000/yak-shop/stock/-1')
        self.assertEqual(response.status_code, 404)

    def test_get_herd(self):
        response = requests.get('http://127.0.0.1:5000/yak-shop/herd/13')
        expected_response = [{"age": 4.13, "age-last-shaved": 4.0, "name": "Betty-1"}, {"age": 8.13, "age-last-shaved": 8.0, "name": "Betty-2"},
            {"age": 9.63, "age-last-shaved": 9.5, "name": "Betty-3"}]
        self.assertEqual(json.loads(response.text), expected_response)

    def test_order_success_output(self):
        xml = {"customer": "Medvedev",
                "order": {
                "milk": 1100,
                "skins": 3
                }
            }
        response = requests.post('http://127.0.0.1:5000/yak-shop/order/13', json=xml)
        self.assertEqual(response.json(), {"milk": 1100, "skins": 3})

    def test_order_success_status_code(self):
        xml = {"customer": "Medvedev",
                "order": {
                "milk": 1100,
                "skins": 3
                }
            }
        response = requests.post('http://127.0.0.1:5000/yak-shop/order/13', json=xml)
        self.assertEqual(response.status_code, 201)

    def test_order_partial_success_output(self):
        xml = {"customer": "Medvedev",
                "order": {
                "milk": 1200,
                "skins": 3
                }
            }
        response = requests.post('http://127.0.0.1:5000/yak-shop/order/13', json=xml)
        self.assertEqual(response.json(), {"skins": 3})

    def test_order_partial_success_status_code(self):
        xml = {"customer": "Medvedev",
                "order": {
                "milk": 1200,
                "skins": 3
                }
            }
        response = requests.post('http://127.0.0.1:5000/yak-shop/order/13', json=xml)
        self.assertEqual(response.status_code, 206)

    def test_order_faile(self):
        xml = {"customer": "Medvedev",
                "order": {
                "milk": 1200,
                "skins": 5
                }
            }
        response = requests.post('http://127.0.0.1:5000/yak-shop/order/13', json=xml)
        self.assertEqual(response.status_code, 404)

    def test_get_herd(self):
        xml = '''<herd>
        <labyak name="Betty-1" age="4" sex="f"/>
        </herd>'''
        herd = get_herd(xml)
        yak_list = herd.get_yaks_list()
        self.assertEqual(yak_list[0].name, "Betty-1")
        self.assertEqual(yak_list[0].age, 400)
        self.assertEqual(yak_list[0].sex, Sex.FEMALE)

    def test_get_herd_incorrect_root(self):
        xml = '''<herd_>
        <labyak name="Betty-1" age="4" sex="f"/>
        </herd_>'''
        self.assertRaises(Exception, get_herd, xml)

    def test_get_herd_incorrect_attribute(self):
        xml = '''<herd>
        <labyak name="Betty-1" age_="4" sex="f"/>
        </herd_>'''
        self.assertRaises(Exception, get_herd, xml)


if __name__ == "__main__":
    unittest.main()