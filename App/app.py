from flask import Flask, render_template
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return render_template('index.html', hostname=hostname, local_ip=local_ip)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)