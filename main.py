from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import map_coordinates
import os
import time
import sys


# Helper function for pyinstaller.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Initialize two empty lists to store words and locations
words = []
locations = []
coordinates = map_coordinates.locations

# Open the map
img = Image.open(resource_path('map.png'))

# Open the text document for reading
try:
    with open('spoiler.log', 'r') as file:
        print("Generating text from spoiler_log.txt...")
        # Iterate through each line in the document
        for line in file:
            # Split the line at the colon
            parts = line.strip().split(':')
            if len(parts) == 2:
                word, location = parts
                # Add the word and location to their respective lists
                words.append(word.strip())
                locations.append(location.strip())
except FileNotFoundError:
    print("spoiler_log.txt not found. This program needs to be in the same directory as the spoiler log from the "
          "randomizer.")
    input("Press any key to exit...")
    exit()

line_number = 0
for w, l in zip(words, locations):
    line_number += 1
    # Look up the location in the dictionary and retrieve its value
    if l in coordinates:
        value = coordinates[l]

        # Call draw Method to add 2D graphics in an image
        draw = ImageDraw.Draw(img)

        # Custom font style and font size
        myFont = ImageFont.truetype(font=resource_path('alittlepot.ttf'), size=85)

        # Add Text to an image
        draw.text(xy=value, text=w, font=myFont, fill=(255, 0, 0), anchor="mm")

    else:
        print(f"({line_number}) '{w}' was not found in the dictionary.")
print("Saving map...")
# Save the edited image
img.save("spoiler_map.png")
print("Map saved, program will exit in 3 seconds.")
time.sleep(3)
