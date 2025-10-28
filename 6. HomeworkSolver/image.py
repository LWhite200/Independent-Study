"""
image.py
Main script: draws images, evaluates, and improves over iterations.
"""

from agents.drawer import Drawer
from agents.evaluator import Evaluator
import os

concepts = ["Tree", "Ocean", "Human", "Sun", "Mountain"]

if __name__ == "__main__":
    drawer = Drawer()
    evaluator = Evaluator()
    output_dir = os.path.join("data", "output")
    os.makedirs(output_dir, exist_ok=True)

    iterations = 3  # number of improvements per concept

    for concept in concepts:
        print(f"\n🎨 Drawing concept: {concept}")
        last_img = None

        for i in range(1, iterations+1):
            filename = f"{concept.lower()}_iter{i}.png"
            img = drawer.draw(concept, filename)
            last_img = img

            suggestions = evaluator.evaluate(img)
            print(f"  Iteration {i}: suggestions -> {suggestions}")

        print(f"✅ Completed concept: {concept}")
