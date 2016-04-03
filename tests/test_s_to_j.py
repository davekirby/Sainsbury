#! env python2
import os
import unittest
import sainsbury_to_json

def load_file(filename):
    ''' Load a test data file from the same directory as this file'''
    test_path = os.path.split(__file__)[0]
    file_path = os.path.join(test_path, filename)
    with open(file_path, "rb") as f:
        return f.read()


class SainsburyTestCase(unittest.TestCase):
    base_url = u'http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/'

    def test_parse_products_page(self):
        html = load_file('5_products.html')
        json = sainsbury_to_json.parse_products(html)
        expected = [
            {'url' : self.base_url + u'sainsburys-apricot-ripe---ready-320g.html',
             'title' : u"Sainsbury's Apricot Ripe & Ready x5",
             'unit_price' : 3.50 },

            {'url' : self.base_url + u'sainsburys-avocado-xl-pinkerton-loose-300g.html',
             'title' : u"Sainsbury's Avocado Ripe & Ready XL Loose 300g",
             'unit_price' : 1.50 },

            {'url' : self.base_url + u'sainsburys-avocado--ripe---ready-x2.html',
             'title' : u"Sainsbury's Avocado, Ripe & Ready x2",
             'unit_price' : 1.80},

            {'url' : self.base_url + u'sainsburys-avocados--ripe---ready-x4.html',
             'title' : u"Sainsbury's Avocados, Ripe & Ready x4",
             'unit_price' : 3.20},

            {'url' : self.base_url + u'sainsburys-conference-pears--ripe---ready-x4-%28minimum%29.html',
             'title' : u"Sainsbury's Conference Pears, Ripe & Ready x4 (minimum)",
             'unit_price' : 1.50},

            {'url' : self.base_url + u'sainsburys-golden-kiwi--taste-the-difference-x4-685641-p-44.html',
             'title' : u"Sainsbury's Golden Kiwi x4",
             'unit_price' : 1.80},

            {'url' : self.base_url + u'sainsburys-kiwi-fruit--ripe---ready-x4.html',
             'title' : u"Sainsbury's Kiwi Fruit, Ripe & Ready x4",
             'unit_price' : 1.50},
        ]
        self.assertEqual(len(json), len(expected))
        for (json_dict, expected_dict) in zip(json, expected):
            self.assertItemsEqual(json_dict, expected_dict)


    def test_parse_single_product(self):
        html = load_file('sainsburys-apricot-ripe---ready-320g.html')
        product_data = sainsbury_to_json.parse_single_product(html)
        self.assertEqual(product_data, (u'Apricots'))


if __name__ == '__main__':
    unittest.main()
