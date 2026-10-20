"""Ladder offer on Leo's bright-red format (same build as ad2-225-sat-red / ppc3-red)."""
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1350
SUP = "/System/Library/Fonts/Supplemental/"
AB, IMPACT = SUP + "Arial Bold.ttf", SUP + "Impact.ttf"
RED, YEL = (228, 30, 37), (255, 225, 0)
def fit(d, t, p, w, s):
    while s > 10 and d.textlength(t, font=ImageFont.truetype(p, s)) > w: s -= 2
    return ImageFont.truetype(p, s)
im = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(im)
lab = "BATH REMODELERS DOING $1M+ A YEAR"; lf = ImageFont.truetype(AB, 40); tw = d.textlength(lab, font=lf)
d.rounded_rectangle([W / 2 - tw / 2 - 28, 70, W / 2 + tw / 2 + 28, 140], radius=12, fill="white")
d.text((W / 2, 106), lab, font=lf, fill=RED, anchor="mm")
d.text((W / 2, 230), "WE WILL GET YOU", font=fit(d, "WE WILL GET YOU", IMPACT, 900, 90), fill="white", anchor="mm")
d.text((W / 2, 420), "$100K", font=fit(d, "$100K", IMPACT, 940, 300), fill="white", anchor="mm")
d.text((W / 2, 610), "IN NEW SIGNED", font=fit(d, "IN NEW SIGNED BATH JOBS", IMPACT, 940, 110), fill="white", anchor="mm")
d.text((W / 2, 720), "BATH JOBS", font=fit(d, "IN NEW SIGNED BATH JOBS", IMPACT, 940, 110), fill="white", anchor="mm")
d.line([(140, 810), (940, 810)], fill="white", width=4)
y = 870
rows = [("You pay 10%. Once.", YEL), ("Or pick $50K, $250K, any number.", "white"),
        ("We shoot your ads + book your calls.", "white"), ("We don't stop until you hit it.", "white")]
bf = min((fit(d, t, AB, 940, 48) for t, _ in rows), key=lambda f: f.size)
for t, c in rows:
    d.text((W / 2, y), t, font=bf, fill=c, anchor="mm"); y += 72
d.rectangle([0, H - 150, W, H], fill=(20, 20, 20))
cf = ImageFont.truetype(AB, 46); txt = "Pick your number"; tw = d.textlength(txt, font=cf)
x0, yc = W / 2 - (tw + 70) / 2, H - 75
d.text((x0, yc), txt, font=cf, fill="white", anchor="lm"); ax = x0 + tw + 26
d.line([(ax, yc), (ax + 44, yc)], fill="white", width=6); d.polygon([(ax + 48, yc), (ax + 28, yc - 16), (ax + 28, yc + 16)], fill="white")
im.save("../ladder-red.jpg", quality=92); print("ok")
