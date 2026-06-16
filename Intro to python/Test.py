from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import math, io

# ── Palette ────────────────────────────────────────────────────────────────
MIDNIGHT   = HexColor("#0D0B2A")   # deep navy
DEEP_BLUE  = HexColor("#1A1650")
PURPLE     = HexColor("#3B2E8C")
LAVENDER   = HexColor("#7B68D9")
SOFT_LILAC = HexColor("#C5B8F5")
BLUSH      = HexColor("#F4C6D7")
GOLD       = HexColor("#F5D87C")
GOLD_DARK  = HexColor("#E0A830")
TEAL       = HexColor("#4ECDC4")
MINT       = HexColor("#A8EDD4")
CORAL      = HexColor("#FF8B6A")
WARM_WHITE = HexColor("#FFF8F0")
STAR_WHITE = HexColor("#FFF9E6")

W, H = letter   # 612 × 792

# ── Helper: draw stars ──────────────────────────────────────────────────────
def draw_stars(c, count=40, seed=0, color=None, alpha=0.6):
    import random
    rng = random.Random(seed)
    for _ in range(count):
        x = rng.uniform(10, W-10)
        y = rng.uniform(10, H-10)
        r = rng.uniform(0.5, 2.5)
        col = color or HexColor("#FFFFFF")
        c.setFillColor(col)
        c.setFillAlpha(rng.uniform(0.3, alpha))
        c.circle(x, y, r, fill=1, stroke=0)
    c.setFillAlpha(1)

def draw_sparkle(c, cx, cy, size=8, color=None):
    col = color or GOLD
    c.setFillColor(col)
    c.setStrokeColor(col)
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        length = size if angle % 90 == 0 else size * 0.6
        x1 = cx + math.cos(rad) * 2
        y1 = cy + math.sin(rad) * 2
        x2 = cx + math.cos(rad) * length
        y2 = cy + math.sin(rad) * length
        c.setLineWidth(1.2)
        c.line(x1, y1, x2, y2)

def night_bg(c, dark=MIDNIGHT, light=DEEP_BLUE):
    c.setFillColor(dark)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # subtle gradient bands
    for i in range(8):
        alpha = 0.04 * (i + 1)
        c.setFillColor(light)
        c.setFillAlpha(alpha)
        c.rect(0, H * i / 8, W, H / 8, fill=1, stroke=0)
    c.setFillAlpha(1)

def light_bg(c, color=WARM_WHITE):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def draw_moon(c, cx, cy, r=45):
    c.setFillColor(GOLD)
    c.setFillAlpha(0.9)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(DEEP_BLUE)
    c.setFillAlpha(0.8)
    c.circle(cx + r * 0.4, cy + r * 0.1, r * 0.78, fill=1, stroke=0)
    c.setFillAlpha(1)

def draw_little_door(c, x, y, w=60, h=80, color=CORAL):
    """Draw a tiny arched door."""
    # door frame
    c.setFillColor(GOLD_DARK)
    c.rect(x-3, y-3, w+6, h+6, fill=1, stroke=0)
    # door body
    c.setFillColor(color)
    c.rect(x, y, w, h, fill=1, stroke=0)
    # arch top
    c.arc(x, y + h - w/2, x + w, y + h + w/2, startAng=0, extent=180)
    c.setFillColor(color)
    c.circle(x + w/2, y + h, w/2, fill=1, stroke=0)
    # door knob
    c.setFillColor(GOLD)
    c.circle(x + w * 0.75, y + h * 0.45, 4, fill=1, stroke=0)
    # glow
    c.setFillColor(GOLD)
    c.setFillAlpha(0.15)
    c.circle(x + w/2, y + h/2, w * 1.4, fill=1, stroke=0)
    c.setFillAlpha(1)

def draw_luna_silhouette(c, cx, cy, scale=1.0):
    """Simple stylized girl silhouette."""
    # body
    c.setFillColor(LAVENDER)
    # dress
    p = c.beginPath()
    p.moveTo(cx - 22*scale, cy)
    p.lineTo(cx - 30*scale, cy - 60*scale)
    p.lineTo(cx + 30*scale, cy - 60*scale)
    p.lineTo(cx + 22*scale, cy)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    # torso
    c.setFillColor(SOFT_LILAC)
    c.rect(cx - 12*scale, cy, 24*scale, 30*scale, fill=1, stroke=0)
    # head
    c.setFillColor(HexColor("#F5C5A3"))
    c.circle(cx, cy + 45*scale, 20*scale, fill=1, stroke=0)
    # hair
    c.setFillColor(HexColor("#3D2314"))
    c.circle(cx, cy + 50*scale, 20*scale, fill=1, stroke=0)
    c.setFillColor(HexColor("#3D2314"))
    p = c.beginPath()
    p.moveTo(cx - 20*scale, cy + 40*scale)
    p.lineTo(cx - 28*scale, cy + 10*scale)
    p.lineTo(cx - 14*scale, cy + 30*scale)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    # stars on dress
    for sx, sy in [(-8, -20), (8, -35), (-3, -50)]:
        c.setFillColor(GOLD)
        c.circle(cx + sx*scale, cy + sy*scale, 2*scale, fill=1, stroke=0)

