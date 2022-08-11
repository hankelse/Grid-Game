from xml.etree.ElementTree import TreeBuilder
import pygame, sys, time, random, math
from pygame.constants import K_SPACE, K_ESCAPE, K_w, K_a, K_s, K_d, K_r, K_LEFT, K_RIGHT, K_UP, K_DOWN
pygame.init()

def sigmoid(x):
    if x<0: return(-1)
    if x>0: return(1)
    else: return(0)
def up_key(keys):
    if keys[K_w] or keys[K_UP]:return True
    return False
def down_key(keys):
    if keys[K_s] or keys[K_DOWN]:return True
    return False
def left_key(keys):
    if keys[K_a] or keys[K_LEFT]:return True
    return False
def right_key(keys):
    if keys[K_d] or keys[K_RIGHT]:return True
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moves = [["X", "X"]]
    def get_moves(self, keys):
        self.x, self.y = round(self.x), round(self.y)

        if self.x + 1 <= grid_size and right_key(keys)== True:
            self.moves = new_move(self.moves, 1, 0, player_move_duration)
        if self.x - 1 >= 1 and left_key(keys) == True:
            self.moves = new_move(self.moves, -1, 0, player_move_duration)
        if self.y + 1 <= grid_size and down_key(keys) == True:
            self.moves = new_move(self.moves, 0, 1, player_move_duration)
        if self.y - 1 >= 1 and up_key(keys) == True:
            self.moves = new_move(self.moves, 0, -1, player_move_duration)
            
    def move(self, keys):
        self.moves, self.x, self.y, new_move = move(self.moves, self.x, self.y)
        if new_move == True:
            self.new_splotch()
        if len(self.moves) == 0:
            self.get_moves(keys)

    def is_alive(self, enemies, player_size, enemy_size):
        kill_distance = grid.convert(player_size, "coord", "set")
        kill_distance = 0.5
        for enemy in enemies:
            if enemy.blocked == False:
                if math.sqrt(((self.x+player_size/2)-(enemy.x+enemy_size/2))**2 + ((self.y+player_size/2)-(enemy.y+enemy_size/2))  **2) <= kill_distance:
                    return(True)
        return(False)

    def draw(self):
        pygame.draw.ellipse(screen, player_color, pygame.Rect(grid.convert(self.x,"grid", "set")-player_size/2, grid.convert(self.y, "grid", "set")-player_size/2, player_size, player_size))
    def new_splotch(self):
        splotches.append(Splotch(self.x, self.y, splotch_color[0], splotch_color[1], splotch_color[2], player_size, 0.1))
        
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
        
class Enemy:
    def __init__(self, x, y, random_moves):
        self.x = x
        self.y = y
        self.moves = [["X", "X"]]
        self.random_moves = random_moves
        self.blocked = False
        if self.random_moves == True: self.enemy_sit_color, self.enemy_jump_color, self.enemy_dead_color = d_enemy_sit_color, d_enemy_jump_color, d_enemy_dead_color
        else: self.enemy_sit_color, self.enemy_jump_color, self.enemy_dead_color = s_enemy_sit_color, s_enemy_jump_color, s_enemy_dead_color
        self.color = self.enemy_sit_color
        
    def get_moves(self, splotch_coords, player): ##add memory of last move, check if enemy is on dot, if enemy on dot move back.
        if self.blocked == False:
            self.blockers = []
            self.possible_moves = []
            self.x, self.y = round(self.x), round(self.y)

            if self.x + 1 <= grid_size:
                if (str(self.x+1)+" "+str(self.y)) not in splotch_coords:
                    self.possible_moves.append([1, 0])
                else: self.blockers.append(splotch_coords[str(self.x+1)+" "+str(self.y)])

            if self.y + 1 <= grid_size:
                if (str(self.x)+" "+str(self.y+1)) not in splotch_coords:
                    self.possible_moves.append([0, 1])
                else: self.blockers.append(splotch_coords[str(self.x)+" "+str(self.y+1)])
            
            if self.x - 1 >= 1:
                if (str(self.x-1)+" "+str(self.y)) not in splotch_coords:
                    self.possible_moves.append([-1, 0])
                else: self.blockers.append(splotch_coords[str(self.x-1)+" "+str(self.y)])
            
            if self.y-1 >= 1:
                if (str(self.x)+" "+str(self.y-1)) not in splotch_coords:
                    self.possible_moves.append([0, -1])
                else: self.blockers.append(splotch_coords[str(self.x)+" "+str(self.y-1)])
            
            if len(self.possible_moves) > 0:
                if self.random_moves == True:
                    self.random_move = self.possible_moves[random.randint(0, len(self.possible_moves)-1)]
                    self.moves = new_move(self.moves, self.random_move[0], self.random_move[1], enemy_move_duration)
                    self.moves = new_move(self.moves, 0, 0, enemy_move_duration)
                else:

                    x_distance = sigmoid(player.x-self.x)
                    y_distance = sigmoid(player.y-self.y)
                    if [x_distance, y_distance].count(0) == 1:
                        if [sigmoid(x_distance), sigmoid(y_distance)] in self.possible_moves:
                            change_x, change_y = sigmoid(x_distance), sigmoid(y_distance)
                        else: change_x, change_y = 0, 0
                    elif [x_distance, y_distance].count(0) == 0:
                        r_choice = random.choice([0, 1])
                        if r_choice == 1: 
                            if [sigmoid(x_distance), 0] in self.possible_moves:
                                change_x, change_y = sigmoid(x_distance), 0
                            elif [0, sigmoid(y_distance)] in self.possible_moves:
                                change_x, change_y = 0, sigmoid(y_distance)
                            else: change_x, change_y = 0, 0
                        else: 
                            if [0, sigmoid(y_distance)] in self.possible_moves:
                                change_x, change_y = 0, sigmoid(y_distance)
                            elif [sigmoid(x_distance), 0] in self.possible_moves:
                                change_x, change_y = sigmoid(x_distance), 0
                            else: change_x, change_y = 0, 0
                    
                    # distance = sorted(distances)[0]
                    # direction = distances[distance]
                    # if direction == "up":
                    #     change_x, change_y = 0, -1
                    # elif direction == "down":
                    #     change_x, change_y = 0, 1
                    # elif direction == "left":
                    #     change_x, change_y = -1, 0
                    # elif direction == "right":
                    #     change_x, change_y = 1, 0
                    self.moves = new_move(self.moves, change_x, change_y, enemy_move_duration)
                    self.moves = new_move(self.moves, 0, 0, enemy_move_duration)
                        

            else:
                self.blocked = True
                self.color = self.enemy_dead_color
                for splotch in self.blockers:
                    splotch.size = player_size
                    splotch.decay = 0

    def move(self, splotch_coords, player):
        self.moves, self.x, self.y, new_move = move(self.moves, self.x, self.y)
        if new_move == True:
            if self.color == self.enemy_jump_color: self.color = self.enemy_sit_color
            elif self.color == self.enemy_sit_color: self.color = self.enemy_jump_color
        if len(self.moves) == 0:
            self.get_moves(splotch_coords, player)
    def draw(self):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(grid.convert(self.x,"grid", "set")-enemy_size/2, grid.convert(self.y, "grid", "set")-enemy_size/2, enemy_size, enemy_size))

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
    change_x, change_y = grid.convert(change_x, "grid", "move"), grid.convert(change_y, "grid", "move")
    #print(change_x, change_y)
    new_moves = []
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
    moves.append(["X", "X"])
    return(moves)

