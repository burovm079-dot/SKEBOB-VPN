# SKEBOB VPN bot

Telegram bot prototype for the SKEBOB VPN project.

## Current status

- Button-based Telegram menu
- One-time 24-hour trial tracking in SQLite
- Account status display
- Plan and support sections are placeholders

## Not implemented yet

- VPN server provisioning and access-link generation
- Payments and automatic subscription renewal
- Production hosting, backups, and monitoring

**The trial currently records a timer only. It does not provide VPN access.**

## Run in a development environment

1. Install dependencies: `pip install -r requirements.txt`
2. Set `BOT_TOKEN` as an environment variable using a private secret setting.
3. Run: `python main.py`

For GitHub Codespaces, add the token under the account's **Settings → Secrets and variables → Codespaces**. Reopen the Codespace after adding a new secret so it becomes available.

Never paste the real token into source files, commits, screenshots, or chats. If it is exposed, revoke it with BotFather and create a replacement.

The `.env.example` file is only a blank template; do not put real credentials in it.
