from PIL import Image, ImageDraw, ImageFilter
import math

S = 2
W = H = 1024
im = Image.new("RGB", (W * S, H * S), (196, 229, 243))
p = im.load()

# Calm vertical ice-blue sky gradient.
for y in range(H * S):
    t = y / (H * S - 1)
    c = tuple(round(a * (1 - t) + b * t)
              for a, b in zip((190, 224, 241), (224, 241, 247)))
    for x in range(W * S):
        p[x, y] = c


def scale_box(box):
    return tuple(round(v * S) for v in box)


def ellipse(box, fill, outline=None, width=1):
    d = ImageDraw.Draw(im)
    d.ellipse(scale_box(box), fill=fill, outline=outline,
              width=max(1, round(width * S)))


def polygon(points, fill):
    ImageDraw.Draw(im).polygon(
        [(round(x * S), round(y * S)) for x, y in points], fill=fill)


def line(points, fill, width):
    ImageDraw.Draw(im).line(
        [(round(x * S), round(y * S)) for x, y in points],
        fill=fill, width=round(width * S), joint="curve")


def soft_ellipse(box, color, blur=18, opacity=110):
    """Lay a softly feathered color patch over the illustration."""
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse(scale_box(box), fill=opacity)
    mask = mask.filter(ImageFilter.GaussianBlur(blur * S))
    tint = Image.new("RGB", im.size, color)
    im.paste(tint, (0, 0), mask)


# A faint warm halo lifts the face from the cool snowy background.
soft_ellipse((286, 160, 738, 582), (255, 220, 176), 62, 48)

# Snowflakes kept subtle and behind the character.
for x, y, r in [(134, 175, 8), (280, 325, 5), (828, 167, 7),
                (900, 319, 5), (160, 474, 5), (845, 472, 6),
                (706, 245, 4), (374, 147, 4)]:
    ellipse((x-r, y-r, x+r, y+r), (244, 250, 250))
    if r >= 7:
        for a in range(3):
            ang = a * math.pi / 3
            dx, dy = math.cos(ang) * r, math.sin(ang) * r
            line([(x-dx, y-dy), (x+dx, y+dy)], (239, 248, 250), 1.5)

# Ground mound.
ellipse((-120, 866, 1144, 1175), (247, 251, 250))
ellipse((94, 908, 184, 921), (235, 245, 247))
ellipse((823, 919, 906, 931), (235, 245, 247))
ellipse((-40, 891, 1060, 1116), (252, 253, 250))

# Soft shadow beneath chick.
ellipse((280, 850, 744, 931), (202, 221, 228))

# Body with cool edge shading and a soft glow across the upper down.
ellipse((304, 427, 725, 891), (112, 139, 157), (98, 125, 145), 3)
ellipse((329, 458, 700, 870), (136, 160, 174))
soft_ellipse((296, 557, 414, 839), (91, 119, 143), 24)
soft_ellipse((610, 550, 734, 839), (91, 119, 143), 24)
soft_ellipse((355, 444, 674, 559), (187, 204, 207), 30)

# Rounded, tapered flippers built from soft overlapping forms.
ellipse((275, 632, 352, 755), (98, 126, 146))
ellipse((251, 673, 315, 758), (103, 132, 152))
ellipse((295, 621, 369, 704), (112, 139, 157))
ellipse((675, 621, 749, 704), (112, 139, 157))
ellipse((709, 632, 786, 755), (98, 126, 146))
ellipse((746, 673, 810, 758), (103, 132, 152))
# Blend the overlapping lobes into a single tapered silhouette.
ellipse((267, 636, 358, 754), (103, 132, 152))
ellipse((666, 636, 757, 754), (103, 132, 152))
line([(279, 719), (302, 693), (323, 668)], (155, 176, 187), 3)
line([(745, 719), (722, 693), (701, 668)], (155, 176, 187), 3)
line([(286, 705), (299, 692)], (128, 153, 168), 2)
line([(738, 705), (725, 692)], (128, 153, 168), 2)

# White belly down, broad and softly shaded.
ellipse((365, 601, 665, 858), (244, 246, 239))
ellipse((383, 620, 647, 838), (250, 250, 244))

