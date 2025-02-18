from ..scene import Scene

class ResultGenerator:
    def __init__(self, scene: Scene):
        self.scene = scene

    def generate_result(self):
        return self.scene.generate_result()