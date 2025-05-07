from maze import Maze, Point, Window
import time
if __name__ == "__main__":
    win = Window(800, 600)

    m = Maze(Point(20, 20), 10, 10, 30, win)

    m.solve(0,0)
    time.sleep(20)

    