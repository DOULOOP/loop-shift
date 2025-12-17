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

### 1. Run the CLI (On Device)
To use the CLI inside the running container:
```bash
docker exec -it loop_shift_app python cli.py
```
-   **Scan Card**: Logs Entry/Exit.
-   **Add Card**: Scans a new card and asks for a name.

### 2. API Access
The API is available at `http://<raspberry-pi-ip>:8000`.
-   **Docs**: `/docs`

## Configuration
-   **Database**: Set via `DATABASE_URL` in `docker-compose.yml`.
-   **I2C Device**: Mapped automatically as `/dev/i2c-1`.