def centered_text(c, text, y, font="Helvetica-Bold", size=14, color=white, max_w=None, leading=None):
    c.setFillColor(color)
    c.setFont(font, size)
    if max_w:
        # wrap manually
        words = text.split()
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, font, size) <= max_w:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        lh = leading or size * 1.35
        start_y = y + lh * (len(lines)-1) / 2
        for i, ln in enumerate(lines):
            c.drawCentredString(W/2, start_y - i*lh, ln)
    else:
        c.drawCentredString(W/2, y, text)

def section_header(c, text, y, color=GOLD):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W/2, y, text)
    # decorative line
    lw = c.stringWidth(text, "Helvetica-Bold", 22) + 40
    c.setStrokeColor(color)
    c.setLineWidth(1.5)
    c.line(W/2 - lw/2, y-6, W/2 + lw/2, y-6)

def body_text_box(c, lines, x, y, w, color=WARM_WHITE, font="Helvetica", size=12, line_h=18):
    c.setFillColor(color)
    c.setFont(font, size)
    for i, ln in enumerate(lines):
        c.drawString(x, y - i*line_h, ln)

def rounded_rect(c, x, y, w, h, r=12, fill_color=None, stroke_color=None, lw=1.5):
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, fill=1 if fill_color else 0, stroke=1 if stroke_color else 0)

def decorative_border(c, color=GOLD, lw=2.5):
    margin = 18
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.setStrokeAlpha(0.4)
    c.roundRect(margin, margin, W-2*margin, H-2*margin, 10, fill=0, stroke=1)
    c.setStrokeAlpha(1)
    # corner stars
    for cx2, cy2 in [(margin+12, margin+12), (W-margin-12, margin+12),
                     (margin+12, H-margin-12), (W-margin-12, H-margin-12)]:
        draw_sparkle(c, cx2, cy2, size=7, color=color)

def page_number(c, n, color=SOFT_LILAC):
    c.setFillColor(color)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, 22, str(n))

# ── PAGE BUILDERS ────────────────────────────────────────────────────────────

def page_cover(c):
    night_bg(c)
    draw_stars(c, 80, seed=1, alpha=0.9)
    # big moon top-right
    draw_moon(c, W-90, H-90, r=60)
    # floating sparkles
    for px, py, sz in [(120,650,10),(480,600,8),(60,500,6),(520,700,7),(300,720,9)]:
        draw_sparkle(c, px, py, size=sz, color=GOLD)
    # Luna silhouette
    draw_luna_silhouette(c, W/2, 240, scale=1.3)
    # Tiny door inside "pocket" area at hem of dress
    draw_little_door(c, W/2 - 8, 185, w=50, h=68, color=CORAL)
    # glow from door
    c.setFillColor(GOLD)
    c.setFillAlpha(0.08)
    c.circle(W/2 + 17, 219, 80, fill=1, stroke=0)
    c.setFillAlpha(1)

    # Title badge
    rounded_rect(c, 80, 96, W-160, 100, r=16,
                 fill_color=HexColor("#1A1650"), stroke_color=GOLD, lw=2)
    c.setFillAlpha(0.3)
    c.setFillColor(PURPLE)
    c.roundRect(80, 96, W-160, 100, 16, fill=1, stroke=0)
    c.setFillAlpha(1)

    centered_text(c, "Luna and the", 182, size=18, color=SOFT_LILAC)
    centered_text(c, "Midnight Pocket", 153, font="Helvetica-Bold", size=34, color=GOLD)
    # subtitle
    c.setFillColor(BLUSH)
    c.setFont("Helvetica-Oblique", 14)
    c.drawCentredString(W/2, 112, "A Tiny Door, a Big Imagination")

    # tagline at top
    c.setFillColor(MINT)
    c.setFont("Helvetica", 10)
    c.drawCentredString(W/2, H-28, "✦  A Children's Story Guide  ✦")

    decorative_border(c, color=GOLD)


def page_welcome(c):
    night_bg(c, dark=HexColor("#100D2E"), light=DEEP_BLUE)
    draw_stars(c, 50, seed=2)
    draw_moon(c, 80, H-80, r=38)
    decorative_border(c, color=LAVENDER)

    section_header(c, "Welcome, Little Dreamer!", H-80, color=GOLD)

    draw_luna_silhouette(c, W - 115, 320, scale=0.85)

    # intro card
    rounded_rect(c, 50, 140, W-260, 480, r=14,
                 fill_color=HexColor("#1E1A4A"), stroke_color=LAVENDER, lw=1.5)

    intro_lines = [
        "This is the story of Luna —",
        "a quiet, dreamy seven-year-old",
        "who discovers something magical",
        "sewn right inside her pajama pocket.",
        "",
        "Every night at midnight, a tiny",
        "door appears. And on the other",
        "side? A whole miniature world",
        "waiting just for her.",
        "",
        "Luna is shy. She worries. She",
        "sometimes feels too small for",
        "the big, noisy world around her.",
        "",
        "But the Pocket World sees her",
        "differently — as a hero.",
        "",
        "Join Luna on 7 adventures that",
        "will change her forever.",
    ]
    body_text_box(c, intro_lines, 72, 590, 200, color=WARM_WHITE, size=12, line_h=19)

    # sparkles
    for sx, sy in [(W-55, 200),(W-35, 350),(W-70, 450)]:
        draw_sparkle(c, sx, sy, size=6, color=GOLD)

    page_number(c, 2)


