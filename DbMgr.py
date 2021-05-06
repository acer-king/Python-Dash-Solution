
from influxdb import InfluxDBClient


class DbMgr():
    def __init__(self):
        self.client = InfluxDBClient(host='ec2-18-116-234-142.us-east-2.compute.amazonaws.com',
                                     port=8086, username='myuser', password='mypass', ssl=True, verify_ssl=True)
        super().__init__()

    def create_newDb(self, dbname):
        dbname = dbname if dbname else "dastan"
        self.client.create_database(dbname)
