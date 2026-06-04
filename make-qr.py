# /// script
# requires-python = ">=3.9"
# dependencies = ["qrcode[pil]>=7.4", "pillow>=10"]
# ///
"""產生朝聖之路 App 的 QR Code 與分享卡。
輸出：qr-plain.png / qr-logo.png / qr.svg
      qr-card.png（直式 1080x1350）/ qr-card-square.png（方形 1080x1080）
      qr-card-photo.png（風景封面 1080x1350，程式繪製日出朝聖景）
用法：uv run make-qr.py"""
import os
import math
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.svg import SvgPathImage
from PIL import Image, ImageDraw, ImageFont

URL = "https://lawsuger.github.io/camino-app/"
TITLE = "築夢之家－兩位新鮮人的朝聖"
KICKER = "C A M I N O   F R A N C É S"
SUBTITLE = "法國之路 · 規劃手冊"
FEATURES = "裝備 · 路線 · 庇護所 · 打卡座標 · 儀式 · 美食"
URL_TEXT = "lawsuger.github.io/camino-app"
CAP = "掃描開啟 · 手機可「加到主畫面」當離線 App"
BLESS = "Buen Camino！一路平安"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr")
os.makedirs(OUT, exist_ok=True)

NAVY = (22, 48, 73); NAVY2 = (27, 58, 91)
GOLD = (242, 183, 5); GOLDD = (198, 138, 24)
MUTED = (120, 111, 98); CREAM = (250, 247, 240)
WHITE = (255, 255, 255); FRAME = (228, 214, 176)

FB = r"C:\Windows\Fonts\msjhbd.ttc"
FR = r"C:\Windows\Fonts\msjh.ttc"
_M = ImageDraw.Draw(Image.new("RGB", (4, 4)))


def f(path, size):
    return ImageFont.truetype(path, size)


def fit(text, path, maxw, start, mn=34):
    s = start
    while s > mn:
        if _M.textlength(text, font=f(path, s)) <= maxw:
            return f(path, s)
        s -= 2
    return f(path, mn)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def scallop(size):
    fr = size / 512.0
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    apex = (256 * fr, 406 * fr)
    dome = [(146, 205), (168, 150), (210, 120), (256, 108),
            (302, 120), (344, 150), (366, 205)]
    dome = [(x * fr, y * fr) for x, y in dome]
    d.polygon([apex] + dome, fill=GOLD)
    for p in dome:
        d.line([apex, p], fill=NAVY, width=max(2, int(7 * fr)))
    r = 7 * fr
    d.ellipse([apex[0] - r, apex[1] - r, apex[0] + r, apex[1] + r], fill=NAVY)
    return im


# ---------- 基礎 QR ----------
qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=20, border=4)
qr.add_data(URL); qr.make(fit=True)
plain = qr.make_image(fill_color=NAVY, back_color="white").convert("RGB")
plain.save(os.path.join(OUT, "qr-plain.png"))

qs2 = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=20, border=4)
qs2.add_data(URL); qs2.make(fit=True)
qs2.make_image(image_factory=SvgPathImage).save(os.path.join(OUT, "qr.svg"))


