from flask import Flask, render_template, make_response

app = Flask(__name__)

FLAG = "LKSWNSB{h3ad3r_jug4_p3nt1ng}"

@app.route("/")
def index():
    response = make_response(render_template("index.html"))
    # The flag is hidden here in a custom HTTP header
    response.headers["X-Flag"] = FLAG
    response.headers["X-Hint"] = "You're looking in the wrong place... or are you?"
    return response

@app.route("/about")
def about():
    response = make_response(render_template("about.html"))
    response.headers["X-Flag"] = FLAG
    response.headers["X-Hint"] = "The answer is right in front of you..."
    return response

@app.route("/hint")
def hint():
    response = make_response(render_template("hint.html"))
    response.headers["X-Flag"] = FLAG
    response.headers["X-Hint"] = "Think about what you can't see on the page..."
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
