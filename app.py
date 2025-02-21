import logging
import requests
import socket
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import ipinfo
import aiohttp

# Replace with your actual IPinfo and ipstack API access tokens
ipinfo_token = 'a6f88e599f7e36'
handler = ipinfo.getHandler(ipinfo_token)
ipstack_api_key = '220e45d1a00539752f4b9f37c53b2c19'

# Replace with your actual Telegram bot token
bot_token = '7791892519:AAF07EHEO-9eS10_5nWcaWYAq0jUVzU_WZ0'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

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
        "country": ipinfo_details.country_name if hasattr(ipinfo_details, 'country_name') else 'N/A',
        "region": ipinfo_details.region if hasattr(ipinfo_details, 'region') else 'N/A',
        "city": ipinfo_details.city if hasattr(ipinfo_details, 'city') else 'N/A',
        "zip": ipinfo_details.postal if hasattr(ipinfo_details, 'postal') else 'N/A',
        "coordinates": ipinfo_details.loc if hasattr(ipinfo_details, 'loc') else 'N/A',
        "organization": ipinfo_details.org if hasattr(ipinfo_details, 'org') else 'N/A',
        "asn": ipinfo_details.asn if hasattr(ipinfo_details, 'asn') else 'N/A',
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
    ip_address = ' '.join(context.args)
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
    hostname = ' '.join(context.args)
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
        await update.message.reply_text(f'Unable to get IP address for hostname: {hostname}')

def main() -> None:
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ip", ip_command))
    application.add_handler(CommandHandler("host", host_command))

    # Serve the application on port 8000
    application.run_polling()

if __name__ == '__main__':
    main()
