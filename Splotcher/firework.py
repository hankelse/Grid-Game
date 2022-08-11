import pygame, sys, random
pygame.init()

size = width, height =  800, 800
screen=pygame.display.set_mode((size))
surface = pygame.Surface((size), pygame.SRCALPHA)

class Firework:
    def __init__(self, size, initial_xv, initial_yv, starting_x, starting_y, scale_factor, size_divisor, num_explosions, explosion_interval, color):
            self.spark_size = size
            self.init_xv = initial_xv
            self.init_yv = scale_factor
            #self.init_yv = 0.01
            self.starting_x = starting_x
            self.starting_y = starting_y
            self.size_divisor = size_divisor
            self.num_explosions = num_explosions
            self.explosion_interval = explosion_interval
            self.color = color

            self.y_deceleration = 0.0005 * scale_factor
            self.x_deceleration = 0.0001 * scale_factor
            self.sparks = [self.Spark(self.starting_x, self.starting_y, self.init_xv, self.init_yv, self.y_deceleration, self.x_deceleration, self.spark_size, self.color )]
            self.round = 0
            self.explosion_start = 2000 - self.num_explosions*self.explosion_interval
    def explode(self):
        print("explosion")
        new_sparks = []
        for spark in self.sparks:
            new_sparks.append(spark)
            new_sparks.append(self.Spark(spark.x, spark.y, spark.xv + (random.randint(1, 2)/self.size_divisor), spark.yv + (random.randint(1, 2)/self.size_divisor), self.y_deceleration, self.x_deceleration, self.spark_size, self.color))
            new_sparks.append(self.Spark(spark.x, spark.y, spark.xv + (random.randint(1, 2)/self.size_divisor), spark.yv - (random.randint(1, 2)/self.size_divisor), self.y_deceleration, self.x_deceleration, self.spark_size, self.color))
            new_sparks.append(self.Spark(spark.x, spark.y, spark.xv - (random.randint(1, 2)/self.size_divisor), spark.yv + (random.randint(1, 2)/self.size_divisor), self.y_deceleration, self.x_deceleration, self.spark_size, self.color))
            new_sparks.append(self.Spark(spark.x, spark.y, spark.xv - (random.randint(1, 2)/self.size_divisor), spark.yv - (random.randint(1, 2)/self.size_divisor), self.y_deceleration, self.x_deceleration, self.spark_size, self.color))
        return(new_sparks)
    def move(self):
        self.round += 1
        
        if self.round >= self.explosion_start and self.round % self.explosion_interval == 0 and self.round < 2000:
            self.sparks = self.explode()

        for spark in self.sparks:
            spark.move()
            spark.draw()
    class Spark:
        def __init__(self, x, y, xv, yv, y_deceleration, x_deceleration, spark_size, color):
            self.x = x
            self.y = y
            self.xv = xv
            self.yv = yv
            self.y_deceleration = y_deceleration
            self.x_deceleration = x_deceleration
            self.spark_size = spark_size
            self.color = color
        def move(self):
            self.x += self.xv
            self.y -= self.yv
            self.yv -= self.y_deceleration
            self.xv -= signus(self.xv)*self.x_deceleration
        def draw(self):
            pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x, self.y, self.spark_size, self.spark_size))
    
                


# size = 10
# scale_factor = 0.4


# initial_xv = 0
# initial_yv = 1 * scale_factor
# starting_x, starting_y = 400, 800
# y_deceleration = 0.00050 * scale_factor
# x_deceleration = 0.0001 * scale_factor
# explosion_force_divisor = 50
# num_explosions = 3
# explosion_interval = 100

#size, initial_xv, initial_yv, starting_x, starting_y, scale_factor, size_divisor, num_explosions, explosion_interval, color

fireworks = [
Firework(4, 0.2, 1, 0, 700, 0.4, 30, 3, 300, (239, 166, 255)),
#Firework(3, -0.25, 1, 800, 700, 0.4, 50, 3, 200, (158, 176, 255)),
#Firework(5, 0, 1, 400, 700, 0.4, 50, 3, 100, (31, 255, 184))
]

# class Spark:
#     def __init__(self, x, y, xv, yv):
#         self.x = x
#         self.y = y
#         self.xv = xv
#         self.yv = yv
#     def move(self):
#         self.x += self.xv
#         self.y -= self.yv
#         self.yv -= y_deceleration
#         self.xv -= signus(self.xv)*x_deceleration
#     def draw(self):
#         pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(self.x, self.y, size, size))

# def explode(sparks):
#     new_sparks = []
#     for spark in sparks:
#         new_sparks.append(spark)
#         new_sparks.append(Spark(spark.x, spark.y, spark.xv + (random.randint(1, 2)/explosion_force_divisor), spark.yv + (random.randint(1, 2)/explosion_force_divisor)))
#         new_sparks.append(Spark(spark.x, spark.y, spark.xv + (random.randint(1, 2)/explosion_force_divisor), spark.yv - (random.randint(1, 2)/explosion_force_divisor)))
#         new_sparks.append(Spark(spark.x, spark.y, spark.xv - (random.randint(1, 2)/explosion_force_divisor), spark.yv + (random.randint(1, 2)/explosion_force_divisor)))
#         new_sparks.append(Spark(spark.x, spark.y, spark.xv - (random.randint(1, 2)/explosion_force_divisor), spark.yv - (random.randint(1, 2)/explosion_force_divisor)))
#     return(new_sparks)

def signus(x):
    if x < 0:
        return(-1)
    elif x > 0:
        return (1)
    else:
        return (0)


# sparks = [Spark(starting_x, starting_y, initial_xv, initial_yv)]

# round = 0

#firework = Firework(10, 0, 1, 400, 800, 0.4, 10, 3, 100)
while 1:
    #round += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    #screen.fill(0, 0, 0, 100)
    pygame.draw.rect(surface, (0, 0, 0, 2), pygame.Rect(0, 0, 800, 800))
    for firework in fireworks:
        firework.move()
    
    #pygame.draw.rect(screen, (0, 0, 0, 255), pygame.Rect(0, 0, 800,800))
    # explosion_start = 2500 - num_explosions*explosion_interval

    # if round >= explosion_start and round % explosion_interval == 0 and round < 2500:
    #     sparks = explode(sparks)

    # for spark in sparks:
    #     spark.move()
    #     spark.draw()
    
    

##
    pygame.display.flip()
    screen.blit(surface, (0,0))