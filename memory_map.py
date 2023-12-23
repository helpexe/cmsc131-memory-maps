# Import statements
from manim import *
from numpy import *


class MemoryMap(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stack = self.Stack()

        # Add components to be animated in the scene
        self.add(self.stack)

    def push(self, label, value):
        return self.stack.push(label, value)

    def add_frame(self, name, fcolor):
        return self.stack.add_frame(name, fcolor)

    def drop_frame(self):
        return self.stack.drop_frame()

    class Stack(VMobject):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            # Instance variables
            self.frame_index = 0
            self.boxes = VGroup(*[Rectangle(height=0.5, width=1) for _ in range(12)])
            self.frames = VGroup()

            # Create the stack and its title
            self.boxes.arrange(direction=UP, buff=0)
            stack_title = (Tex(str("Stack"))
                           .set_height(self.boxes[0].height / 2)
                           .move_to(self.boxes[-1])
                           .set_z_index(1))
            self.font_size = stack_title.font_size

            # Create starting frame
            main_frame = self.Frame("main", self.boxes, self.frame_index, self.font_size, WHITE)
            self.frames.add(main_frame)

            # Add components to be animated in the scene
            self.add(self.boxes, stack_title, self.frames)

        def push(self, label, value):
            self.frame_index += 1
            return self.frames[-1].push(label, value)

        def add_frame(self, name, fcolor):
            new_frame = self.Frame(name, self.boxes, self.frame_index, self.font_size, fcolor)
            self.frames.add(new_frame)
            return FadeIn(new_frame)

        def drop_frame(self):
            old_frame = self.frames[-1]
            animation_group, self.frame_index = old_frame.drop_frame()
            self.frames.remove(old_frame)
            return animation_group

        class Frame(VMobject):
            def __init__(self, name, boxes, loc, font_size, font_color, **kwargs):
                super().__init__(**kwargs)

                # Instance variables
                self.start = self.end = loc
                self.name = str(name)
                self.boxes = boxes
                self.font_size = font_size
                self.frame_color = font_color
                self.empty = True

                # Frame components to be animated in the scene
                self.values = VGroup()
                self.labels = VGroup()
                self.br = (BraceLabel(boxes[loc], self.name, LEFT, Tex, buff=1.5, font_size=self.font_size)
                           .set(color=self.frame_color))

                self.add(self.values, self.labels, self.br)

            def __peek(self) -> VMobject:
                return self.boxes[self.end]

            def __create_value(self, value):
                box = self.__peek()
                return (
                    Tex(str(value))
                    .set_color(self.frame_color)
                    .move_to(box)
                    .set_z_index(1)
                    .set(font_size=self.font_size)
                )

            def __create_label(self, label) -> Tex:
                box = self.__peek()
                return (
                    Tex(str(label))
                    .set_color(self.frame_color)
                    .next_to(box, LEFT, buff=0.2)
                    .set_z_index(1)
                    .set(font_size=self.font_size)
                )

            def push(self, label, value):
                new_value = self.__create_value(value)
                new_label = self.__create_label(label)

                self.values.add(new_value)
                self.labels.add(new_label)
                self.end += 1

                old_br = self.br
                self.br = BraceLabel(
                    VGroup(*[self.boxes[i] for i in range(self.start, self.end)]),
                    self.name, LEFT, Tex, buff=1.5, font_size=self.font_size
                ).set(color=self.frame_color)

                return AnimationGroup(
                    FadeIn(new_value),
                    FadeIn(new_label),
                    ReplacementTransform(old_br, self.br)
                )

            def drop_frame(self):
                return AnimationGroup(
                    FadeOut(self.br),
                    *[FadeOut(self.values[i]) for i in range(self.end - self.start)],
                    *[FadeOut(self.labels[i]) for i in range(self.end - self.start)]
                ), self.start
