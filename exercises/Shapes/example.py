from Grid2d.Grid import Grid2d


def main():
    grid = Grid2d()
    grid.draw_cells()
    grid.shape.cube()
    grid.show()
    grid.clear()

if __name__ == '__main__':
    main()
