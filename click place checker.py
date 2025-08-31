from pynput import mouse

clicked = 0

def on_click(x, y, button, pressed):
    global clicked
    if pressed and button == mouse.Button.left:
        clicked += 1
        print(f"Number of clicks: {clicked}")
        print(f"Mouse position: ({x}, {y})")

listener = mouse.Listener(on_click=on_click)
listener.start()

if __name__ == "__main__":
    while True:
        if clicked == 3:
            listener.stop()
            break