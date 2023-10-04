from dataclasses import dataclass
from enum import Enum
import numpy as np
from PIL import Image


class ColorEnum(Enum):
    BLACK = 0
    WHITE = 1


# class Field:
#     def __init__(self, coordinates) -> None:
#         self.color = ColorEnum.WHITE  # color must be 1 - white and 0 - black
#         self.coordinates = coordinates

#     def invert_color(self):
#         match self.color:
#             case ColorEnum.WHITE:
#                 self.color = ColorEnum.BLACK
#             case ColorEnum.BLACK:
#                 self.color = ColorEnum.WHITE

#     def get_color_onebit(self):
#         return self.color.value


class Area:
    def __init__(self, y=1024, x=1024) -> None:
        self.matrix = np.empty((y, x), dtype=bool)  # in matrix x - cols, y - rows ([rows, cols]  == [y, x])
        self.initialize_area()

    def initialize_area(self):
        rows, cols = self.get_area_size()
        
        for i in range(rows):
            for j in range(cols):
                # self.matrix[i, j] = Field((i, j))
                self.matrix[i, j] = 1

    def get_field(self, rows_y, cols_x):
        return self.matrix[rows_y , cols_x]
    
    def set_field(self, rows, cols, field):
        self.matrix[rows, cols] = field

    def check_border(self, rows, cols):
        rows_size, cols_size = self.get_area_size()

        if any([
            rows + 1 > rows_size,
            rows < 0,
            cols + 1 > cols_size,
            cols < 0,
        ]):
            return False
        
        return True
    
    def get_area_size(self):
        return self.matrix.shape

    


class Direction:
    def __init__(self, y=1, x=0) -> None:  # default values direction to UP
        self.y = y
        self.x = x

    def rotate(self, color):
        # color = field

        match ColorEnum(color):
            case ColorEnum.BLACK:
                self.turn_counterclockwise()
            case ColorEnum.WHITE:
                self.turn_clockwise()
            case _:
                raise Exception('Unvalid ColorEnum for process rotate direction')

    def turn_clockwise(self):
        x_rotate_coefficient = 1
        y_rotate_coefficient = -1

        self.x, self.y = self.turn_wise(x_rotate_coefficient, y_rotate_coefficient)

    def turn_counterclockwise(self):
        x_rotate_coefficient = -1
        y_rotate_coefficient = 1

        self.x, self.y = self.turn_wise(x_rotate_coefficient, y_rotate_coefficient)

    def turn_wise(self, x_rotate_coefficient, y_rotate_coefficient):
        if self.x:
            x = 0
        else:
            x = self.y * x_rotate_coefficient

        if self.y:
            y = 0
        else:
            y = self.x * y_rotate_coefficient

        return x, y


class Position:
    def __init__(self, x=511, y=511) -> None:  # default value position on Centre
        self.x = x
        self.y = y

    def do_next_step(self, direction):

        self.x += direction.x
        self.y += direction.y

    def get_positions(self):
        return self.x, self.y
    

def invert_color(color):
    match ColorEnum(color):
        case ColorEnum.BLACK:
            return ColorEnum.WHITE.value
        case ColorEnum.WHITE:
            return ColorEnum.BLACK.value


class Ant:
    def __init__(self, position: Position, area: Area, direction: Direction) -> None:
        self.position = position
        self.area = area
        self.direction = direction

    def do_next_step(self):
        cols_x, rows_y = self.position.get_positions()
        # current_field = self.area.get_field(
        #     cols=cols,
        #     rows=rows,
        # )
        field_color = self.area.get_field(
            cols_x=cols_x,
            rows_y=rows_y,
        )


        self.direction.rotate(field_color)
        
        
        # field_color.invert_color()
        field_color = invert_color(field_color)

        self.area.set_field(
            rows=rows_y,
            cols=cols_x,
            field=field_color,
        )

        if not self.area.check_border(
            cols=cols_x + 1,
            rows=rows_y + 1,
        ):
            return False

        self.position.do_next_step(self.direction)
        create_picture(self.area)
        return True


def create_picture(area: Area):
    area_size = area.get_area_size()
    
    image = Image.new('1', area_size)

    for y in range(area_size[0]):
        for x in range(area_size[1]):
            color = area.get_field(cols_x=x, rows_y=y)
            # color = field.get_color_onebit()
            image.putpixel((x, y), int(color))

    image.save('matrix_ant.png')
        

def main():

    position = Position(1, 1)
    area = Area(4, 4)
    direction = Direction()

    ant = Ant(
        position,
        area,
        direction
    )
    
    next_step = True

    while next_step:
        next_step = ant.do_next_step()

    
    create_picture(area)
    
    
if __name__ == '__main__':
    main()

















# @dataclass
# class Position:
#     x: int = 511
#     y: int = 511


# class VerticalEnum(Enum):
#     UP = 1
#     DOWN = -1

# class HorizontalEnum(Enum):
#     RIGHT = 1
#     LEFT = -1

# class DirectionEnum(Enum):
#     UP = (0, 1)
#     DOWN = (0, -1)
#     RIGHT = (1, 0)
#     LEFT = (-1, 0)