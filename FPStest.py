from time import sleep
import threading
class LEDtest ():
    def __init__(self, color, state):
        self._color = color
        self._state = state

    def LEDwork(self):
        while True:
            while not self._state == 0:
                while self._state == 1:
                    print(self._color)
                    sleep(1)
                    print('off')
                    sleep(1)
                while self._state == 2:
                    print(self._color)
                    sleep(1)

if __name__ == "__main__":
    blue = LEDtest('blue', 2)
    colorful = LEDtest('red', 1)
    t = threading.Thread(name='Test1', target=blue.LEDwork)
    s = threading.Thread(name='Test2', target=colorful.LEDwork)
    t.daemon = True
    s.daemon = False
    t.start()
    s.start()
    i = 1
    while True:
        sleep(5)
        if i < 3:
            blue._state = 1
        colorful._color = 'green'
        sleep(5)
        if i < 3:
            blue._state = 2
        colorful._color = 'red'
        i += 1
        if i > 3:
            blue._state = 0