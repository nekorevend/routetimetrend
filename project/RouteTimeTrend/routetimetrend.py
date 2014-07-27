__author__ = 'vchang'

from flask import Flask
import re
import urllib

app = Flask(__name__)

@app.route('/')
def index():
    sock = urllib.urlopen('https://www.google.com/maps/dir/Los+Angeles,+CA/San+Francisco,+CA/@35.8599167,-124.7220576,6z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x80c2c75ddc27da13:0xe22fdf6f254608f4!2m2!1d-118.2436849!2d34.0522342!1m5!1m1!1s0x80859a6d00690021:0x4a501367f076adff!2m2!1d-122.4194155!2d37.7749295')
    htmlSource = sock.read()
    sock.close()
    m = re.search('<span> +In current traffic: (.*?) +</span>', htmlSource)
    result = m.group(1)
    return result

if __name__ == '__main__':
    app.run()