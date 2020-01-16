from geomdl import BSpline
from geomdl import utilities
from PIL import Image, ImageDraw
import numpy as np

def bspline2mask(cps, width, height, delta=0.05, downscale=1):
    connecs = []
    for i in range(len(cps)):
        curve = BSpline.Curve()
        curve.degree = 3
        curve.ctrlpts = cps[i]
        curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))
        # print('delta',delta)
        curve.delta = delta
        curve.evaluate()
        connecs.append(curve.evalpts)

    polygon = np.array(connecs).flatten().tolist()
    img = Image.new('L', (height, width), 255)
    ImageDraw.Draw(img).polygon(polygon, outline=0, fill=0)
    mask = np.array(img.resize((int(height//downscale), int(width//downscale)), Image.NEAREST))
    #print(mask.shape, width, height, downscale,int(width//downscale), int(height//downscale))
    return mask == False


def crl2mask(crl, width, height, delta=.05, downscale=1):
    c, r, l = crl if type(crl) == list else crl.tolist()
    cps = []
    for i in range(len(c)):
        ip = (i+1) % len(c)
        cps.append([c[i], r[i], l[ip], c[ip]])
    return bspline2mask(cps, width, height, delta=delta, downscale=downscale)