def move(moves, x, y):  #moves x and y according to moves and delete the finished move
    if len(moves) > 0:
        if moves[0][0] == "X":
            return moves[1::], x, y, True
        return moves[1::], x+moves[0][0], y+moves[0][1], False
    else: return moves, x, y, False

def round_won(enemies):
    for enemy in enemies:
        if enemy.blocked == False:
            return False
    return True

def setup_animation():
    grid_size = 7
    grid_unit_size = int(width/grid_size)
    grid = Grid(grid_unit_size)
    dot_size = int(grid_unit_size/2)
    return grid, grid_unit_size, dot_size

def display_level_animation(levels, level, duration):
    dots = []
    setups = [
        [[4, 2],[4, 3], [3, 3], [4, 4], [4, 5], [5, 6], [4, 6], [3, 6]],
        [[3,2],[4,2],[5,2],[5,3],[5,4],[4,4],[3,4],[3,5],[3,6],[4,6],[5,6]],
        [[3,2],[4,2],[5,2],[5,3],[5,4],[4,4],[5,5],[3,4],[3,6],[4,6],[5,6]],
        [ [3,2], [5,2], [3,3], [3, 4], [4,4], [5,3], [5,4], [5,5], [5,6]],
        [[3,2],[4,2],[5,2],[3,3],[5,4],[4,4],[3,4],[5,5],[3,6],[4,6],[5,6]],
        ]
    for coord in setups[level]:
        dots.append(Dot(coord[0], coord[1], 7))

    for dot in dots:
        dot.get_moves(duration)
    while len(dots) > 0:
        now = time.time()
        keys = pygame.key.get_pressed()
        screen.fill(grid_background_color)
        if keys[K_ESCAPE]:
            quit()
        if keys[K_SPACE]:
            dots = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        grid.print_grid()

        for dot in dots:
            active = dot.move()
            if active == False:
                dots.remove(dot)
            dot.draw()
        pygame.display.flip()
        elapsed = time.time()-now
        if elapsed < cycle_time:
            time.sleep(cycle_time-elapsed)
    else:
        frames = []
        frames_num = anim_zoom_frames
        _cycle_time = int(cycle_time/(frames_num))
        nl_size = levels[level][1] #next level size
        for i in range(1, frames_num+1):
            frames.append(7-( ( (7-nl_size) /frames_num)*i) )
        for num in frames:
            _grid = Grid(int(width/num))
            for i in range(10):
                screen.fill(grid_background_color)
                now = time.time()
                _grid.print_grid()
                pygame.display.flip()
                elapsed = time.time()-now
                if elapsed < _cycle_time:
                    time.sleep(_cycle_time-elapsed)

