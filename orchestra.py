import time
from orchestra_controller import Orchestra
from gpiozero import Button

# start_stop_button = Button(5, pull_up=False, bounce_time=0.3)
start_stop_button = Button(5, bounce_time=0.1)

orchestra = Orchestra()
orchestra.start()

def handle_button():
    print("Button pressed")
    orchestra.toggle()
    print(f"Orchestra is running: {orchestra.is_running()}")

start_stop_button.when_pressed = handle_button

while True:
    time.sleep(0.1)
    orchestra.handle_buttons() # TODO: should this be done internally by the Orchestra class?

