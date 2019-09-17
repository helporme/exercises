from PIL import Image, ImageDraw


class Figure:
    def Parallelogram(self, x = 0, y = 0, ln = 3):
        parallelogram = {
            'A1': (x + ln, y),
            'B1': (x + ln * 2, y),
            'C1': (x + ln * 2, y + ln),
            'D1': (x, y + ln)
        }
        return self._pack(parallelogram)

    def _pack(self, figure):
        self.dict = figure
        self.points = list(figure.values())
        return self

    def _figure_methods(self):
        return {'Parallelogram': self.Parallelogram}


class Grid2d(Figure):
    def __init__(self, size=(500, 500), cells=(50, 50)):
        self.image = Image.new('RGB', size, 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.figures = self._figure_methods()

        self.x, self.y = size
        self.cx, self.cy = cells
        self.cy_size = int(self.y / self.cy)
        self.cx_size = int(self.x / self.cx)

        self.points = {}
        self.lines = {}

        self.generate_points()
        self.generate_lines()

        self._draw_lines(fill=(56, 149, 255, 255))

    def generate_points(self):
        for y in range(self.cy):
            for x in range(self.cx):
                self.points[x, y] = x * self.cx_size, y * self.cy_size

    def generate_lines(self):
        self.lines['x'] = [(0, x * self.cx_size, self.y, x * self.cx_size) for x in range(self.cx)]
        self.lines['y'] = [(y * self.cy_size, 0, y * self.cy_size, self.x) for y in range(self.cy)]

    def show(self):
        self.image.show()

    def _draw_points(self):
        for xy, cxy in self:
            self.draw.point(cxy, fill='red')

    def _draw_lines(self, fill = (0, 0, 0, 255)):
        for line in self.lines.values():
            for cxy in line:
                self.draw.line(cxy, fill=fill)

    def __iter__(self):
        return iter(self.points.items())

    def __str__(self):
        return f"<Grid2d: y({self.y}), x({self.x}), " \
               f"cells_x({self.cx}), cells_y({self.cy}), " \
               f"cell_width({self.cx_size}), cell_height({self.cy_size})>"
