from PIL import Image
import glob

files = glob.glob("spacenet/PS-RGB/*")
print(files)

import numpy
for i, infile in enumerate(files):
       outfile = "spacenet/PNG-RGB/" + infile.split("\\")[-1].split('.')[0] + ".png"
       im = Image.open(infile)
       out = im.convert("RGB")
       out.save(outfile, "PNG", quality=90)