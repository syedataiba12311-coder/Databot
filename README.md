# Databot — WhatsApp Data Bot for Google Sheets

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![Python CI](https://github.com/syedataiba12311-coder/Databot/actions/workflows/python-ci.yml/badge.svg)](https://github.com/syedataiba12311-coder/Databot/actions)

Databot lets businesses collect structured data from WhatsApp messages and store it in Google Sheets automatically. Send simple messages like "Sold 5 shirts" and the bot extracts the fields and appends them to a spreadsheet. It can also generate daily sales reports.

## Demo
- Live demo: (add your demo URL or a short GIF here)
- Example interaction:
  - You: `Sold 5 shirts`
  - Bot: logs a row in Google Sheets with Timestamp, Sender, Item: `shirts`, Quantity: `5`

## Features
- Parse natural-language WhatsApp messages into structured rows (Timestamp, Sender, Item, Quantity)
- Append entries to Google Sheets via the Sheets API
- On-demand `report` command to get today's summary
- Scheduled daily report to owner WhatsApp number
- Easy to configure via environment variables

## Tech stack
- Backend: Python + Flask
- Messaging: Twilio WhatsApp Sandbox
- Data store: Google Sheets (via Google Sheets API and a Service Account)
- Deployment: ngrok for local testing; recommended: Heroku / Railway / VPS for production

## Quick start (local)
1. Clone the repo
   ```bash
   git clone https://github.com/syedataiba12311-coder/Databot.git
   cd Databot
   ```
2. (Recommended) create a virtual environment and activate it
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS / Linux
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Google Sheets setup
   - Enable Google Sheets API and Google Drive API in Google Cloud Console
   - Create a Service Account, download the JSON key, rename it to `service_account.json` and place it in the project root
   - Share the target Google Sheet with the service account email (Editor)
   - Ensure the sheet's header row contains: `Timestamp`, `Sender`, `Item`, `Quantity`
   - Copy the Spreadsheet ID (from the sheet URL)

5. Twilio WhatsApp setup
   - Create a Twilio account and enable the WhatsApp sandbox
   - Note your Account SID and Auth Token
   - Run ngrok to expose your local Flask server during development: `ngrok http 5000`
   - Set Twilio Sandbox webhook to `https://<your-ngrok-url>/bot`

6. Environment variables
   - Copy `.env.example` to `.env` and fill values:
     - TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
     - SPREADSHEET_ID
     - OWNER_WHATSAPP_NUMBER (e.g. `whatsapp:+92300XXXXXXX`)
     - Any other keys listed in `.env.example`

7. Run the app
   ```bash
   python app.py
   ```

## Usage
- Send: `Sold 5 shirts` → a new row is appended with parsed Item and Quantity
- Send: `report` → the bot returns the sum of today's items
- The bot sends an automated daily report at 20:00 (8 PM) to the owner number

## Configuration
- Update `service_account.json` and `.env` with your credentials
- To run in production, host the Flask app on a public server and update Twilio webhook

## Contributing
Contributions are welcome! Suggested ways to help:
- Improve message parsing & edge-case handling
- Add tests and CI checks
- Add deployment guides for Heroku / Railway
- Open issues for bugs or feature requests

## Roadmap / Improvements
- Add more robust NLP for varied message formats
- Add multi-item message parsing
- Add user authentication & role-based access for reports
- Add unit tests and integration tests

## License
This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

---

If you'd like, I can add screenshots, a GIF demo, and an architecture diagram — provide the images or let me generate a simple GIF from a demo run and I'll include it.