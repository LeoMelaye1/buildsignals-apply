"""Exact copy of the winning $225 glass ad (ad1-225-sat-glass.jpg) with only the words changed.
winner_glass_clean.png = that image with its lettering removed (OpenCV inpaint, band-limited)."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
HELV = "/System/Library/Fonts/HelveticaNeue.ttc"
HAND = "fonts/PatrickHand-Regular.ttf"
HAND_SC = "fonts/PatrickHandSC-Regular.ttf"
INK = (238, 238, 234, 255)


def fit(d, text, path, max_w, start, stroke=0, index=0):
    s = start
    while s > 10 and d.textlength(text, font=ImageFont.truetype(path, s, index=index)) + 2 * stroke > max_w:
        s -= 2
    return ImageFont.truetype(path, s, index=index)


def make(pills, big, small, out):
    im = Image.open("winner_glass_clean.png").convert("RGBA")
    d = ImageDraw.Draw(im)
    # Two white label boxes, same size and font as the winner
    hf = min((fit(d, t, HELV, 900, 80, index=1) for t in pills), key=lambda f: f.size)
    y = 72
    for t in pills:
        tw = d.textlength(t, font=hf)
        d.rounded_rectangle([W / 2 - tw / 2 - 20, y, W / 2 + tw / 2 + 20, y + 102], radius=16, fill=(255, 255, 255, 255))
        d.text((W / 2, y + 51), t, font=hf, fill=(17, 17, 17), anchor="mm")
        y += 98
    # Marker lettering on the glass, same positions as the winner
    ink = Image.new("RGBA", im.size, (0, 0, 0, 0))
    k = ImageDraw.Draw(ink)
    bf = min((fit(k, t, HAND, 840, 120, 3) for t in big), key=lambda f: f.size)
    for t, yy in zip(big, (590, 700)):
        k.text((555, yy), t, font=bf, fill=INK, anchor="mm", stroke_width=3, stroke_fill=INK)
    sf = min((fit(k, t, HAND_SC, 690, 60, 1) for t in small), key=lambda f: f.size)
    for t, yy in zip(small, (830, 895, 960, 1025)):
        k.text((225, yy), t, font=sf, fill=INK, anchor="lm", stroke_width=1, stroke_fill=INK)
    ink = ink.filter(ImageFilter.GaussianBlur(0.7))  # soften to match the photo, like the original
    im.alpha_composite(ink)
    im.convert("RGB").save(out, quality=92)


if False: make(["Pay Per Close", "Bath Remodelers $1M+"],
     ["PAY PER CLOSE", "$1K/MO + 5%"],
     ["NO SETUP FEE. NO CONTRACT.", "WE SHOOT + RUN YOUR ADS", "WE CALL + BOOK EVERY LEAD", "MONTH 1 PAYS OFF OR IT'S FREE"],
     "../ppc1-winnerglass-1k5.jpg")
make(["Bath Remodelers", "$100K In 2 Months"],
     ["$100K IN NEW JOBS", "IN 2 MONTHS"],
     ["OR YOU OWE US NOTHING", "WE RUN YOUR ADS + BOOK THE CALLS", "YOU JUST SHOW UP + SELL"],
     "../simple-ladder-glass-owe.jpg")
make(["Pay Per Close", "Bath Remodelers $1M+"],
     ["YOU ONLY PAY", "WHEN IT CLOSES"],
     ["WE RUN YOUR ADS", "WE CALL + BOOK EVERY LEAD", "YOU JUST SHOW UP + SELL"],
     "../simple-ppc-glass.jpg")
print("ok")
