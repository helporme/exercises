# Grid to draw different shapes
# Existing methods:
#   object.figure.*
#   object.draw_cells
#   object.show
#   object.clear
#
# You can see an example of use in ./example.py


from PIL import Image, ImageDraw
from io import BytesIO

from Errors import *
from Shapes import Shapes


class Grid2d:
    def __init__(self, size=(500, 500), cells=(25, 25)):
        self.image = Image.new('RGB', size, 'white')
        self.draw = ImageDraw.Draw(self.image)
        self._shape = {}
        self.shape = Shapes(self)

        self.x, self.y = size
        self.cx, self.cy = cells
        self.cy_size = int(self.y / self.cy)
        self.cx_size = int(self.x / self.cx)

        self.cells = {}
        self.lines = {}

        self._generate_cells()
        self._generate_lines()

    def show(self):
        """Show image"""
        self.image.show()

    def draw_cells(self):
        """Draws all cells"""
        for line in self.lines.values():
            for cxy in line:
                self.draw.line(cxy, fill=(3, 132, 252))

    def clear(self):
        """Clear image"""
        self.draw.rectangle((0, 0, self.image.size), fill='white')

    def _draw_shape(self):
        """
        Draw shape from class Figure
        Example:
            Grid().shape.cube()
        """

        # Get all points
        points = []
        for layer, positions in self._shape.items():
            points.extend([(layer, ind, xy) for ind, xy in positions.items()])

        # Draws main lines
        for layer, char, xy in points:
            for layer2, char2, xy2 in points:
                if char == char2 + 1 or char == char2 + layer * len(points) * 10 or char == 0:
                    try:
                        self.draw.line((self.cells[xy], self.cells[xy2]), fill='black')

                    except KeyError:
                        raise ImageToSmall(f"One of the cells {xy, xy2} not detected")

        # Connects first point with last point
        for ind, positions in self._shape.items():
            chars = list(positions.keys())
            chars.sort()

            try:
                self.draw.line((self.cells[positions[chars[0]]], self.cells[positions[chars[-1]]]), fill='black')

            except KeyError:
                raise ImageToSmall(f"One of the cells {xy, xy2} not detected")

        return self

    def _generate_cells(self):
        # Creates cell coordinates (each cell has 4 angles = 4 coordinates)
        for y in range(self.cy):
            for x in range(self.cx):
                self.cells[x, y] = x * self.cx_size, y * self.cy_size

    def _generate_lines(self):
        self.lines['x'] = [(0, x * self.cx_size, self.y, x * self.cx_size) for x in range(self.cx)]
        self.lines['y'] = [(y * self.cy_size, 0, y * self.cy_size, self.x) for y in range(self.cy)]

    def __getattr__(self, item):
        if item == 'bytes':
            bytes_img = BytesIO()
            self.save(bytes_img)
            return bytes_img.getvalue()

    def __str__(self):
        return f"<Grid2d: y({self.y}), x({self.x}), " \
               f"cells_x({self.cx}), cells_y({self.cy}), " \
               f"cell_width({self.cx_size}), cell_height({self.cy_size})>"
