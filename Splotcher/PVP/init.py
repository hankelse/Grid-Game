##pvp where if one player touches another's splotch they die
# if the a player hits another player they win


import pygame, sys, time, random, math
from pygame.constants import K_SPACE, K_ESCAPE, K_w, K_a, K_s, K_d, K_r, K_LEFT, K_RIGHT, K_UP, K_DOWN
pygame.init()

def sigmoid(x):
    if x<0: return(-1)
    if x>0: return(1)
    else: return(0)
def up_key(keys, controls):
    if controls == 1:
        if keys[K_UP]:return True
        return False
    if controls == 2:
        if keys[K_w]:return True
        return False
def down_key(keys, controls):
    if controls == 1:
        if keys[K_DOWN]:return True
        return False
    if controls == 2:
        if keys[K_s]:return True
        return False
def left_key(keys, controls):
    if controls == 1:
        if keys[K_LEFT]:return True
        return False
    if controls == 2:
        if keys[K_a]:return True
        return False
def right_key(keys, controls):
    if controls == 1:
        if keys[K_RIGHT]:return True
        return False
    if controls == 2:
        if keys[K_d]:return True
        return False


class Grid:
    def __init__(self, grid_size):
        self.grid_unit_size = grid_size
    def print_grid(self):
        for grid_row in range(0,height,self.grid_unit_size):
            for grid_space in range(0,width,self.grid_unit_size):
                pygame.draw.rect(screen, grid_cell_back_color, pygame.Rect(grid_space+(int(self.grid_unit_size/20)), grid_row+(int(self.grid_unit_size/20)), self.grid_unit_size-(int(self.grid_unit_size/10)),self.grid_unit_size-(int(self.grid_unit_size/10))))
                pygame.draw.rect(screen, grid_cell_color, pygame.Rect(grid_space+(int(self.grid_unit_size/10)), grid_row+(int(self.grid_unit_size/10)), self.grid_unit_size-(int(self.grid_unit_size/5)),self.grid_unit_size-(int(self.grid_unit_size/5))))
    def convert(self, x, convert_from="", mode=""): #convert_from: "grid" or "coord", mode: "move" or "set"
        if convert_from == "coord":
            if mode == "set":
                return((x+grid_unit_size/2)/grid_unit_size)
            elif mode =="move":
                return(x/grid_unit_size)
            else: print(mode, "is not a valid mode")
        elif convert_from == "grid":
            if mode == "set":
                return(x*grid_unit_size-(grid_unit_size/2))
            elif mode == "move":
                return(x*grid_unit_size)
            else: print(mode, "is not a valid mode")
        else: print(convert_from, "is not a valid form")

class Character:
    def __init__(self, x, y, controls, colors_dict):
        self.x = x
        self.y = y
        self.controls = controls
        self.moves = [["0", "0"]]
        self.splotches = []
        self.player_color = colors_dict["player_color"]
        self.splotch_color = colors_dict["splotch_color"]
        self.eye_color = colors_dict["eye_color"]
        self.x_direction, self.y_direction = 0, 0
    def get_moves(self, keys):
        self.x, self.y = round(self.x), round(self.y)
        is_new_move = False
        self.new_moves = []
        if self.x + 1 <= grid_size and right_key(keys, self.controls)== True:
            self.new_moves.append([1, 0])
        elif self.x - 1 >= 1 and left_key(keys, self.controls) == True:
            self.new_moves.append([-1, 0])
        if self.y + 1 <= grid_size and down_key(keys, self.controls) == True:
            self.new_moves.append([0, 1])
        elif self.y - 1 >= 1 and up_key(keys, self.controls) == True:
            self.new_moves.append([0, -1])
        if len(self.new_moves) >= 1: 
            for move in self.new_moves:
                self.moves = new_move(self.moves, move[0], move[1], player_move_duration)    
    def move(self, keys):
        self.moves, self.x, self.y, new_move, direction = move(self.moves, self.x, self.y)
        if new_move == True:
            self.new_splotch()
            self.x_direction, self.y_direction = int(direction[0]), int(direction[1])
            print(self.x_direction, self.y_direction)
        if len(self.moves) == 0:
            self.get_moves(keys)

    def draw(self):
        #print(self.x_direction, self.y_direction)
        pygame.draw.ellipse(screen, self.player_color, pygame.Rect(grid.convert(self.x,"grid", "set")-player_size/2, grid.convert(self.y, "grid", "set")-player_size/2, player_size, player_size))
        pygame.draw.ellipse(screen, self.eye_color, pygame.Rect(grid.convert(self.x,"grid", "set")-player_size/8+ (player_size/4*self.x_direction), grid.convert(self.y, "grid", "set")-player_size/8+ (player_size/4*self.y_direction), player_size/4, player_size/4))
        #pygame.draw.ellipse(screen, (0, 0, 0), pygame.Rect(grid.convert(self.x,"grid", "set")-player_size/2, grid.convert(self.y, "grid", "set")-player_size/2, player_size, player_size))
    def new_splotch(self):
        self.splotches.append(Splotch(self.x, self.y, self.splotch_color[0], self.splotch_color[1], self.splotch_color[2], player_size, 0.1))
        
