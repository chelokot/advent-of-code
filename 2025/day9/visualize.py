from PIL import Image
from PIL import ImageDraw

with open("input.txt") as f:
    points = list(map(
        lambda line: tuple(map(lambda x: int(x) // 100, line.split(","))), 
        f.read().splitlines()
    ))

image = Image.new("RGB", (1000, 1000), color=(0, 0, 255))

draw = ImageDraw.Draw(image)
print(points[:10])
draw.polygon(points, outline=(0, 255, 255), fill=(255, 255, 0))

image.save("./visualization.png")