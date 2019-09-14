from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class Graph:
    def __init__(self, problem, size=(1000, 1000)):
        self.image = Image.new('RGB', size, 'white')

        self.x, self.y = self.image.size
        self.mid = int((self.x + self.y) / 2)
        self.scale = int(self.mid / 200)
        self.problem = problem.replace(' ', '')

        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype('calibri.ttf', 10+int(1.5*self.scale))

        self.create()

    def _draw_text(self, xy, text):
        self.draw.text(xy, text, font=self.font, fill=(255, 0, 0, 255))

    def _draw_line(self, xy, color='black'):
        self.draw.line(xy, fill=color)

    def points(self):
        points = []
        for x in range(-self.mid, self.mid+1, 1):
            try:
                y = -eval(self.problem.replace('x', f"({x})"))
            except ZeroDivisionError:
                continue

            if isinstance(y, complex):
                y = y.real

            # If the coordinates are more than the sides
            # of the image
            x, y = x * self.scale, y * self.scale
            if not (abs(x) >= self.x or abs(y) >= self.y):
                points.append((int(self.x / 2 + x), int(self.y / 2 + y)))

        return points

    def blank(self, points):
        # Draw x,y lines
        self._draw_line((0, self.y / 2, self.x, self.y / 2))
        self._draw_line((self.x / 2, 0, self.x / 2, self.y))

        # Draw tiny lines
        for x, y in points:
            self._draw_line((x, self.y / 2 - self.scale / 2, x, self.y / 2 + self.scale / 1.5))
            self._draw_line((self.x / 2 - self.scale / 2, y, self.x / 2 + self.scale / 1.5, y))

        # Draw x, y symbols
        self._draw_text((self.x - 3 * self.scale, self.y / 2 + self.scale), 'x')
        self._draw_text((self.x / 2 + 2 * self.scale, 0), 'y')

        # Draw 0,0 pos
        self._draw_text((self.x / 2 + 2 * self.scale, self.y / 2 + self.scale), '0, 0')

        # Draw problem
        self._draw_text((10, 10), f"y={self.problem}")

    def draw_points(self, points):
        ox, oy = points[0]
        for n, (x, y) in enumerate(points[1:]):
            if not abs((x + y) - (ox + oy)) > 100 * self.scale:
                self._draw_line((ox, oy, x, y), 'blue')
            ox, oy = x, y

    def create(self):
        points = self.points()
        self.blank(points)
        self.draw_points(points)

    def save(self, name):
        self.image.save(name, 'PNG')

    def show(self):
        self.image.show()

    def __str__(self):
        return f"<Graph object: problem({self.problem})>"

    def __getattr__(self, item):
        if item == 'bytes':
            bytes_img = BytesIO()
            self.image.save(bytes_img, format='PNG')
            return bytes_img.getvalue()

        elif item == 'points':
            return self.points()
