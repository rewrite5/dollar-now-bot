from flask import Flask
from threading import Thread
import time

app = Flask(__name__)


@app.route('/')
def home():
  dataTime = time.ctime()
  dataTime = dataTime.split()
  return f'Bot RUN - {dataTime}'


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()