# Oversized head, leaning gently to the chick's left.
ellipse((272, 196, 750, 627), (119, 146, 164), (99, 126, 145), 3)
ellipse((294, 213, 727, 601), (143, 166, 178))
soft_ellipse((310, 430, 713, 610), (105, 132, 153), 28)
soft_ellipse((330, 217, 686, 319), (173, 190, 196), 25)
# Cream face patch.
ellipse((331, 264, 694, 584), (248, 247, 237))
ellipse((348, 276, 679, 567), (252, 250, 242))

# A few small rounded crown wisps merge gently into the head.
ellipse((405, 204, 437, 230), (143, 166, 178))
ellipse((568, 202, 601, 232), (143, 166, 178))
ellipse((484, 193, 513, 218), (143, 166, 178))

# Large glossy eyes; two white sparkles in each.
for cx, cy in [(431, 411), (590, 397)]:
    ellipse((cx-43, cy-50, cx+43, cy+52), (51, 67, 83))
    ellipse((cx-34, cy-41, cx+34, cy+42), (26, 39, 56))
    ellipse((cx-22, cy-32, cx-5, cy-12), (255, 255, 250))
    ellipse((cx+13, cy+12, cx+23, cy+23), (220, 239, 246))

# Pink cheeks, softly feathered by layered translucent-looking circles.
ellipse((342, 467, 412, 514), (247, 181, 180))
ellipse((349, 471, 405, 508), (250, 194, 188))
ellipse((605, 453, 675, 500), (247, 181, 180))
ellipse((612, 457, 668, 494), (250, 194, 188))

# One little golden orange beak.
polygon([(482, 444), (540, 438), (563, 459), (536, 485),
         (506, 482), (477, 462)], (231, 137, 54))
polygon([(488, 447), (538, 443), (552, 459), (529, 472),
         (505, 470)], (249, 173, 73))
line([(503, 477), (536, 476)], (193, 103, 42), 2)

# Red scarf across the neck; folded band, knot, and two short ends.
polygon([(353, 573), (407, 591), (504, 604), (607, 577),
         (626, 619), (525, 650), (407, 638), (348, 615)], (190, 54, 68))
polygon([(357, 578), (409, 600), (505, 613), (614, 584),
         (619, 603), (516, 632), (405, 622), (352, 598)], (224, 78, 83))
polygon([(495, 610), (541, 610), (562, 643), (533, 669),
         (503, 650)], (173, 43, 59))
polygon([(516, 638), (551, 643), (569, 703), (546, 714),
         (529, 672)], (190, 54, 68))
polygon([(482, 637), (508, 645), (495, 691), (476, 695)], (208, 59, 70))
line([(372, 594), (420, 611), (470, 616)], (244, 119, 113), 3)
line([(545, 607), (574, 598), (600, 591)], (244, 119, 113), 2)
line([(521, 629), (529, 633)], (248, 151, 139), 2)
line([(524, 634), (532, 638)], (248, 151, 139), 2)

# Two small rounded feet peek out beneath the downy body.
ellipse((380, 832, 482, 887), (222, 127, 54))
ellipse((541, 832, 643, 887), (222, 127, 54))
ellipse((376, 855, 431, 887), (240, 151, 65))
ellipse((409, 853, 462, 889), (244, 159, 69))
ellipse((559, 853, 612, 889), (244, 159, 69))
ellipse((592, 855, 647, 887), (240, 151, 65))

# Fine, low-contrast down marks tucked against the body contour.
for x, y in [(320, 577), (314, 776), (339, 824),
             (700, 575), (711, 775), (685, 824)]:
    ellipse((x-5, y-7, x+5, y+7), (151, 173, 183))

# Subtle corner vignette, applied as a soft alpha mask.
vignette = Image.new("L", im.size, 0)
vd = ImageDraw.Draw(vignette)
vd.rectangle((0, 0, W*S, H*S), fill=70)
vd.ellipse((-150*S, -150*S, (W+150)*S, (H+150)*S), fill=0)
vignette = vignette.filter(ImageFilter.GaussianBlur(100*S))
im.paste(Image.new("RGB", im.size, (99, 128, 153)), (0, 0), vignette)

# Supersampling gives smooth clean edges at final size.
im = im.resize((W, H), Image.Resampling.LANCZOS)
im.save("entry.png", format="PNG", optimize=True)
