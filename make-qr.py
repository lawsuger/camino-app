# /// script
# requires-python = ">=3.9"
# dependencies = ["qrcode[pil]>=7.4", "pillow>=10"]
# ///
"""產生朝聖之路 App 的 QR Code 與分享卡。
卡片底圖 qr/bg-pilgrims.jpg = Alto del Perdón 鐵雕朝聖者（Unsplash 免費授權）。
輸出：qr-plain / qr-logo / qr.svg
      qr-card(-square)        乾淨版
      qr-card-photo(-square)  真實照片版（兩位朝聖者 + Camino 地標）
      qr-card-illust(-square) 旅行海報插畫版
用法：uv run make-qr.py"""
import os
import math
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.svg import SvgPathImage
from PIL import Image, ImageDraw, ImageFont, ImageOps

URL = "https://lawsuger.github.io/camino-app/"
T_MAIN = "竹孟之家的朝聖之路"
T_SUB = "人生上下半場新鮮人"
T_TAG = "800 公里的初登場及再出發"
KICKER = "C A M I N O   F R A N C É S"
URL_TEXT = "lawsuger.github.io/camino-app"
CAP = "掃描開啟 · 加到主畫面當離線 App"
IG_TEXT = "@harbor.__.0618 · @sugarlee0129"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr")
BG = os.path.join(OUT, "bg-pilgrims.jpg")
os.makedirs(OUT, exist_ok=True)

NAVY = (22, 48, 73); NAVY2 = (27, 48, 73)
GOLD = (242, 183, 5); GOLDD = (198, 138, 24)
MUTED = (120, 111, 98); CREAM = (250, 247, 240)
WHITE = (255, 255, 255); FRAME = (228, 214, 176)
FB = r"C:\Windows\Fonts\msjhbd.ttc"
FR = r"C:\Windows\Fonts\msjh.ttc"
_M = ImageDraw.Draw(Image.new("RGB", (4, 4)))


def f(p, s): return ImageFont.truetype(p, s)


def fit(text, p, maxw, start, mn=32):
    s = start
    while s > mn and _M.textlength(text, font=f(p, s)) > maxw:
        s -= 2
    return f(p, s)


def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def scallop(size):
    fr = size / 512.0
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    apex = (256 * fr, 406 * fr)
    dome = [(146, 205), (168, 150), (210, 120), (256, 108), (302, 120), (344, 150), (366, 205)]
    dome = [(x * fr, y * fr) for x, y in dome]
    d.polygon([apex] + dome, fill=GOLD)
    for p in dome:
        d.line([apex, p], fill=NAVY, width=max(2, int(7 * fr)))
    r = 7 * fr
    d.ellipse([apex[0] - r, apex[1] - r, apex[0] + r, apex[1] + r], fill=NAVY)
    return im


def ig_glyph(d, cx, cy, s, color):
    r = s / 2; w = max(2, int(s * 0.1))
    d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=s * 0.30, outline=color, width=w)
    cr = s * 0.27
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=color, width=w)
    dr = s * 0.075; dx, dy = cx + r * 0.46, cy - r * 0.46
    d.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=color)


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
    ImageDraw.Draw(card).rounded_rectangle(
        [fx - 24, top - 24, fx + size + 24, top + size + 24], radius=30, fill=WHITE, outline=FRAME, width=3)
    card.paste(qr_logo(size), (fx, top))
    return top + size + 24


def footer(card, W, H, y):
    d = ImageDraw.Draw(card)
    d.text((W / 2, y), CAP, font=f(FB, int(H * 0.0225)), fill=NAVY, anchor="mm")
    y += int(H * 0.037)
    d.text((W / 2, y), URL_TEXT, font=f(FB, int(H * 0.029)), fill=GOLDD, anchor="mm")
    y += int(H * 0.036)
    gs = int(H * 0.026); igf = f(FB, int(H * 0.0215))
    tw = _M.textlength(IG_TEXT, font=igf); gap = int(H * 0.011)
    sx = W / 2 - (gs + gap + tw) / 2
    ig_glyph(d, sx + gs / 2, y, gs, NAVY)
    d.text((sx + gs + gap, y), IG_TEXT, font=igf, fill=NAVY, anchor="lm")


