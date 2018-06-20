
import pygame, math

#constants
FRAME_SIZE = 600

STROKE_WIDTH = 25

START_LOCATION_RADIUS = 25
CORNER_RADIUS = STROKE_WIDTH / 2
END_LOCATION_RADIUS = STROKE_WIDTH / 2

GRID_BLOCK_SIZE = 50
FRAME_PADDING = STROKE_WIDTH + 25

CURSOR_DEFAULT_COLOR = (255, 255, 255)

class Cursor():

    class MouseLockDir:
        NONE, HORIZONTAL, VERTICAL = range(3)

    def __init__(self):
        self.path = []
        self.path_pos = []
        self.head_pos = []
        self.cursor_color = CURSOR_DEFAULT_COLOR

        #self.mouse_lock_dir = Cursor.MouseLockDir.NONE
        self.path_started = False

    """-"""
    def set_cursor_color(self, color):
        self.cursor_color = color

    """-"""
    def set_mouse_visibility(self):
        pygame.mouse.set_visible(not self.path_started)

    """-"""
    def is_path_started(self):
        return self.path_started
    
    """-"""
    def check_for_start(self, nodes, start_nodes):
        if not self.path_started:
            for s in range(len(start_nodes)):
                m_pos = pygame.mouse.get_pos()
                s_pos = nodes[start_nodes[s][0]][start_nodes[s][1]]
                
                dist_to_s = math.hypot(m_pos[0] - s_pos[0], m_pos[1] - s_pos[1])

                if dist_to_s < START_LOCATION_RADIUS:
                    self.path_started = True
                    
                    self.path.append(start_nodes[s])
                    self.path_pos.append(s_pos)

    """-"""
    def check_for_win(self, nodes, end_nodes):
        if self.path_started:
            for e in range(len(end_nodes)):
                e_pos = nodes[end_nodes[e][0]][end_nodes[e][1]] #more nuanced than this

                if self.dist_head_to_pt(e_pos) < END_LOCATION_RADIUS:
                    #check for win
                    
                    print("end")
                    self.cancel_path()
                else:
                    self.cancel_path()

    """-"""
    def update_path_nodes(self, nodes):
        if self.path_started:
            #try to add new nodes
            for x in range(len(nodes)):
                for y in range(len(nodes[0])):
                    if (nodes[x][y] is not None) and (nodes[x][y] not in self.path_pos):
                        if self.dist_head_to_pt(nodes[x][y]) < CORNER_RADIUS:
                            self.path.append((x, y))
                            self.path_pos.append(nodes[x][y])

            #try to remove old nodes
            if len(self.path_pos) > 1:
                #print(self.path_pos)
                latest_n = self.path_pos[len(self.path_pos) - 1]
                next_latest_n = self.path_pos[len(self.path_pos) - 2]
                
                if self.dist_head_to_pt(latest_n) > CORNER_RADIUS:
                    if self.head_pos[0] < latest_n[0] and self.head_pos[0] > next_latest_n[0]:
                        self.path.pop(len(self.path) - 1)
                        self.path_pos.pop(len(self.path_pos) - 1)

                    elif self.head_pos[0] > latest_n[0] and self.head_pos[0] < next_latest_n[0]:
                        self.path.pop(len(self.path) - 1)
                        self.path_pos.pop(len(self.path_pos) - 1)

                    elif self.head_pos[1] < latest_n[1] and self.head_pos[1] > next_latest_n[1]:
                        self.path.pop(len(self.path) - 1)
                        self.path_pos.pop(len(self.path_pos) - 1)

                    elif self.head_pos[1] > latest_n[1] and self.head_pos[1] < next_latest_n[1]:
                        self.path.pop(len(self.path) - 1)
                        self.path_pos.pop(len(self.path_pos) - 1)

    """-"""
    def cancel_path(self):
        if self.path_started:
            self.path_started = False
            
            self.path = []
            self.path_pos = []

    """-"""
    def update_head_pos(self, nodes):
        if self.path_started:
            m_pos = pygame.mouse.get_pos()

            #update head position
            self.head_pos = [m_pos[0], m_pos[1]]
            
            latest_n_index = self.path[len(self.path) - 1]
            latest_n = self.path_pos[len(self.path_pos) - 1]

            #apply inter-node lock
            if self.dist_head_to_pt(latest_n) > CORNER_RADIUS:
                if abs(self.head_pos[0] - latest_n[0]) > CORNER_RADIUS:
                    self.head_pos[1] = latest_n[1]
                    
                elif abs(self.head_pos[1] - latest_n[1]) > CORNER_RADIUS:
                    self.head_pos[0] = latest_n[0]

            #apply self-collision lock
            for n in range(len(self.path_pos)):
                if self.path_pos[n] is not latest_n:
                    if self.dist_head_to_pt(self.path_pos[n]) < (CORNER_RADIUS * 2):
                        #if the head is touching this node, correct
                        if self.head_pos[0] < self.path_pos[n][0]:
                            self.head_pos[0] = self.path_pos[n][0] - (CORNER_RADIUS * 2)

                        elif self.head_pos[0] > self.path_pos[n][0]:
                            self.head_pos[0] = self.path_pos[n][0] + (CORNER_RADIUS * 2)

                        elif self.head_pos[1] < self.path_pos[n][1]:
                            self.head_pos[1] = self.path_pos[n][1] - (CORNER_RADIUS * 2)

                        elif self.head_pos[1] > self.path_pos[n][1]:
                            self.head_pos[1] = self.path_pos[n][1] + (CORNER_RADIUS * 2)
            
            #apply x border lock
            if latest_n_index[0] == 0:
                if self.head_pos[0] < latest_n[0]:
                    self.head_pos[0] = latest_n[0]

            elif latest_n_index[0] == len(nodes) - 1:
                if self.head_pos[0] > latest_n[0]:
                    self.head_pos[0] = latest_n[0]

            #apply x null node lock
            elif nodes[latest_n_index[0] - 1][latest_n_index[1]] is None:
                if self.head_pos[0] < latest_n[0]:
                    self.head_pos[0] = latest_n[0]

            elif nodes[latest_n_index[0] + 1][latest_n_index[1]] is None:
                if self.head_pos[0] > latest_n[0]:
                    self.head_pos[0] = latest_n[0]

            #apply y border lock
            if latest_n_index[1] == 0:
                if self.head_pos[1] < latest_n[1]:
                    self.head_pos[1] = latest_n[1]

            elif latest_n_index[1] == len(nodes[0]) - 1:
                if self.head_pos[1] > latest_n[1]:
                    self.head_pos[1] = latest_n[1]

            #apply y null node lock
            elif nodes[latest_n_index[0]][latest_n_index[1] - 1] is None:
                if self.head_pos[1] < latest_n[1]:
                    self.head_pos[1] = latest_n[1]

            elif nodes[latest_n_index[0]][latest_n_index[1] + 1] is None:
                if self.head_pos[1] > latest_n[1]:
                    self.head_pos[1] = latest_n[1]

    """-"""
    def lock_mouse(self):
        if self.path_started:
            pygame.mouse.set_pos((self.head_pos[0], self.head_pos[1]))

    """-"""
    def dist_head_to_pt(self, pt):
        return math.hypot(pt[0] - self.head_pos[0], pt[1] - self.head_pos[1])

    """-"""
    def draw(self, canvas):
        #draw starting circle and head
        if len(self.path) > 0:
            pygame.draw.circle(canvas, self.cursor_color, self.path_pos[0], START_LOCATION_RADIUS)

            self.draw_head(canvas)

        #draw node segments
        if len(self.path) > 1:
            pygame.draw.lines(canvas, self.cursor_color, False, self.path_pos, STROKE_WIDTH)

            for n in range(len(self.path)):
                pygame.draw.circle(canvas, self.cursor_color, self.path_pos[n], CORNER_RADIUS)
        
    """-"""
    def draw_head(self, canvas):
        latest_n = self.path_pos[len(self.path_pos) - 1]

        if self.dist_head_to_pt(latest_n) > CORNER_RADIUS:
            pygame.draw.line(canvas, self.cursor_color, latest_n, self.head_pos, STROKE_WIDTH)
            pygame.draw.circle(canvas, self.cursor_color, self.head_pos, CORNER_RADIUS)
