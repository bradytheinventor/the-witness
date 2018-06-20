
import pygame

#constants
FRAME_SIZE = 600

STROKE_WIDTH = 25

START_LOCATION_RADIUS = 25
END_LOCATION_RADIUS = STROKE_WIDTH / 2
END_LOCATION_OFFSET = 25
CORNER_RADIUS = STROKE_WIDTH / 2

GRID_BLOCK_SIZE = 50
FRAME_PADDING = STROKE_WIDTH + 25

BOARD_DEFAULT_COLOR = (100, 100, 100)

class Board():
    #enum of possible board shapes
    class BoardShape():
        SQUARE_2x2, SQUARE_3x3, SQUARE_5x5, CROSS_3x3, CROSS_5x5, RECT_1x2, RECT_2x3 = range(7)
    
    def __init__(self):
        self.nodes = []
        self.start_nodes = []
        self.end_nodes = []
        self.board_color = BOARD_DEFAULT_COLOR

    """-"""
    def set_board_color(self, color):
        self.board_color = color

    """-"""
    def add_start_node(self, pt):
        node_at_pt = self.nodes[pt[0]][pt[1]]
        
        if node_at_pt is not None:
            self.start_nodes.append(pt)

    """-"""
    def add_end_node(self, pt):
        node_at_pt = self.nodes[pt[0]][pt[1]]

        if node_at_pt is not None:
            self.end_nodes.append(pt)

    """-"""
    def get_board_row(self, row):
        row_elements = []

        for x in range(len(self.nodes)):
            row_elements.append(self.nodes[x][row])

        return row_elements

    """-"""
    def get_board_column(self, column):
        return self.nodes[column]

    """-"""
    def draw(self, canvas):
        self.draw_grid(canvas)
        self.draw_rounded_corners(canvas)
        self.draw_start_nodes(canvas)
        self.draw_end_nodes(canvas)

    """-"""
    def draw_start_nodes(self, canvas):
        for s in range(len(self.start_nodes)):
            pt = self.start_nodes[s]
            
            start_node = self.nodes[pt[0]][pt[1]]
            pygame.draw.circle(canvas, self.board_color, start_node, START_LOCATION_RADIUS)

    """-"""
    def draw_end_nodes(self, canvas):
        for e in range(len(self.end_nodes)):
            pt = self.end_nodes[e]
            
            end_node = self.nodes[pt[0]][pt[1]]
            end_pt = list(end_node)
            
            #move the end out left or right depending on its side
            if pt[0] == 0:
                end_pt[0] -= END_LOCATION_OFFSET
            elif pt[0] == (len(self.nodes) - 1):
                end_pt[0] += END_LOCATION_OFFSET

            #move the end out up or down depending on its side
            if pt[1] == 0:
                end_pt[1] -= END_LOCATION_OFFSET
            elif pt[1] == (len(self.nodes[0]) - 1):
                end_pt[1] += END_LOCATION_OFFSET

            pygame.draw.line(canvas, self.board_color, end_node, end_pt, STROKE_WIDTH)  #TODO: this looks funny if end is diagonal
            pygame.draw.circle(canvas, self.board_color, end_pt, END_LOCATION_RADIUS)

    def draw_rounded_corners(self, canvas):
        for x in range(len(self.nodes)):
            for y in range(len(self.nodes[0])):
                if self.nodes[x][y] is not None:
                    pygame.draw.circle(canvas, self.board_color, self.nodes[x][y], CORNER_RADIUS)
    
    """-"""
    def draw_grid(self, canvas):
        rows = []
        columns = []

        #for each column
        for x in range(len(self.nodes)):
            columns.append([])
            column_x = self.get_board_column(x)

            #if the column contains a 'None' node, ignore it
            for y in range(len(column_x)):
                if column_x[y] is not None:
                    columns[x].append(column_x[y])

            pygame.draw.lines(canvas, self.board_color, False, columns[x], STROKE_WIDTH)

        #for each row
        for y in range(len(self.nodes[0])):
            rows.append([])
            row_y = self.get_board_row(y)

            #if the row contains a 'None' node, ignore it
            for x in range(len(row_y)):
                if row_y[x] is not None:
                    rows[y].append(row_y[x])
                    
            pygame.draw.lines(canvas, self.board_color, False, rows[y], STROKE_WIDTH)

    """-"""
    def set_board_shape(self, shape):

        #SQUARE_2x2
        if shape is Board.BoardShape.SQUARE_2x2:
            grid_block_size = (FRAME_SIZE - (FRAME_PADDING * 2)) / 2

            for x in range(3):
                self.nodes.append([])
                
                for y in range(3):
                    self.nodes[x].append((FRAME_PADDING + (grid_block_size * x), FRAME_PADDING + (grid_block_size * y)))

        #SQUARE_3x3
        if shape is Board.BoardShape.SQUARE_3x3:
            grid_block_size = (FRAME_SIZE - (FRAME_PADDING * 2)) / 3

            for x in range(4):
                self.nodes.append([])
                
                for y in range(4):
                    self.nodes[x].append((FRAME_PADDING + (grid_block_size * x), FRAME_PADDING + (grid_block_size * y)))

        #SQUARE_5x5
        elif shape is Board.BoardShape.SQUARE_5x5:
            grid_block_size = (FRAME_SIZE - (FRAME_PADDING * 2)) / 5

            for x in range(6):
                self.nodes.append([])

                for y in range(6):
                    self.nodes[x].append((FRAME_PADDING + (grid_block_size * x), FRAME_PADDING + (grid_block_size * y)))

        #CROSS_3x3
        elif shape is Board.BoardShape.CROSS_3x3:
            self.set_board_shape(Board.BoardShape.SQUARE_3x3)

            self.nodes[0][0] = None
            self.nodes[0][3] = None
            self.nodes[3][0] = None
            self.nodes[3][3] = None

        #CROSS_5x5
        elif shape is Board.BoardShape.CROSS_5x5:
            self.set_board_shape(Board.BoardShape.SQUARE_5x5)

            self.nodes[0][0] = None
            self.nodes[0][5] = None
            self.nodes[5][0] = None
            self.nodes[5][5] = None

        #RECT_1x2
        elif shape is Board.BoardShape.RECT_1x2:
            grid_block_size = (FRAME_SIZE - (FRAME_PADDING * 2)) / 2

            for x in range(2):
                self.nodes.append([])

                for y in range(3):
                    self.nodes[x].append((FRAME_PADDING + (grid_block_size * x), FRAME_PADDING + (grid_block_size * y)))

        #RECT_2x3
        elif shape is Board.BoardShape.RECT_2x3:
            grid_block_size = (FRAME_SIZE - (FRAME_PADDING * 2)) / 3

            for x in range(3):
                self.nodes.append([])

                for y in range(4):
                    self.nodes[x].append((FRAME_PADDING + (grid_block_size * x), FRAME_PADDING + (grid_block_size * y)))
