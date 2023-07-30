
import random
from enum import Enum
from collections import namedtuple
import numpy as np
from PIL import Image
import cv2
import math

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 1

d = {
    1: (255,175,0),
    2: (0, 255, 0),
    3: (0,0,200)
}
FOOD = 3
SNAKE = 1
SNAKE_HEAD = 2
class SnakeGameAI:
    
    def __init__(self, w=10, h=10):
        self.w = w
        self.h = h
        self.action_space = 3
        self.state_space = 11
        self.reset()
        
    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(5, 5)
        self.snake = [self.head] 
                    #   Point(self.head.x-BLOCK_SIZE, self.head.y),
                    #   Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.fo_dis = self.get_distance()
        img = np.array(self.get_image())
        state = self.get_state()

        return state

        # return img
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        self.frame_iteration += 1

        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        self.new_fo_dis = self.get_distance()
        if self.fo_dis < self.new_fo_dis:
            reward = -1
        else:
            reward = 1
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -100
            state = self.get_state()
            return state ,reward, game_over
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = +10
            self._place_food()
        else:
            self.snake.pop()
        
        self.fo_dis = self.get_distance()
        state = self.get_state()
        # 6. return game over and score
        return state ,reward, game_over
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        
        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d 
        
        self.direction = new_dir
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
    def get_image(self):
        env = np.zeros((self.w,self.h,3), dtype=np.uint8)
        env[self.food.y][self.food.x] = d[FOOD]
        env[self.head.y][self.head.x] = d[SNAKE_HEAD]
        for pt in self.snake[1:]:
            env[pt.y][pt.x] = d[SNAKE]
        img = Image.fromarray(env, "RGB")
        return img
    def display(self):
        img = self.get_image()
        img = img.resize((300,300), resample=Image.BOX)
        img = self.draw_grid(np.array(img),(10,10))

        # img = cv2.applyColorMap(img, cv2.COLORMAP_BONE)
        cv2.imshow("", np.array(img))
        cv2.waitKey(1)
        return img
    def draw_grid(self,img, grid_shape, color=(0,0,0), thickness=2):
        h, w,_ = img.shape
        rows, cols = grid_shape
        dy, dx = h / rows, w / cols

        # draw vertical lines
        for x in np.linspace(start=dx, stop=w-dx, num=cols-1):
            x = int(round(x))
            cv2.line(img, (x, 0), (x, h), color=color, thickness=thickness)

        # draw horizontal lines
        for y in np.linspace(start=dy, stop=h-dy, num=rows-1):
            y = int(round(y))
            cv2.line(img, (0, y), (w, y), color=color, thickness=thickness)

        return img
    def get_distance(self):
        dis = math.sqrt((self.head.x-self.food.x)**2 + (self.head.y-self.food.y)**2)
        return dis
    def get_state(self):
        point_l = Point(self.head.x - 1, self.head.y)
        point_r = Point(self.head.x + 1, self.head.y)
        point_u = Point(self.head.x, self.head.y - 1)
        point_d = Point(self.head.x, self.head.y + 1)
        
        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and self.is_collision(point_r)) or 
            (dir_l and self.is_collision(point_l)) or 
            (dir_u and self.is_collision(point_u)) or 
            (dir_d and self.is_collision(point_d)),

            # Danger right
            (dir_u and self.is_collision(point_r)) or 
            (dir_d and self.is_collision(point_l)) or 
            (dir_l and self.is_collision(point_u)) or 
            (dir_r and self.is_collision(point_d)),

            # Danger left
            (dir_d and self.is_collision(point_r)) or 
            (dir_u and self.is_collision(point_l)) or 
            (dir_r and self.is_collision(point_u)) or 
            (dir_l and self.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            self.food.x < self.head.x,  # food left
            self.food.x > self.head.x,  # food right
            self.food.y < self.head.y,  # food up
            self.food.y > self.head.y  # food down
            ]

        return np.array(state, dtype=int)


