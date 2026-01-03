import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    pod_name = os.getenv("POD_NAME", "Not Set")
    pod_ip = os.getenv("POD_IP", "Not Set")
    
    return render_template("index.html", pod_name=pod_name, pod_ip=pod_ip, version="v2.0")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)