import pandas as pd
import time
from influxdb_client import InfluxDBClient, Point, Dialect, WriteOptions, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
from dotenv import load_dotenv
import os
import configparser
from datetime import datetime, timedelta, timezone
import rx
from pytz import UTC
from rx import operators as ops
import json
import socket
logging.basicConfig(filename='datasource/std.log', filemode='w+',
                    format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv()
client = None


def saveVar(name, value):
    data = {}
    data[name] = value
    with open("status.json", 'w+') as outfile:
        json.dump(data, outfile)


def readVar(name):
    if(not os.path.exists('status.json')):
        return datetime.now().timestamp()
    with open('status.json') as f:
        data = json.load(f)
        return data[name]


def connect_db():
    # connect to database
    global client
    read_config = configparser.ConfigParser()
    while True:
        try:
            read_config.read("config/influx-configs")
            break
        except Exception as err:
            time.sleep(3)
            pass
    
    url = (read_config.get("default", "url")).strip(
        '"').replace('localhost', 'influxdb')
    while True:
        if checknetstate("influxdb", int(url.split(":")[-1])):
            break
        else:
            time.sleep(3)
    client = InfluxDBClient(
        url=url, token=read_config.get("default", "token").strip('"'), org=read_config.get("default", "org").strip('"'),
        verify_ssl=False, timeout=6000, ssl=False, debug=False)
    return client


def extractFromCsv():
    while True:
        try:
            df = pd.read_csv("datasource/"+os.getenv('datasource'))
            return df
        except Exception as e:
            logging.info("automatically try to get data from csv after 5s")
            time.sleep(5)


def insertDataIntoDb():
    bucketname = os.getenv('bucketname')
    org = os.getenv('org')
    client = connect_db()
    write_client = client.write_api(write_options=SYNCHRONOUS)
    points = []
    df = extractFromCsv()
    starttime = readVar("lasttime")
    for index, row in df.iterrows():
        pt = Point("price").tag("test", "test").field("stockvalue", row['Stock_value']).time(
            int(starttime*1000000000))
        starttime += 1
        write_client.write(bucketname, org, pt)

    saveVar("lasttime", starttime)
    write_client.flush()
    write_client.__del__()
    client.__del__()


def deleteDataSource():
    try:
        os.remove("datasource/"+os.getenv('datasource'))
    except Exception as err:
        print(err)
        logging.info(err)


def runCron():
    while True:
        try:
            insertDataIntoDb()
            deleteDataSource()
        except Exception as err:
            logging.info(err)
        time.sleep(5)


def checknetstate(url, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((url, port))
    except Exception as err:
        return False
    if result == 0:
        return True
    else:
        return False
    sock.close()


if __name__ == "__main__":
    runCron()
