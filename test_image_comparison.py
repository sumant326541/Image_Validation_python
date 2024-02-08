import subprocess
import pytest
import time
import pyautogui
from PIL import Image, ImageChops

image1_Path = "Images/IMAGE_1.png"
image2_Path = "Images/IMAGE_2.png"
export_image_path ="ImagesOut/exported_Image.jpg"

@pytest.fixture
def open_paintx():
    appName="Paint X"
    #Open PaintX
    subprocess.run(["open", "-a", appName])
    time.sleep(3)
    convert_image_To_jpg(image1_Path) 
   
    yield
    # Close PaintX 
    subprocess.run(["pkill", "-f", appName])

 # Function convert and export png to jpg 
def convert_image_To_jpg(image_path):  
    image = Image.open(image_path) 
    image = image.convert("RGB")
    # Export the image to JPG format
    image.save(export_image_path, "JPEG")  

  
# Function to compare two images
def images_are_equal(img1, img2):
    diff = ImageChops.difference(img1, img2)
    diff.show()
    time.sleep(5)
    subprocess.run(["pkill", "-f", "Preview.app"])
    return diff.getbbox() is None

def test_image_comparison(open_paintx):
    image_2 = Image.open(image2_Path)
    exported_image = Image.open(export_image_path)
    diff = ImageChops.difference(image_2,exported_image)
    subprocess.run(["pkill", "-f", "Preview.app"])
    # Compare the images and fail the test if there is any difference
    assert images_are_equal(exported_image, image_2), "Exported image is not equal to IMAGE_2. Differences found:{}".format(diff.getbbox())

#To run test from terminal   
#pytest test_image_comparison.py -s --html=Report/report.html