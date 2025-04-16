# Reflect: AI‑Powered Life Tracker

A personal logging and analytics assistant built with FastAPI, SQLite, SQLAlchemy, Pydantic, APScheduler and Telegram Bot API. Track anything—from workouts and expenses to water intake, cigarettes, books read, and more—simply by sending messages to your bot. Get automated daily, weekly and monthly summary reports delivered back to your Telegram chat.

---

## 🚀 Current MVP (v0.1)

- **Conversational Input via Telegram**  
  Send free‑form messages (e.g. “I ran 5 km today”, “Spent ₹200 on lunch”, “Drank 2 L water”) and the bot:
  - Parses out a category (`exercise`, `expense`, `water`, etc.)
  - Extracts numeric quantity + unit (if present)
  - Saves a structured `LogEntry` in a SQLite database

- **REST API**  
  - `POST /chat` – accept and store a log message  
  - `GET  /logs?limit=N` – retrieve your N most recent entries  
  - `GET  /summary/daily` – counts per category over the last 24 hours  
  - `GET  /summary/weekly` – counts per category over the past 7 days  
  - `GET  /summary/monthly` – counts per category over the past 30 days  

- **Scheduler**  
  - Uses APScheduler to call each summary endpoint on a cron schedule (e.g. daily at 20:00 IST)  
  - Formats the JSON response into a human‑readable Telegram message and sends it back via the Bot API

- **Automated Tests**  
  - Unit tests for the message parser  
  - Integration tests for all API endpoints (using FastAPI’s TestClient)  
  - Coverage of daily/weekly/monthly summary logic  

---

## 📦 Tech Stack

- **Backend**: FastAPI, Uvicorn  
- **Database**: SQLite via SQLAlchemy ORM  
- **Data Validation & Docs**: Pydantic models & OpenAPI  
- **Scheduler**: APScheduler (AsyncIO)  
- **Bot Integration**: pyTelegramBotAPI (TeleBot)  
- **Testing**: pytest, httpx  
- **Repo Management**: Git with feature‑branch workflow  

---

## ⚙️ Getting Started

1. **Clone & install**
   ```bash
   git clone https://github.com/your‑username/reflect.git
   cd reflect
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
2. **Environment Create a .env file in the project root:**
   ```bash
   TELEGRAM_BOT_TOKEN=12345:ABCDEF…
   TELEGRAM_CHAT_ID=987654321
   API_BASE_URL=http://127.0.0.1:8000

3. **Initialise the database**
   ```bash
   python -m app.database.db_init

4. **Run the API + Scheduler**
  ```bash
   uvicorn app.main:app --reload
```
This will:  
- Create any missing tables
- Start your daily/weekly/monthly APScheduler jobs

5. **Run the Telegram bot**
```bash
python bots/telegram_bot.py
```

6. **Receive Summaries**
- Log messages in your bot chat
- Get automated reports at your scheduled times 

---
## 🧪 Running Tests

```bash
pytest -q
```
All unit and integration tests should pass.
---
## 📁 Directory Structure

```bash
.
├── app/
│   ├── main.py            # FastAPI application & routes
│   ├── models.py          # SQLAlchemy models
│   ├── database.py        # DB engine & session setup
│   ├── database/          # db_init script
│   ├── scheduler.py       # APScheduler job definitions
│   └── schemas.py         # Pydantic response models
├── bots/
│   ├── telegram_bot.py    # production bot logic
│   └── echo_chat_id.py    # helper to fetch your chat_id
├── tests/                 # pytest suites
├── reflect.db             # SQLite file (should be git‑ignored)
├── requirements.txt
├── pytest.ini
└── .env                   # your secrets (git‑ignored)
```
---
## 🛣️ Roadmap & Future Enhancements

### Dashboard UI
- Single‑page app (React or vanilla JS + Chart.js)  
- Browse/filter logs, visualise trends in bar/pie charts

### Advanced NLP & Analytics
- Use spaCy or HuggingFace to extract moods, meal items, locations  
- Sentiment analysis on free‑form thoughts  
- Detect and normalize relative dates (“yesterday”, “last Monday”)

### User Accounts & Authentication
- JWT‑based signup/login  
- Multi‑user support: one account, one chat, private data

### Per‑User Goals & Notifications
- Define custom goals (e.g. 2 L water/day, 10 cigs/week)  
- Compare actuals vs. targets in daily/weekly reports  
- Push notifications if you miss a goal streak

### Data Export & Integrations
- CSV/JSON export endpoints  
- Notion & Google Sheets sync  
- Email‑to‑log ingestion (IMAP polling)

### Machine‑Learning Insights
- Trend detection & anomaly alerts  
- Personalized recommendations (“run more on gym days”)

### Mobile App / PWA
- Package dashboard as a Progressive Web App  
- Offline logging, push notifications
 
---
