from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!, <a href='static/index.html'>click here</a> for UI demo"

if __name__ == "__main__":
    app.run()