from .multimodal import MultiModal
from .text import Sentence

class DataGenerator:

    def __init__(self):
        self.multimodal = MultiModal()
        self.sentence = Sentence()

    def run(self):
        self.multimodal.run()
        self.sentence.run()