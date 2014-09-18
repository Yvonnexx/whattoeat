from flask import Flask

app = Flask('Symantec-Ordering-app')

from apis.v1 import menu, order
