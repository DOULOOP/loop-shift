import sys
import time
import os

# Import directly from database.py
from database import init_db, add_user, get_user, get_last_action, log_access, get_logs
# Import the RFID reader wrapper
from rfid_reader import RFIDReader
# Import LED controller
from led_controller import LEDController

# Set encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize reader and LED
reader = RFIDReader()
led = LEDController(pin=17)

def print_separator():
    print("-" * 50)

def handle_scan(card_id):
    user = get_user(card_id)
    
    if not user:
        print_separator()
        print(f"Card ID '{card_id}' not recognized.")
        print("Please use 'Add New Card' option to register.")
        return

    # Determine Entry or Exit
    last_action = get_last_action(card_id)
    
    if last_action == 'ENTRY':
        new_action = 'EXIT'
    else:
        new_action = 'ENTRY' # Default to ENTRY if no logs or last was EXIT
        
    log_access(card_id, new_action)
    
    # Control LED based on action
    if new_action == 'ENTRY':
        led.blink(times=2)  # Blink 2 times for entry
    else:  # EXIT
        led.blink(times=3)  # Blink 3 times for exit
    
    print_separator()
    print(f"SUCCESS: {new_action} logged for {user['full_name']} ({card_id})")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

def show_history():
    print_separator()
    print("ACCESS HISTORY")
    print_separator()
    logs = get_logs()
    
    if not logs:
        print("No records found.")
    else:
        print(f"{'TIME':<20} | {'ACTION':<10} | {'NAME'}")
        print("-" * 50)
        for log in logs:
            print(f"{log['scan_time']:<20} | {log['action']:<10} | {log['full_name']}")
    input("\nPress Enter to return to menu...")

def add_new_card_flow():
    print_separator()
    print("ADD NEW CARD")
    print("Please scan the new card now...")
    
    # Use the hardware reader
    card_id = reader.read_card()
    
    if not card_id:
        print("Error: No card ID received.")
        return

    # Check if exists
    existing_user = get_user(card_id)
    if existing_user:
        print(f"Error: Card '{card_id}' is already registered to {existing_user['full_name']}.")
        return

    print(f"Card ID captured: {card_id}")
    full_name = input("Enter Full Name for this card: ").strip()
    
    if not full_name:
        print("Registration cancelled: Name is required.")
        return
        
    if add_user(card_id, full_name):
        print(f"Success! Card registered to {full_name}.")
    else:
        print("Error: Failed to register card.")
    
    input("\nPress Enter to return...")

def main():
    init_db()
    
    # Pre-seed the requested user if not exists
    if not get_user("00x-abc-bcd"):
        add_user("00x-abc-bcd", "Furkan Ulutaş")

    while True:
        print_separator()
        print("CARD ACCESS SYSTEM")
        print_separator()
        print("1. Scan Card (Entry/Exit)")
        print("2. Add New Card")
        print("3. View Access History")
        print("4. Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            print("\nWaiting for card scan (Entry/Exit)...")
            # Use hardware reader
            card_id = reader.read_card()
            if card_id:
                handle_scan(card_id)
        elif choice == '2':
            add_new_card_flow()
        elif choice == '3':
            show_history()
        elif choice == '4':
            print("System shutting down...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        led.cleanup()
        sys.exit(0)

