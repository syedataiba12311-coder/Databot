# WhatsApp Data Bot for Google Sheets

This bot allows you to collect data from WhatsApp messages and append them to a Google Sheet. It also includes functionality to generate a daily report.

## Setup Instructions

### 1. Google Sheets Setup
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the **Google Sheets API** and **Google Drive API**.
4. Create **Service Account** credentials and download the JSON key file.
5. Rename the downloaded JSON file to `service_account.json` and place it in this project folder (`C:\Users\User\Videos\Chatbot\WhatsAppBot\`).
6. Create a new Google Sheet and share it with the email address found in your `service_account.json` (give it Editor access).
7. Ensure your sheet has the following columns in the first row (Header): `Timestamp`, `Sender`, `Item`, `Quantity`.
8. Copy the **Spreadsheet ID** from the sheet's URL (it's the long string of characters between `/d/` and `/edit`).

### 2. Twilio WhatsApp Setup
1. Create a [Twilio Account](https://www.twilio.com/).
2. Activate your Twilio Sandbox for WhatsApp.
3. Note your `Account SID` and `Auth Token` from the Twilio Console.
4. Set up an ngrok server to expose your local Flask app to the internet (e.g., `ngrok http 5000`).
5. Set the Twilio Sandbox webhook URL to `https://<your-ngrok-url>/bot`.

### 3. Environment Variables
1. Copy the `.env.example` file and rename it to `.env`.
2. Fill in the `.env` file with your Twilio and Google Sheets details.
   - For phone numbers, Make sure to include the `whatsapp:` prefix, e.g., `whatsapp:+923001234567`.

### 4. Running the Bot
1. Open a terminal in this directory.
2. Install the required Python packages:
   ```cmd
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```cmd
   python app.py
   ```



## Usage
- Text the bot: `Sold 5 shirts`
  - The bot will log: `Timestamp: <current time>`, `Sender: <your number>`, `Item: shirts`, `Quantity: 5`.
- Text the bot: `report`
  - The bot will instantly return the sum of all items sold today.
- The bot will also automatically send a daily report every day at 20:00 (8:00 PM) to the `OWNER_WHATSAPP_NUMBER`.
