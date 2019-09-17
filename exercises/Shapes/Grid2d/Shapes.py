# Class with the coordinates of the shapes
# Existing shapes:
#   Cube
#   Square
#   Pyramid
#   Triangular pyramid
#   Triangular prism


class Shapes:
    def __init__(self, grid):
        self.grid = grid
        self.shape = {}

    def cube(self, x=1, y=1, ln=3):
        self.shape = {
            0: {
                'A': (x + int(ln / 2), y),
                'B': (x + int(ln / 2) + ln, y),
                'C': (x + ln, y + int(ln / 2)),
                'D': (x, y + int(ln / 2))
            },
            1: {
                'A': (x + int(ln / 2), y + ln),
                'B': (x + int(ln / 2) + ln, y + ln),
                'C': (x + ln, y + int(ln / 2) + ln),
                'D': (x, y + int(ln / 2) + ln)
            }
        }
        return self._pack()

    def square_pyramid(self, x=1, y=1, ln=3):
        self.shape = {
            0: {
                'O': (x + int(ln / 2), y)
            },
            1: {
                'A': (x, y + ln),
                'B': (x + int(ln / 2), y + int(ln/1.3)),
                'C': (x + ln, y + ln),
                'D': (x + int(ln/2), y + ln + int(ln/3))
            }
        }
        return self._pack()

    def triangular_pyramid(self, x=1, y=1, ln=3):
        self.shape = {
            0: {
                'O': (x + int(ln/2), y)
            },
            1: {
                'A': (x, y + ln),
                'B': (x + ln, y + ln),
                'C': (x + int(ln/2), y + int(ln/3) + ln)
            }
        }
        return self._pack()

    def triangular_prism(self, x=1, y=1, ln=3):
        self.shape = {
            0: {
                'A': (x + int(ln / 1.5), y),
                'B': (x + ln, y + int(ln/3) + ln),
                'C': (x, y + ln)
            },
            1: {
                'A': (x + int(ln / 1.5) + ln * 2, y),
                'B': (x + ln + ln * 2, y + int(ln / 3) + ln),
                'C': (x + ln * 2, y + ln)
            }
        }
        return self._pack()

    def custom_shape(self, shape):
        self.shape = shape
        return self._pack()

    def _parse(self):
        points_count = 0
        for points in self.shape.values():
            points_count += len(list(points.values()))

        # Edit names to indexes
        for layer, points in self.shape.copy().items():
            for name, point in points.copy().items():
                del self.shape[layer][name]
                # "O" connect with all points
                if name == 'O':
                    self.shape[layer][0] = point
                else:
                    self.shape[layer][ord(name) + int(layer)*(points_count*10)] = point

    def _pack(self):
        self._parse()
        self.grid._shape = self.shape
        return self.grid._draw_shape()
