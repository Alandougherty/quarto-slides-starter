"""Pre-rendered background art for the keynote example.

assets/bokeh.html draws the floating 'bokeh' Gaussians live with CSS
animation. This script bakes the same look into static images for the
slides that attach them with the documented background-image attribute.

Run with any Python that has Pillow installed, from the examples/keynote
directory (output paths are relative to it):
    python assets/make_bokeh.py
"""
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080

def blob(draw_img, x, y, r, colour, alpha):
    layer = Image.new("RGBA", draw_img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((x-r, y-r, x+r, y+r), fill=colour + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.55))
    draw_img.alpha_composite(layer)

def base():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    for i in range(H):  # vertical navy gradient, radial-ish feel
        t = i / H
        d.line([(0, i), (W, i)], fill=(11 + int(8*(1-t)), 16 + int(14*(1-t)), 38 + int(30*(1-t)), 255))
    return img

CYAN, PURPLE, TEAL, LILAC = (70,211,255), (199,125,255), (94,224,212), (157,180,255)

img = base()
for x,y,r,c,a in [(1350,140,190,CYAN,190),(1650,400,150,PURPLE,170),(1480,700,130,TEAL,180),
                  (1780,860,110,CYAN,160),(1180,850,120,LILAC,150),(1060,300,80,CYAN,160),
                  (1860,90,85,PURPLE,150),(300,180,110,TEAL,130),(180,820,95,CYAN,120),
                  (620,930,80,LILAC,120),(760,120,75,PURPLE,110)]:
    blob(img, x, y, r, c, a)
img.convert("RGB").save("assets/bokeh.png", quality=92)

img = base()
SKIN, BROWN = (232,201,168), (138,106,74)
for x,y,r,c,a in [(1500,250,160,CYAN,45),(1250,780,120,PURPLE,40),(400,500,140,TEAL,30),
                  (960,430,175,SKIN,190),(880,325,85,BROWN,140),(1010,575,105,CYAN,130)]:
    blob(img, x, y, r, c, a)
img.convert("RGB").save("assets/bokeh-dim.png", quality=92)
# content slides: plain navy with a cyan-to-purple strip at the top edge
img = base()
d = ImageDraw.Draw(img)
for x in range(W):
    t = x / W
    col = (int(70 + t*(199-70)), int(211 + t*(125-211)), int(255))
    d.line([(x, 0), (x, 10)], fill=col + (255,))
img.convert("RGB").save("assets/content-bg.png", quality=92)
print("saved bokeh.png, bokeh-dim.png, content-bg.png")
