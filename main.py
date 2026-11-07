
import os
import sqlite3
from datetime import datetime, timedelta, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
DB = "users.db"


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                trial_used INTEGER DEFAULT 0,
                expires_at TEXT
            )
        """)


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Попробовать 24 часа", callback_data="trial")],
        [InlineKeyboardButton("💳 Тарифы", callback_data="plans")],
        [InlineKeyboardButton("👤 Мой аккаунт", callback_data="account")],
        [InlineKeyboardButton("🆘 Поддержка", callback_data="support")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Добро пожаловать в SKEBOB VPN!\n\nВыбери действие:",
        reply_markup=menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "trial":
        with sqlite3.connect(DB) as con:
            row = con.execute(
                "SELECT trial_used FROM users WHERE user_id = ?",
                (user_id,)
            ).fetchone()

            if row and row[0]:
                await query.edit_message_text(
                    "Ты уже использовал пробный период.",
                    reply_markup=menu()
                )
                return

            expires = (
                datetime.now(timezone.utc) + timedelta(hours=24)
            ).isoformat()

            con.execute("""
                INSERT INTO users (user_id, trial_used, expires_at)
                VALUES (?, 1, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                trial_used = 1, expires_at = excluded.expires_at
            """, (user_id, expires))

        await query.edit_message_text(
            "🎉 Пробный период на 24 часа активирован!\n\n"
            "Пока это тестовый режим: подключение к VPN ещё не настроено.",
            reply_markup=menu()
        )

    elif query.data == "plans":
        await query.edit_message_text(
            "💳 Тарифы SKEBOB VPN:\n\n"
            "Неделя\n"
            "1 месяц\n"
            "3 месяца\n"
            "6 месяцев\n"
            "12 месяцев\n\n"
            "Оплата пока настраивается.",
            reply_markup=menu()
        )

    elif query.data == "account":
        with sqlite3.connect(DB) as con:
            row = con.execute(
                "SELECT expires_at FROM users WHERE user_id = ?",
                (user_id,)
            ).fetchone()

        if row and row[0]:
            expires = datetime.fromisoformat(row[0])
            if expires > datetime.now(timezone.utc):
                status = "Пробный период активен."
            else:
                status = "Подписка не активна."
        else:
            status = "У тебя пока нет активной подписки."

        await query.edit_message_text(
            "👤 Твой аккаунт\n\n" + status,
            reply_markup=menu()
        )

    elif query.data == "support":
        await query.edit_message_text(
            "🆘 Поддержка SKEBOB VPN\n\n"
            "Раздел пока находится в разработке.",
            reply_markup=menu()
        )


def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN")

    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    print("SKEBOB VPN запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
