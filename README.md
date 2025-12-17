# Card Access Logging System

A Python application to log entry and exit times based on card IDs using **PostgreSQL** and an **PN532 NFC/RFID Reader**.

## Features
- **Hardware Integration**: Supports PN532 RFID reader via I2C on Raspberry Pi.
- **LED Indicator**: Visual feedback for entry/exit events.
- **Dockerized**: Easy deployment with Docker and Docker Compose.
- **FastAPI Service**: REST API for remote management.
- **CLI Tool**: On-device interface for scanning.

## Hardware Requirements
- **Raspberry Pi** (3, 4, or Zero W)
- **PN532 NFC/RFID Module**
- **LED** (optional, for visual feedback)

### Wiring
- **PN532 Module**: I2C (SDA to Pin 3, SCL to Pin 5, VCC to 3.3V/5V, GND to GND)
- **LED**: Connected to GPIO 17 (Pin 11) with appropriate current-limiting resistor (220-330Ω recommended)
  - LED anode (+) → GPIO 17 (through resistor)
  - LED cathode (-) → GND

### LED Behavior
- **Entry (Clock In)**: LED blinks **2 times**
- **Exit (Clock Out)**: LED blinks **3 times**

## Installation (Docker)

1.  Clone the repository to your Raspberry Pi.
2.  Enable I2C on your Pi (`sudo raspi-config` -> Interface Options -> I2C).
3.  Build and run the container:
    ```bash
    docker-compose up --build -d
    ```

## Usage

### 1. Continuous Card Listener (Recommended)
The system includes a dedicated continuous listener service that automatically scans and logs cards 24/7:

**Run as a service (auto-start with Docker):**
```bash
docker-compose up -d
```
Both the API server and card listener will start automatically. The listener will continuously wait for cards.

**View listener logs:**
```bash
docker logs -f loop_shift_listener
```

**Stop the listener:**
```bash
docker-compose stop card_listener
```

### 2. Interactive CLI (Manual Mode)
To use the CLI with menu options inside the running container:
```bash
docker exec -it loop_shift_app python cli.py
```
Options:
-   **Continuous Scan Mode**: Automatically listens for cards (Ctrl+C to return to menu)
-   **Single Scan**: One-time card scan
-   **Add Card**: Register a new card
-   **View History**: See access logs

### 3. Standalone Listener (Alternative)
Run the continuous listener directly:
```bash
docker exec -it loop_shift_app python card_listener.py
```

### 4. API Access
The API is available at `http://<raspberry-pi-ip>:8000`.
-   **Docs**: `/docs`
-   **Health Check**: `/`

## Configuration
-   **Database**: Set via `DATABASE_URL` in `docker-compose.yml`.
-   **I2C Device**: Mapped automatically as `/dev/i2c-1`.
-   **LED Pin**: Default is GPIO 17, can be changed in `led_controller.py`.

## Quick Start

1. **Deploy everything:**
   ```bash
   docker-compose up -d
   ```

2. **Watch card scans in real-time:**
   ```bash
   docker logs -f loop_shift_listener
   ```

3. **Register a new card (in a separate terminal):**
   ```bash
   docker exec -it loop_shift_app python cli.py
   # Select option 3: "Add New Card"
   ```

That's it! The system will now continuously listen for cards and automatically log entries/exits with LED feedback.

## System Architecture

- **API Service** (`loop_shift_app`): FastAPI server on port 8000
- **Card Listener** (`loop_shift_listener`): Background service that continuously scans cards
- **Database**: PostgreSQL (external)
- **Hardware**: PN532 RFID reader + LED indicator
