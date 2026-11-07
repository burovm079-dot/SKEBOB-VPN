# SKEBOB VPN bot

Telegram bot prototype for the SKEBOB VPN project.

## Current status

- Button-based Telegram menu
- One-time 24-hour trial tracking in SQLite
- Account status display
- Plan and support sections are placeholders

## Not implemented yet

- VPN server provisioning and access-link generation
- Subscription payments
- Automatic renewal and expiry enforcement
- Production hosting and monitoring

## Run locally

1. Install dependencies: `pip install -r requirements.txt`
2. Set the `BOT_TOKEN` environment variable securely.
3. Run: `python main.py`

Never commit your Telegram bot token or `.env` file.