# ---------- 乾淨版 ----------
def clean_card(W, H):
    card = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(card)
    band = int(H * 0.150)
    d.rectangle([0, 0, W, band], fill=NAVY2)
    ss = int(band * 0.46); sh = scallop(ss)
    card.paste(sh, (int(W / 2 - ss / 2), int(band * 0.13)), sh)
    d.text((W / 2, band * 0.83), KICKER, font=f(FB, int(band * 0.135)), fill=GOLD, anchor="mm")
    y = band + int(H * 0.052)
    d.text((W / 2, y), T_MAIN, font=fit(T_MAIN, FB, W - 150, int(H * 0.062)), fill=NAVY, anchor="mm")
    y += int(H * 0.040)
    d.rounded_rectangle([W / 2 - 66, y - 3, W / 2 + 66, y + 3], radius=3, fill=GOLD)
    y += int(H * 0.032)
    d.text((W / 2, y), T_SUB, font=f(FB, int(H * 0.030)), fill=GOLDD, anchor="mm")
    y += int(H * 0.031)
    d.text((W / 2, y), T_TAG, font=f(FR, int(H * 0.024)), fill=MUTED, anchor="mm")
    qsz = int(min(W * 0.47, H * 0.37))
    bottom = framed_qr(card, qsz, W / 2, y + int(H * 0.036))
    footer(card, W, H, bottom + int(H * 0.038))
    return card


clean_card(1080, 1350).save(os.path.join(OUT, "qr-card.png"))
clean_card(1080, 1080).save(os.path.join(OUT, "qr-card-square.png"))


# ---------- 場景版（真實照片 / 插畫共用版型）----------
def scene_photo(W, H):
    return ImageOps.fit(Image.open(BG).convert("RGB"), (W, H), method=Image.LANCZOS, centering=(0.42, 0.46))


def scene_card(W, H, sq, scene_fn):
    card = Image.new("RGB", (W, H), CREAM)
    sceneH = int(H * (0.50 if sq else 0.55))
    card.paste(scene_fn(W, sceneH), (0, 0))
    sh = int(sceneH * 0.62)
    scrim = Image.new("L", (W, sh), 0)
    sd = ImageDraw.Draw(scrim)
    for yy in range(sh):
        sd.line([(0, yy), (W, yy)], fill=int(165 * (1 - yy / sh)))
    card.paste((10, 18, 34), (0, 0, W, sh), scrim)
    d = ImageDraw.Draw(card)

    def st(xy, t, fo, fi):
        d.text((xy[0] + 2, xy[1] + 2), t, font=fo, fill=(0, 0, 0), anchor="mm")
        d.text(xy, t, font=fo, fill=fi, anchor="mm")

    es = int(H * 0.040); semb = scallop(es)
    card.paste(semb, (int(W / 2 - es / 2), int(H * (0.030 if sq else 0.034))), semb)
    st((W / 2, int(H * (0.090 if sq else 0.096))), KICKER, f(FB, int(H * 0.021)), GOLD)
    st((W / 2, int(H * (0.140 if sq else 0.150))), T_MAIN, fit(T_MAIN, FB, W - 130, int(H * 0.060)), WHITE)
    st((W / 2, int(H * (0.186 if sq else 0.200))), T_SUB, f(FB, int(H * 0.028)), (248, 230, 196))
    st((W / 2, int(H * (0.222 if sq else 0.238))), T_TAG, f(FB, int(H * 0.024)), (245, 208, 124))
    qsz = int(W * (0.28 if sq else 0.32))
    bottom = framed_qr(card, qsz, W / 2, sceneH + int(H * 0.028))
    footer(card, W, H, bottom + int(H * 0.036))
    return card


scene_card(1080, 1350, False, scene_photo).save(os.path.join(OUT, "qr-card-photo.png"))
scene_card(1080, 1080, True, scene_photo).save(os.path.join(OUT, "qr-card-photo-square.png"))


# ---------- 插畫版場景 ----------
def cypress(d, x, base, h, w):
    d.rectangle([x - w * 0.09, base - h * 0.12, x + w * 0.09, base], fill=(74, 58, 42))
    d.ellipse([x - w / 2, base - h, x + w / 2, base - h * 0.05], fill=(48, 86, 56))
    d.ellipse([x - w / 2, base - h, x + w * 0.05, base - h * 0.05], fill=(40, 76, 48))


def house(d, x, y, w, h, wall=(240, 230, 208), roof=(198, 104, 70)):
    d.rectangle([x, y, x + w, y + h], fill=wall)
    d.polygon([(x - w * 0.08, y), (x + w * 1.08, y), (x + w / 2, y - h * 0.55)], fill=roof)


