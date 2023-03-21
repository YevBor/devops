from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Just for practice up number 1"

if __name__ == "__main__":
        app.run(debug=True)