class Splotch:
    def __init__(self, x, y, R, G, B, size, decay):
        self.x = round(x)
        self.y = round(y)
        self.opacity = 255
        self.color = (R, G, B, self.opacity)
        self.size = size
        self._decay = decay
        self.decay = self._decay
        self.fadex = self.x
        self.fadey = self.y 
        self.color = (R, G, B)
    def fade(self):
        self.size-=self.decay
    def draw(self):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(grid.convert(self.fadex, "grid", "set")-self.size/2, grid.convert(self.fadey, "grid", "set")-self.size/2, self.size, self.size))
        
class Dot:
    def __init__(self, x, y, grid_size):
        self.x, self.y, self.grid_size = x, y, grid_size
        self.moves = []
    def get_moves(self, duration):
        #distances:
        direction = {
            self.y: "top",
            self.grid_size - self.y: "bottom",
            self.x: "left",
            self.grid_size - self.x: "right"
        }
        distance = sorted(direction)[0]
        closest = direction[distance]
        if closest == "top":
            change_x, change_y = 0, -1
        elif closest == "bottom":
            change_x, change_y = 0, 1
        elif closest == "left":
            change_x, change_y = -1, 0
        elif closest == "right":
            change_x, change_y = 1, 0

        self.moves = new_move(self.moves, 0, 0, 2*duration)
        for i in range(distance+1):
            self.moves = new_move(self.moves, 0, 0, random.randint(duration-5, duration+5))
            self.moves = new_move(self.moves, change_x, change_y, duration)
    def move(self):
        self.moves, self.x, self.y, new_move = move(self.moves, self.x, self.y)
        if len(self.moves) > 0:
            return(True)
        else: return(False)
    def draw(self):
        pygame.draw.ellipse(screen, d_enemy_sit_color, pygame.Rect(grid.convert(self.x,"grid", "set")-dot_size/2, grid.convert(self.y, "grid", "set")-dot_size/2, dot_size, dot_size))
        
def new_move(moves, change_x, change_y, duration): # combindes get_new_moves and add_moves
    moves = add_moves(moves, get_new_moves(change_x, change_y, duration))
    return moves

def get_new_moves(change_x, change_y, duration): #creates coordinates for new move
    og_change_x, og_change_y = change_x, change_y
    change_x, change_y = grid.convert(change_x, "grid", "move"), grid.convert(change_y, "grid", "move")
    #print(change_x, change_y)
    new_moves = []
    new_moves.append([str(og_change_x), str(og_change_y)])
    for i in range(0,duration+1):
        x = change_x/(duration+1)
        if change_x != 0 or change_y != 0:
            y = change_y/(duration+1) + -1*((2*i*grid_unit_size)/(-1*(duration**2))+(grid_unit_size/duration))
        else:
            y = change_y/duration
        new_moves.append([grid.convert(x, "coord", "move"), grid.convert(y, "coord", "move")])
    return new_moves

def add_moves(moves, new_moves): #adds new moves from get_new_moves() to move queue
    for move in new_moves:
        moves.append(move)
    return(moves)

def move(moves, x, y):  #moves x and y according to moves and delete the finished move
    if len(moves) > 0:
        if moves[0][0] == str(moves[0][0]):
            return moves[1::], x, y, True, moves[0]
        return moves[1::], x+moves[0][0], y+moves[0][1], False, None
    else: return moves, x, y, False, None

