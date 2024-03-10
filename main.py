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


def draw_item(coordinate, item, color_rgb):
    # Call draw Method to add 2D graphics in an image
    draw = ImageDraw.Draw(img)

    # Custom font style and font size
    myFont = ImageFont.truetype(font=resource_path('alittlepot.ttf'), size=45)

    # Add Text to an image
    draw.text(xy=coordinate, text=item, font=myFont, fill=color_rgb, anchor="mm")


# Initialize two empty lists to store words and locations
words = []
locations = []
coordinates = map_coordinates.locations
big_twilight_locs = ["20", "safe", "show"]
red = (255, 0, 0)
teal = (137, 207, 240)
green = (77, 204, 32)
yellow = (255, 255, 102)

# Open the map
img = Image.open(resource_path('map.png'))

# Set variables for split settings
isSplitGreaves = False
isSplitCling = False
isNotes = False
isGoatlings = False
isChairs = False

# Store list of split coordinates to memory
splitCoords = map_coordinates.tri_coordinates
SplitGreavesCoords = splitCoords["splitgreaves"]
SplitClingCoords = splitCoords["splitcling"]
TwilightGoatlingsCoords = splitCoords["twilightgoatlings"]
LickCoords = splitCoords["licklocations"]
TwilightTableCoords = splitCoords["twilighttable"]

# Open the text document for reading
try:
    with open('spoiler.log', 'r') as file:
        print("Parsing text from spoiler.log...")
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
    print("spoiler.log not found. This program needs to be in the same directory as the spoiler log from the "
          "randomizer.")
    input("Press any key to exit...")
    exit()


if "SunGreaves" not in words:
    isSplitGreaves = True
print(f"Split Greaves: {isSplitGreaves}")
if "ClingGem(2)" in words:
    isSplitCling = True
print(f"Split Cling: {isSplitCling}")
if "Note" in words:
    isNotes = True
print(f"Notes: {isNotes}")
if "Goatling" in words:
    isGoatlings = True
print(f"Goatlings: {isGoatlings}")
if "Chair" in words:
    isChairs = True
print(f"Chairs: {isChairs}")

line_number = 0
for w, l in zip(words, locations):
    line_number += 1
    color = red
    # Look up the location in the dictionary and retrieve its value
    if "Twilight" in l and any(item in l for item in big_twilight_locs):
        color = teal
        value = TwilightGoatlingsCoords[0]
        del TwilightGoatlingsCoords[0]

        draw_item(value, w, color)

    elif "lick" in l:
        value = LickCoords[0]
        del LickCoords[0]

        if "goatling" in l:
            color = teal

        if "chair" in l:
            color = yellow

        draw_item(value, w, color)

    elif "around the table" in l:
        color = yellow
        value = TwilightTableCoords[0]
        del TwilightTableCoords[0]

        draw_item(value, w, color)


    elif l in coordinates:
        value = coordinates[l]

        if isSplitGreaves and l == "where sun greaves normally is in Listless Library":
            value = SplitGreavesCoords[0]
            del SplitGreavesCoords[0]

        if isSplitCling and l == "where cling gem normally is in Tower Ruins":
            value = SplitClingCoords[0]
            del SplitClingCoords[0]

        if "goatling" in l:
            color = teal

        if "note" in l:
            color = green

        if "chair" in l:
            color = yellow

        draw_item(value, w, color)

    else:
        print(f"({line_number}) '{w}' was not found in the dictionary.")

if isGoatlings or isChairs:
    draw = ImageDraw.Draw(img)
    draw.line(xy=((2479, 2095), (2554, 2170)), fill=(255, 255, 255, 50), width=2)

if isGoatlings:
    draw = ImageDraw.Draw(img)
    draw.line(xy=((3586, 2264), (3686, 2364)), fill=(255, 255, 255, 50), width=2)

print("Saving map...")
# Save the edited image
img.save("spoiler_map.png")
print("Map saved, program will exit in 3 seconds.")
time.sleep(3)
