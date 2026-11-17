from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path("assets")
OUT.mkdir(exist_ok=True)
W = 960

def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, size)

def generate(path, height, footer=False):
    count = 18
    frames = []
    tracks = [
        [(0, 18), (160, 18), (187, 37), (340, 37), (366, 18), (535, 18)],
        [(960, 31), (805, 31), (779, 53), (642, 53), (621, 38), (545, 38)],
        [(0, height - 26), (144, height - 26), (170, height - 49), (334, height - 49), (365, height - 26), (520, height - 26)],
        [(960, height - 18), (793, height - 18), (763, height - 43), (602, height - 43)],
        [(0, height // 2), (125, height // 2), (150, height // 2 - 13), (263, height // 2 - 13)],
        [(960, height // 2 + 8), (820, height // 2 + 8), (799, height // 2 + 20), (701, height // 2 + 20)]
    ]
    if footer:
        tracks = tracks[:4]

    def point_at(points, progress):
        lengths = [math.dist(a,b) for a,b in zip(points, points[1:])]
        distance = progress * sum(lengths)
        for a,b,L in zip(points,points[1:],lengths):
            if distance <= L:
                t=distance/L
                return (round(a[0]+t*(b[0]-a[0])),round(a[1]+t*(b[1]-a[1])))
            distance-=L
        return points[-1]

    for frame_no in range(count):
        im = Image.new("RGB", (W,height), "#070709")
        d = ImageDraw.Draw(im)
        for i,points in enumerate(tracks):
            d.line(points, fill="#6a1322", width=2, joint="curve")
            for x,y in [points[0],points[-1]]:
                d.ellipse((x-3,y-3,x+3,y+3),fill="#a61e32")
            phase=((frame_no/count)+(i*0.23))%1
            x,y=point_at(points,phase)
            d.ellipse((x-11,y-11,x+11,y+11),fill="#2a080e")
            d.ellipse((x-6,y-6,x+6,y+6),fill="#8e122a")
            d.ellipse((x-3,y-3,x+3,y+3),fill="#ff3a50")

        if not footer:
            d.rounded_rectangle((263,55,697,116),radius=5,fill="#070709")
            title_left="ALLAN"
            title_right="SANTANA"
            f=font(33,True)
            left_box=d.textbbox((0,0),title_left,font=f)
            right_box=d.textbbox((0,0),title_right,font=f)
            left_w=left_box[2]
            right_w=right_box[2]
            gap=13
            start=(W-left_w-right_w-gap)/2
            d.text((start,59),title_left,fill="#f2edf0",font=f)
            d.text((start+left_w+gap,59),title_right,fill="#ef233c",font=f)
            desc="SOFTWARE DEVELOPER"
            d.text((W/2,103),desc,font=font(11),anchor="mm",fill="#c7adb4",stroke_width=0)
        else:
            d.rounded_rectangle((277,29,683,60),radius=4,fill="#070709")
            d.text((W/2,45),"BUILDING  ·  LEARNING  ·  EVOLVING",font=font(13),anchor="mm",fill="#e1c7ce")
        frames.append(im.quantize(colors=32))
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True,disposal=2)

generate(OUT/"circuit-header.gif",150)
generate(OUT/"circuit-footer.gif",90,True)

readme=Path("README.md")
text=readme.read_text(encoding="utf-8")
text=text.replace("./assets/circuit-header.svg","./assets/circuit-header.gif")
text=text.replace("./assets/circuit-footer.svg","./assets/circuit-footer.gif")
readme.write_text(text,encoding="utf-8")
