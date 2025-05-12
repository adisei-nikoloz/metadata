

from PIL import Image, ImageEnhance,ImageFilter
import cv2
import numpy as np 

image = Image.open( r"C:\Users\DESKTOP.GE\Desktop\pyphoto\photos_folder\1733425927671.jpg")

enhancer = ImageEnhance.Brightness(image)
image = enhancer.enhance(0.8)

enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2)

cv_image = np.array(image)
 
denoised_image = cv2.fastNlMeansDenoisingColored(cv_image, None, 10, 10, 7, 21)

denoised_image_pil = Image.fromarray(cv2.cvtColor(denoised_image, cv2.COLOR_BGR2RGB))


sharpened_image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

sharpened_image.save("corrected_image.jpg")
sharpened_image.show()