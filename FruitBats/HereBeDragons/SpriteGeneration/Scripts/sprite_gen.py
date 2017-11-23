import random
from sprite import Sprite
from get_images import GetImages

"""
This module is a utility module to be used by designers/artists to quickly generate random sprites from possible components. Running this module will create and save one sprite.
The path to your assets folder, and the type of image files being used can be set below. See get_images.py for the how the different components are loaded.
"""

# Specify file type to load and the image directories
sprite_file_type = ".png"
path_to_assets = "../Assets"

# Get the component images
images = GetImages(path_to_assets, sprite_file_type)

# Create new sprite with random component, draw it and save the image to file
# Arguments: Sprite Size, background colour, base image, legs image, body image, hair image, feetImage, weaponImage (currently not implemented)

new_sprite = Sprite((16, 16), (0, 0, 0, 0), random.choice(images.base), random.choice(images.legs), random.choice(images.body), random.choice(images.hair), random.choice(images.feet), 0)
new_sprite.draw()
new_sprite.save_with_id(path_to_assets + "\Sprites\CustomSprites", "png")
