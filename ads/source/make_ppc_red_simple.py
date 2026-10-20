"""Pay-per-close on Leo's bright-red format (same build as ad2-225-sat-red / ppc3-red)."""
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
d.text((W / 2, 300), "PAY PER", font=ImageFont.truetype(IMPACT, 250), fill="white", anchor="mm")
d.text((W / 2, 530), "CLOSE", font=ImageFont.truetype(IMPACT, 250), fill="white", anchor="mm")
d.text((W / 2, 700), "YOU ONLY PAY WHEN THE JOB CLOSES", font=fit(d, "YOU ONLY PAY WHEN THE JOB CLOSES", IMPACT, 940, 70), fill=YEL, anchor="mm")
d.line([(140, 790), (940, 790)], fill="white", width=4)
y = 860
rows = ["We run your ads.", "We call every lead + book the appointment.", "You show up and sell."]
bf = min((fit(d, t, AB, 940, 50) for t in rows), key=lambda f: f.size)
for t in rows:
    d.text((W / 2, y), t, font=bf, fill="white", anchor="mm"); y += 80
d.rectangle([0, H - 150, W, H], fill=(20, 20, 20))
cf = ImageFont.truetype(AB, 46); txt = "See if you qualify"; tw = d.textlength(txt, font=cf)
x0, yc = W / 2 - (tw + 70) / 2, H - 75
d.text((x0, yc), txt, font=cf, fill="white", anchor="lm"); ax = x0 + tw + 26
d.line([(ax, yc), (ax + 44, yc)], fill="white", width=6); d.polygon([(ax + 48, yc), (ax + 28, yc - 16), (ax + 28, yc + 16)], fill="white")
im.save("../ppc-red-simple.jpg", quality=92); print("ok")
