"""
evaluator.py
Analyzes an image and suggests improvements for the next iteration.
"""

from PIL import ImageStat
import random

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, img):
        """
        Analyze the image and return 'improvement suggestions'.
        Currently uses simple metrics like color variance or randomness.
        """
        stat = ImageStat.Stat(img)
        mean_color = tuple(int(c) for c in stat.mean)
        suggestions = {}

        # Simple heuristic: if image is too light, add more shapes
        if sum(mean_color)/3 > 200:
            suggestions['more_shapes'] = True
        else:
            suggestions['more_shapes'] = random.choice([True, False])

        # Randomly decide if colors should be more varied
        suggestions['color_variation'] = random.choice([True, False])

        return suggestions
