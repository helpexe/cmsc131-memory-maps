from manim import *
from memory_map import MemoryMap


class MemoryMapDemo(Scene):
    def construct(self):
        mem_map = MemoryMap()

        self.play(Write(mem_map))

        # Add two elements to main frame
        for i in range(4):
            self.play(mem_map.push(f"x{i}", i))

        # Create new frame, add two elements
        self.play(mem_map.add_frame("foo", BLUE_D))
        for i in range(2):
            self.play(mem_map.push(f"y{i}", i))

        # Try to drop the frame
        self.play(mem_map.drop_frame())

        # Add an element to main frame
        self.play(mem_map.push("filler", 21))

        # Create one more frame, add three elements
        self.play(mem_map.add_frame("volume", RED_D))
        for i in range(3):
            self.play(mem_map.push(f"z{i}", i))

        # Drop remaining frames
        self.play(mem_map.drop_frame())
        self.play(mem_map.drop_frame())

        # Let things hang around...
        self.wait(3)
