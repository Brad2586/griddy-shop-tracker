import os
import time
from datetime import datetime

from keyid import KeyID
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TO_EMAIL = "bleon42@hotmail.com"
HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "griddy_status.html")
agent_email = KeyID()


def check_for_griddy():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://fortnite.gg/shop")
        time.sleep(10)

        page_text = driver.page_source.lower()
        return "the griddy" in page_text

    finally:
        driver.quit()


def send_email(found: bool):
    if found:
        subject = "The Griddy is IN the Fortnite Shop!"
        body = (
            "The Griddy emote is available in the Fortnite Item Shop right now!\n\n"
            "https://fortnite.gg/shop"
        )
    else:
        subject = "The Griddy is NOT in the Fortnite Shop"
        body = (
            "The Griddy emote was not found in today's Fortnite Item Shop.\n\n"
            "https://fortnite.gg/shop"
        )

    try:
        result = agent_email.provision()
        print(f"Sending from: {result['email']}")
        agent_email.send(TO_EMAIL, subject, body)
        print(f"Email sent to {TO_EMAIL}: {subject}")
    except Exception as e:
        print(f"Email send failed: {e}")


def update_html(found: bool):
    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    if found:
        status = "Available"
        color = "#2ecc71"
        message = "The Griddy emote is in the Fortnite Item Shop right now!"
        emoji = "&#x1F525;"
    else:
        status = "Not Currently Available"
        color = "#e74c3c"
        message = "The Griddy emote is not in today's Fortnite Item Shop."
        emoji = "&#x274C;"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Griddy Shop Tracker</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0d0d1a;
            color: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .card {{
            background: linear-gradient(145deg, #1a1a2e, #16213e);
            border-radius: 20px;
            padding: 50px 60px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            max-width: 520px;
            width: 90%;
        }}
        .emoji {{ font-size: 64px; margin-bottom: 20px; }}
        h1 {{
            font-size: 28px;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .status {{
            font-size: 48px;
            font-weight: 900;
            color: {color};
            margin: 20px 0;
            text-shadow: 0 0 30px {color}66;
        }}
        .message {{
            font-size: 18px;
            color: #b0b0c0;
            margin-bottom: 30px;
            line-height: 1.5;
        }}
        .timestamp {{
            font-size: 13px;
            color: #555570;
            border-top: 1px solid #2a2a40;
            padding-top: 20px;
        }}
        a {{
            color: #60a5fa;
            text-decoration: none;
        }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="emoji">{emoji}</div>
        <h1>Griddy Shop Tracker</h1>
        <div class="status">{status}</div>
        <p class="message">{message}</p>
        <p class="timestamp">Last checked: {now}<br>
        <a href="https://fortnite.gg/shop" target="_blank">View Fortnite Item Shop</a></p>
    </div>
</body>
</html>"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML updated: {HTML_PATH}")


if __name__ == "__main__":
    found = check_for_griddy()
    send_email(found)
    update_html(found)
    print("Available" if found else "Not Currently Available")
