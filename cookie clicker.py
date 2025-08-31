import pynput
import keyboard

COOKIE_COORDS = (374, 565)

def click_cookie():
    mouse_controller = pynput.mouse.Controller()
    mouse_controller.position = COOKIE_COORDS
    mouse_controller.click(pynput.mouse.Button.left, 1)

if __name__ == "__main__":
    while not keyboard.is_pressed("esc"):

        if keyboard.is_pressed("space"):
            click_cookie()