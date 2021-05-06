import unittest
from influxdb import InfluxDBClient


class TestStringMethods(unittest.TestCase):

    def test_connection(self):
        self.client = InfluxDBClient(host='ec2-18-116-234-142.us-east-2.compute.amazonaws.com',
                                     port=8086, username='dauren', password='acer-king1991412', path="influxdb")
        self.client.create_database("test")
        pass

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
