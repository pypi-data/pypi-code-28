from flask import Flask

app = Flask(__name__)

from .views import *
from .api import *
