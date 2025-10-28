"""
drawer.py
Responsible for drawing an image for a concept.
"""

import os
import random
from PIL import Image, ImageDraw

class Drawer:
    def __init__(self, width=400, height=400):
        self.width = width
        self.height = height

    def draw(self, concept, filename):
        """
        Draw an image based on the concept.
        Returns PIL Image object.
        """
        # Create output folder
        output_dir = os.path.join("data", "output")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        # Blank canvas
        img = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Number of shapes
        num_shapes = random.randint(5, 15)

        for _ in range(num_shapes):
            shape_type = random.choice(["circle", "rectangle", "triangle"])
            color = self.choose_color(concept)

            if shape_type == "circle":
                radius = random.randint(10, 50)
                x = random.randint(radius, self.width - radius)
                y = random.randint(radius, self.height - radius)
                draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
            elif shape_type == "rectangle":
                w = random.randint(20, 80)
                h = random.randint(20, 80)
                x = random.randint(0, self.width - w)
                y = random.randint(0, self.height - h)
                draw.rectangle([x, y, x + w, y + h], fill=color)
            else:  # triangle
                points = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(3)]
                draw.polygon(points, fill=color)

        img.save(filepath)
        return img

    def choose_color(self, concept):
        """Choose a color based on the concept"""
        concept = concept.lower()
        if concept == "tree":
            return random.choice([(34,139,34), (0,100,0), (85,107,47)])
        elif concept == "ocean":
            return random.choice([(0,105,148), (70,130,180), (0,191,255)])
        elif concept == "sun":
            return random.choice([(255,215,0), (255,165,0), (255,255,0)])
        elif concept == "mountain":
            return random.choice([(139,137,137), (105,105,105), (160,160,160)])
        elif concept == "human":
            return random.choice([(255,224,189), (205,133,63), (139,69,19)])
        else:
            return tuple(random.randint(0, 255) for _ in range(3))
