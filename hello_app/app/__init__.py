import signal
import sys

from flask import Flask

def signal_term_handler(signal, frame):
  sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)
app = Flask(__name__)

from app import routes
