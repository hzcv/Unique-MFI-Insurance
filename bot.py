import os
import random
import time
import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =====================================
# BOT TOKEN
# =====================================
BOT_TOKEN = "YOUR_TG_BOTOKEN"

# =====================================
# ADMIN ID
# =====================================
ADMIN_ID = 

# =====================================
# FILES
# =====================================
INSURANCE_FILE = "Insurance.txt"
MFI_FILE = "Mfi.txt"
USERS_FILE = "users.txt"
STATS_FILE = "stats.txt"

# =====================================
# CREATE FILES
# =====================================
for file_name in [
    INSURANCE_FILE,
    MFI_FILE,
    USERS_FILE,
    STATS_FILE
]:

    if not os.path.exists(file_name):

        open(file_name, "w").close()

# =====================================
# LOAD NUMBERS
# =====================================
def load_numbers(file_name):

    with open(file_name, "r") as file:

        return set(
            line.strip()
            for line in file
            if line.strip()
        )

insurance_numbers = load_numbers(INSURANCE_FILE)
mfi_numbers = load_numbers(MFI_FILE)

# =====================================
# SAVE USER
# =====================================
def save_user(user_id, username):

    users = set()

    with open(USERS_FILE, "r") as file:

        users = set(
            line.strip()
            for line in file
            if line.strip()
        )

    user_data = f"{user_id}|{username}"

    if user_data not in users:

        with open(USERS_FILE, "a") as file:

            file.write(user_data + "\n")

# =====================================
# UPDATE STATS
# =====================================
def update_stats(user_id, amount):

    stats = {}

    if os.path.exists(STATS_FILE):

        with open(STATS_FILE, "r") as file:

            for line in file:

                if "|" in line:

                    uid, count = line.strip().split("|")

                    stats[uid] = int(count)

    uid = str(user_id)

    if uid not in stats:

        stats[uid] = 0

    stats[uid] += amount

    with open(STATS_FILE, "w") as file:

        for uid, count in stats.items():

            file.write(f"{uid}|{count}\n")

# =====================================
# TOTAL USERS
# =====================================
def get_total_users():

    with open(USERS_FILE, "r") as file:

        users = [
            line.strip()
            for line in file
            if line.strip()
        ]

    return len(users)

# =====================================
# TOTAL GENERATED
# =====================================
def get_total_generated():

    total = 0

    if os.path.exists(STATS_FILE):

        with open(STATS_FILE, "r") as file:

            for line in file:

                if "|" in line:

                    total += int(
                        line.strip().split("|")[1]
                    )

    return total

# =====================================
# USER STATS
# =====================================
def get_user_stats():

    users = {}

    with open(USERS_FILE, "r") as file:

        for line in file:

            if "|" in line:

                uid, username = line.strip().split("|")

                users[uid] = username

    stats = {}

    if os.path.exists(STATS_FILE):

        with open(STATS_FILE, "r") as file:

            for line in file:

                if "|" in line:

                    uid, count = line.strip().split("|")

                    stats[uid] = count

    result = ""

    for uid, username in users.items():

        count = stats.get(uid, "0")

        result += (
            f"User: @{username}\n"
            f"ID: {uid}\n"
            f"Generated: {count}\n\n"
        )

    return result

# =====================================
# GENERATE UNIQUE
# =====================================
def generate_unique(prefix, digits, existing_set):

    while True:

        random_digits = ''.join(
            str(random.randint(0, 9))
            for _ in range(digits)
        )

        number = prefix + random_digits

        if number not in existing_set:

            existing_set.add(number)

            return number

# =====================================
# SAVE NUMBER
# =====================================
def save_number(file_name, number):

    with open(file_name, "a") as file:

        file.write(number + "\n")

# =====================================
# START COMMAND
# =====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    save_user(
        user.id,
        user.username or "NoUsername"
    )

    keyboard = [

        [
            InlineKeyboardButton(
                "𝐼𝑁𝑆𝑈𝑅𝐴𝑁𝐶𝐸",
                callback_data="insurance"
            )
        ],

        [
            InlineKeyboardButton(
                "𝑀𝐹𝐼",
                callback_data="mfi"
            )
        ]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo="https://wallpapercave.com/wp/wp2897370.jpg",
        caption="⚡ 𝘾𝙝𝙤𝙤𝙨𝙚 𝙂𝙚𝙣𝙚𝙧𝙖𝙩𝙤𝙧 ⚡:",
        reply_markup=reply_markup
    )

# =====================================
# BUTTON CLICK
# =====================================
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "insurance":

        context.user_data["type"] = "insurance"

        await query.message.reply_text(
            "How many Insurance numbers do you want?"
        )

    elif query.data == "mfi":

        context.user_data["type"] = "mfi"

        await query.message.reply_text(
            "How many MFI numbers do you want?"
        )

# =====================================
# GENERATE NUMBERS
# =====================================
async def generate_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "type" not in context.user_data:

        return

    text = update.message.text

    if not text.isdigit():

        await update.message.reply_text(
            "Please send only numbers."
        )

        return

    count = int(text)

    generated_list = []

    # =================================
    # INSURANCE
    # =================================
    if context.user_data["type"] == "insurance":

        for _ in range(count):

            number = generate_unique(
                "T00",
                15,
                insurance_numbers
            )

            save_number(
                INSURANCE_FILE,
                number
            )

            generated_list.append(number)

    # =================================
    # MFI
    # =================================
    elif context.user_data["type"] == "mfi":

        for _ in range(count):

            number = generate_unique(
                "CA041",
                8,
                mfi_numbers
            )

            save_number(
                MFI_FILE,
                number
            )

            generated_list.append(number)

    # Update user stats
    update_stats(
        update.effective_user.id,
        count
    )

    # Send numbers
    result = "\n".join(generated_list)

    # Temporary message
    boss = await update.message.reply_text("𝐋𝐞𝐠𝐚𝐜𝐲 𝐨𝐟 𝐒𝐚𝐢𝐲𝐚𝐧 🚬")

    await asyncio.sleep(2)

    try:
        await boss.delete()
    except:
        pass

    await update.message.reply_text(result)

    # Clear mode
    context.user_data.clear()

# =====================================
# ADMIN PANEL
# =====================================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "Access Denied"
        )

        return

    total_users = get_total_users()

    total_generated = get_total_generated()

    user_stats = get_user_stats()

    message = (

        f"TOTAL USERS: {total_users}\n\n"

        f"TOTAL GENERATED: {total_generated}\n\n"

        f"USER STATS:\n\n"

        f"{user_stats}"

    )

    await update.message.reply_text(message)

# =====================================
# BROADCAST
# =====================================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "Access Denied"
        )

        return

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage:\n/broadcast Your Message"
        )

        return

    broadcast_text = " ".join(context.args)

    success = 0
    failed = 0

    with open(USERS_FILE, "r") as file:

        users = [
            line.strip()
            for line in file
            if line.strip()
        ]

    for user in users:

        try:

            user_id = int(user.split("|")[0])

            await context.bot.send_message(
                chat_id=user_id,
                text=broadcast_text
            )

            success += 1

        except:

            failed += 1

    await update.message.reply_text(

        f"Broadcast Completed\n\n"

        f"Success: {success}\n"

        f"Failed: {failed}"

    )

# =====================================
# MAIN
# =====================================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("admin", admin)
    )

    app.add_handler(
        CommandHandler("broadcast", broadcast)
    )

    app.add_handler(
        CallbackQueryHandler(button_click)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            generate_numbers
        )
    )

    print("Bot Running...")

    app.run_polling()

# =====================================
# AUTO RESTART
# =====================================
if __name__ == "__main__":
    main()
