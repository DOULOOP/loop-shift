import time
import board
import busio
from adafruit_pn532.i2c import PN532_I2C

class RFIDReader:
    def __init__(self):
        self.pn532 = None
        try:
            # Initialize I2C connection
            i2c = busio.I2C(board.SCL, board.SDA)
            # Initialize PN532
            self.pn532 = PN532_I2C(i2c, debug=False)
            self.pn532.SAM_configuration()
            print("PN532 NFC/RFID reader initialized found.")
        except Exception as e:
            print(f"Warning: Could not initialize PN532 reader: {e}")
            print("Running in simulation mode (keyboard input).")

    def read_card(self, timeout=None):
        """
        Waits for a card to be present and returns its ID.
        If timeout is set, returns None if no card found within time.
        """
        if not self.pn532:
            # Fallback to keyboard input for testing without hardware
            try:
                print("(Simulation) Enter Card ID: ", end='', flush=True)
                # Non-blocking input is hard in pure Python console without libraries, 
                # so we just block for input in simulation mode
                return input().strip()
            except EOFError:
                return None

        print("Waiting for RFID/NFC card...")
        start_time = time.time()
        
        while True:
            # Check if timeout occurred
            if timeout and (time.time() - start_time > timeout):
                return None
                
            # Try to read a card
            uid = self.pn532.read_passive_target(timeout=0.5)
            
            if uid is not None:
                # Convert byte array to hex string (e.g., "0x00 0x01" -> "0001")
                # Format: 0x12 0x34 -> 12-34-56-78
                card_id = '-'.join([hex(i)[2:].zfill(2) for i in uid])
                print(f"Card detected: {card_id}")
                
                # Wait for card removal to avoid repeated reads
                while self.pn532.read_passive_target(timeout=0.5) is not None:
                    time.sleep(0.1)
                    
                return card_id
            
            time.sleep(0.1)



