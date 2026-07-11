import os
import re
from datetime import datetime
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER') # e.g. whatsapp:+14155238886
OWNER_WHATSAPP_NUMBER = os.getenv('OWNER_WHATSAPP_NUMBER') # where to send daily reports

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID else None

# Google Sheets configuration
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Provide path to your service account credential JSON file
SERVICE_ACCOUNT_FILE = 'service_account.json'
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

def get_sheet():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        return None
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    # Get the first sheet
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    return sheet

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From', '')
    
    resp = MessagingResponse()
    reply = resp.message()
    
    # Simple regex to find patterns like "sold 5 shirts"
    # match "sold <number> <item>"
    match = re.match(r'sold\s+(\d+)\s+(.+)', incoming_msg)
    if match:
        quantity = int(match.group(1))
        item = match.group(2).strip()
        
        sheet = get_sheet()
        if sheet:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                # Update spreadsheet
                sheet.append_row([timestamp, sender, item, quantity])
                reply.body(f"✅ Recorded: Sold {quantity} of {item}")
            except Exception as e:
                reply.body(f"❌ Error updating sheet: {str(e)}")
        else:
            reply.body("❌ Sheet configuration missing (service_account.json or SPREADSHEET_ID).")
    elif incoming_msg == "report":
        # Allow instant report generation via a message
        report_msg = generate_daily_report()
        reply.body(report_msg)
    else:
        reply.body("Welcome to your Data Bot!\n\nCommands:\n- Type 'Sold [number] [item]' to log a sale (e.g. 'Sold 5 shirts')\n- Type 'report' to get today's summary.")
        
    return str(resp)

def generate_daily_report():
    sheet = get_sheet()
    if not sheet:
        return "❌ Sheet configuration missing (service_account.json or SPREADSHEET_ID). Ensure they are provided."
        
    try:
        records = sheet.get_all_records()
    except Exception as e:
        return f"❌ Could not retrieve records: {str(e)}. (Ensure your sheet has a header row: Timestamp, Sender, Item, Quantity)"
        
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    today_sales = 0
    items_sold = {}
    
    for row in records:
        # Assuming sheet has columns: Timestamp, Sender, Item, Quantity
        timestamp = str(row.get("Timestamp", ""))
        if today_str in timestamp:
            try:
                quantity = int(row.get("Quantity", 0))
            except ValueError:
                quantity = 0
                
            item = str(row.get("Item", "Unknown"))
            today_sales += quantity
            
            if item in items_sold:
                items_sold[item] += quantity
            else:
                items_sold[item] = quantity
                
    report = f"📊 *Daily Report ({today_str})*\n\n"
    report += f"Total Items Sold: {today_sales}\n\n"
    report += "Breakdown:\n"
    for item, qty in items_sold.items():
        report += f"- {item}: {qty}\n"
        
    return report

def send_daily_report():
    if not twilio_client or not OWNER_WHATSAPP_NUMBER or not TWILIO_WHATSAPP_NUMBER:
        print("Missing Twilio configuration for daily report.")
        return
        
    report = generate_daily_report()
    try:
        twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=report,
            to=OWNER_WHATSAPP_NUMBER
        )
        print("Daily report sent successfully.")
    except Exception as e:
        print(f"Failed to send daily report: {str(e)}")

# Set up the background scheduler for daily reports (e.g. at 20:00 every day)
scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_report, 'cron', hour=20, minute=0)
scheduler.start()

if __name__ == '__main__':
    # Run the Flask app
    app.run(port=5000, debug=True, use_reloader=False)
