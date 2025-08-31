import pyautogui
import pytesseract
import pynput
from PIL import Image, ImageOps
import time
import winsound
import numpy as np
import re
from decimal import Decimal

# Scale multipliers
SCALE_MAP = {
    "thousand": 10**3,
    "million": 10**6,
    "billion": 10**9,
    "trillion": 10**12,
    "quadrillion": 10**15,
}

CROP_FOR_COOKIES = (225, 160, 544, 223)
CROP_FOR_UPGRADES = (2329, 190, 2375, 1388)
CROP_FOR_POWERUPS = (2125, 60, 2225, 80)

powerup_coords = [(2273+60*i,100) for i in range(4)]

mouse_controller = pynput.mouse.Controller()

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
        raise ValueError(f"Unknown scale: {scale_word}")
    
    return int(number * SCALE_MAP[scale_word])

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

def capture_screen_text(): 

    # # Take a screenshot
    # screenshot = pyautogui.screenshot()

    # # Save the screenshot to a file
    # screenshot.save('screenshot.png')

    # # Crop the screenshot to a specific area
    # crop_image('screenshot.png', 'cropped_screenshot.png', CROP_FOR_POWERUPS)

    # Open the image
    img = Image.open('cropped_screenshot.png')

    print(img.mode)

    r, g, b, a = img.split()

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

print(capture_screen_text())

winsound.Beep(500, 100)