import logging

from faststream import FastStream
from service_y.app.workers import broker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastStream(broker)