def page_meet_luna(c):
    light_bg(c, HexColor("#F0EDF9"))
    # soft top band
    c.setFillColor(DEEP_BLUE)
    c.rect(0, H-140, W, 140, fill=1, stroke=0)
    draw_stars(c, 30, seed=3, alpha=0.7)

    section_header(c, "Meet Luna", H-75, color=GOLD)

    # Luna big illustration area
    c.setFillColor(SOFT_LILAC)
    c.setFillAlpha(0.25)
    c.circle(W/2, 500, 110, fill=1, stroke=0)
    c.setFillAlpha(1)
    draw_luna_silhouette(c, W/2, 460, scale=1.5)

    # Trait bubbles
    traits = [
        ("🌙  Dreamy", 120, 360),
        ("🌿  Kind", 440, 360),
        ("⭐  Brave", 80, 240),
        ("🦋  Curious", 460, 240),
        ("💫  Quiet", 270, 185),
    ]
    for label, bx, by in traits:
        rounded_rect(c, bx-50, by-16, 110, 32, r=16,
                     fill_color=LAVENDER, stroke_color=GOLD, lw=1.5)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(bx + 5, by - 8, label)

    # description
    desc = [
        "Luna is 7 years old. She has big dark eyes",
        "that notice everything, tangled braids she",
        "never quite tames, and a pajama set covered",
        "in tiny crescent moons.",
        "",
        "At school she sits near the window. At home",
        "she fills notebooks with drawings of places",
        "that don't exist yet — at least, not until",
        "the clock strikes midnight.",
    ]
    body_text_box(c, desc, 55, 140, 500, color=MIDNIGHT, size=11, line_h=17)
    page_number(c, 3)


def page_the_door(c):
    night_bg(c)
    draw_stars(c, 60, seed=4)
    decorative_border(c, color=TEAL)

    section_header(c, "The Tiny Door", H-70, color=TEAL)

    # Big door illustration centered
    draw_little_door(c, W/2 - 55, 350, w=110, h=148, color=CORAL)
    # glow rings
    for r, alpha in [(90, 0.06), (130, 0.04), (175, 0.025)]:
        c.setFillColor(GOLD)
        c.setFillAlpha(alpha)
        c.circle(W/2, 424, r, fill=1, stroke=0)
    c.setFillAlpha(1)

    # floating sparkles around door
    for angle in range(0, 360, 40):
        rad = math.radians(angle)
        px = W/2 + math.cos(rad) * 160
        py = 424 + math.sin(rad) * 100
        draw_sparkle(c, px, py, size=5, color=GOLD)

    # description card
    rounded_rect(c, 45, 55, W-90, 270, r=14,
                 fill_color=HexColor("#1A1650"), stroke_color=TEAL, lw=1.5)
    door_lines = [
        "Rules of the Midnight Door:",
        "",
        "  ✦  It only appears at midnight.",
        "  ✦  It is no bigger than a playing card.",
        "  ✦  It glows gold when Luna is near.",
        "  ✦  Only Luna can open it.",
        "  ✦  Time inside moves differently —",
        "       a whole adventure fits in one night.",
        "  ✦  Whatever courage she finds inside...",
        "       she carries with her when she wakes.",
    ]
    body_text_box(c, door_lines, 68, 295, W-136, color=WARM_WHITE, size=11, line_h=18)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(68, 310, "Rules of the Midnight Door:")
    page_number(c, 4)


def adventure_page(c, num, title, setting, challenge, what_luna_does, lesson, bg_color, accent, seed):
    night_bg(c, dark=bg_color, light=HexColor("#1A1650"))
    draw_stars(c, 45, seed=seed, color=STAR_WHITE, alpha=0.7)
    decorative_border(c, color=accent)

    # adventure badge
    c.setFillColor(accent)
    c.circle(W/2, H-65, 28, fill=1, stroke=0)
    c.setFillColor(MIDNIGHT)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W/2, H-71, str(num))
    c.setFillColor(WARM_WHITE)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, H-90, "ADVENTURE")

    # Title
    centered_text(c, title, H-118, font="Helvetica-Bold", size=20, color=accent, max_w=W-120)

    # Illustration zone (stylized)
    c.setFillColor(accent)
    c.setFillAlpha(0.1)
    c.roundRect(W/2 - 100, H-300, 200, 155, 20, fill=1, stroke=0)
    c.setFillAlpha(1)
    draw_luna_silhouette(c, W/2, H-205, scale=0.75)
    draw_sparkle(c, W/2 + 60, H-170, size=9, color=accent)
    draw_sparkle(c, W/2 - 55, H-190, size=7, color=GOLD)

    # Info cards
    cards = [
        ("🌍  Setting", setting, 380),
        ("⚡  Challenge", challenge, 280),
        ("💪  Luna Does", what_luna_does, 180),
        ("💡  She Learns", lesson, 80),
    ]
    for label, text, y in cards:
        rounded_rect(c, 45, y, W-90, 82, r=10,
                     fill_color=HexColor("#12103A"), stroke_color=accent, lw=1)
        c.setFillColor(accent)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(62, y+62, label)
        # wrap text
        c.setFillColor(WARM_WHITE)
        c.setFont("Helvetica", 10)
        words = text.split()
        line = ""
        lines_out = []
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, "Helvetica", 10) <= W - 124:
                line = test
            else:
                lines_out.append(line)
                line = w
        if line:
            lines_out.append(line)
        for i, ln in enumerate(lines_out[:3]):
            c.drawString(62, y + 45 - i*14, ln)

    page_number(c, 4 + num)


