from tkinter import Tk, BOTH, Canvas
import time, random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1: Point, p2:Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, c: Canvas, color):
        c.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=color, width=2)

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title = "My Window"
        self.canvas = Canvas(width=width, height=height)
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        pass


    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, l: Line, color):
        l.draw(self.canvas, color)

class Cell:
    def __init__(self, p1: Point, p2: Point, win: Window, left: bool = True, right: bool = True, top: bool = True, bottom: bool= True, size=20):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.top_left = p1
        self.bottom_right = p2
        self.win = win
        self.size = size
        self.visited = False
    
    def draw(self):
        print(self.top, self.left, self.bottom, self.right)

        background = "gray"

        color1 = background if not self.left else "black"

        self.win.draw_line(Line(self.top_left, Point(self.top_left.x, self.top_left.y + self.size)), color1)
        
        color2 = background if not self.top else "black"
        self.win.draw_line(Line(self.top_left, Point(self.top_left.x + self.size, self.top_left.y)), color2)

        color3 = background if not self.bottom else "black"
        self.win.draw_line(Line(Point(self.bottom_right.x - self.size, self.bottom_right.y), self.bottom_right), color3)

        color4 = background if not self.right else "black"
        self.win.draw_line(Line(self.bottom_right, Point(self.bottom_right.x, self.bottom_right.y - self.size) ), color4)
            
    def draw_move(self, to_cell, undo: bool = False):
        center1 = Point(self.top_left.x + (self.bottom_right.x - self.top_left.x)/2, 
                        self.bottom_right.y + (self.top_left.y - self.bottom_right.y)/2)
        
        center2 = Point(to_cell.top_left.x + (to_cell.bottom_right.x - to_cell.top_left.x)/2, 
                        to_cell.bottom_right.y + (to_cell.top_left.y - to_cell.bottom_right.y)/2)

        
        color = "gray" if not undo else "red"

        self.win.draw_line(Line(center1, center2), color)
        
class Maze:
    def  __init__(self, p1: Point, num_rows, num_cols, size, win: Window, seed = None):
        self.p1 = p1
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.size = size
    
        self.win = win
        self._cells = []

        if seed != None:
            random.seed(seed)

        self._create_cells()
        self._break_entrace_and_exit()

        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def solve(self, i, j):
        return self._solve_r(i, j)

    def _wall_exists(self, cell1, direction):
        if direction == "left":
            if cell1.left == False:
                return True 
        elif direction == "top":
            if cell1.top == False:
                return True
        elif direction == "right":
            if cell1.right == False:
                return True
        elif direction == "bottom":
            if cell1.bottom == False:
                return True
        return False
    
    def _solve_r(self, i, j):
        self._animate()

        current_cell = self._cells[i][j]
        current_cell.visited = True

        last_cell = self._cells[self.num_rows-1][self.num_cols-1]

        if current_cell == last_cell:
            return True


        dirs = [
            ((i-1,j), "top"), ((i,j-1), "left"), ((i+1,j), "bottom"),  ((i,j+1), "right"), 
        ]

        for dir in dirs:    
            temp_i, temp_j = dir[0][0], dir[0][1]
            
            try:
                temp_cell = self._cells[temp_i][temp_j]
            except IndexError:
                continue
            
            if temp_cell == None:
                print("no cell")
                continue
            
            if temp_cell.visited:
                print("is already visited")
                continue

            if self._wall_exists(temp_cell, dir[1]):
                print("wall exists")
                continue
                
            current_cell.draw_move(temp_cell, undo=True)
            
            time.sleep(0.5)
            
            result = self._solve_r(temp_i, temp_j)
            if result:
                return True
            
            current_cell.draw_move(temp_cell)
        
        return False

    def _break_entrace_and_exit(self):
        first_cell = self._cells[0][0]
        last_cell = self._cells[self.num_rows-1][self.num_cols-1]

        first_cell.left = False
        last_cell.right = False

        print(first_cell.top_left.x, first_cell.top_left.y)

        print(last_cell.bottom_right.x, last_cell.bottom_right.y)

        first_cell.draw()
        last_cell.draw()
        self._animate()
        
    def _reset_cells_visited(self):

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            top_cell, left_cell, bottom_cell, right_cell = None, None, None, None

            if i > 0:
                top_cell = self._cells[i-1][j]
            
            if j > 0:
                left_cell = self._cells[i][j-1]
    
            if i < self.num_rows - 1:
                bottom_cell = self._cells[i+1][j]

            if j < self.num_cols - 1:
                right_cell = self._cells[i][j+1]

            dirs = [
                (top_cell, "top"), (left_cell, "left"), (bottom_cell, "bottom"),  (right_cell, "right"), 
            ]

            next_dirs = []
            
            for elem in dirs:
                if elem[0] != None:
                    if not elem[0].visited:
                        next_dirs.append(elem)

            if len(next_dirs) <= 0:
                return 

            next_node = random.randrange(len(next_dirs))
            next_node = next_dirs[next_node]
            next_cell = None
            next_i, next_j = 0, 0

            if next_node[1] == "top":
                next_i, next_j = i-1, j
                next_cell = self._cells[next_i][next_j]
                current_cell.top = False
                next_cell.bottom = False
                
            elif next_node[1] == "bottom":
                next_i, next_j = i+1, j
                next_cell = self._cells[next_i][next_j]
                current_cell.bottom = False
                next_cell.top = False

            elif next_node[1] == "right":
                next_i, next_j = i, j+1
                next_cell = self._cells[next_i][next_j]
                current_cell.right = False
                next_cell.left = False
            
            elif next_node[1] == "left":
                next_i, next_j = i, j-1
                next_cell = self._cells[next_i][next_j]
                current_cell.left = False
                next_cell.right = False

            current_cell.draw()
            next_cell.draw()
            self._animate()

            self._break_walls_r(next_i, next_j)

    def _create_cells(self):
        for i in range(self.num_rows):
            temp_row = []
            for j in range(self.num_cols):
                
                temp_p1_x = self.p1.x + (i + 1) * self.size
                temp_p1_y = self.p1.y + (j + 1) * self.size

                temp_p2_x = self.p1.x + (i + 1) * self.size + self.size
                temp_p2_y = self.p1.y + (j + 1) * self.size + self.size

                p1 = Point(temp_p1_x, temp_p1_y)
                p2 = Point(temp_p2_x, temp_p2_y)
                cell = Cell(p1, p2, self.win, size=self.size)
                temp_row.append(cell)
            
            self._cells.append(temp_row)
        
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw()
        self._animate(interval=0.0005)

    def _animate(self, interval=0.05):
        self.win.redraw()
        time.sleep(interval)