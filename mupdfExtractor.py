from __future__ import print_function
import os, sys, time
import fitz
from tqdm import tqdm
import io
from PIL import Image

"""
PyMuPDF utility
----------------
For Deprecated names 
https://pymupdf.readthedocs.io/en/latest/znames.html?highlight=getImageList#deprecated-names

For a given entry in a page's getImagleList() list, function "recoverpix"
returns either the raw image data, or a modified pixmap if an /SMask entry
exists.
The item's first two entries are PDF xref numbers. The first one is the image in
question, the second one may be 0 or the object id of a soft-image mask. In this
case, we assume it being a sequence of alpha bytes belonging to our image.
We then create a new Pixmap giving it these alpha values, and return it.
If the result pixmap is CMYK, it will be converted to RGB first.

"""
print(fitz.__doc__)
# if not tuple(map(int, fitz.version[0].split("."))) >= (1, 18, 18):
#     raise SystemExit("require PyMuPDF v1.18.18+")

dimlimit = 100  # 100  # each image side must be greater than this
relsize = 0.1  # 0.05  # image : pixmap size ratio must be larger than this (5%)
abssize = 2048  # 2048  # absolute image size limit 2 KB: ignore if smaller
imgdir = "images"  # found images are stored in this subfolder

if not os.path.exists(imgdir):
    os.mkdir(imgdir)


def recoverpix(doc, item):
    x = item[0]  # xref of PDF image
    s = item[1]  # xref of its /SMask
    if s == 0:  # no smask: use direct image output
        return doc.extract_image(x)     # extract a list of images

    def getimage(pix):
        if pix.colorspace.n != 4:
            return pix
        tpix = fitz.Pixmap(fitz.csRGB, pix)
        return tpix

    # we need to reconstruct the alpha channel with the smask
    pix1 = fitz.Pixmap(doc, x)
    pix2 = fitz.Pixmap(doc, s)  # create pixmap of the /SMask entry

    """Sanity check:
    - both pixmaps must have the same rectangle
    - both pixmaps must not have alpha
    - pix2 must consist of 1 byte per pixel
    """
    if not (pix1.irect == pix2.irect and pix1.alpha == pix2.alpha == 0 and pix2.n == 1):
        pix2 = None
        print("Warning: unsupported /SMask %i for %i." % (s, x))
        return getimage(pix1)

    pix = fitz.Pixmap(pix1)  # copy of pix1, with an alpha channel added
    pix.setAlpha(pix2.samples)  # treat pix2.samples as the alpha values

    # we may need to adjust something for CMYK pixmaps here:
    return getimage(pix)

def filter_position(width, height, limit_dim, limit_ratio):

    if min(width, height) < limit_dim:
        return True
    # image aspect ratio
    current_ratio = width / height
    if current_ratio < limit_ratio or current_ratio > (1/limit_ratio):
        return True
    else:
        return False

def filter_size(byte_img, size=2048):
    if len(byte_img) <= size:
        return True
    else:
        return False

fname = "pdf/more_diagrams.pdf"
# fname = sys.argv[1] if len(sys.argv) == 2 else None
if not fname:
    print("PyMuPDF PDF Image Extraction")
    # fname = sg.PopupGetFile("Select file:", title="PyMuPDF PDF Image Extraction")
if not fname:
    raise SystemExit()

t0 = time.time()
doc = fitz.open(fname)

page_count = len(doc)  # number of pages

xreflist = []
imglist = []
for pno in tqdm(range(page_count), desc="progressing:"):
    # sg.QuickMeter(
    #     "Extract Images",  # show our progress
    #     pno + 1,
    #     page_count,
    #     "*** Scanning Pages ***",
    # )

    il = doc.get_page_images(pno)
    imglist.extend([x[0] for x in il])
    for img in il:
        xref = img[0]   # image element id in the pdf
        if xref in xreflist:    # 不重复
            continue
        width = img[2]
        height = img[3]
        if filter_position(width, height, dimlimit, relsize):
            continue
        pix = recoverpix(doc, img)
        if type(pix) is dict:  # we got a raw image
            ext = pix["ext"]
            imgdata = pix["image"]
            n = pix["colorspace"]
            if filter_size(imgdata, abssize):
                continue
            imgfile = os.path.join(imgdir, "img-%i.%s" % (xref, ext))

            # rgb_pix = fitz.Pixmap(fitz.csRGB, cmyk_pix)   convert cmyk to rgb
            pil_image = Image.open(io.BytesIO(imgdata))
            # pil_image.show()
            pil_image.save(imgfile, compression="JPEG")
        else:  # we got a pixmap
            imgfile = os.path.join(imgdir, "img-%i.png" % xref)
            if pix.colorspace.name not in (fitz.csGRAY.name, fitz.csRGB.name):
                # if image is not Gray (pix.n=4) bytes per pixel or RGB(pix.n=3), convert it into RGB
                pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(os.path.join(imgdir, "img-%i.pam" % (xref)))
            imgdata = pix.getPNGData()
            if filter_size(imgdata, abssize):
                continue
            pix.writePNG(imgfile)

        xreflist.append(xref)

t1 = time.time()
imglist = list(set(imglist))
print(len(set(imglist)), "images in total")
print(len(xreflist), "images extracted")
print("total time %g sec" % (t1 - t0))
warnings = fitz.TOOLS.mupdf_warnings()
if warnings:
    print("The following warnings have been issued:")
    print("----------------------------------------")
    print(warnings)