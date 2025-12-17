import time
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except (ImportError, RuntimeError):
    GPIO_AVAILABLE = False
    print("Warning: RPi.GPIO not available. LED control disabled.")


class LEDController:
    def __init__(self, pin=17):
        """
        Initialize LED controller on specified GPIO pin.
        Default is GPIO 17 (BCM numbering).
        """
        self.pin = pin
        self.enabled = False
        
        if GPIO_AVAILABLE:
            try:
                # Use BCM pin numbering
                GPIO.setmode(GPIO.BCM)
                # Suppress warnings if pin already in use
                GPIO.setwarnings(False)
                # Setup pin as output
                GPIO.setup(self.pin, GPIO.OUT)
                # Ensure LED is off initially
                GPIO.output(self.pin, GPIO.LOW)
                self.enabled = True
                print(f"LED controller initialized on GPIO pin {self.pin}")
            except Exception as e:
                print(f"Warning: Could not initialize LED on GPIO {self.pin}: {e}")
                self.enabled = False
        else:
            print("LED controller running in simulation mode.")
    
    def blink(self, times=1, duration=0.2, interval=0.2):
        """
        Blink the LED a specified number of times.
        
        Args:
            times: Number of times to blink
            duration: How long the LED stays on (seconds)
            interval: Time between blinks (seconds)
        """
        if not self.enabled:
            print(f"[LED SIMULATION] Blinking {times} time(s)")
            return
        
        try:
            for i in range(times):
                GPIO.output(self.pin, GPIO.HIGH)  # LED on
                time.sleep(duration)
                GPIO.output(self.pin, GPIO.LOW)   # LED off
                
                # Don't wait after the last blink
                if i < times - 1:
                    time.sleep(interval)
        except Exception as e:
            print(f"Error blinking LED: {e}")
    
    def on(self):
        """Turn LED on continuously."""
        if self.enabled:
            GPIO.output(self.pin, GPIO.HIGH)
    
    def off(self):
        """Turn LED off."""
        if self.enabled:
            GPIO.output(self.pin, GPIO.LOW)
    
    def cleanup(self):
        """Clean up GPIO resources."""
        if self.enabled:
            try:
                GPIO.output(self.pin, GPIO.LOW)
                GPIO.cleanup(self.pin)
                print("LED controller cleaned up")
            except Exception as e:
                print(f"Error during LED cleanup: {e}")

