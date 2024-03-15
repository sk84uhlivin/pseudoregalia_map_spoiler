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


def decide_color(text):
    if "chair" in text:
        out_color = yellow

    elif "goatling" in text:
        out_color = teal

    elif "note" in text:
        out_color = green

    else:
        out_color = red

    return out_color


def draw_item(coordinate, item, color_rgb):
    # Call draw Method to add 2D graphics in an image
    draw = ImageDraw.Draw(img)

    # Custom font style and font size
    myFont = ImageFont.truetype(font=resource_path('KGPrimaryPenmanship2.ttf'), size=55)

    # Add Text to an image
    draw.text(xy=coordinate, text=item, font=myFont, fill=color_rgb, anchor="mm")


def draw_legend():
    # Make legend.
    draw = ImageDraw.Draw(img)

    draw.rectangle((243, 3522, 267, 3546), fill=red)
    draw.rectangle((243, 3629, 267, 3653), fill=teal)
    draw.rectangle((243, 3736, 267, 3760), fill=yellow)
    draw.rectangle((243, 3843, 267, 3867), fill=green)

    # Custom font style and font size
    myFont = ImageFont.truetype(font=resource_path('KGPrimaryPenmanship2.ttf'), size=65)

    # Add text to map.
    draw.text(xy=(350, 3515), text="Items", font=myFont, fill=red, anchor="lt", stroke_width=1,
              stroke_fill=(0, 0, 0))
    draw.text(xy=(350, 3622), text="Goatlings", font=myFont, fill=teal, anchor="lt", stroke_width=1,
              stroke_fill=(0, 0, 0))
    draw.text(xy=(350, 3729), text="Chairs", font=myFont, fill=yellow, anchor="lt", stroke_width=1,
              stroke_fill=(0, 0, 0))
    draw.text(xy=(350, 3836), text="Notes", font=myFont, fill=green, anchor="lt", stroke_width=1,
              stroke_fill=(0, 0, 0))


# Initialize two empty lists to store words and locations
words = []
locations = []
coordinates = map_coordinates.locations
big_twilight_locs = ["20", "safe", "show"]
red = (204, 102, 119)
teal = (136, 204, 238)
green = (68, 170, 153)
yellow = (221, 204, 119)

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

# Open the spoiler log for reading.
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

# Check what settings are enabled.
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

# Draw lines depending on what settings are on.
if isGoatlings or isChairs:
    draw = ImageDraw.Draw(img)
    draw.line(xy=((2479, 2085), (2620, 2226)), fill=(255, 255, 255, 50), width=2)

if isGoatlings:
    draw = ImageDraw.Draw(img)
    draw.line(xy=((3586, 2264), (3686, 2364)), fill=(255, 255, 255, 50), width=2)

# Match the location to the coordinate.
line_number = 0
for w, l in zip(words, locations):
    line_number += 1
    color = red
    # Look up the location in the dictionary and retrieve its value
    if "Twilight" in l and any(item in l for item in big_twilight_locs):
        value = TwilightGoatlingsCoords[0]
        del TwilightGoatlingsCoords[0]

        color = decide_color(l)

        draw_item(value, w, color)

    elif "lick" in l:
        value = LickCoords[0]
        del LickCoords[0]

        color = decide_color(l)

        draw_item(value, w, color)

    elif "around the table" in l:
        value = TwilightTableCoords[0]
        del TwilightTableCoords[0]

        color = decide_color(l)

        draw_item(value, w, color)

    elif l in coordinates:
        value = coordinates[l]

        if isSplitGreaves and l == "where sun greaves normally is in Listless Library":
            value = SplitGreavesCoords[0]
            del SplitGreavesCoords[0]

        if isSplitCling and l == "where cling gem normally is in Tower Ruins":
            value = SplitClingCoords[0]
            del SplitClingCoords[0]

        color = decide_color(l)

        draw_item(value, w, color)

    else:
        print(f"({line_number}) '{w}' was not found in the dictionary.")

draw_legend()

# Save the edited image.
print("Saving map...")
img.save("spoiler_map.png")
print("Map saved, program will exit in 3 seconds.")
time.sleep(3)
