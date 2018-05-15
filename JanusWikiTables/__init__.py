from flask import Flask

app = Flask(__name__)
from JanusWikiTables.views import *

if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=False)
