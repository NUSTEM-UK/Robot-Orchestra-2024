import time
from orchestra_controller import Orchestra

orchestra = Orchestra()
orchestra.start()


while True:
    time.sleep(0.1)
    orchestra.handle_buttons()