def page_the_world(c):
    night_bg(c, dark=HexColor("#0A1A2E"), light=HexColor("#1A2E50"))
    draw_stars(c, 55, seed=10)
    decorative_border(c, color=MINT)

    section_header(c, "The Pocket World", H-70, color=MINT)

    # world zones
    zones = [
        ("Dewdrop Forest", "Trees as tall as thimbles, lit by firefly lanterns.", TEAL, 310, 580),
        ("Pebble Mountains", "Rocky peaks where tiny dragons sleep in crystal caves.", LAVENDER, 310, 460),
        ("Cloud Meadow", "Soft, floating islands where dream-sheep roam free.", BLUSH, 310, 340),
        ("The Glowing River", "A stream of liquid moonlight — it sings as it flows.", GOLD, 310, 220),
        ("Mirror Lake Village", "A town of creatures who've never met a human before.", CORAL, 310, 100),
    ]
    for name, desc, color, x, y in zones:
        rounded_rect(c, 45, y, W-90, 72, r=10,
                     fill_color=HexColor("#0D1F3C"), stroke_color=color, lw=1.5)
        draw_sparkle(c, 68, y+36, size=7, color=color)
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(88, y+46, name)
        c.setFillColor(WARM_WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(88, y+28, desc)

    page_number(c, 12)


def page_characters(c):
    light_bg(c, HexColor("#EFF0FB"))
    c.setFillColor(DEEP_BLUE)
    c.rect(0, H-130, W, 130, fill=1, stroke=0)
    draw_stars(c, 25, seed=11, alpha=0.7)

    section_header(c, "Friends in the Pocket World", H-75, color=GOLD)

    chars = [
        ("Pip", "A tiny fox with a broken compass.\nAlways lost, always cheerful.", CORAL, 90, 560),
        ("Moss", "An ancient frog who speaks in riddles.\nGuardian of the Glowing River.", TEAL, 330, 560),
        ("Twill", "A moth with torn wings who paints\nstars onto cave ceilings.", LAVENDER, 90, 390),
        ("The Hush", "A gentle shadow creature who is\nscared of its own echo.", BLUSH, 330, 390),
        ("Captain Nim", "Tiniest knight in the land.\nBig feelings, small armor.", GOLD, 90, 220),
        ("Elder Lumen", "A firefly who remembers every\nstory ever told at midnight.", MINT, 330, 220),
    ]
    for name, desc, color, cx, cy in chars:
        rounded_rect(c, cx-70, cy-60, 200, 130, r=14,
                     fill_color=white, stroke_color=color, lw=2)
        # colored dot icon
        c.setFillColor(color)
        c.circle(cx-42, cy+22, 16, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(cx-42, cy+18, name[0])
        # name
        c.setFillColor(MIDNIGHT)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(cx-18, cy+30, name)
        # desc
        c.setFillColor(HexColor("#333355"))
        c.setFont("Helvetica", 9)
        for i, ln in enumerate(desc.split("\n")):
            c.drawString(cx-18, cy+14 - i*14, ln)

    page_number(c, 13)


def page_theme_courage(c):
    night_bg(c)
    draw_stars(c, 50, seed=15)
    draw_moon(c, W-70, H-70, r=50)
    decorative_border(c, color=GOLD)

    section_header(c, "The Heart of the Story", H-75, color=GOLD)

    themes = [
        ("Courage", "Luna is afraid — of speaking up, of being wrong,\nof being seen. But every adventure asks her to be\nbrave anyway. She learns that courage isn't\n not being scared. It's acting while you are.", CORAL),
        ("Curiosity", "The Pocket World only opens to those who wonder.\nLuna's imagination is her superpower — it literally\nbuilds the worlds she explores. She learns that\nasking questions is never the wrong thing to do.", TEAL),
        ("Believing in Yourself", "Every creature Luna helps sees her as capable before\nshe sees it herself. By the final adventure, Luna starts\nto see it too — and carries that knowing back into\nher real, wide-awake life.", GOLD),
    ]

    y = H - 135
    for title2, text, color in themes:
        y -= 185
        rounded_rect(c, 45, y, W-90, 170, r=14,
                     fill_color=HexColor("#13112E"), stroke_color=color, lw=2)
        # icon circle
        c.setFillColor(color)
        c.circle(80, y+115, 20, fill=1, stroke=0)
        draw_sparkle(c, 80, y+115, size=9, color=white)
        # title
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(112, y+128, title2)
        # body
        c.setFillColor(WARM_WHITE)
        c.setFont("Helvetica", 10)
        for i, ln in enumerate(text.split("\n")):
            c.drawString(62, y+105 - i*16, ln)

    page_number(c, 14)


def page_adventure_map(c):
    night_bg(c, dark=HexColor("#0A0D2A"))
    draw_stars(c, 60, seed=20)
    decorative_border(c, color=GOLD)

    section_header(c, "Luna's Adventure Map", H-70, color=GOLD)
    c.setFillColor(SOFT_LILAC)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W/2, H-100, "Seven nights. Seven worlds. One brave girl.")

    adventures = [
        (1, "The Lost Compass",     CORAL,    W*0.18, 580),
        (2, "The Singing Storm",    TEAL,     W*0.5,  540),
        (3, "Dragon Lullaby",       LAVENDER, W*0.78, 575),
        (4, "The Invisible Bridge", GOLD,     W*0.15, 420),
        (5, "Stolen Starlight",     MINT,     W*0.5,  390),
        (6, "The Echo Caves",       BLUSH,    W*0.82, 430),
        (7, "Home Is the Bravest",  GOLD,     W*0.5,  240),
    ]

    # path line
    pts = [(a[3], a[4]) for a in adventures]
    c.setStrokeColor(GOLD)
    c.setStrokeAlpha(0.3)
    c.setLineWidth(2)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    c.drawPath(p, stroke=1, fill=0)
    c.setStrokeAlpha(1)

    for num, title3, color, ax, ay in adventures:
        c.setFillColor(color)
        c.circle(ax, ay, 22, fill=1, stroke=0)
        # glow
        c.setFillColor(color)
        c.setFillAlpha(0.15)
        c.circle(ax, ay, 34, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(MIDNIGHT)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(ax, ay-5, str(num))
        # label
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(ax, ay-38, title3)

    # Luna at start
    draw_luna_silhouette(c, pts[0][0] - 5, pts[0][1] - 45, scale=0.5)

    page_number(c, 15)


def page_real_world_connections(c):
    light_bg(c, HexColor("#F5F0FF"))
    c.setFillColor(DEEP_BLUE)
    c.rect(0, H-130, W, 130, fill=1, stroke=0)
    draw_stars(c, 20, seed=22, alpha=0.6)

    section_header(c, "Luna in Real Life", H-75, color=GOLD)

    c.setFillColor(WARM_WHITE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W/2, H-105, "How the Pocket World mirrors the real world")

    pairs = [
        ("In the Pocket World...", "In Real Life...", LAVENDER, CORAL),
        ("Luna speaks up for Pip\neven though she's scared.", "Luna raises her hand\nin class for the first time.", TEAL, MINT),
        ("Luna builds a bridge from\nsticks and moonbeam thread.", "Luna stops saying 'I can't'\nand tries the monkey bars.", CORAL, GOLD),
        ("Luna comforts The Hush\nwho is afraid of its shadow.", "Luna sits with the new kid\nat school who eats alone.", LAVENDER, BLUSH),
        ("Luna finds her voice to\nsing the Dragon to sleep.", "Luna performs her poem\nat the school assembly.", GOLD, TEAL),
    ]

    y = H-145
    for row in pairs:
        if len(row) == 4:
            left, right, c1, c2 = row
            y -= 95
            # left card
            rounded_rect(c, 40, y, W/2 - 55, 82, r=10, fill_color=white, stroke_color=c1, lw=1.5)
            c.setFillColor(c1)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(55, y+64, "In the Pocket World...")
            c.setFillColor(MIDNIGHT)
            c.setFont("Helvetica", 9)
            for i, ln in enumerate(left.split("\n")):
                c.drawString(55, y+48 - i*14, ln)
            # right card
            rounded_rect(c, W/2 + 15, y, W/2 - 55, 82, r=10, fill_color=white, stroke_color=c2, lw=1.5)
            c.setFillColor(c2)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(W/2+30, y+64, "In Real Life...")
            c.setFillColor(MIDNIGHT)
            c.setFont("Helvetica", 9)
            for i, ln in enumerate(right.split("\n")):
                c.drawString(W/2+30, y+48 - i*14, ln)
            # arrow
            c.setFillColor(GOLD)
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(W/2, y+32, "→")

    page_number(c, 16)


def page_discussion_questions(c):
    night_bg(c)
    draw_stars(c, 40, seed=25)
    draw_moon(c, 80, H-80, r=42)
    decorative_border(c, color=LAVENDER)

    section_header(c, "Talk About It!", H-75, color=LAVENDER)
    c.setFillColor(SOFT_LILAC)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W/2, H-105, "Questions to share with a grown-up or friend")

    questions = [
        ("1.", "Luna feels shy at school. Has there been a time\n   you felt shy? What happened?"),
        ("2.", "The Pocket World only opens for Luna.\n   What special world would open just for you?"),
        ("3.", "Luna is scared but goes through the door anyway.\n   What does that tell us about bravery?"),
        ("4.", "Which Pocket World creature is most like you?\n   Why did you choose that one?"),
        ("5.", "Luna's imagination is her superpower.\n   What do you think YOUR superpower is?"),
        ("6.", "At the end, Luna feels different at school.\n   What changed inside her? What helped?"),
        ("7.", "If you could give Luna one piece of advice,\n   what would you tell her?"),
    ]
    y = H - 140
    for num, q in questions:
        y -= 77
        rounded_rect(c, 45, y, W-90, 65, r=10,
                     fill_color=HexColor("#14103A"), stroke_color=LAVENDER, lw=1)
        c.setFillColor(LAVENDER)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(62, y+40, num)
        c.setFillColor(WARM_WHITE)
        c.setFont("Helvetica", 10)
        for i, ln in enumerate(q.split("\n")):
            c.drawString(84, y+40 - i*15, ln)

    page_number(c, 17)


def page_activity_draw(c):
    light_bg(c, HexColor("#FFF5F8"))
    c.setFillColor(DEEP_BLUE)
    c.rect(0, H-130, W, 130, fill=1, stroke=0)
    draw_stars(c, 22, seed=30, alpha=0.6)

    section_header(c, "Draw Your Own Door!", H-75, color=GOLD)
    c.setFillColor(WARM_WHITE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W/2, H-108, "Design the magical door that leads to YOUR world.")

    # big drawing box
    rounded_rect(c, 60, 190, W-120, H-360, r=16,
                 fill_color=white, stroke_color=LAVENDER, lw=2)
    # dotted hint lines inside
    c.setStrokeColor(SOFT_LILAC)
    c.setStrokeAlpha(0.4)
    c.setLineWidth(0.6)
    c.setDash([4, 6])
    for i in range(1, 6):
        yy = 190 + (H-360) * i / 6
        c.line(75, yy, W-75, yy)
    c.setDash([])
    c.setStrokeAlpha(1)

    # small door template
    draw_little_door(c, 68, 205, w=40, h=55, color=HexColor("#DDD0FF"))
    c.setFillColor(LAVENDER)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(68, 198, "example →")

    # instructions
    steps = [
        "✦  What color is your door?",
        "✦  What shape is it? (Round? Star-shaped? Wiggly?)",
        "✦  Does it have a handle? A knocker? A keyhole?",
        "✦  What glows or sparkles around it?",
        "✦  What world waits on the other side?",
    ]
    c.setFillColor(MIDNIGHT)
    c.setFont("Helvetica", 10)
    for i, s in enumerate(steps):
        c.drawString(60, 175 - i*16, s)

    page_number(c, 18)


def page_activity_journal(c):
    night_bg(c)
    draw_stars(c, 35, seed=33)
    decorative_border(c, color=TEAL)

    section_header(c, "Luna's Dream Journal", H-75, color=TEAL)
    c.setFillColor(SOFT_LILAC)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(W/2, H-100, "Write or draw your own midnight adventure here.")

    # journal page look
    rounded_rect(c, 50, 60, W-100, H-175, r=14,
                 fill_color=HexColor("#1A1650"), stroke_color=TEAL, lw=1.5)

    prompts = [
        "Tonight I dreamed I went to...",
        "The creatures I met were...",
        "They needed my help because...",
        "The bravest thing I did was...",
        "When I woke up I felt...",
    ]
    y = H - 160
    for prompt in prompts:
        c.setFillColor(TEAL)
        c.setFont("Helvetica-BoldOblique", 10)
        c.drawString(70, y, prompt)
        c.setStrokeColor(SOFT_LILAC)
        c.setStrokeAlpha(0.4)
        c.setLineWidth(0.8)
        c.line(70, y-12, W-70, y-12)
        c.line(70, y-28, W-70, y-28)
        c.setStrokeAlpha(1)
        y -= 80

    # moon doodle in corner
    draw_moon(c, W-80, 100, r=30)

    page_number(c, 19)


def page_brave_list(c):
    light_bg(c, HexColor("#F0FBF8"))
    c.setFillColor(DEEP_BLUE)
    c.rect(0, H-130, W, 130, fill=1, stroke=0)
    draw_stars(c, 18, seed=35, alpha=0.6)

    section_header(c, "My Brave List", H-75, color=TEAL)
    c.setFillColor(WARM_WHITE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W/2, H-105, "Luna kept a list of her brave moments. Now it's your turn!")

    # intro quote
    rounded_rect(c, 60, H-200, W-120, 60, r=10,
                 fill_color=HexColor("#E8FAFF"), stroke_color=TEAL, lw=1.5)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-BoldOblique", 11)
    c.drawCentredString(W/2, H-170, '"Every brave moment is worth writing down."')
    c.setFillColor(MIDNIGHT)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(W/2, H-188, "— Luna, Adventure #7")

    # checkboxes
    c.setFillColor(MIDNIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(62, H-228, "Things I was brave enough to do:")

    brave_items = [
        "I tried something new even though I was scared.",
        "I spoke up when it felt hard.",
        "I was kind to someone who seemed lonely.",
        "I kept going even when I wanted to quit.",
        "I asked for help when I needed it.",
        "I told someone how I really felt.",
        "I made a mistake and tried again anyway.",
        "I believed in myself, even for just a minute.",
    ]
    y = H - 260
    for item in brave_items:
        rounded_rect(c, 62, y-8, 22, 22, r=4, stroke_color=TEAL, lw=1.5)
        c.setFillColor(MIDNIGHT)
        c.setFont("Helvetica", 11)
        c.drawString(94, y+4, item)
        y -= 42

    # add your own
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(62, y+10, "My own brave moment:")
    c.setStrokeColor(TEAL)
    c.setStrokeAlpha(0.5)
    c.line(62, y-10, W-62, y-10)
    c.setStrokeAlpha(1)

    page_number(c, 20)


def page_for_grownups(c):
    light_bg(c, HexColor("#F8F5FF"))
    c.setFillColor(DEEP_BLUE)
    c.rect(0, H-130, W, 130, fill=1, stroke=0)
    draw_stars(c, 18, seed=40, alpha=0.5)

    section_header(c, "A Note for Grown-Ups", H-75, color=LAVENDER)

    rounded_rect(c, 50, 60, W-100, H-200, r=14,
                 fill_color=white, stroke_color=LAVENDER, lw=1.5)

    notes = [
        ("Why Luna's Story Matters", LAVENDER,
         "Children who struggle with shyness, anxiety, or low self-confidence\n"
         "often can't hear the advice 'just be brave.' But they can feel it —\n"
         "through a character who faces the same fears and finds a way through."),
        ("Reading Together", TEAL,
         "Read one adventure per night. Pause where Luna hesitates — ask\n"
         "'What do you think she should do?' This builds empathy and\n"
         "decision-making alongside the story."),
        ("Watch for Real-Life Moments", CORAL,
         "After reading, keep an ear out for small brave moments in your\n"
         "child's day. Name them: 'That was Luna-brave.' Connecting the\n"
         "story to real life deepens the impact."),
        ("If Your Child Feels Seen", GOLD,
         "Some children will recognize themselves in Luna immediately.\n"
         "If your child says 'That's like me' — that's magic. Honor it.\n"
         "Ask: 'What would Luna do next?' and 'What could YOU do?'"),
    ]

    y = H - 155
    for heading, color, text in notes:
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(68, y, heading)
        c.setFillColor(MIDNIGHT)
        c.setFont("Helvetica", 10)
        for i, ln in enumerate(text.split("\n")):
            c.drawString(68, y - 18 - i*15, ln)
        y -= 105

    page_number(c, 21)


def page_bonus_activities(c):
    night_bg(c)
    draw_stars(c, 50, seed=44)
    draw_moon(c, W-80, H-80, r=45)
    decorative_border(c, color=CORAL)

    section_header(c, "More Magic Activities", H-75, color=CORAL)

    activities = [
        ("🌙  Make a Midnight Pocket", CORAL,
         "Sew or draw a tiny pocket onto an old pair of pajamas. Hide\n"
         "a small folded note inside — your own 'door' message!"),
        ("⭐  Creature Creator", GOLD,
         "Design your own Pocket World creature. What is its name?\n"
         "What does it need? How will you help it?"),
        ("🦋  Courage Coins", TEAL,
         "Cut out small circles. Each time you do something brave,\n"
         "write it on a coin and drop it in a jar. Watch it fill up!"),
        ("🌿  The Pocket World Playlist", LAVENDER,
         "Choose 7 songs that feel like each of Luna's adventures.\n"
         "Play them at bedtime as you re-read each chapter."),
        ("✨  Write Chapter 8", MINT,
         "What happens on Luna's EIGHTH night? Create your own\n"
         "adventure — setting, creature, challenge, and lesson!"),
    ]

    y = H - 130
    for label, color, desc in activities:
        y -= 105
        rounded_rect(c, 45, y, W-90, 90, r=12,
                     fill_color=HexColor("#120F30"), stroke_color=color, lw=1.5)
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(65, y+64, label)
        c.setFillColor(WARM_WHITE)
        c.setFont("Helvetica", 10)
        for i, ln in enumerate(desc.split("\n")):
            c.drawString(65, y+46 - i*15, ln)

    page_number(c, 22)


def page_quotes(c):
    night_bg(c)
    draw_stars(c, 65, seed=50)
    draw_moon(c, W/2, H-60, r=50)
    decorative_border(c, color=GOLD)

    section_header(c, "Words to Remember", H-130, color=GOLD)

    quotes_data = [
        ('"The door only opens\nfor those who are willing\nto be a little afraid."', TEAL, 530),
        ('"You don\'t need to be fearless.\nYou just need to be\none step braver than before."', LAVENDER, 380),
        ('"Your imagination isn\'t\nrunning away from the world.\nIt\'s running toward something better."', CORAL, 230),
        ('"Home is the bravest\nplace of all."', GOLD, 100),
    ]

    for quote, color, y in quotes_data:
        c.setFillColor(color)
        c.setFillAlpha(0.1)
        c.roundRect(55, y-10, W-110, len(quote.split("\n"))*22+20, 8, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(color)
        c.setFont("Helvetica-BoldOblique", 13)
        lines2 = quote.split("\n")
        base_y = y + (len(lines2)-1)*22 + 6
        for i, ln in enumerate(lines2):
            c.drawCentredString(W/2, base_y - i*22, ln)

    page_number(c, 23)


def page_closing(c):
    night_bg(c, dark=MIDNIGHT, light=HexColor("#1A1650"))
    draw_stars(c, 80, seed=55, alpha=0.85)
    draw_moon(c, W/2, H-90, r=65)
    decorative_border(c, color=GOLD)

    # Luna center, larger
    draw_luna_silhouette(c, W/2, 340, scale=1.6)
    draw_little_door(c, W/2 - 10, 230, w=55, h=74, color=CORAL)

    # glow
    c.setFillColor(GOLD)
    c.setFillAlpha(0.07)
    c.circle(W/2, 340, 200, fill=1, stroke=0)
    c.setFillAlpha(1)

    # sparkles
    for px, py, sz in [(W/2-130, 420, 10),(W/2+140, 400, 8),(W/2-90, 550, 6),(W/2+80, 560, 7)]:
        draw_sparkle(c, px, py, size=sz, color=GOLD)

    centered_text(c, "Sweet dreams, brave dreamer.", 185,
                  font="Helvetica-BoldOblique", size=18, color=GOLD)
    centered_text(c, "Your pocket is waiting.", 158,
                  font="Helvetica-Oblique", size=14, color=SOFT_LILAC)

    c.setFillColor(BLUSH)
    c.setFont("Helvetica", 10)
    c.drawCentredString(W/2, 80, "Luna and the Midnight Pocket  ✦  A Children's Story Guide")
    c.drawCentredString(W/2, 62, "Designed to inspire courage, curiosity, and self-belief")

    page_number(c, 24)


# ── MAIN BUILD ──────────────────────────────────────────────────────────────

def build():
    path = "/mnt/user-data/outputs/Luna_and_the_Midnight_Pocket.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.setTitle("Luna and the Midnight Pocket")
    c.setAuthor("Story Guide")
    c.setSubject("A Children's Story Guide: Courage, Curiosity, Believing in Yourself")

    # 1. Cover
    page_cover(c);  c.showPage()

    # 2. Welcome
    page_welcome(c);  c.showPage()

    # 3. Meet Luna
    page_meet_luna(c);  c.showPage()

    # 4. The Tiny Door
    page_the_door(c);  c.showPage()

    # 5-11. Seven Adventure Pages
    adventures = [
        (1, "The Lost Compass",
         "Dewdrop Forest — thimble-tall trees, firefly lanterns",
         "Pip the fox is lost. His magic compass spins endlessly and he's been walking in circles for seven nights.",
         "Luna reads the stars (just like her dad taught her) and guides Pip home, even though she's terrified of the dark.",
         "She knows more than she thinks she does.",
         HexColor("#0A1A10"), TEAL, 5),
        (2, "The Singing Storm",
         "Cloud Meadow — floating islands, dream-sheep",
         "A storm of mixed-up lullabies is scrambling the dream-sheep's sleep, causing nightmares across the meadow.",
         "Luna, who hates performing, sings her grandmother's lullaby out loud for the very first time.",
         "Her voice is strong enough — even when it shakes.",
         HexColor("#0A1020"), LAVENDER, 6),
        (3, "Dragon Lullaby",
         "Pebble Mountains — crystal caves, sleeping dragons",
         "A baby dragon's cries are cracking the mountain walls. If it doesn't sleep, the whole mountain crumbles.",
         "Luna stays with the frightened dragon, telling it stories until it finally drifts off.",
         "Patience and gentleness are kinds of bravery too.",
         HexColor("#1A0A0A"), CORAL, 7),
        (4, "The Invisible Bridge",
         "The Glowing River — liquid moonlight that sings",
         "The bridge over the Glowing River has turned invisible. The village on the other side is stranded.",
         "Luna closes her eyes and trusts what she can't see — she walks across first to prove it's safe.",
         "Trust is sometimes more powerful than proof.",
         HexColor("#0A1A18"), TEAL, 8),
        (5, "Stolen Starlight",
         "Mirror Lake Village — the only town lit by starlight",
         "Someone has been collecting all the fallen stars, leaving the village in shadow.",
         "Luna confronts the star-collector (a lonely creature who only wanted light for reading) with kindness, not blame.",
         "Most problems have a sad story behind them.",
         HexColor("#0D0A1A"), GOLD, 9),
        (6, "The Echo Caves",
         "Echo Caves — underground passages filled with whispers",
         "The Hush is trapped in the caves, too frightened of its own echoing voice to call for help.",
         "Luna teaches The Hush to turn its scary echo into a song — and together they find the way out.",
         "The things that frighten us can sometimes become our gifts.",
         HexColor("#120A1A"), BLUSH, 10),
        (7, "Home Is the Bravest",
         "The entire Pocket World — it's changing, shifting",
         "The Pocket World is fading. The door is getting smaller. Luna must say goodbye.",
         "Luna walks back through the door on her own — and on Monday, raises her hand in class.",
         "The bravest journey always leads back to yourself.",
         HexColor("#0A0A1A"), GOLD, 11),
    ]

    for adv in adventures:
        adventure_page(c, *adv)
        c.showPage()

    # 12. The Pocket World
    page_the_world(c);  c.showPage()

    # 13. Characters
    page_characters(c);  c.showPage()

    # 14. Themes
    page_theme_courage(c);  c.showPage()

    # 15. Adventure Map
    page_adventure_map(c);  c.showPage()

    # 16. Real-world connections
    page_real_world_connections(c);  c.showPage()

    # 17. Discussion questions
    page_discussion_questions(c);  c.showPage()

    # 18. Draw your door activity
    page_activity_draw(c);  c.showPage()

    # 19. Dream journal
    page_activity_journal(c);  c.showPage()

    # 20. Brave list
    page_brave_list(c);  c.showPage()

    # 21. For grown-ups
    page_for_grownups(c);  c.showPage()

    # 22. Bonus activities
    page_bonus_activities(c);  c.showPage()

    # 23. Quotes
    page_quotes(c);  c.showPage()

    # 24. Closing
    page_closing(c);  c.showPage()

    c.save()
    print(f"Done! Pages: 24  →  {path}")

build()