def is_round_over(p1, p2, player_size):
    if math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2) <= grid.convert(player_size, "coord", "set")/2: #if players collide

        #is p1 colliding with p2? is the side it is facing the side which it is colliding?
 
        if p1.x_direction != 0: #is p1 is moving on the x axis
            if -1*sigmoid(p1.x-p2.x) == p1.x_direction: #if p1 is moving in the direction of contact
                if -1*sigmoid(p2.x-p1.x) != p2.x_direction:   #p2 was  not moving in the direction of contact
                    print("p1 strikes p2")
                    return True, "p1", p1, p2
                else: 
                    print("double collision")
                    return True, None, None, None
        elif p1.y_direction != 0:
            if -1*sigmoid(p1.y-p2.y) == p1.y_direction: 
                if -1*sigmoid(p2.y-p1.y) != p2.y_direction:
                    print("p1 strikes p2")
                    return True, "p1", p1, p2
                else: 
                    print("double collision")
                    return True, None, None, None
        if p2.x_direction != 0:
            print(-1*sigmoid(p2.x-p1.x), p2.x_direction)
            if -1*sigmoid(p2.x-p1.x) == p2.x_direction: 
                print("p2 strikes p1")
                return True, "p2", p2, p1
        elif p2.y_direction != 0:
            if -1*sigmoid(p2.y-p1.y) == p2.y_direction: 
                print("p2 strikes p1")
                return True, "p2", p2, p1

        return True, "both", p1, p1

    for splotch in p1.splotches:
        kill_distance = grid.convert(player_size/2 + splotch.size/2, "coord", "set")/2
        x_distance = p2.x - splotch.x
        y_distance = p2.y - splotch.y
        #print("distances", x_distance, y_distance, math.sqrt(x_distance**2 + y_distance**2), kill_distance)
        if math.sqrt(x_distance**2 + y_distance**2) <= kill_distance:
            print("p2 hits a splotch")
            return True, "p1", p2, p2


    for splotch in p2.splotches:
        kill_distance = grid.convert(player_size/2 + splotch.size/2, "coord", "set")/2
        x_distance = p1.x - splotch.x
        y_distance = p1.y - splotch.y
        if math.sqrt(x_distance**2 + y_distance**2) <= kill_distance:
            return True, "p2", p1, p1

    return False, None, None, None

class Particle:
    def __init__ (self, x, y, x_direction, y_direction, speed, color, size):
        self.x, self.y, self.x_direction, self.y_direction, self.speed = x, y, x_direction+(random.randint(-10, 10)/30), y_direction+(random.randint(-10, 10)/30), speed
        self.color, self.size = color, size
    def move(self):
        self.x += self.x_direction/self.speed
        self.y += self.y_direction/self.speed
    def draw(self):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(grid.convert(self.x,"grid", "set")-self.size/2, grid.convert(self.y, "grid", "set")-self.size/2, self.size, self.size))




def setup_arena():

    size = width, height =  800, 800
    grid_unit_size = int(width/grid_size)
    grid = Grid(grid_unit_size)
    
    player_size = int(grid_unit_size/2)
    p1 = Character(1, 1, 1, p1_colors)
    p2 = Character(grid_size, grid_size, 2, p2_colors)
    return(p1, p2, grid, grid_unit_size, player_size)

def destroy(winner, loser):

    particles = []
    for i in range(10): particles.append(Particle(loser.x, loser.y, winner.x_direction, winner.y_direction, 5, loser.player_color, player_size/5))

    while len(particles) > 0:
        now = time.time()
        screen.fill(grid_background_color)
        keys=pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            quit()
        if keys[K_r]:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        grid.print_grid()

        for particle in particles:
            particle.move()
            particle.draw()
            if particle.x > grid_size or particle.x < 0 or particle.y > grid_size or particle.y < 0:
                particles.remove(particle)

        pygame.display.flip()
        elapsed = time.time()-now
        if elapsed < cycle_time:
            time.sleep(cycle_time-elapsed)
        



def run(p1, p2, grid):
    round_over = False
    while 1:
        now = time.time()
        screen.fill(grid_background_color)
        keys=pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            quit()
        if keys[K_r]:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        grid.print_grid()

        if round_over == False:

        #SPLOTCH ---
            for player in [p1, p2]:
                for splotch in player.splotches:
                    splotch.fade()
                    splotch.draw()
                    if splotch.size <1:
                        player.splotches.remove(splotch)


        #PLAYER ---    
            for player in [p1, p2]:
                player.move(keys)
                player.draw()


        #CHECK GAME STATE ---
            round_over, winner_name, winner, loser = is_round_over(p1, p2, player_size)
        else:
            return(winner_name, winner, loser)
            print(winner_name, "wins!")
            destroy(winner, loser)
            round_over = False
            
            

        pygame.display.flip()
        elapsed = time.time()-now
        if elapsed < cycle_time:
            time.sleep(cycle_time-elapsed)

def print_win():
    screen.fill((0, 255, 0))
    pygame.display.flip()
    while 1:
        keys=pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            quit()
        if keys[K_SPACE]:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()



grid_background_color, grid_cell_back_color, grid_cell_color = (160, 160, 160), (200, 200, 205), (190, 190, 190)
cycle_time = 0.02

size = width, height = 800, 800
screen = pygame.display.set_mode(size)

grid_size = 10


player_move_duration = 8

p1_colors = {
    "splotch_color" : [75, 150, 255],
    "player_color" : (50, 75, 255),
    "eye_color": (40, 60, 220)
}

p2_colors = {
    "splotch_color" : [75, 175, 150],
    "player_color" : (50, 175 , 75),
    "eye_color": (40, 150, 60)
}






animate = True


while 1:
    p1, p2, grid, grid_unit_size, player_size = setup_arena()
    winner_name, winner, loser = run(p1, p2, grid)
    if winner_name != None:
        print(winner_name, "wins!")
        destroy(winner, loser)
    #print_win()
    time.sleep(1)
