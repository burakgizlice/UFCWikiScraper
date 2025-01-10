from flask import Flask, request
import importlib

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    url_input = ""
    if request.method == "POST":
        url_input = request.form.get("url", "")

    return f"""
    <h1>UFC Fighters Wiki Scraper!</h1>
    <form method="post">
        <label for="url">Enter a URL:</label>
        <input type="text" id="url" name="url" value="{url_input}" placeholder="https://example.com">
        <button type="submit">Submit</button>
    </form>
    <p>URL Entered: {url_input}</p>
    <button onclick="window.location.href='/opponents?url={url_input
    }'">Opponents</button>
    <button onclick="window.location.href='/info?url={url_input}'">Info</button>
    <button onclick="window.location.href='/ops-info?url={url_input}">Ops 
    Info</button>
    <button onclick="window.location.href='/deep-ops?url={url_input}'">Deep 
    Ops</button>
    """


@app.route("/opponents")
def opponents():
    url_input = request.args.get("url", "No URL")
    scraper = importlib.import_module(f"wiki_fighters.scraper")
    entry_point = getattr(scraper, "run")
    data = entry_point(["ops", url_input])
    return data


@app.route("/info")
def info():
    url_input = request.args.get("url", "No URL")
    scraper = importlib.import_module(f"wiki_fighters.scraper")
    entry_point = getattr(scraper, "run")
    data = entry_point(["info", url_input])
    return data


@app.route("/ops-info")
def ops_info():
    url_input = request.args.get("url", "No URL")
    scraper = importlib.import_module(f"wiki_fighters.scraper")
    entry_point = getattr(scraper, "run")
    data = entry_point(["ops+info", url_input])
    return data


@app.route("/deep-ops")
def deep_ops():
    url_input = request.args.get("url", "No URL")
    scraper = importlib.import_module(f"wiki_fighters.scraper")
    entry_point = getattr(scraper, "run")
    data = entry_point(["deep-ops", url_input, "output.json"])
    return data
