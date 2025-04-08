import datetime
import re

from flask import Flask

app = Flask(__name__)

# Set of valid strftime format codes
VALID_FORMAT_CODES = {
    "a",
    "A",
    "w",
    "d",
    "b",
    "B",
    "m",
    "y",
    "Y",
    "H",
    "I",
    "p",
    "M",
    "S",
    "f",
    "z",
    "Z",
    "j",
    "U",
    "W",
    "c",
    "x",
    "X",
    "%",
    "G",
    "u",
    "V",
}


@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>StrftimeAPI</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; }
                .example { margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <h1>Welcome to StrftimeAPI</h1>
            <p>Request a path in strftime format to get the current time formatted accordingly.</p>
            <h2>Examples:</h2>
            <div class="example">
                <code>/%%Y-%%m-%%d</code> - Current date in YYYY-MM-DD format
            </div>
            <div class="example">
                <code>/%%H:%%M:%%S</code> - Current time in HH:MM:SS format
            </div>
            <div class="example">
                <code>/%%A, %%B %%d, %%Y</code> - Day of week, month name, day, and year
            </div>
            <p>Note: The % character is already escaped in the examples above. 
            In your actual URL, use single % characters (e.g., /%Y-%m-%d).</p>
        </body>
    </html>
    """
