from PIL import Image
import sys

colorImage  = Image.open(sys.argv[1])

for i in range(0, 359, 2):
  rotated = colorImage.rotate(i)
  rotated.save("output/" + sys.argv[1] + "_" + str(i) + ".jpg", "JPEG")

