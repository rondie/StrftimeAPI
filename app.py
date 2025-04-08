import datetime
import re

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Time Server</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; }
                .example { margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <h1>Welcome to the Time Server</h1>
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


@app.route("/<path:format_string>")
def get_time(format_string):
    try:
        # Replace URL encoded characters if present
        format_string = format_string.replace("%25", "%")

        # Enhanced security check to prevent command injection and invalid formats
        if re.search(r'[^a-zA-Z0-9\s%\-_.:;,/\\() ]', format_string):
            return "Error: Format string contains invalid characters", 400
        
        # Check for potential command injection patterns
        if ";" in format_string or "`" in format_string or "&" in format_string:
            return "Error: Format string contains invalid characters", 400
        
        # Test for valid format string
        try:
            # Try a sample formatting to see if the format string is valid
            datetime.datetime.now().strftime(format_string)
        except ValueError:
            return f"Error: Invalid format string", 400

        # Format the current time according to the provided strftime format
        current_time = datetime.datetime.now().strftime(format_string)
        return current_time
    except Exception as e:
        return f"Error: {str(e)}", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)