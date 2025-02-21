import logging
import requests
import socket
import threading
import ipinfo
import aiohttp
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Replace with your actual API keys
ipinfo_token = 'a6f88e599f7e36'
handler = ipinfo.getHandler(ipinfo_token)
ipstack_api_key = '220e45d1a00539752f4b9f37c53b2c19'
bot_token = '7791892519:AAF07EHEO-9eS10_5nWcaWYAq0jUVzU_WZ0'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app for health check
app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "OK"})

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Use /ip <IP_ADDRESS> or /host <HOSTNAME> to get information.')

async def get_ip_info(ip_address: str) -> dict:
    ipinfo_details = handler.getDetails(ip_address)

    async with aiohttp.ClientSession() as session:
        url = f'http://api.ipstack.com/{ip_address}?access_key={ipstack_api_key}'
        async with session.get(url) as response:
            ipstack_details = await response.json()

    details = {
        "ip": ipinfo_details.ip,
        "continent": ipstack_details.get("continent_name", "N/A"),
        "country": getattr(ipinfo_details, 'country_name', 'N/A'),
        "region": getattr(ipinfo_details, 'region', 'N/A'),
        "city": getattr(ipinfo_details, 'city', 'N/A'),
        "zip": getattr(ipinfo_details, 'postal', 'N/A'),
        "coordinates": getattr(ipinfo_details, 'loc', 'N/A'),
        "organization": getattr(ipinfo_details, 'org', 'N/A'),
        "asn": getattr(ipinfo_details, 'asn', 'N/A'),
        "timezone": ipstack_details.get("time_zone", {}).get("id", "N/A"),
        "current_time": ipstack_details.get("time_zone", {}).get("current_time", "N/A"),
        "vpn": ipstack_details.get("security", {}).get("vpn", "N/A"),
        "proxy": ipstack_details.get("security", {}).get("proxy", "N/A"),
        "tor": ipstack_details.get("security", {}).get("tor", "N/A"),
        "hosting": ipstack_details.get("hosting", "N/A"),
        "bot_status": "N/A",
        "recent_abuse": "N/A",
        "used_to_attack": "N/A",
        "ipqs_score": "N/A",
        "ipintel_score": "N/A",
        "abuseipdb_score": "N/A",
        "scamalytics_score": "N/A"
    }
    return details

async def ip_command(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /ip <IP_ADDRESS>")
        return
    
    ip_address = context.args[0]
    details = await get_ip_info(ip_address)

    response_text = f"""
🔍 **IP Check**

🖥️ **IP Address**: {details['ip']}
---------------------------------------
🌍 **Continent**: {details['continent']}
🌎 **Country**: {details['country']}
🏙️ **Region**: {details['region']}
🏡 **City**: {details['city']}
📮 **ZIP Code**: {details['zip']}
📍 **Coordinates**: {details['coordinates']}
---------------------------------------
🏢 **Organization**: {details['organization']}
🔢 **ASN**: {details['asn']}
---------------------------------------
🕒 **Timezone**: {details['timezone']}
⏱️ **Current Time**: {details['current_time']}
---------------------------------------
🛡️ **VPN**: {details['vpn']}
🕵️ **Proxy**: {details['proxy']}
🌐 **Tor Node**: {details['tor']}
🏢 **Hosting**: {details['hosting']}
🤖 **Bot Status**: {details['bot_status']}
⚠️ **Recent Abuse**: {details['recent_abuse']}
🚨 **Used to Attack**: {details['used_to_attack']}
📊 **IPQS Score**: {details['ipqs_score']}
📊 **IPIntel Score**: {details['ipintel_score']}
📊 **AbuseIPDB Score**: {details['abuseipdb_score']}
📊 **Scamalytics Score**: {details['scamalytics_score']}

**MADE BY DARKBOY**
📌 @darkboy336
"""
    await update.message.reply_text(response_text, parse_mode='Markdown')

async def host_command(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /host <HOSTNAME>")
        return

    hostname = context.args[0]
    try:
        ip_address = socket.gethostbyname(hostname)
        details = await get_ip_info(ip_address)

        response_text = f"""
🔍 **Host Check**

🖥️ **Hostname**: {hostname}
🖥️ **IP Address**: {details['ip']}
---------------------------------------
🌍 **Continent**: {details['continent']}
🌎 **Country**: {details['country']}
🏙️ **Region**: {details['region']}
🏡 **City**: {details['city']}
📮 **ZIP Code**: {details['zip']}
📍 **Coordinates**: {details['coordinates']}
---------------------------------------
🏢 **Organization**: {details['organization']}
🔢 **ASN**: {details['asn']}
---------------------------------------
🕒 **Timezone**: {details['timezone']}
⏱️ **Current Time**: {details['current_time']}
---------------------------------------
🛡️ **VPN**: {details['vpn']}
🕵️ **Proxy**: {details['proxy']}
🌐 **Tor Node**: {details['tor']}
🏢 **Hosting**: {details['hosting']}
🤖 **Bot Status**: {details['bot_status']}
⚠️ **Recent Abuse**: {details['recent_abuse']}
🚨 **Used to Attack**: {details['used_to_attack']}
📊 **IPQS Score**: {details['ipqs_score']}
📊 **IPIntel Score**: {details['ipintel_score']}
📊 **AbuseIPDB Score**: {details['abuseipdb_score']}
📊 **Scamalytics Score**: {details['scamalytics_score']}

**MADE BY DARKBOY**
📌 @darkboy336
"""
        await update.message.reply_text(response_text, parse_mode='Markdown')
    except socket.gaierror:
        await update.message.reply_text(f'Unable to resolve hostname: {hostname}')

def run_flask():
    """Run the Flask app in a separate thread."""
    app.run(host='0.0.0.0', port=8000)

def main() -> None:
    """Start the Telegram bot and Flask app simultaneously."""
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ip", ip_command))
    application.add_handler(CommandHandler("host", host_command))

    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start the Telegram bot
    application.run_polling()

if __name__ == '__main__':
    main()
