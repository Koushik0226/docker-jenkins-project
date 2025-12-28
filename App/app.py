from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # This looks for index.html inside the 'templates' folder
    # If you don't have an html file yet, just return "Hello World"
    try:
        return render_template('index.html')
    except:
        return "Hello from your Containerized Python App!"

if __name__ == '__main__':
    # Host='0.0.0.0' is crucial for Docker containers to be accessible
    app.run(host='0.0.0.0', port=5000)