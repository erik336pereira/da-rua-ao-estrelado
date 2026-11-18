"""Draw the project's original sprite sheets and pixel-art tiles."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "assets" / "sprites"
ROOT.mkdir(parents=True, exist_ok=True)

OUTLINE = "#18263c"
SKIN = "#df9a70"
BLUE = "#258dd4"
GOLD = "#ffe06a"
WHITE = "#f4edd6"
NAVY = "#253d5b"


def rect(draw, xy, color):
    draw.rectangle(xy, fill=color)


def player_frame(frame: int) -> Image.Image:
    im = Image.new("RGBA", (24, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pose = "idle" if frame == 0 else "walk" if frame in (1, 2, 3) else "jump" if frame == 4 else "head" if frame == 5 else "slide"
    step = {-1: 0}.get(frame, 0)
    if frame == 1: step = -2
    if frame == 2: step = 0
    if frame == 3: step = 2
    dy = -1 if frame in (1, 3, 4) else 0
    # Long dark fringe, face, and a bright bandana make the silhouette distinct.
    rect(d, (7, 3+dy, 16, 10+dy), OUTLINE)
    rect(d, (9, 3+dy, 15, 4+dy), "#402c2d")
    rect(d, (8, 5+dy, 9, 10+dy), "#4c3030")
    rect(d, (10, 6+dy, 15, 10+dy), SKIN)
    rect(d, (8, 4+dy, 16, 5+dy), GOLD)
    rect(d, (13, 7+dy, 14, 8+dy), OUTLINE)
    rect(d, (13, 9+dy, 15, 9+dy), "#9c4d50")
    # Neck and jersey.
    rect(d, (10, 10+dy, 14, 12+dy), SKIN)
    rect(d, (6, 12+dy, 17, 21+dy), OUTLINE)
    rect(d, (7, 12+dy, 16, 20+dy), BLUE)
    rect(d, (8, 14+dy, 15, 15+dy), GOLD)
    rect(d, (11, 16+dy, 12, 18+dy), "#d7eaf3")
    # Arms change pose while remaining readable at 1x.
    if pose == "jump":
        rect(d, (3, 10, 6, 15), OUTLINE); rect(d, (4, 9, 5, 14), SKIN)
        rect(d, (17, 9, 20, 14), OUTLINE); rect(d, (18, 8, 19, 13), SKIN)
    elif pose == "head":
        rect(d, (3, 13, 6, 18), OUTLINE); rect(d, (4, 13, 5, 17), SKIN)
        rect(d, (17, 12, 20, 16), OUTLINE); rect(d, (18, 12, 19, 15), SKIN)
    elif pose == "slide":
        rect(d, (3, 17, 8, 20), OUTLINE); rect(d, (4, 17, 8, 18), SKIN)
        rect(d, (16, 15, 21, 18), OUTLINE); rect(d, (17, 15, 21, 16), SKIN)
    else:
        rect(d, (4, 13+dy, 7, 19+dy), OUTLINE); rect(d, (5, 14+dy, 6, 18+dy), SKIN)
        rect(d, (16, 13+dy, 19, 19+dy), OUTLINE); rect(d, (17, 14+dy, 18, 18+dy), SKIN)
    # White shorts and animated legs.
    rect(d, (7, 20+dy, 16, 24+dy), OUTLINE)
    rect(d, (8, 21+dy, 15, 23+dy), WHITE)
    if pose == "slide":
        rect(d, (11, 24, 20, 27), OUTLINE); rect(d, (12, 24, 20, 26), NAVY)
        rect(d, (16, 26, 23, 28), OUTLINE); rect(d, (18, 26, 23, 27), "#e9b64e")
        rect(d, (4, 23, 12, 26), OUTLINE); rect(d, (4, 23, 10, 25), NAVY)
        rect(d, (2, 25, 8, 27), OUTLINE); rect(d, (2, 25, 7, 26), "#e9b64e")
    elif pose == "jump":
        rect(d, (8, 23, 11, 27), OUTLINE); rect(d, (9, 24, 10, 26), NAVY)
        rect(d, (13, 23, 16, 26), OUTLINE); rect(d, (14, 24, 15, 25), NAVY)
        rect(d, (6, 27, 12, 29), OUTLINE); rect(d, (7, 27, 11, 28), "#e9b64e")
        rect(d, (13, 26, 19, 28), OUTLINE); rect(d, (14, 26, 18, 27), "#e9b64e")
    else:
        left_knee = 26 + max(0, step)
        right_knee = 26 + max(0, -step)
        rect(d, (8, 23+dy, 11, left_knee+dy), OUTLINE)
        rect(d, (9, 24+dy, 10, left_knee+dy-1), NAVY)
        rect(d, (13, 23+dy, 16, right_knee+dy), OUTLINE)
        rect(d, (14, 24+dy, 15, right_knee+dy-1), NAVY)
        rect(d, (6+max(0,-step), left_knee+dy, 12+max(0,-step), left_knee+dy+2), OUTLINE)
        rect(d, (7+max(0,-step), left_knee+dy, 11+max(0,-step), left_knee+dy+1), "#e9b64e")
        rect(d, (12+max(0,step), right_knee+dy, 18+max(0,step), right_knee+dy+2), OUTLINE)
        rect(d, (13+max(0,step), right_knee+dy, 17+max(0,step), right_knee+dy+1), "#e9b64e")
    canvas = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    canvas.alpha_composite(im, (4, 0))
    return canvas


def tackle_frame(frame: int) -> Image.Image:
    """Five bottom-aligned poses: crouch, launch, slide, impact, and recovery."""
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def head(x: int, y: int) -> None:
        rect(d, (x, y, x+9, y+9), OUTLINE)
        rect(d, (x+2, y+2, x+8, y+7), SKIN)
        rect(d, (x+1, y, x+9, y+2), "#402c2d")
        rect(d, (x, y+2, x+8, y+3), GOLD)
        rect(d, (x+6, y+4, x+7, y+5), OUTLINE)
        rect(d, (x+6, y+7, x+8, y+7), "#9c4d50")

    if frame == 0:
        # Compact squat before the player drops into the slide.
        head(10, 4)
        d.polygon([(8,13),(20,13),(24,18),(22,25),(10,25),(7,20)], fill=OUTLINE)
        d.polygon([(10,14),(19,14),(21,18),(20,23),(11,23),(9,19)], fill=BLUE)
        rect(d, (10, 16, 20, 17), GOLD); rect(d, (15, 18, 16, 20), "#d7eaf3")
        rect(d, (4, 16, 9, 20), OUTLINE); rect(d, (5, 17, 8, 19), SKIN)
        rect(d, (21, 17, 27, 20), OUTLINE); rect(d, (22, 18, 26, 19), SKIN)
        rect(d, (8, 23, 14, 28), OUTLINE); rect(d, (9, 24, 13, 27), NAVY)
        rect(d, (15, 23, 21, 28), OUTLINE); rect(d, (16, 24, 20, 27), NAVY)
        rect(d, (5, 27, 15, 30), OUTLINE); rect(d, (6, 28, 14, 29), "#e9b64e")
        rect(d, (15, 27, 26, 30), OUTLINE); rect(d, (16, 28, 25, 29), "#e9b64e")
    elif frame in (1, 2, 3):
        # One compact side silhouette keeps the head, arms, jersey, shorts, and legs joined.
        head_x, head_y = (7, 7) if frame == 1 else ((3, 10) if frame == 2 else (2, 9))
        head(head_x, head_y)
        body_y = 14 if frame == 1 else (16 if frame == 2 else 15)
        d.polygon([(head_x+6,body_y+3),(head_x+10,body_y),(21,body_y+1),(25,body_y+5),(24,25),(19,28),(10,25),(8,21)], fill=OUTLINE)
        d.polygon([(head_x+8,body_y+4),(head_x+11,body_y+2),(20,body_y+3),(22,body_y+6),(21,23),(18,25),(11,23),(10,21)], fill=BLUE)
        rect(d, (head_x+9, body_y+5, 21, body_y+6), GOLD)
        rect(d, (head_x+11, body_y+7, head_x+12, body_y+9), "#d7eaf3")
        # Neck overlaps the jaw and collar so the diving pose does not split at the shoulder.
        rect(d, (head_x+6, head_y+7, head_x+10, head_y+10), SKIN)
        rect(d, (head_x+5, head_y+7, head_x+10, head_y+10), OUTLINE)
        rect(d, (head_x+6, head_y+8, head_x+9, head_y+9), SKIN)
        # The forward arm reaches along the grass; the rear arm stays against the ribs.
        d.polygon([(21,body_y+3),(25,body_y+4),(29,body_y+7),(31,body_y+9),(29,body_y+11),(26,body_y+9),(23,body_y+7),(20,body_y+6)], fill=OUTLINE)
        d.polygon([(23,body_y+4),(25,body_y+5),(28,body_y+7),(29,body_y+9),(27,body_y+8),(24,body_y+7)], fill=SKIN)
        d.polygon([(head_x+7,body_y+5),(head_x+10,body_y+6),(head_x+9,body_y+10),(head_x+6,body_y+12),(head_x+3,body_y+11),(head_x+4,body_y+8)], fill=OUTLINE)
        d.polygon([(head_x+7,body_y+7),(head_x+8,body_y+7),(head_x+7,body_y+10),(head_x+5,body_y+10)], fill=SKIN)
        # Shorts and the two joined legs form one clear sliding base.
        d.polygon([(18,body_y+8),(24,body_y+8),(25,body_y+11),(21,body_y+13),(17,body_y+11)], fill=OUTLINE)
        d.polygon([(19,body_y+9),(23,body_y+9),(23,body_y+11),(20,body_y+12),(18,body_y+11)], fill=WHITE)
        d.polygon([(20,body_y+10),(25,body_y+10),(29,body_y+11),(31,body_y+13),(30,body_y+15),(24,body_y+14),(20,body_y+13)], fill=OUTLINE)
        d.polygon([(23,body_y+11),(28,body_y+12),(29,body_y+13),(24,body_y+13)], fill=NAVY)
        d.polygon([(28,body_y+12),(31,body_y+13),(31,body_y+15),(28,body_y+15)], fill="#e9b64e")
        d.polygon([(17,body_y+10),(21,body_y+12),(19,body_y+15),(15,body_y+15),(12,body_y+13)], fill=OUTLINE)
        d.polygon([(16,body_y+12),(19,body_y+13),(18,body_y+14),(15,body_y+14)], fill=NAVY)
        d.polygon([(12,body_y+13),(17,body_y+14),(16,body_y+16),(11,body_y+16),(9,body_y+15)], fill=OUTLINE)
        d.polygon([(11,body_y+14),(15,body_y+15),(14,body_y+15)], fill="#e9b64e")
    else:
        # Lift the chest and tuck both knees before returning to the run cycle.
        head(10, 5)
        d.polygon([(9,14),(20,14),(24,19),(21,26),(11,25),(8,20)], fill=OUTLINE)
        d.polygon([(11,15),(19,15),(21,19),(19,23),(12,23),(10,19)], fill=BLUE)
        rect(d, (11, 17, 20, 18), GOLD); rect(d, (15, 19, 16, 21), "#d7eaf3")
        rect(d, (5, 20, 10, 25), OUTLINE); rect(d, (6, 21, 9, 24), SKIN)
        rect(d, (21, 19, 27, 24), OUTLINE); rect(d, (22, 20, 26, 23), SKIN)
        rect(d, (10, 23, 15, 28), OUTLINE); rect(d, (11, 24, 14, 27), NAVY)
        rect(d, (17, 23, 22, 28), OUTLINE); rect(d, (18, 24, 21, 27), NAVY)
        rect(d, (7, 27, 16, 30), OUTLINE); rect(d, (8, 28, 15, 29), "#e9b64e")
        rect(d, (16, 27, 25, 30), OUTLINE); rect(d, (17, 28, 24, 29), "#e9b64e")
    return im


def kick_frame(frame: int) -> Image.Image:
    """Three grounded side-view poses for wind-up, contact, and follow-through."""
    im = player_frame(0)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 22, 31, 31), fill=(0, 0, 0, 0))
    # Shorts and the planted leg share the same anchor in every frame.
    rect(d, (10, 20, 21, 25), OUTLINE)
    rect(d, (11, 21, 20, 24), WHITE)
    d.polygon([(10,23),(15,23),(15,28),(18,29),(18,31),(6,31),(6,29),(10,27)], fill=OUTLINE)
    d.polygon([(11,24),(13,24),(13,28),(15,29),(8,29),(10,27)], fill=NAVY)
    rect(d, (5, 28, 17, 31), OUTLINE)
    rect(d, (6, 29, 16, 30), "#e9b64e")

    if frame == 0:
        # The knee draws back before the foot swings toward the ball.
        d.polygon([(17,22),(22,22),(24,25),(22,28),(17,27),(15,25)], fill=OUTLINE)
        d.polygon([(18,23),(21,23),(22,25),(20,26),(17,25)], fill=NAVY)
        d.polygon([(16,25),(22,26),(23,29),(20,31),(14,29)], fill=OUTLINE)
        d.polygon([(16,27),(21,28),(20,29),(15,28)], fill="#e9b64e")
    elif frame == 1:
        # Contact pose: the shin and cleat extend forward at ball height.
        d.polygon([(17,22),(21,21),(24,23),(23,26),(19,27),(16,25)], fill=OUTLINE)
        d.polygon([(18,23),(21,22),(22,24),(19,25)], fill=NAVY)
        d.polygon([(21,22),(25,19),(29,19),(31,21),(30,24),(25,25),(22,25)], fill=OUTLINE)
        d.polygon([(24,22),(27,20),(29,20),(30,21),(29,22),(25,24)], fill=NAVY)
        d.polygon([(28,18),(31,18),(31,22),(29,23),(27,21)], fill="#e9b64e")
    else:
        # The leg follows through while the planted boot remains on the turf.
        d.polygon([(17,22),(21,21),(24,23),(23,26),(19,27),(16,25)], fill=OUTLINE)
        d.polygon([(18,23),(21,22),(22,24),(19,25)], fill=NAVY)
        d.polygon([(21,23),(25,21),(29,21),(31,23),(30,26),(25,27),(22,26)], fill=OUTLINE)
        d.polygon([(24,24),(27,22),(29,22),(30,23),(29,24),(25,26)], fill=NAVY)
        d.polygon([(28,20),(31,20),(31,24),(29,25),(27,23)], fill="#e9b64e")
    return im


def headbutt_frame(frame: int) -> Image.Image:
    """Three compact poses that visibly drive the head forward and recover."""
    im = player_frame(0)
    d = ImageDraw.Draw(im)
    # Clear the original head and neck; the body, arms, and legs stay planted.
    d.rectangle((10, 2, 21, 12), fill=(0, 0, 0, 0))
    if frame == 0:       # draw the head back before the hit
        head_x, head_y = 9, 4
        neck_points = [(14,9),(18,9),(19,12),(17,14),(13,12)]
    elif frame == 1:     # lunge the head forward at contact
        head_x, head_y = 14, 3
        neck_points = [(14,9),(18,9),(22,12),(21,14),(16,13),(13,11)]
    else:                # return to the neutral stance
        head_x, head_y = 11, 4
        neck_points = [(14,9),(18,9),(20,12),(18,14),(14,13),(13,11)]

    d.polygon(neck_points, fill=OUTLINE)
    d.polygon([(15,10),(17,10),(19,12),(18,12),(16,12)], fill=SKIN)

    # Side-facing head: hair and bandana remain readable as it translates.
    d.polygon([(head_x+1,head_y),(head_x+8,head_y),(head_x+10,head_y+2),
               (head_x+10,head_y+6),(head_x+8,head_y+8),(head_x+1,head_y+8),
               (head_x,head_y+6),(head_x,head_y+2)], fill=OUTLINE)
    rect(d, (head_x+2, head_y+3, head_x+8, head_y+7), SKIN)
    rect(d, (head_x+1, head_y+1, head_x+8, head_y+2), "#402c2d")
    rect(d, (head_x, head_y+2, head_x+2, head_y+4), "#4c3030")
    rect(d, (head_x+1, head_y+3, head_x+9, head_y+3), GOLD)
    rect(d, (head_x+7, head_y+5, head_x+8, head_y+5), OUTLINE)
    rect(d, (head_x+7, head_y+7, head_x+9, head_y+7), "#9c4d50")
    return im


def enemy_frame(kind: str, frame: int) -> Image.Image:
    im = Image.new("RGBA", (24, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    swing = frame % 2
    leg_y = 28 + swing
    if kind == "referee":
        shirt = "#f5f0dc"; accent = "#27364b"; hair = "#483333"; skin = "#d9946b"
    elif kind == "goalie":
        shirt = "#ed9b42"; accent = "#4c5e95"; hair = "#392d2d"; skin = "#d9946b"
    else:
        shirt = "#d84c5a"; accent = "#f6cf57"; hair = "#493333"; skin = "#dc9b72"
    # Head/face.
    rect(d, (8, 3, 16, 11), OUTLINE); rect(d, (9, 5, 15, 10), skin)
    rect(d, (8, 3, 16, 5), hair); rect(d, (8, 5, 9, 8), hair)
    rect(d, (13, 7, 14, 8), OUTLINE)
    rect(d, (10, 11, 14, 13), skin)
    # Torso and a role-specific detail.
    rect(d, (6, 12, 18, 24, ), OUTLINE); rect(d, (7, 13, 17, 23), shirt)
    if kind == "referee":
        rect(d, (8, 14, 10, 22), accent); rect(d, (13, 14, 15, 22), accent)
        rect(d, (15, 15, 17, 17), "#e94a55")
        rect(d, (6, 5, 18, 6), "#f1cf5c")
    elif kind == "goalie":
        rect(d, (8, 15, 16, 17), accent); rect(d, (3, 16, 6, 19), "#f7d75d")
        rect(d, (18, 16, 21, 19), "#f7d75d"); rect(d, (10, 7, 12, 8), "#e8d85f")
    else:
        rect(d, (6, 14, 18, 16), accent); rect(d, (10, 18, 14, 20), "#f5f0dc")
    # Arms and running feet.
    rect(d, (3, 14-swing, 6, 21), OUTLINE); rect(d, (4, 15-swing, 5, 20), skin)
    rect(d, (18, 14+swing, 21, 21), OUTLINE); rect(d, (19, 15+swing, 20, 20), skin)
    rect(d, (7, 23, 11, leg_y), OUTLINE); rect(d, (13, 23, 17, 28-swing), OUTLINE)
    rect(d, (8, 24, 10, leg_y-1), accent); rect(d, (14, 24, 16, 27-swing), accent)
    rect(d, (5+swing*2, 28, 12+swing*2, 30), OUTLINE); rect(d, (12-swing*2, 27, 19-swing*2, 29), OUTLINE)
    return im


def boss_frame(frame: int) -> Image.Image:
    im = Image.new("RGBA", (32, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    red = "#d32f43"; darkred = "#8f2036"; cream = "#fff0ce"
    step = 1 if frame == 3 else 0

    # Arms are attached to the card's sides and animate through the throw.
    rect(d, (1, 15, 7, 19), OUTLINE); rect(d, (2, 16, 6, 18), "#e1a078")
    if frame == 1:
        rect(d, (24, 10, 28, 15), OUTLINE); rect(d, (25, 5, 28, 12), "#e1a078")
        rect(d, (24, 2, 30, 11), OUTLINE); rect(d, (25, 3, 29, 9), red)
        rect(d, (27, 1, 29, 2), cream)
    elif frame == 2:
        rect(d, (23, 15, 30, 18), OUTLINE); rect(d, (27, 14, 31, 17), "#e1a078")
        rect(d, (30, 12, 32, 15), cream)
    else:
        rect(d, (24, 17, 30, 21), OUTLINE); rect(d, (25, 18, 29, 20), "#e1a078")

    # Broad, beveled red rectangle: the boss is a living football card.
    card_top = 3 if frame != 3 else 2
    d.polygon([(8,card_top),(23,card_top),(26,card_top+3),(26,29),(23,32),(8,32),(5,29),(5,card_top+3)], fill=OUTLINE)
    d.polygon([(9,card_top+2),(22,card_top+2),(24,card_top+4),(24,28),(22,30),(9,30),(7,28),(7,card_top+4)], fill=cream)
    d.rectangle((9,card_top+4,22,28), fill=red)
    d.rectangle((10,card_top+5,12,card_top+13), "#f36b74")
    d.rectangle((13,card_top+5,22,card_top+7), "#e74a5a")
    # Angry eyes frame the large white exclamation mark.
    d.rectangle((11,card_top+9,13,card_top+10), cream)
    d.rectangle((19,card_top+9,21,card_top+10), cream)
    d.rectangle((15,card_top+9,18,card_top+20), cream)
    d.rectangle((15,card_top+22,18,card_top+24), cream)
    d.rectangle((12,card_top+13,14,card_top+14), darkred)
    d.rectangle((19,card_top+13,21,card_top+14), darkred)

    # Short legs and cleats keep the card visibly animated as a character.
    left_y = 30 if frame != 3 else 29
    right_y = 30+step
    rect(d, (9, left_y, 14, 36), OUTLINE); rect(d, (10, left_y+1, 13, 35), "#253d5b")
    rect(d, (18, right_y, 23, 36), OUTLINE); rect(d, (19, right_y+1, 22, 35), "#253d5b")
    rect(d, (6, 35, 15, 39), OUTLINE); rect(d, (7, 36, 14, 38), "#ffe06a")
    rect(d, (17, 35+step, 26, 39+step), OUTLINE); rect(d, (18, 36+step, 25, 38+step), "#ffe06a")
    return im


def save_sheet(name: str, frames: list[Image.Image]) -> None:
    width = sum(frame.width for frame in frames)
    sheet = Image.new("RGBA", (width, frames[0].height), (0, 0, 0, 0))
    for i, frame in enumerate(frames): sheet.alpha_composite(frame, (i*frame.width, 0))
    sheet.save(ROOT / f"{name}.png")


def make_background() -> None:
    im = Image.new("RGB", (320, 180), "#39aadd"); d = ImageDraw.Draw(im)
    # Soft but pixel-defined late-afternoon sky.
    for y in range(180):
        c = (42 + int(58*y/180), 156 + int(50*y/180), 221 + int(16*y/180))
        d.line((0,y,319,y), fill=c)
    # Stepped cloud silhouettes with cool shadows and sparse pixel dithering.
    def cloud(x, y, scale):
        shape = [(0,11),(3,11),(3,7),(7,7),(7,4),(11,4),(11,1),(18,1),
                 (18,3),(24,3),(24,6),(29,6),(29,10),(34,10),(34,14),(0,14)]
        points = [(x+px*scale,y+py*scale) for px,py in shape]
        d.polygon(points, fill="#c8eaf1")
        top = [(0,10),(4,10),(4,7),(8,7),(8,4),(12,4),(12,2),(18,2),
               (18,4),(23,4),(23,6),(28,6),(28,9),(32,9),(32,11),(0,11)]
        d.polygon([(x+px*scale,y+py*scale) for px,py in top], fill="#f7feff")
        d.rectangle((x+2*scale,y+10*scale,x+13*scale,y+11*scale), fill="#e5f8fb")
        for px,py in [(2,8),(5,5),(10,3),(20,5),(26,7),(30,10),(14,12)]:
            if (px+py)%3 != 0:
                d.point((x+px*scale,y+py*scale), fill="#b9dfe9")
    for x,y,scale in [(8,39,1),(101,23,2),(224,44,2),(287,24,1),(172,63,1)]:
        cloud(x,y,scale)
    # Distant hills and a small skyline in alternating green tones.
    d.polygon([(0,121),(29,102),(61,120),(100,95),(145,120),(183,103),(232,122),(273,96),(320,116),(320,180),(0,180)],fill="#438f78")
    d.polygon([(0,140),(44,118),(78,138),(126,113),(176,142),(226,119),(267,139),(301,116),(320,128),(320,180),(0,180)],fill="#286f61")
    for x,y,w,h in [(14,111,12,32),(32,120,18,25),(75,108,14,34),(111,125,18,24),(211,114,17,29),(252,106,13,36),(286,122,20,25)]:
        d.rectangle((x,y,x+w,y+h),fill="#b47655")
        d.polygon([(x,y),(x+w//2,y-5),(x+w,y)],fill="#843e48")
        d.rectangle((x+2,y+6,x+5,y+10),fill="#a4d8df")
        d.rectangle((x+8,y+6,x+11,y+10),fill="#a4d8df")
        d.rectangle((x+2,y+18,x+5,y+22),fill="#a4d8df")
        d.rectangle((x+8,y+18,x+11,y+22),fill="#a4d8df")
        d.line((x+w-1,y+2,x+w-1,y+h),fill="#d49368")
    # Tree silhouettes break up the skyline before the playfield begins.
    for x,base in [(4,147),(58,150),(166,149),(237,148),(309,150),(100,151),(194,152),(278,150)]:
        d.rectangle((x+5,base-18,x+8,base),fill="#70483a")
        d.rectangle((x+1,base-28,x+13,base-18),fill="#1e604b")
        d.rectangle((x-2,base-32,x+6,base-24),fill="#2f8554")
        d.rectangle((x+7,base-33,x+15,base-27),fill="#3da15e")
        d.rectangle((x+3,base-23,x+6,base-20),fill="#79c85e")
        d.rectangle((x,base-29,x+2,base-26),fill="#54b960")
        d.rectangle((x+10,base-25,x+14,base-21),fill="#337f50")
    # A few high pixel glints add texture to the sky without visual noise.
    for x,y in [(21,78),(88,72),(159,83),(204,69),(276,79),(303,58)]:
        d.rectangle((x,y,x+1,y+1),fill="#d5f6ff")
    # Foreground shrubs sit just behind the turf, with varied leafy silhouettes.
    for index,x in enumerate(range(-4,320,16)):
        base=159-(index%3)
        d.rectangle((x,base-5,x+13,base),fill="#1d6448")
        d.rectangle((x+2,base-9,x+7,base-4),fill="#2b8453")
        d.rectangle((x+7,base-11,x+12,base-5),fill="#399b59")
        d.rectangle((x+4,base-10,x+5,base-8),fill="#7bc761")
        if index%4==1:
            d.point((x+10,base-9),fill="#a4dc70")
    im.save(ROOT / "background.png")


def make_tiles() -> None:
    sheet = Image.new("RGB", (128, 32), "#9e633e")
    underground = Image.new("RGB", (128, 32), "#805036")
    for variant in range(4):
        im = Image.new("RGB", (32, 32), "#9e633e"); d = ImageDraw.Draw(im)
        d.rectangle((0,0,31,4),fill=["#59b85f","#64c05e","#4da958","#6bc464"][variant])
        d.rectangle((0,5,31,8),fill="#368950")
        blocks = [[(3,10,11,15),(18,12,28,17),(8,21,16,26),(22,23,28,29)],
                  [(1,14,8,19),(12,10,18,15),(22,19,30,24),(5,25,12,29)],
                  [(5,10,14,14),(21,11,27,17),(2,21,10,25),(15,24,24,29)],
                  [(0,11,7,16),(15,13,23,18),(8,20,16,24),(25,24,31,28)]][variant]
        for i,(x0,y0,x1,y1) in enumerate(blocks):
            d.rectangle((x0,y0,x1,y1),fill=["#b7784b","#895537","#bd8050","#a56a42"][i])
        for i in range(5):
            x=(i*7+variant*3)%30+1; y=10+(i*5+variant*2)%19
            d.point((x,y),fill="#d4945b" if i%2==0 else "#744832")
        d.line((0,0,31,0),fill="#9be66b"); d.line((0,31,31,31),fill="#68432f")
        sheet.paste(im,(variant*32,0))
        deep = Image.new("RGB", (32, 32), ["#805036", "#89583a", "#794b34", "#855438"][variant]); dd = ImageDraw.Draw(deep)
        seams = [[(0,5,11,10),(18,8,29,14),(7,20,17,26),(22,25,31,29)],
                 [(2,8,9,14),(14,4,23,10),(20,17,30,23),(3,24,12,29)],
                 [(5,5,16,11),(21,10,29,15),(0,19,9,24),(14,24,25,30)],
                 [(0,9,8,15),(16,5,25,11),(9,18,17,23),(23,22,31,27)]][variant]
        for i,(x0,y0,x1,y1) in enumerate(seams):
            dd.rectangle((x0,y0,x1,y1),fill=["#986343", "#70462f", "#a06c46", "#8b5839"][i])
        for i in range(9):
            x=(i*11+variant*5)%31; y=(i*7+variant*3)%31
            dd.point((x,y),fill="#c18751" if i%3==0 else "#68432f")
        underground.paste(deep,(variant*32,0))
    sheet.save(ROOT / "ground_tile.png")
    underground.save(ROOT / "underground_tile.png")
    platform = Image.new("RGB", (32, 12), "#a66c45"); p = ImageDraw.Draw(platform)
    p.rectangle((0,0,31,3),fill="#6fd06c"); p.rectangle((0,4,31,6),fill="#3e9959")
    p.rectangle((1,7,30,11),fill="#9b633f"); p.line((4,8,10,8),fill="#d8975a")
    platform.save(ROOT / "platform_tile.png")


def make_stadium() -> None:
    im = Image.new("RGBA", (280, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # A complete structure with visible piers and a foundation that meets the ground.
    d.polygon([(8,42),(33,22),(247,22),(272,42),(272,120),(8,120)], fill="#152c50")
    d.rectangle((17,38,263,74), fill="#243e69")
    for row in range(3):
        y = 31+row*11
        for i in range(30):
            x = 19+i*8
            color = ["#e84d61","#fff0c0","#ffd45a","#218bd2"][((i+row*3)%4)]
            d.rectangle((x,y,x+3,y+6), fill=color)
            d.rectangle((x+4,y+1,x+5,y+6), fill="#111e37")
    # Structural supports carry the stands down to a solid plinth.
    d.rectangle((17,69,263,105), fill="#1b3155")
    for x in (25, 61, 103, 171, 213, 251):
        d.rectangle((x,68,x+7,105), fill="#29466e")
        d.rectangle((x+2,70,x+4,102), fill="#526987")
    # Main pitch and chalk lines sit above the base course.
    d.rectangle((52,77,225,104), fill="#37856a")
    d.rectangle((57,80,220,101), outline="#f5f1dc", width=1)
    d.line((138,81,138,100), fill="#f5f1dc", width=1)
    d.rectangle((58,84,72,98), outline="#f5f1dc", width=1)
    d.rectangle((205,84,219,98), outline="#f5f1dc", width=1)
    d.ellipse((131,86,145,98), outline="#f5f1dc", width=1)
    # Stadium lights and entry arch.
    d.rectangle((27,11,31,30), fill="#d9e7ec"); d.rectangle((248,11,252,30), fill="#d9e7ec")
    d.rectangle((18,8,40,13), fill="#ffe582"); d.rectangle((239,8,261,13), fill="#ffe582")
    d.rectangle((229,72,246,106), fill="#101d36")
    d.rectangle((232,77,243,104), fill="#74c8da")
    d.rectangle((229,70,246,75), fill="#f4e6c4")
    # Entry ramp and broad stone foundation connect the door to the pitch edge.
    d.polygon([(226,102),(249,102),(264,120),(211,120)], fill="#738995")
    d.polygon([(231,105),(245,105),(256,118),(220,118)], fill="#a9b9b7")
    d.rectangle((8,104,272,120), fill="#24354f")
    d.rectangle((8,104,272,108), fill="#9aaeb3")
    d.rectangle((8,108,272,111), fill="#52677f")
    for x in range(16, 270, 24):
        d.line((x,112,x,119), fill="#405573", width=1)
        d.line((x+12,108,x+12,111), fill="#c3cfca", width=1)
    # Restore the ramp face above the course so it reads as an attached entrance.
    d.polygon([(226,102),(249,102),(264,120),(211,120)], fill="#738995")
    d.polygon([(231,105),(245,105),(256,118),(220,118)], fill="#a9b9b7")
    # Blocky crowd pixels, original color rhythm.
    for i in range(42):
        x = 20+(i*37)%238
        y = 66+(i*17)%7
        d.rectangle((x,y,x+2,y+2), fill=["#fff0c0","#f05a64","#64d2bb","#ffc857"][i%4])
    im.save(ROOT / "stadium.png")


def main() -> None:
    save_sheet("player", [player_frame(i) for i in range(6)] + [kick_frame(i) for i in range(3)] + [tackle_frame(i) for i in range(5)] + [headbutt_frame(i) for i in range(3)])
    for kind in ("referee", "goalie", "fan"):
        save_sheet(kind, [enemy_frame(kind, i) for i in range(4)])
    save_sheet("red_card_boss", [boss_frame(i) for i in range(4)])
    make_background(); make_tiles(); make_stadium()


if __name__ == "__main__": main()
