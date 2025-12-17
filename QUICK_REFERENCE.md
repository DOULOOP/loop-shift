# Quick Reference Card

## 🚀 Start Everything
```bash
docker-compose up -d
```

## 👀 Watch Cards Being Scanned
```bash
docker logs -f loop_shift_listener
```

## 📝 Register a New Card
```bash
docker exec -it loop_shift_app python cli.py
# Select option 3
```

## 🔄 Restart Listener
```bash
docker-compose restart card_listener
```

## 🛑 Stop Everything
```bash
docker-compose down
```

## 📊 View History
```bash
# Via CLI
docker exec -it loop_shift_app python cli.py
# Select option 4

# Via API
curl http://localhost:8000/history
```

## 🌐 API Documentation
Open in browser: `http://<raspberry-pi-ip>:8000/docs`

## 💡 LED Behavior
- **2 blinks** = Entry (Clock In)
- **3 blinks** = Exit (Clock Out)

## 🔧 Troubleshooting

### Check if services are running
```bash
docker ps | grep loop_shift
```

### View all logs
```bash
docker-compose logs -f
```

### Test I2C connection
```bash
docker exec -it loop_shift_app i2cdetect -y 1
```

### Test LED manually
```bash
docker exec -it loop_shift_app python -c "from led_controller import LEDController; led = LEDController(17); led.blink(5); led.cleanup()"
```

### Rebuild everything
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📁 Important Files
- `card_listener.py` - Continuous scanner (runs 24/7)
- `cli.py` - Interactive menu
- `main.py` - API server
- `led_controller.py` - LED control
- `docker-compose.yml` - Service configuration

## 🔌 Hardware Pins
- **PN532 SDA** → GPIO 2 (Pin 3)
- **PN532 SCL** → GPIO 3 (Pin 5)
- **LED** → GPIO 17 (Pin 11) + Resistor → GND

## 📞 Quick Commands

| Task | Command |
|------|---------|
| Start all | `docker-compose up -d` |
| Stop all | `docker-compose down` |
| View logs | `docker logs -f loop_shift_listener` |
| Add card | `docker exec -it loop_shift_app python cli.py` |
| Restart | `docker-compose restart` |
| Status | `docker ps` |
| API docs | Browse to `:8000/docs` |

---

**That's it! The system is now continuously listening for cards. 🎉**

