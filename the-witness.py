
import pygame, sys
from pygame.locals import *

from board import *
from cursor import *

#constants
FRAME_SIZE = 600
FPS = 60

STROKE_WIDTH = 10
GRID_BLOCK_SIZE = 50
FRAME_PADDING = 10

#initialize pygame and start frame
pygame.init()
canvas = pygame.display.set_mode((FRAME_SIZE, FRAME_SIZE))
pygame.display.set_caption("The Witness Puzzles")

class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.board = Board()
        self.board.set_board_shape(Board.BoardShape.CROSS_5x5)
        self.board.set_board_color((255, 255, 255))
        self.board.add_start_node((1, 0))
        self.board.add_end_node((4, 5))

        self.cursor = Cursor()
        self.cursor.set_cursor_color((175, 255, 57))

    def draw_board(self):
        self.board.draw(canvas)

    def draw_path(self):
        self.cursor.draw(canvas)

#init game
game = Game()

#main loop
while 1:
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                game.cursor.check_for_win(game.board.nodes, game.board.end_nodes)
                game.cursor.check_for_start(game.board.nodes, game.board.start_nodes)

            if pygame.mouse.get_pressed()[2]:
                game.cursor.cancel_path()

    #update cursor and lock mouse to grid
    game.cursor.set_mouse_visibility()
    game.cursor.update_head_pos(game.board.nodes)   #fix unsnapping at nodes
    game.cursor.lock_mouse()
    
    #check if the cursor has reached a new node
    game.cursor.update_path_nodes(game.board.nodes) #fix phasing through nodes
                                                    #from moving the mouse too fast

    #draw game
    game.draw_board()
    game.draw_path()

    #update display and tick clock
    pygame.display.update()
    canvas.fill((75, 157, 255))

    game.clock.tick(FPS)
