"""PPC offer ads ($1k/mo + 5% of what we close) on the 3 formats that won in the BuildSignals account,
plus the ladder test ("Pick Your Number") on the #1 format so only the offer changes."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

SUP = "/System/Library/Fonts/Supplemental/"
SYS = "/System/Library/Fonts/"
HELV = SYS + "HelveticaNeue.ttc"
MARK = SYS + "Noteworthy.ttc"
IMPACT = SUP + "Impact.ttf"
RED = (224, 50, 43)
YEL = (255, 230, 0)


def f(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def fit(d, text, path, max_w, start, index=0):
    s = start
    while s > 10 and d.textlength(text, font=f(path, s, index)) > max_w:
        s -= 2
    return f(path, s, index)


def shadow(base, xy, text, font, fill=(255, 255, 255, 255), anchor="mm", blur=5):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((xy[0], xy[1] + 3), text, font=font, fill=(0, 0, 0, 170), anchor=anchor)
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(base).text(xy, text, font=font, fill=fill, anchor=anchor)


# ---------- Format 1: "Glass" replica (account winner: 6.34% CTR, $27.97 / booked call) ----------
def glass(pills, big, items, out):
    W, H = 1080, 1350
    im = Image.new("RGBA", (W, H), (128, 120, 108, 255))  # warm gray band like the winner
    photo = Image.open("bg1.png").convert("RGB")
    s = W / photo.width
    photo = photo.resize((W, round(photo.height * s)), Image.LANCZOS)
    photo = ImageEnhance.Brightness(photo).enhance(0.62)  # gray marble so white marker reads
    top = 270
    im.paste(photo.crop((0, 0, W, H - top)), (0, top))
    d = ImageDraw.Draw(im)
    hf = f(HELV, 78, 1)
    y = 72
    for line in pills:
        tw = d.textlength(line, font=hf)
        d.rounded_rectangle([W / 2 - tw / 2 - 24, y, W / 2 + tw / 2 + 24, y + 102], radius=16, fill=(255, 255, 255, 255))
        d.text((W / 2, y + 51), line, font=hf, fill=(17, 17, 17), anchor="mm")
        y += 98
    yy = 560
    bf = min((fit(d, t, MARK, 880, 130, 1) for t in big), key=lambda x: x.size)
    for t in big:
        shadow(im, (W / 2, yy), t, bf)
        yy += 125
    yy += 20
    it = min((fit(d, t, MARK, 820, 62, 1) for t in items), key=lambda x: x.size)  # one size for every line
    for t in items:
        shadow(im, (150, yy), t, it, anchor="lm")
        yy += 74
    im.convert("RGB").save(out, quality=92)


# ---------- Format 2: bright red (account #3: 3.5% CTR, $34 / booked call) ----------
def red(out):
    W, H = 1080, 1350
    im = Image.new("RGB", (W, H), (228, 30, 37))
    d = ImageDraw.Draw(im)
    lab = "REMODELERS DOING $1M+ A YEAR"
    lf = f(SUP + "Arial Bold.ttf", 40)
    tw = d.textlength(lab, font=lf)
    d.rounded_rectangle([W / 2 - tw / 2 - 28, 70, W / 2 + tw / 2 + 28, 140], radius=12, fill="white")
    d.text((W / 2, 106), lab, font=lf, fill=(228, 30, 37), anchor="mm")
    d.text((W / 2, 330), "PAY PER", font=fit(d, "PAY PER", IMPACT, 900, 250), fill="white", anchor="mm")
    d.text((W / 2, 560), "CLOSE", font=fit(d, "PAY PER", IMPACT, 900, 250), fill="white", anchor="mm")
    sub = f(IMPACT, 92)
    d.text((W / 2, 730), "$1K/MO + 5%", font=sub, fill=(255, 225, 0), anchor="mm")
    d.line([(140, 810), (940, 810)], fill="white", width=4)
    y = 870
    for t in ["No setup fee. No contract.",
              "We script, shoot + edit your ads.",
              "We call every lead + book the appointment.",
              "We follow up after your estimate."]:
        d.text((W / 2, y), t, font=fit(d, t, SUP + "Arial Bold.ttf", 940, 46), fill="white", anchor="mm")
        y += 72
    d.rectangle([0, H - 150, W, H], fill=(20, 20, 20))
    cf = f(SUP + "Arial Bold.ttf", 46)
    txt = "See if you qualify"
    tw = d.textlength(txt, font=cf)
    x0, yc = W / 2 - (tw + 70) / 2, H - 75
    d.text((x0, yc), txt, font=cf, fill="white", anchor="lm")
    ax = x0 + tw + 26
    d.line([(ax, yc), (ax + 44, yc)], fill="white", width=6)
    d.polygon([(ax + 48, yc), (ax + 28, yc - 16), (ax + 28, yc + 16)], fill="white")
    im.save(out, quality=92)


# ---------- Format 3: before/after with black + yellow bars (account #2: 4.4% CTR, $29.58 / booked call) ----------
def before_after(out):
    S = 1080
    ref = Image.open("ref_imgoffer1.jpg").convert("RGB")
    photos = ref.crop((95, 200, 925, 745))  # the tilted before/after pair from the winner
    im = Image.new("RGB", (S, S), (248, 246, 240))
    p = photos.resize((round(photos.width * 1.06), round(photos.height * 1.06)), Image.LANCZOS)
    im.paste(p, ((S - p.width) // 2, 196))
    d = ImageDraw.Draw(im)
    d.rectangle([20, 18, S - 20, 190], fill="black")
    d.text((S / 2, 66), "REMODELERS DOING $1M+", font=fit(d, "REMODELERS DOING $1M+", IMPACT, 980, 84), fill="white", anchor="mm")
    d.text((S / 2, 145), "PAY ONLY WHEN THE JOB CLOSES.", font=fit(d, "PAY ONLY WHEN THE JOB CLOSES.", IMPACT, 980, 70), fill=YEL, anchor="mm")
    big = "$1K/MO + 5%"
    d.text((S / 2, 868), big, font=fit(d, big, IMPACT, 900, 150), fill="black", anchor="mm")
    d.rectangle([20, 945, S - 20, S - 18], fill="black")
    l1 = "NO SETUP FEE. NO CONTRACT. CANCEL ANYTIME."
    d.text((S / 2, 983), l1, font=fit(d, l1, IMPACT, 980, 52), fill="white", anchor="mm")
    l2 = "WE SHOOT YOUR ADS + BOOK YOUR APPOINTMENTS"
    d.text((S / 2, 1035), l2, font=fit(d, l2, IMPACT, 980, 46), fill=YEL, anchor="mm")
    im.save(out, quality=92)


glass(["Pay Per Close", "Remodelers Doing $1M+"],
      ["PAY PER CLOSE", "$1K/MO + 5%"],
      ["NO SETUP FEE. NO CONTRACT.", "WE SCRIPT, SHOOT + EDIT YOUR ADS", "WE CALL + BOOK EVERY LEAD", "WE FOLLOW UP AFTER YOUR ESTIMATE"],
      "../ppc1-glass-1k5.jpg")
glass(["Pick Your Number", "Remodelers Doing $1M+"],
      ["PICK YOUR NUMBER", "PAY 10%. WE DELIVER."],
      ["$30K CLOSED = $3K", "$50K CLOSED = $5K", "$100K CLOSED = $10K", "WE DON'T STOP TILL YOU HIT IT"],
      "../ppc2-glass-ladder.jpg")
red("../ppc3-red-1k5.jpg")
before_after("../ppc4-beforeafter-1k5.jpg")
print("ok")
