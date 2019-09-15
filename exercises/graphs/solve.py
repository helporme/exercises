from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class Graph:
    def __init__(self, problem, *methods, size=(1000, 1000)):
        self.methods = self.__import_methods(methods)
        self.image = Image.new('RGB', size, 'white')

        self.x, self.y = self.image.size
        self.mid = int((self.x + self.y) / 2)
        self.scale = int(self.mid / 200)
        self.problem = problem
        self.points = []

        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype('calibri.ttf', 10+int(1.5*self.scale))

        self.create()

    def _draw_text(self, xy, text, color='red'):
        self.draw.text(xy, text, font=self.font, fill=color)

    def _draw_line(self, xy, color='black'):
        self.draw.line(xy, fill=color)

    def get_points(self):
        for x in range(-self.mid, self.mid+1, 1):
            task = self.problem.replace('x', f"({x})")
            for name, method in self.methods.items():
                task = task.replace(name, f"self.methods['{name}']")

            try:
                y = -eval(task)
            except ZeroDivisionError:
                continue

            if isinstance(y, complex):
                y = y.real

            # If the coordinates are more than the sides
            # of the image
            x, y = x * self.scale, y * self.scale
            if not (abs(x) >= self.x or abs(y) >= self.y):
                self.points.append((int(self.x / 2 + x), int(self.y / 2 + y)))

    def marks(self):
        # Draw marks
        for x, y in self.points:
            self._draw_line((x, self.y / 2 - self.scale / 2, x, self.y / 2 + self.scale / 1.5))
            self._draw_line((self.x / 2 - self.scale / 2, y, self.x / 2 + self.scale / 1.5, y))

    def blank(self):
        # Draw x,y lines
        self._draw_line((0, self.y / 2, self.x, self.y / 2))
        self._draw_line((self.x / 2, 0, self.x / 2, self.y))

        # Draw x, y symbols
        self._draw_text((self.x - 3 * self.scale, self.y / 2 + self.scale), 'x')
        self._draw_text((self.x / 2 + 2 * self.scale, 0), 'y')

        # Draw 0,0 pos
        self._draw_text((self.x / 2 + 2 * self.scale, self.y / 2 + self.scale), '0, 0')

        # Draw problem
        self._draw_text((10, 10), f"y={self.problem}")

    def draw_points(self):
        ox, oy = self.points[0]
        for x, y in self.points[1:]:
            if not abs((x + y) - (ox + oy)) > 100 * self.scale:
                self._draw_line((ox, oy, x, y), 'blue')
            ox, oy = x, y

    def create(self):
        self.blank()
        self.get_points()
        self.draw_points()

    def save(self, name):
        self.image.save(name, 'PNG')

    def show(self):
        self.image.show()

    @staticmethod
    def __import_methods(methods):
        module = __import__('numpy', fromlist=list(methods))
        methods = [getattr(module, method) for method in methods]
        return {getattr(method, '__name__'): method for method in methods}

    def __getattr__(self, item):
        if item == 'bytes':
            bytes_img = BytesIO()
            self.save(bytes_img)
            return bytes_img.getvalue()

    def __str__(self):
        return f"<Graph object: problem({self.problem})>"
