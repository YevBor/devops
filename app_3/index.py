from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Just for practice, app number 3"

if __name__ == "__main__":
        app.run(debug=True)