def qr_logo(size):
    img = plain.resize((size, size), Image.NEAREST).convert("RGBA")
    ls = int(size * 0.20)
    badge = Image.new("RGBA", (ls, ls), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.rounded_rectangle([0, 0, ls - 1, ls - 1], radius=ls * 0.28, fill=WHITE)
    sc = scallop(int(ls * 0.76))
    badge.alpha_composite(sc, (int((ls - sc.width) / 2), int((ls - sc.height) / 2)))
    img.alpha_composite(badge, (int((size - ls) / 2), int((size - ls) / 2)))
    return img.convert("RGB")


qr_logo(1000).save(os.path.join(OUT, "qr-logo.png"))


def framed_qr(card, size, cx, top):
    fx = int(cx - size / 2)
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([fx - 26, top - 26, fx + size + 26, top + size + 26],
                        radius=32, fill=WHITE, outline=FRAME, width=3)
    card.paste(qr_logo(size), (fx, top))
    return top + size + 26


# ---------- 乾淨版分享卡（直式 / 方形共用）----------
def clean_card(W, H):
    card = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(card)
    band = int(H * 0.165)
    d.rectangle([0, 0, W, band], fill=NAVY2)
    ss = int(band * 0.46)
    sh = scallop(ss)
    card.paste(sh, (int(W / 2 - ss / 2), int(band * 0.14)), sh)
    d.text((W / 2, band * 0.83), KICKER, font=f(FB, int(band * 0.135)),
           fill=GOLD, anchor="mm")

    y = band + int(H * 0.058)
    tf = fit(TITLE, FB, W - 150, int(H * 0.060), 40)
    d.text((W / 2, y), TITLE, font=tf, fill=NAVY, anchor="mm")
    y += int(H * 0.040)
    d.rounded_rectangle([W / 2 - 66, y - 3, W / 2 + 66, y + 3], radius=3, fill=GOLD)
    y += int(H * 0.034)
    d.text((W / 2, y), SUBTITLE, font=f(FB, int(H * 0.030)), fill=GOLDD, anchor="mm")
    y += int(H * 0.034)
    d.text((W / 2, y), FEATURES, font=f(FR, int(H * 0.0225)), fill=MUTED, anchor="mm")

    qsz = int(min(W * 0.50, H * 0.40))
    qtop = y + int(H * 0.040)
    bottom = framed_qr(card, qsz, W / 2, qtop)

    y = bottom + int(H * 0.045)
    d.text((W / 2, y), CAP, font=f(FB, int(H * 0.0245)), fill=NAVY, anchor="mm")
    y += int(H * 0.040)
    d.text((W / 2, y), URL_TEXT, font=f(FB, int(H * 0.030)), fill=GOLDD, anchor="mm")
    y += int(H * 0.036)
    d.text((W / 2, y), BLESS, font=f(FR, int(H * 0.022)), fill=MUTED, anchor="mm")
    return card


clean_card(1080, 1350).save(os.path.join(OUT, "qr-card.png"))
clean_card(1080, 1080).save(os.path.join(OUT, "qr-card-square.png"))


# ---------- 風景封面版 ----------
def pilgrim(d, cx, feet, h, color=(34, 42, 58)):
    hr = h * 0.13
    top = feet - h
    bw = h * 0.22
    d.line([(cx + bw * 0.95, feet + h * 0.02), (cx + bw * 0.95, top - hr)],
           fill=color, width=max(2, int(h * 0.028)))            # 朝聖杖
    d.rounded_rectangle([cx - bw * 1.0, top + 2 * hr, cx - bw * 0.15,
                         top + 2 * hr + h * 0.36], radius=h * 0.06, fill=color)  # 背包
    d.ellipse([cx - hr, top, cx + hr, top + 2 * hr], fill=color)  # 頭
    d.polygon([(cx - bw * 0.55, top + 2 * hr), (cx + bw * 0.55, top + 2 * hr),
               (cx + bw * 0.7, feet), (cx - bw * 0.7, feet)], fill=color)  # 身體


def landscape(W, H):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    hz = int(H * 0.60)
    sky = [(38, 44, 92), (84, 72, 122), (172, 96, 100), (232, 150, 99), (250, 207, 150)]
    for y in range(hz):
        seg = (y / hz) * (len(sky) - 1)
        i = min(int(seg), len(sky) - 2)
        d.line([(0, y), (W, y)], fill=lerp(sky[i], sky[i + 1], seg - i))
    sx, sy, R = int(W * 0.5), int(hz * 0.95), int(W * 0.14)
    for r in range(R, 0, -1):
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=lerp((255, 240, 205), (251, 196, 116), r / R))
    for y in range(hz, H):
        d.line([(0, y), (W, y)], fill=lerp((226, 206, 166), (188, 172, 144), (y - hz) / (H - hz)))
    layers = [(int(hz * 0.88), (150, 138, 168), 0.020, 20, 0.0),
              (int(hz * 0.95), (108, 118, 138), 0.026, 28, 1.3),
              (int(hz * 1.01), (74, 98, 96), 0.030, 26, 2.2)]
    for base, col, freq, amp, ph in layers:
        pts = [(0, H)]
        for x in range(0, W + 1, 6):
            yy = base + int(math.sin(x * freq + ph) * amp + math.sin(x * freq * 0.5 + ph) * amp * 0.5)
            pts.append((x, yy))
        pts += [(W, H)]
        d.polygon(pts, fill=col)
    # 朝聖小徑
    tx, tw = int(W * 0.52), int(W * 0.02)
    mx, my, mw = int(W * 0.42), int((hz + H) / 2), int(W * 0.14)
    bx, bw = int(W * 0.50), int(W * 0.36)
    d.polygon([(tx - tw, hz), (mx - mw, my), (bx - bw, H),
               (bx + bw, H), (mx + mw, my), (tx + tw, hz)], fill=(232, 214, 173))
    # 兩位朝聖者（兩位新鮮人）
    pilgrim(d, int(W * 0.45), int(hz + (H - hz) * 0.52), int(H * 0.135))
    pilgrim(d, int(W * 0.55), int(hz + (H - hz) * 0.66), int(H * 0.165))
    return img, hz


def photo_card(W, H):
    card = Image.new("RGB", (W, H), CREAM)
    sceneH = int(H * 0.55)
    scene, hz = landscape(W, sceneH)
    card.paste(scene, (0, 0))
    # 頂部暗罩（讓白字清楚）
    sh = int(sceneH * 0.60)
    scrim = Image.new("L", (W, sh), 0)
    sd = ImageDraw.Draw(scrim)
    for y in range(sh):
        sd.line([(0, y), (W, y)], fill=int(150 * (1 - y / sh)))
    card.paste((16, 26, 44), (0, 0, W, sh), scrim)
    d = ImageDraw.Draw(card)

    def st(xy, text, font, fill):
        d.text((xy[0] + 2, xy[1] + 2), text, font=font, fill=(0, 0, 0), anchor="mm")
        d.text(xy, text, font=font, fill=fill, anchor="mm")

    st((W / 2, int(H * 0.070)), KICKER, f(FB, int(H * 0.024)), GOLD)
    tf = fit(TITLE, FB, W - 130, int(H * 0.060), 40)
    st((W / 2, int(H * 0.125)), TITLE, tf, WHITE)
    st((W / 2, int(H * 0.175)), SUBTITLE, f(FB, int(H * 0.027)), (244, 226, 190))

    # 底部米白區的 QR
    qsz = int(W * 0.34)
    qtop = sceneH + int(H * 0.035)
    bottom = framed_qr(card, qsz, W / 2, qtop)
    y = bottom + int(H * 0.042)
    d.text((W / 2, y), CAP, font=f(FB, int(H * 0.0235)), fill=NAVY, anchor="mm")
    y += int(H * 0.038)
    d.text((W / 2, y), URL_TEXT, font=f(FB, int(H * 0.029)), fill=GOLDD, anchor="mm")
    return card


photo_card(1080, 1350).save(os.path.join(OUT, "qr-card-photo.png"))

for fn in ("qr-plain.png", "qr-logo.png", "qr.svg", "qr-card.png",
           "qr-card-square.png", "qr-card-photo.png"):
    p = os.path.join(OUT, fn)
    print(f"{fn:20} {os.path.getsize(p):>8,} bytes")
print("OK ->", OUT)
