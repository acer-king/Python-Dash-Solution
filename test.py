import unittest
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import configparser
from dotenv import load_dotenv
from dotenv import dotenv_values
import os
from datetime import datetime, timedelta


class TestStringMethods(unittest.TestCase):

    def test_connection(self):
        # You can generate a Token from the "Tokens Tab" in the UI

        # using Http
        read_config = configparser.ConfigParser()
        read_config.read("config/influx-configs")
        url = (read_config.get("default", "url")).strip('"')
        self.client = InfluxDBClient(
            url=url, token=read_config.get("default", "token"), org=read_config.get("default", "org"), verify_ssl=False, timeout=6000, ssl=False)
        status = self.client.ready()
        # dbs = client.get_list_users()
        self.assertTrue(status.status == "ready")

    def test_env(self):
        load_dotenv()
        bucketname = os.getenv('bucketname')
        self.assertTrue(bucketname == 'acer')

    def test_test(self):
        x = 1257894000123456000
        print(type(x))


if __name__ == '__main__':
    unittest.main()
    # small4
    # small5
    # samll6
    #111