def setup_level(levels, level):


    size = width, height =  800, 800
    grid_size = levels[level][1]
    grid_unit_size = int(width/grid_size)
    grid = Grid(grid_unit_size)

    screen = pygame.display.set_mode(size)
    player = Character(grid_size, grid_size)
    

    splotches = []

    enemies = []
    for i in range(levels[level][2]): enemies.append(Enemy(random.randint(1,grid_size), random.randint(1,grid_size-2), True))
    for i in range(levels[level][3]): enemies.append(Enemy(random.randint(1,grid_size), random.randint(1,grid_size-2), False))
   

    player_size = int(grid_unit_size/2)
    enemy_size =int(grid_unit_size/2)

    return(player, enemies, splotches, screen, grid, grid_size, grid_unit_size, player_size, enemy_size, width, height)

def run_level(player, enemies, splotches, screen, grid, player_size, enemy_size, levels,level):
    level_over = False
    first = True
    while 1:
        now = time.time()
        screen.fill(grid_background_color)
        keys=pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            quit()
        if keys[K_r]:
            level_over = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        grid.print_grid()

        if level_over == False:
            win = False

        #SPLOTCH ---
            splotch_coords = {}
            for splotch in splotches:
                splotch.fade()
                splotch.draw()
                if splotch.size <1:
                    splotches.remove(splotch)

            for splotch in splotches:
                splotch_coords[str(splotch.x)+" "+str(splotch.y)] = splotch

        #PLAYER ---    
            player.move(keys)
            player.draw()

        #ENEMIES ---
            for enemy in enemies:
                enemy.move(splotch_coords, player)
                enemy.draw()

        #CHECK GAME STATE ---
            level_over = player.is_alive(enemies, player_size, enemy_size)
            if level_over == False:
                level_over = round_won(enemies)
                if level_over == True:
                    win = True
        else:
            if first == True: #runs the first time
                for splotch in splotches:
                    splotch.decay = 2
                if win == True:
                    #print("level won")
                    level += 1
                else:
                    #print("dead")
                    if on_lose == "back":
                        if level >= 1:
                            level -= 1
                        else: level = 0
                    elif on_lose == "reset":
                        level = 0
                    elif on_lose == "remain":
                        pass
                    else: print(on_lose, "is not a valid type")

                first = False

            player.draw()
            
            for splotch in splotches:
                splotch.fade()
                splotch.draw()
                if splotch.size <1:
                    splotches.remove(splotch)

            for enemy in enemies:
                enemy.draw()

            if len(splotches) == 0:
                return(level)
            

        
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

def get_levels(random_levels, r_level_number):
    levels = []
    if random_levels != True:
        levels = [
    # level number, grid size, dumb enemies, smart enemies
        [1, 5, 1, 1],
        [2, 5, 3, 1],
        [3, 5, 2, 3],
        [4, 10, 8, 4],
        [5, 5, 1, 6]]
    else:
        for i in range(1, r_level_number+1):
            level_grid_size = random.randint(5, 10)
            enemies_number = random.randint(round(level_grid_size/2), level_grid_size)
            smart_enemies = random.randint(1, enemies_number)
            levels.append([i, level_grid_size, enemies_number-smart_enemies, smart_enemies])
    return(levels)

def get_scores():
    score_file = open("Splotcher/scores.txt")
    dirty_scores = score_file.readlines()
    clean_scores = []
    for score in dirty_scores:
        clean_scores.append(int(score.strip("\n")))
    return clean_scores


grid_background_color, grid_cell_back_color, grid_cell_color = (160, 160, 160), (200, 200, 205), (190, 190, 190)
cycle_time = 0.02

size = width, height = 800, 800
screen = pygame.display.set_mode(size)


player_move_duration = 8
enemy_move_duration = 20
splotch_color = [75, 150, 255]
player_color = (50, 75, 255)
d_enemy_sit_color, d_enemy_jump_color, d_enemy_dead_color = (230, 50, 50), (230, 75, 75), (200, 100, 150)
s_enemy_sit_color, s_enemy_jump_color, s_enemy_dead_color = (230, 0, 100), (230, 25, 125), (200, 125, 200)

enemy_move_random = False #True or False
on_lose = "remain" # "reset" "back" or "remain"
random_levels = True #True or False
r_level_number = 5 #number of levels generated if random

anim_jump_duration = 20
anim_zoom_frames = 10

level = 0
animate = True
levels = get_levels(random_levels, r_level_number)

get_scores()

while level < len(levels):
    if animate == True:
        grid, grid_unit_size, dot_size = setup_animation()
        display_level_animation(levels, level, anim_jump_duration)
    player, enemies, splotches, screen, grid, grid_size, grid_unit_size, player_size, enemy_size, width, height = setup_level(levels,level)
    current = level
    level = run_level(player, enemies, splotches, screen, grid, player_size, enemy_size, levels, level)
    if level == current: animate = False
    else: animate = True
else:
    print_win()


#  NEXT STEPS
#  - Add Score: (save in .txt file?) Score's increase decreases until another is trapped so waiting is penalized
#  - Make Splotches grow when they have trapped a enemie
#  - Add Enemy number info on Animation
