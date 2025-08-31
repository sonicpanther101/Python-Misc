import pynput
import keyboard
import pyautogui
import pytesseract
from PIL import Image, ImageOps
import time
import winsound
import numpy as np
import re
from decimal import Decimal

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

def text_to_int(text: str) -> int:
    """
    Convert strings like "50 billion" or "40.965 trillion" into integers.
    """
    # Extract number and scale word
    match = re.match(r"([\d,.]+)\s*(\w+)", text.lower().strip())
    if not match:
        raise ValueError(f"Invalid input: {text}")
    
    number_str, scale_word = match.groups()
    number = Decimal(number_str.replace(",", ""))  # handles decimals safely
    
    if scale_word not in SCALE_MAP:
        raise ValueError(f"Unknown scale: {scale_word}, raw text: {text}")
    
    return int(number * SCALE_MAP[scale_word])

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
    threshold = 170
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

    upgrade_prices = [text_to_int(item.replace(',', '.')) for item in availible]

    return upgrade_prices

def click_upgrade(upgrade):
    mouse_controller.position = UPGRADE_COORDS[upgrade]
    mouse_controller.click(pynput.mouse.Button.left, 1)
    winsound.Beep(500, 100)
    mouse_controller.position = NEUTRAL_COORDS

def get_powerup_price(): 
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a file
    screenshot.save('screenshot.png')

    # Crop the screenshot to a specific area
    crop_image('screenshot.png', 'cropped_screenshot.png', CROP_FOR_POWERUPS)

    # Open the image
    img = Image.open('cropped_screenshot.png')

    r, g, b = img.split()

    # Convert the images to numpy arrays
    r_array = np.array(r)
    g_array = np.array(g)
    b_array = np.array(b)

    # Take only the green channel and subtract the average of the red and blue channels
    image_green = g_array - 0.6*b_array

    # Convert the result back to a PIL Image
    image_green = Image.fromarray(image_green.astype(np.uint8))

    image_green.save('green_channel.png')

    # Apply simple thresholding
    threshold = 150
    img_thresholded = image_green.convert('L')  # Convert to grayscale
    img_thresholded = img_thresholded.point(lambda x: 0 if x < threshold else 255)

    # Save the thresholded image
    img_thresholded.save('thresholded_image.png')

    # Use Tesseract OCR to extract text from the screenshot
    text = pytesseract.image_to_string(Image.open('thresholded_image.png'))

    return text_to_int(text) if text else 0

def check_powerups():

    mouse_controller.position = POWERUP_COORDS[0]

    time.sleep(0.1)

    price = get_powerup_price()

    mouse_controller.position = NEUTRAL_COORDS

    time.sleep(0.1)

    return price

def click_powerup():
    print(f"Upgrading powerup")
    mouse_controller.position = POWERUP_COORDS[0]
    mouse_controller.click(pynput.mouse.Button.left, 1)
    winsound.Beep(500, 100)
    mouse_controller.position = NEUTRAL_COORDS

if __name__ == "__main__":

    COOKIE_COORDS = (374, 565)
    NEUTRAL_COORDS = (411, 1119)
    CROP_FOR_UPGRADES = (2310, 190, 2547, 1388)
    CROP_FOR_UPGRADE_PRICES = (2329, 190, 2450, 1388) 
    CROP_FOR_POWERUPS = (2125, 60, 2225, 80)
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
    # Scale multipliers
    SCALE_MAP = {
        "thousand": 10**3,
        "million": 10**6,
        "billion": 10**9,
        "trillion": 10**12,
        "quadrillion": 10**15,
    }

    UPGRADE_COORDS = {UPGRADES[i]: (2350, 222 + 64*i) for i in range(len(UPGRADES))}
    POWERUP_COORDS = [(2273+60*i,100) for i in range(4)]

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

            powerup_price = check_powerups()

            if (len(availible_upgrades) == 0 or len(upgrade_prices) == 0) and powerup_price == 0:
                print("No upgrades availible")
                continue

            print(f"Availible upgrades: {availible_upgrades}") 
            print(f"Upgrade prices: {upgrade_prices}")
            if powerup_price != 0:
                print(f"Powerup price: {powerup_price}")

            cheapest_upgrade = min(upgrade_prices)

            if powerup_price < cheapest_upgrade and powerup_price != 0:
                click_powerup()
                continue 

            cheapest_upgrade_index = upgrade_prices.index(min(upgrade_prices))

            print(f"Upgrading: {availible_upgrades[cheapest_upgrade_index]}")
            click_upgrade(availible_upgrades[cheapest_upgrade_index])