def pilgrim_color(d, cx, feet, h, pack):
    hr = h * 0.11; top = feet - h; lw = h * 0.10
    d.rounded_rectangle([cx - lw * 1.3, feet - h * 0.44, cx - lw * 0.1, feet], radius=lw * 0.5, fill=(54, 60, 72))
    d.rounded_rectangle([cx + lw * 0.1, feet - h * 0.44, cx + lw * 1.3, feet], radius=lw * 0.5, fill=(46, 52, 64))
    d.line([(cx + h * 0.23, feet + h * 0.01), (cx + h * 0.23, top - hr * 0.4)], fill=(150, 116, 74), width=max(2, int(h * 0.028)))
    d.rounded_rectangle([cx - h * 0.15, top + 1.7 * hr, cx + h * 0.15, feet - h * 0.38], radius=h * 0.05, fill=(64, 76, 92))
    d.rounded_rectangle([cx - h * 0.18, top + 1.6 * hr, cx + h * 0.18, top + 1.6 * hr + h * 0.42], radius=h * 0.07, fill=pack)
    d.ellipse([cx - hr, top, cx + hr, top + 2 * hr], fill=(70, 60, 58))
    d.chord([cx - hr * 1.1, top - hr * 0.3, cx + hr * 1.1, top + hr * 1.0], 180, 360, fill=(236, 210, 152))
    d.ellipse([cx - hr * 1.6, top + hr * 0.55, cx + hr * 1.6, top + hr * 1.15], fill=(236, 210, 152))


def poster_scene(W, H):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    hz = int(H * 0.45)
    sky = [(60, 92, 150), (104, 126, 178), (188, 156, 152), (240, 170, 120), (252, 216, 156)]
    for y in range(hz):
        seg = (y / hz) * (len(sky) - 1); i = min(int(seg), len(sky) - 2)
        d.line([(0, y), (W, y)], fill=lerp(sky[i], sky[i + 1], seg - i))
    sx, sy, R = int(W * 0.63), int(hz * 0.82), int(W * 0.095)
    for r in range(R, 0, -1):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=lerp((255, 246, 214), (252, 200, 120), r / R))
    d.polygon([(0, hz), (W * 0.18, hz - H * 0.05), (W * 0.34, hz - H * 0.015), (W * 0.52, hz - H * 0.06),
               (W * 0.7, hz - H * 0.02), (W * 0.86, hz - H * 0.055), (W, hz - H * 0.02), (W, hz)], fill=(126, 144, 178))
    for frac, col in [(0.0, (176, 182, 96)), (0.13, (120, 156, 78)), (0.30, (200, 186, 104)),
                      (0.52, (104, 142, 70)), (0.76, (156, 170, 86))]:
        ytop = hz + int((H - hz) * frac)
        pts = [(0, H)] + [(x, ytop + int(math.sin(x * 0.007 + frac * 6) * 9)) for x in range(0, W + 1, 18)] + [(W, H)]
        d.polygon(pts, fill=col)
    vx, vy = int(W * 0.30), hz + int(H * 0.02)
    house(d, vx, vy, int(W * 0.05), int(H * 0.03)); house(d, vx + int(W * 0.06), vy + int(H * 0.006), int(W * 0.04), int(H * 0.025))
    house(d, vx - int(W * 0.055), vy + int(H * 0.004), int(W * 0.04), int(H * 0.026))
    d.polygon([(int(W * 0.32), hz + int(H * 0.02)), (int(W * 0.30), hz + int(H * 0.02)), (int(W * 0.34), int(H * 0.66)),
               (int(W * 0.20), H), (int(W * 0.62), H), (int(W * 0.50), int(H * 0.66)), (int(W * 0.345), hz + int(H * 0.02))], fill=(228, 214, 176))
    cypress(d, int(W * 0.075), int(H * 0.82), int(H * 0.42), int(W * 0.085))
    cypress(d, int(W * 0.90), int(H * 0.70), int(H * 0.26), int(W * 0.07))
    wx, wb, ws = int(W * 0.36), int(H * 0.74), int(H * 0.075)
    d.rounded_rectangle([wx - ws * 0.32, wb - ws, wx + ws * 0.32, wb], radius=ws * 0.12, fill=(238, 233, 222))
    d.rectangle([wx - ws * 0.32, wb - ws, wx + ws * 0.32, wb - ws * 0.55], fill=(40, 86, 140))
    d.polygon([(wx - ws * 0.16, wb - ws * 0.86), (wx + ws * 0.12, wb - ws * 0.78), (wx - ws * 0.16, wb - ws * 0.70)], fill=(244, 202, 44))
    pilgrim_color(d, int(W * 0.49), int(H * 0.84), int(H * 0.165), (216, 96, 46))
    pilgrim_color(d, int(W * 0.57), int(H * 0.88), int(H * 0.185), (58, 122, 120))
    return img


scene_card(1080, 1350, False, poster_scene).save(os.path.join(OUT, "qr-card-illust.png"))
scene_card(1080, 1080, True, poster_scene).save(os.path.join(OUT, "qr-card-illust-square.png"))

for fn in ("qr-plain.png", "qr-logo.png", "qr.svg", "qr-card.png", "qr-card-square.png",
           "qr-card-photo.png", "qr-card-photo-square.png", "qr-card-illust.png", "qr-card-illust-square.png"):
    p = os.path.join(OUT, fn)
    print(f"{fn:26} {os.path.getsize(p):>8,} bytes")
print("OK ->", OUT)
