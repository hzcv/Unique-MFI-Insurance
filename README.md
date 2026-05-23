# Unique-MFI-Insurance

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/Unique-MFI-Insurance.git

cd telegram-number-generator-bot
```

---

### 2. Create Virtual Environment

#### Linux / Ubuntu / Debian

```bash
python3 -m venv venv
```

Activate venv:

```bash
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
```

Activate venv:

```bash
venv\Scripts\activate
```

---

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

### 4. Configure Bot

Open `bot.py`

Replace:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
```

With your real Telegram bot token.

Replace:

```python
ADMIN_ID = 123456789
```

With your Telegram user ID.

---

### 5. Run Bot

```bash
python bot.py
```


# Add systemd Service Section

# Run Bot 24/7 Using systemd (Linux VPS)

## Create Service File

```bash
sudo nano /etc/systemd/system/telegrambot.service
```

Paste this:

```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/bot
ExecStart=/home/ubuntu/bot/venv/bin/python /home/ubuntu/bot/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## Reload systemd

```bash
sudo systemctl daemon-reload
```

---

## Enable Service

```bash
sudo systemctl enable telegrambot
```

---

## Start Service

```bash
sudo systemctl start telegrambot
```

---

## Check Status

```bash
sudo systemctl status telegrambot
```

---

## View Logs

```bash
journalctl -u telegrambot -f
```

---

## Restart Bot

```bash
sudo systemctl restart telegrambot
```

---

## Stop Bot

```bash
sudo systemctl stop telegrambot
```
