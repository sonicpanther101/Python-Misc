import pyautogui
import pytesseract
from PIL import Image, ImageOps
import time
import winsound
import numpy as np

CROP_FOR_COOKIES = (225, 160, 544, 223)
CROP_FOR_UPGRADES = (2329, 190, 2375, 1388)

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
    # Wait for 5 seconds
    time.sleep(2)

    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a file
    screenshot.save('screenshot.png')

    # Crop the screenshot to a specific area
    # crop_image('screenshot.png', 'cropped_screenshot.png', CROP_FOR_UPGRADES)

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

    availible = text.split('\n')

    for item in availible:
        if item == '':
            availible.remove(item)

    availible = [''.join(filter(lambda x: x.isdigit() or x == '.', item)) for item in availible]

    try:
        upgrade_prices = [int(item) for item in availible]
    except:
        print("error: ", availible)

    return upgrade_prices

print(capture_screen_text())

winsound.Beep(2500, 100)