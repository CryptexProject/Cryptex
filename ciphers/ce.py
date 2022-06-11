#!/usr/bin/python

from PIL import Image
import numpy as np

# created by : marvhus

# help menu for cipheringing process
help_menu = """
+------------------------------------------------------+
| [✓] ARGUMENTS Color Encryption                       |
| [✓] ARG 2. Additional Aruments                       |
|         [-t <plaintext>] --------- Input Text        |
|         [-f <file path>] --------- File Path         |
+------------------------------------------------------+
| [✓] Example:                                         |
|  cryptex ce -e -t 'Hello, World!' -f image.png       |
|  cryptex ce -d -f image.png                          |
+------------------------------------------------------+
"""

# Generate the image
def gen_image(output, pixels):
    # Convert the pixels into an array using numpy
    array = np.array(pixels, dtype=np.uint8)

    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array)
    new_image.save(output)

# Read the image data
def read_image(input_file):
    pixels = []
    img = Image.open(input_file)
    pix = img.load()
    width, height = img.size
    for i in range(height): # Vertical
        row = []
        for j in range(width): # Horizontal
            row.append(pix[j, i])
        pixels.append(row)
    return pixels

# decode function [!] Each Cipher Must Have This <---------- [!]
def encode(args):
    # Getting text from all passed in args
    # All other args can be grabbed the same way
    # Example key = input.key | range = input.range
    text = args.text
    image_path = args.file

    if not image_path:
        return ['You must suply file path for cryptext to make an image (-f)', False]

    if not text:
        return ['You must suply an input text for this to work', False]

    output = f'Encoding | {text}'

    pixels = []
    # Loop over the input text in groups of 3
    for i in range(0, len(text), 3):
        # The group of 3 chars
        chars = text[i:i+3]
        # If there are not enough chars to make only groups of 3, then ths will say how many extra we will need (2, or 3)
        extra = 3 - len(chars)
        # Empty pixel array
        pixel = []

        # Get the ASCII values of the chars and add them to the pixel array
        for _, char in enumerate(chars):
            pixel.append(ord(char))

        # Add the extra value
        for i in range(extra):
            pixel.append(0)

        # Convert the pixel array to an array with a tupel inside
        pixel = [(pixel[0], pixel[1], pixel[2])]
        pixels.append(pixel)

    gen_image(image_path, pixels)

    output += f"\nImage saved at | {image_path}"

    return [output, True]

# decode function [!] Each Cipher Must Have This <---------- [!]
def decode(args):
    # Getting text from all passed in args
    # All other args can be grabbed the same way
    # Example key = input.key | range = input.range
    image_path = args.file

    if not image_path:
        return ['You must suply an image path for this to work (-f)', False]

    output = f'Decoding image | {image_path}'

    # Get the pixel data
    pixels = read_image(image_path)

    # Make empty string for the decoded text to be in
    decrypted = ""
    for _, height in enumerate(pixels): # Vertical
        for _, width in enumerate(height): # Horizontal
            for _, val in enumerate(width): # Pixel
                # Convert the ASCII value to char and add it to the decrypted variable
                decrypted += chr(val)

    output += f'\nText | {decrypted}'

    return [output,True]

# brute function [!] Optional Per Cipher <----------------- [!]
def brute(args):
    # Getting text from all passed in args
    # All other args can be grabbed the same way
    # Example key = input.key | range = input.range
    text = args.text

    if text:
        # Run Decode
        output = f'Bruteforcing | {text}'

        # Output content as string for main.py to print
        # Pass True if Success Message
        return [output,True]
    else:
        # Pass False if Fail Message
        # Return Nothing to have no output
        return ['Custom Fail Message', False]
