"""
Continuous Card Listener Service
Automatically scans and logs cards 24/7 without manual intervention.
"""
import sys
import time
import signal
from database import init_db, add_user, get_user, get_last_action, log_access
from rfid_reader import RFIDReader
from led_controller import LEDController

# Set encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize reader and LED
reader = RFIDReader()
led = LEDController(pin=17)

# Flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print("\n\nShutting down card listener...")
    running = False

def handle_card_scan(card_id):
    """Process a card scan"""
    user = get_user(card_id)
    
    if not user:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ UNKNOWN CARD: {card_id}")
        print("   Please register this card first.")
        return
    
    # Determine Entry or Exit
    last_action = get_last_action(card_id)
    
    if last_action == 'ENTRY':
        new_action = 'EXIT'
    else:
        new_action = 'ENTRY'
    
    # Log the access
    log_access(card_id, new_action)
    
    # Control LED based on action
    if new_action == 'ENTRY':
        led.blink(times=2)  # Blink 2 times for entry
        emoji = "🔓"
    else:  # EXIT
        led.blink(times=3)  # Blink 3 times for exit
        emoji = "🔒"
    
    # Print confirmation
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {emoji} {new_action}: {user['full_name']} ({card_id})")

def main():
    """Main continuous listening loop"""
    global running
    
    # Setup signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize database
    init_db()
    
    # Pre-seed the requested user if not exists
    if not get_user("00x-abc-bcd"):
        add_user("00x-abc-bcd", "Furkan Ulutaş")
        print("Pre-seeded user: Furkan Ulutaş")
    
    print("=" * 60)
    print("  CARD ACCESS SYSTEM - CONTINUOUS LISTENER")
    print("=" * 60)
    print("  Status: 🟢 ACTIVE")
    print("  Listening for cards...")
    print("  Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Continuous scanning loop
    while running:
        try:
            # Wait for a card (non-blocking with timeout)
            card_id = reader.read_card(timeout=1)
            
            if card_id:
                handle_card_scan(card_id)
                print("  Waiting for next card...")
                
        except Exception as e:
            print(f"Error during scan: {e}")
            time.sleep(1)  # Brief pause on error
    
    # Cleanup
    print("\nCleaning up...")
    led.cleanup()
    print("Card listener stopped.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        led.cleanup()
        sys.exit(1)

