'''
from PIL import Image

# Open an image file
li = ['bomb','flag','captain','colonel','general','lieutenant','major','marshal','miner','scout','sergeant','spy']
for i in li:
    with Image.open(f'assests/images2/img/{i}.png') as img:
    # Resize the image to 128x128 pixels
        resized_img = img.resize((57, 57))
    
    # Save the resized image
        resized_img.save(f'assests/img/{i}.png')
'''

from PIL import Image, ImageOps

def resize_and_add_border(input_path, output_path, size=(55, 55), border_size=2, border_color="blue"):
    # Open an image file
    with Image.open(input_path) as img:
        # Resize the image to the specified size
        resized_img = img.resize(size)
        
        # Add a border around the image
        bordered_img = ImageOps.expand(resized_img, border=border_size, fill=border_color)
        
        # Save the resulting image
        bordered_img.save(output_path)

# Example usage
li = ['bomb','flag','captain','colonel','general','lieutenant','major','marshal','miner','scout','sergeant','spy']
for i in li:
    resize_and_add_border(f'assests/images2/img/{i}.png', f'assests/img/{i}_blue.png',border_color='blue')
    resize_and_add_border(f'assests/images2/img/{i}.png', f'assests/img/{i}_red.png',border_color='red')

