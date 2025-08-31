import pynput
import keyboard
import pyautogui
import pytesseract
from PIL import Image, ImageOps
import time
import winsound
import numpy as np

def crop_image(input_image, output_image, COORDS):
    """
    Crop a specific area of an image and save it to a new PNG file.

    Args:
        input_image (str): Path to the input image file.
        output_image (str): Path to the output image file.
        x (int): X-coordinate of the top-left corner of the crop area.
        y (int): Y-coordinate of the top-left corner of the crop area.
        width (int): Width of the crop area.
        height (int): Height of the crop area.
    """
    img = Image.open(input_image)
    cropped_img = img.crop(COORDS)
    cropped_img.save(output_image, 'PNG')

def click_cookie():
    mouse_controller.position = COOKIE_COORDS
    mouse_controller.click(pynput.mouse.Button.left, 1)

def get_availible_upgrades(): 
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a file
    screenshot.save('OCR/availible_upgrades_screenshot.png')

    # Crop the screenshot to a specific area
    crop_image('OCR/availible_upgrades_screenshot.png', 'OCR/availible_upgrades_cropped_screenshot.png', CROP_FOR_UPGRADES)

    # Open the image
    img = Image.open('OCR/availible_upgrades_cropped_screenshot.png')

    # Apply simple thresholding
    threshold = 210
    img_thresholded = img.convert('L')  # Convert to grayscale
    img_thresholded = img_thresholded.point(lambda x: 0 if x < threshold else 255)

    # Save the thresholded image
    img_thresholded.save('OCR/availible_upgrades_thresholded_image.png')

    # Use Tesseract OCR to extract text from the screenshot
    text = pytesseract.image_to_string(Image.open('OCR/availible_upgrades_thresholded_image.png'))

    availible = text.split('\n')

    for item in availible:
        if item == '':
            availible.remove(item)

    return availible

def get_availible_upgrade_prices(): 
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a file
    screenshot.save('OCR/upgrade_prices_screenshot.png')

    # Crop the screenshot to a specific area
    crop_image('OCR/upgrade_prices_screenshot.png', 'OCR/upgrade_prices_cropped_screenshot.png', CROP_FOR_UPGRADE_PRICES)

    # Open the image
    img = Image.open('OCR/upgrade_prices_cropped_screenshot.png')

    r, g, b = img.split()

    # Convert the images to numpy arrays
    g_array = np.array(g)
    b_array = np.array(b)

    # Take only the green channel and subtract the average of the red and blue channels
    image_green = g_array - 0.6*b_array

    # Convert the result back to a PIL Image
    image_green = Image.fromarray(image_green.astype(np.uint8))

    mouse_controller = pynput.mouse.Controller()
    image_green.save('OCR/upgrade_prices_green_channel.png')

    # Apply simple thresholding
    threshold = 150
    img_thresholded = image_green.convert('L')  # Convert to grayscale
    img_thresholded = img_thresholded.point(lambda x: 0 if x < threshold else 255)

    # Save the thresholded image
    img_thresholded.save('OCR/upgrade_prices_thresholded_image.png')

    # Use Tesseract OCR to extract text from the screenshot
    text = pytesseract.image_to_string(Image.open('OCR/upgrade_prices_thresholded_image.png'))

    availible = text.split('\n')

    for item in availible:
        if item == '':
            availible.remove(item)

    availible = [''.join(filter(lambda x: x.isdigit() or x == '.', item)) for item in availible]

    try:
        upgrade_prices = [float(item) for item in availible]
    except:
        print("error: ", availible)
        upgrade_prices = []

    return upgrade_prices

def click_upgrade(upgrade):
    mouse_controller.position = UPGRADE_COORDS[upgrade]
    mouse_controller.click(pynput.mouse.Button.left, 1)
    winsound.Beep(2500, 100)
    mouse_controller.position = NEUTRAL_COORDS

if __name__ == "__main__":

    COOKIE_COORDS = (374, 565)
    NEUTRAL_COORDS = (411, 1119)
    CROP_FOR_UPGRADES = (2310, 190, 2547, 1388)
    CROP_FOR_UPGRADE_PRICES = (2329, 190, 2375, 1388) 
    UPGRADES = [
        'Cursor',
        'Grandma',
        'Farm',
        'Mine',
        'Factory',
        'Bank',
        'Temple',
        'Wizard tower',
        'Shipment',
        'Alchemy lab',
        'Portal',
        'Time machine',
        'Antimatter condenser'
    ]

    UPGRADE_COORDS = {UPGRADES[i]: (2350, 222 + 64*i) for i in range(len(UPGRADES))}

    UPGRADE_PERIOD = 10

    Time = time.time()

    mouse_controller = pynput.mouse.Controller()
    mouse_controller.position = NEUTRAL_COORDS

    while not keyboard.is_pressed("esc"):
        time.sleep(0.001)

        if keyboard.is_pressed("space"):
            click_cookie()

        if time.time() - Time >= UPGRADE_PERIOD:
            Time = time.time()

            upgrade_prices = get_availible_upgrade_prices()
            availible_upgrades = get_availible_upgrades()

            if len(availible_upgrades) == 0 or len(upgrade_prices) == 0:
                print("No upgrades availible")
                continue

            print(f"Availible upgrades: {availible_upgrades}") 
            print(f"Upgrade prices: {upgrade_prices}")

            cheapest_upgrade_index = upgrade_prices.index(min(upgrade_prices))

            print(f"Upgrading: {availible_upgrades[cheapest_upgrade_index]}")
            click_upgrade(availible_upgrades[cheapest_upgrade_index])