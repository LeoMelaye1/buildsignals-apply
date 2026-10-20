"""Replicas of Kitchen & Bath Marketing Co's long-running ads (live since Aug 25, 2026, 7 variants):
Same layouts, value-led: the done-for-you system behind $8.2M, pay when it closes. Price lives in the ad text and page.
Same layouts, BuildSignals logo, bath remodelers. 1080x1080."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

S = 1080
PB = "fonts/Poppins-Black.ttf"; PX = "fonts/Poppins-ExtraBold.ttf"; PBo = "fonts/Poppins-Bold.ttf"; PS = "fonts/Poppins-SemiBold.ttf"
GOLD_L, GOLD_D = (240, 214, 150), (176, 132, 58)
INK = (22, 22, 22)


def F(p, s): return ImageFont.truetype(p, s)


def fit(d, t, p, w, s):
    while s > 10 and d.textlength(t, font=F(p, s)) > w: s -= 2
    return F(p, s)


def gold(im, xy, t, font, anchor="mm"):
    """Text filled with a vertical gold gradient."""
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).text(xy, t, font=font, fill=255, anchor=anchor)
    box = m.getbbox()
    if not box: return
    g = Image.new("RGB", im.size, GOLD_D); gd = ImageDraw.Draw(g)
    for y in range(box[1], box[3] + 1):
        k = (y - box[1]) / max(1, box[3] - box[1]); k = abs(k - 0.35) / 0.65
        c = tuple(int(GOLD_L[i] + (GOLD_D[i] - GOLD_L[i]) * k) for i in range(3))
        gd.line([(box[0], y), (box[2], y)], fill=c)
    im.paste(g, (0, 0), m)


def cover(path, w, h):
    im = Image.open(path).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


def logo(im, cx, cy, h, dark=True):
    lg = Image.open("../../buildsignals-horizontal-dark.png" if dark else "../../buildsignals-horizontal-white.png").convert("RGBA")
    lg = lg.resize((round(lg.width * h / lg.height), h), Image.LANCZOS)
    im.paste(lg, (int(cx - lg.width / 2), int(cy - lg.height / 2)), lg)


# 1) Cream, big gold number (their #2)
def cream(out):
    im = Image.new("RGB", (S, S), (244, 239, 230)); d = ImageDraw.Draw(im)
    logo(im, S / 2, 120, 70, dark=True)
    d.text((S / 2, 290), "Bath Remodelers,", font=fit(d, "Bath Remodelers,", PB, 900, 104), fill=INK, anchor="mm")
    d.text((S / 2, 395), "get the system behind", font=F(PX, 64), fill=INK, anchor="mm")
    BIG, BIGF = "$8.2M", fit(d, "$8.2M", PB, 820, 300)
    gold(im, (S / 2, 590), BIG, BIGF)
    d = ImageDraw.Draw(im)
    if d.textlength(BIG, font=BIGF) < 420:
     for (x1, y1, x2, y2) in [(250, 520, 320, 545), (240, 600, 320, 600), (250, 680, 320, 655), (830, 520, 760, 545), (840, 600, 760, 600), (830, 680, 760, 655)]:
         d.line([(x1, y1), (x2, y2)], fill=GOLD_D, width=6)
    gold(im, (S / 2, 790), "in signed bath jobs", fit(d, "in signed bath jobs", PX, 900, 76))
    d = ImageDraw.Draw(im); d.line([(150, 845), (930, 845)], fill=GOLD_D, width=3)
    d.text((S / 2, 915), "done for you. You only pay", font=fit(d, "done for you. You only pay", PX, 960, 70), fill=INK, anchor="mm")
    d.text((S / 2, 1005), "when the job closes", font=fit(d, "done for you. You only pay", PX, 960, 70), fill=INK, anchor="mm")
    im.save(out, quality=92)


# 2) ATTENTION hazard banner (their #3)
def attention(out):
    im = Image.new("RGB", (S, S), (12, 12, 12))
    bg = ImageEnhance.Brightness(cover("bg2.png", S, 720)).enhance(0.35)
    im.paste(bg, (0, 200)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S, 210], fill=(214, 172, 74))
    for x in range(-200, S + 200, 120):  # hazard stripes on the edges
        d.polygon([(x, 0), (x + 55, 0), (x - 145, 210), (x - 200, 210)], fill=(18, 18, 18))
    d.rounded_rectangle([60, 22, S - 60, 190], radius=10, fill=(214, 172, 74))
    d.polygon([(130, 150), (195, 40), (260, 150)], outline=INK, width=12)
    d.text((195, 108), "!", font=F(PB, 70), fill=INK, anchor="mm")
    d.text((640, 82), "ATTENTION", font=F(PB, 112), fill=INK, anchor="mm")
    d.text((640, 162), "BATH REMODELERS", font=F(PX, 58), fill=INK, anchor="mm")
    f1 = fit(d, "WE FILL", PB, 960, 190); wp = d.textlength("WE ", font=f1); x0 = S / 2 - d.textlength("WE FILL", font=f1) / 2
    gold(im, (x0, 335), "WE", f1, anchor="lm")
    d = ImageDraw.Draw(im)
    d.text((x0 + wp, 335), "FILL", font=f1, fill="white", anchor="lm")
    d.text((S / 2, 500), "YOUR CALENDAR", font=fit(d, "YOUR CALENDAR", PB, 960, 150), fill="white", anchor="mm")
    d.text((S / 2, 640), "WITH BATH JOBS", font=fit(d, "WITH BATH JOBS", PB, 960, 150), fill="white", anchor="mm")
    gold(im, (S / 2, 760), "DONE FOR YOU", F(PX, 70))
    d = ImageDraw.Draw(im)
    d.line([(90, 760), (250, 760)], fill=GOLD_D, width=5); d.line([(830, 760), (990, 760)], fill=GOLD_D, width=5)
    d.rectangle([150, 810, 930, 905], fill=(214, 172, 74))
    d.text((S / 2, 858), "PAY WHEN IT CLOSES", font=fit(d, "PAY WHEN IT CLOSES", PB, 740, 82), fill=INK, anchor="mm")
    d.pieslice([-300, 940, S + 300, 1500], 180, 360, fill=(244, 239, 230))
    d.rectangle([0, 1000, S, S], fill=(244, 239, 230))
    d.arc([-300, 940, S + 300, 1500], 180, 360, fill=GOLD_D, width=6)
    logo(im, S / 2, 1025, 56, dark=True)
    im.save(out, quality=92)


def icon_row(d, im, y, items, color, txt):
    xs = [S * 0.2, S * 0.5, S * 0.8] if len(items) == 3 else [S * 0.33, S * 0.67]
    for x, (kind, l1, l2) in zip(xs, items):
        d.ellipse([x - 52, y - 52, x + 52, y + 52], outline=color, width=5)
        if kind == "cal":
            d.rounded_rectangle([x - 26, y - 22, x + 26, y + 26], radius=5, outline=color, width=5); d.line([(x - 26, y - 8), (x + 26, y - 8)], fill=color, width=5)
            d.line([(x - 12, y - 32), (x - 12, y - 16)], fill=color, width=5); d.line([(x + 12, y - 32), (x + 12, y - 16)], fill=color, width=5)
        elif kind == "shield":
            d.polygon([(x, y - 32), (x + 28, y - 20), (x + 24, y + 12), (x, y + 32), (x - 24, y + 12), (x - 28, y - 20)], outline=color, width=5)
            d.line([(x - 12, y), (x - 2, y + 10), (x + 14, y - 10)], fill=color, width=5)
        else:
            d.text((x, y), "$", font=F(PB, 62), fill=color, anchor="mm")
        d.text((x, y + 85), l1, font=F(PBo, 28), fill=txt, anchor="mm"); d.text((x, y + 118), l2, font=F(PBo, 28), fill=txt, anchor="mm")


# 3) Black split with photo (their #5)
def black(out):
    im = Image.new("RGB", (S, S), (10, 10, 10))
    ph = ImageEnhance.Brightness(cover("bg2.png", 620, S)).enhance(1.05)
    fade = Image.new("L", (620, S)); fd = ImageDraw.Draw(fade)
    for x in range(620): fd.line([(x, 0), (x, S)], fill=min(255, int(255 * x / 320)))  # soft left edge
    im.paste(ph, (S - 620, 0), fade)
    d = ImageDraw.Draw(im)
    logo(im, 330, 110, 60, dark=False)
    y = 270
    for t, c in [("Bath Remodelers,", "white"), ("we shoot your ads,", "white"), ("call every lead +", "white"), ("book your calendar.", "g"), ("You only pay", "white"), ("when it closes.", "g")]:
        f = F(PX, 70)
        if c == "white": d.text((70, y), t, font=f, fill="white", anchor="lm")
        elif c == "g": gold(im, (70, y), t, f, anchor="lm"); d = ImageDraw.Draw(im)
        else:
            d.text((70, y), "or it's ", font=f, fill="white", anchor="lm"); w = d.textlength("or it's ", font=f)
            gold(im, (70 + w, y), "free", f, anchor="lm"); d = ImageDraw.Draw(im)
        y += 96
    icon_row(d, im, 900, [("cal", "APPOINTMENTS", "BOOKED FOR YOU"), ("shield", "$8.2M CLOSED", "IN 2026"), ("$", "PAY WHEN", "IT CLOSES")], GOLD_D, "white")
    im.save(out, quality=92)


# 4) Before / after with icon strip (their #1)
def before_after(out):
    im = Image.new("RGB", (S, S), (12, 12, 12))
    ref = Image.open("ref_imgoffer1.jpg").convert("RGB")
    b = cover_img(ref.crop((120, 215, 495, 735)), S // 2, 520); a = cover_img(ref.crop((530, 215, 910, 735)), S // 2, 520)
    im.paste(b, (0, 0)); im.paste(a, (S // 2, 0))
    d = ImageDraw.Draw(im)
    d.line([(S / 2, 0), (S / 2, 520)], fill=(244, 239, 230), width=6)
    for x, t in [(90, "BEFORE"), (S - 90, "AFTER")]:
        tw = d.textlength(t, font=F(PBo, 30)); d.rectangle([x - tw / 2 - 16, 30, x + tw / 2 + 16, 76], fill=(20, 20, 20) if t == "BEFORE" else (214, 172, 74))
        d.text((x, 53), t, font=F(PBo, 30), fill="white" if t == "BEFORE" else INK, anchor="mm")
    d.ellipse([S / 2 - 95, 20, S / 2 + 95, 210], fill=(244, 239, 230), outline=GOLD_D, width=4)
    lg = Image.open("../../buildsignals-icon-white.png").convert("RGBA"); lg = lg.resize((110, round(lg.height * 110 / lg.width)))
    dark = Image.new("RGBA", lg.size, (22, 22, 22, 255)); dark.putalpha(lg.split()[3]); im.paste(dark, (int(S / 2 - 55), int(115 - lg.height / 2)), dark)
    grad = Image.linear_gradient("L").resize((S, 260))
    im.paste(Image.new("RGB", (S, 260), (12, 12, 12)), (0, 380), grad)
    d = ImageDraw.Draw(im)
    d.text((S / 2, 590), "Bath Remodelers,", font=F(PX, 72), fill="white", anchor="mm")
    f = F(PX, 72); t1, t2 = "we turn homeowners ", "into"
    w = d.textlength(t1 + t2, font=f); x0 = S / 2 - w / 2
    d.text((x0, 675), t1, font=f, fill="white", anchor="lm"); gold(im, (x0 + d.textlength(t1, font=f), 675), t2, f, anchor="lm")
    gold(im, (S / 2, 760), "signed bath jobs", f)
    d = ImageDraw.Draw(im)
    d.text((S / 2, 845), "Done for you. You only pay when it closes.", font=fit(d, "Done for you. You only pay when it closes.", PX, 980, 64), fill="white", anchor="mm")
    d.rounded_rectangle([60, 905, S - 60, 1040], radius=14, outline=GOLD_D, width=3)
    for i, (l1, l2) in enumerate([("ADS SHOT", "FOR YOU"), ("APPOINTMENTS", "BOOKED FOR YOU"), ("PAY WHEN", "IT CLOSES")]):
        x = 60 + (S - 120) * (i + 0.5) / 3
        d.text((x, 952), l1, font=F(PBo, 30), fill="white", anchor="mm"); d.text((x, 992), l2, font=F(PBo, 30), fill="white", anchor="mm")
        if i: d.line([(60 + (S - 120) * i / 3, 925), (60 + (S - 120) * i / 3, 1020)], fill=GOLD_D, width=2)
    im.save(out, quality=92)


def cover_img(im, w, h):
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


cream("../kb1-cream-ppc.jpg")
attention("../kb2-attention-ppc.jpg")
black("../kb3-black-ppc.jpg")
before_after("../kb4-beforeafter-ppc.jpg")
print("ok")
