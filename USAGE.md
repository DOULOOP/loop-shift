# Loop Shift - Card Access System Usage Guide

## 🚀 Quick Start

### First Time Setup

1. **Start the system:**
   ```bash
   docker-compose up -d
   ```

2. **Verify services are running:**
   ```bash
   docker ps
   ```
   You should see two containers:
   - `loop_shift_app` (API server)
   - `loop_shift_listener` (Card listener)

3. **Watch the listener in action:**
   ```bash
   docker logs -f loop_shift_listener
   ```

### Register Your First Card

1. **Open the CLI in a new terminal:**
   ```bash
   docker exec -it loop_shift_app python cli.py
   ```

2. **Select option 3** (Add New Card)

3. **Scan your card** when prompted

4. **Enter the person's name**

5. **Done!** The card is now registered.

---

## 📋 Usage Modes

### Mode 1: Continuous Listener (Recommended) ⭐

**Best for:** Production use, unattended operation

The card listener runs 24/7 in the background, automatically processing all card scans.

```bash
# Start (already running if you used docker-compose up)
docker-compose up -d card_listener

# View real-time logs
docker logs -f loop_shift_listener

# Stop
docker-compose stop card_listener

# Restart
docker-compose restart card_listener
```

**What happens:**
- 🔍 System continuously waits for cards
- 📇 Card detected → Automatically logged
- 💡 LED blinks (2x for entry, 3x for exit)
- 📊 Logs displayed in real-time
- ♻️ Repeats forever

---

### Mode 2: Interactive CLI

**Best for:** Manual operation, card registration, viewing history

```bash
docker exec -it loop_shift_app python cli.py
```

**Menu Options:**

1. **Continuous Scan Mode (Auto)**
   - Automatically scans cards until you press Ctrl+C
   - Same as the dedicated listener, but interactive

2. **Single Scan (Manual)**
   - Scan one card at a time
   - Returns to menu after each scan

3. **Add New Card**
   - Register a new card with a person's name
   - Guided process

4. **View Access History**
   - See recent entries and exits
   - Shows timestamps, actions, and names

5. **Exit**
   - Close the CLI

---

### Mode 3: API Access

**Best for:** Integration with other systems, remote management

**Base URL:** `http://<raspberry-pi-ip>:8000`

**Interactive Docs:** `http://<raspberry-pi-ip>:8000/docs`

**Example API Calls:**

```bash
# Scan a card (manual trigger)
curl -X POST "http://localhost:8000/scan" \
  -H "Content-Type: application/json" \
  -d '{"card_id": "00x-abc-bcd"}'

# Get access history
curl "http://localhost:8000/history?limit=10"

# Get specific user
curl "http://localhost:8000/users/00x-abc-bcd"

# Register new user
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"card_id": "new-card-id", "full_name": "John Doe"}'
```

---

## 💡 LED Indicator Behavior

| Action | LED Blinks | Meaning |
|--------|-----------|---------|
| **Entry** (Clock In) | ✨✨ (2 times) | Person entered |
| **Exit** (Clock Out) | ✨✨✨ (3 times) | Person exited |

**Blink Pattern:**
- Each blink: 0.2 seconds ON
- Between blinks: 0.2 seconds OFF

---

## 🔧 Common Tasks

### View Listener Logs
```bash
docker logs -f loop_shift_listener
```

### Stop Everything
```bash
docker-compose down
```

### Restart Everything
```bash
docker-compose restart
```

### Restart Only the Listener
```bash
docker-compose restart card_listener
```

### Check if Services are Running
```bash
docker ps | grep loop_shift
```

### Access API Documentation
Open in browser: `http://<raspberry-pi-ip>:8000/docs`

### Backup Database
The database is hosted externally (PostgreSQL), so backups should be handled there.

---

## 🐛 Troubleshooting

### Card Not Detected

1. **Check I2C connection:**
   ```bash
   docker exec -it loop_shift_app i2cdetect -y 1
   ```
   You should see a device at address `0x24` (PN532)

2. **Check listener logs:**
   ```bash
   docker logs loop_shift_listener
   ```

3. **Verify hardware:**
   - PN532 power LED should be on
   - Check wiring connections

### LED Not Working

1. **Check GPIO permissions:**
   ```bash
   docker exec -it loop_shift_listener ls -l /dev/gpiomem
   ```

2. **Verify LED wiring:**
   - GPIO 17 → Resistor (220-330Ω) → LED (+)
   - LED (-) → GND

3. **Test LED manually:**
   ```bash
   docker exec -it loop_shift_app python -c "from led_controller import LEDController; led = LEDController(17); led.blink(5); led.cleanup()"
   ```

### Card Not Recognized

The card needs to be registered first:
```bash
docker exec -it loop_shift_app python cli.py
# Select option 3: Add New Card
```

### Services Won't Start

1. **Check if ports are available:**
   ```bash
   sudo netstat -tulpn | grep 8000
   ```

2. **Check Docker logs:**
   ```bash
   docker-compose logs
   ```

3. **Rebuild containers:**
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

## 📊 System Flow

```
┌─────────────────────────────────────────────────────────┐
│                    CARD SCAN EVENT                      │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              PN532 Reader Detects Card                  │
│                  (via I2C Bus)                          │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│         Card Listener / CLI / API Processes             │
│                                                         │
│  1. Read Card ID                                        │
│  2. Check if user exists in database                    │
│  3. Determine action (ENTRY or EXIT)                    │
│  4. Log to PostgreSQL database                          │
│  5. Trigger LED feedback                                │
└─────────────────────────────────────────────────────────┘
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
┌──────────────────────┐    ┌──────────────────────┐
│   LED Controller     │    │   Database Record    │
│                      │    │                      │
│  ENTRY: Blink 2x ✨✨│    │  • Card ID           │
│  EXIT:  Blink 3x ✨✨✨│    │  • Action            │
│                      │    │  • Timestamp         │
│  (GPIO 17)           │    │  • User Name         │
└──────────────────────┘    └──────────────────────┘
```

---

## 🎯 Best Practices

1. **Always run the continuous listener** for production use
2. **Use the CLI** only for registration and viewing history
3. **Monitor logs** regularly to catch any issues
4. **Keep the API** available for remote management
5. **Backup your database** regularly
6. **Test LED and reader** after any hardware changes

---

## 📝 Notes

- The system automatically determines ENTRY vs EXIT based on the last action
- First scan for any user is always ENTRY
- Cards must be registered before they can be used
- The listener service auto-restarts if it crashes (configured in docker-compose)
- LED feedback is optional - system works without it

---

## 🆘 Support

For issues or questions:
1. Check the logs: `docker logs -f loop_shift_listener`
2. Review this guide
3. Check hardware connections
4. Verify database connectivity

