import numpy as np
import random
import pygame
import time

rand = random.Random()


class SnakeGame():

    def __init__(self):
        self.game_state = True  # False when Game Over
        self.height = 30
        self.width = 30
        self.size = [self.height, self.width]
        self.board = np.zeros(self.size)
        self.score = 0
        self.head = [self.height // 2, self.width // 2]
        self.vel = rand.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])
        self.snake = [[self.head[0] - i * self.vel[0], self.head[1] - i * self.vel[1]] for i in range(3)]
        for s in self.snake:
            self.board[s[0], s[1]] = 1
        self.board[self.head[0], self.head[1]] = 2
        self.food = self.rand_food()
        self.board[self.food[0], self.food[1]] = -1

    def __str__(self):
        b_str = " " + "_" * self.width + f"  Score: {self.score}\n"
        for i in range(self.height):
            b_str += "|"
            for j in range(self.width):
                if self.board[i, j] == 2:
                    # if [i, j] == self.head:
                    b_str += "X"
                elif self.board[i, j] == 1:
                    # elif [i, j] in self.snake:
                    b_str += "x"
                elif self.board[i, j] == -1:
                    # elif [i, j] == self.food:
                    b_str += "O"
                else:
                    b_str += " "
            b_str += "|\n"
        b_str += u" \u0305" * self.width
        return b_str

    def rand_food(self):
        empty_spaces = [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0]
        return rand.choices(empty_spaces)[0]

    def update_vel(self, vel):
        temp_head = [self.head[0] + vel[0], self.head[1] + vel[1]]
        if temp_head != self.snake[1]:  # make sure it's not previous body part
            self.vel = vel

    def update_state(self):
        self.head[0] += self.vel[0]
        self.head[1] += self.vel[1]

        if self.head[0] < 0 or self.head[0] >= self.height:
            self.head = self.snake[0].copy()  # did not enter valid move
            self.game_state = False
        elif self.head[1] < 0 or self.head[1] >= self.width:
            self.head = self.snake[0].copy()  # did not enter valid move
            self.game_state = False
        elif self.head in self.snake[2::]:  # snake in body and no u-turn
            self.head = self.snake[0].copy()  # did not enter valid move
            self.game_state = False
        elif self.head not in self.snake:  # snake moved
            if self.head == self.food:  # ate food, grow snake, gen food
                self.score += 1
                self.snake.insert(0, self.head.copy())
                self.board[self.snake[1][0], self.snake[1][1]] = 1
                self.board[self.head[0], self.head[1]] = 2
                self.food = self.rand_food()
                self.board[self.food[0], self.food[1]] = -1
            else:  # move snake
                self.snake.insert(0, self.head.copy())
                self.board[self.snake[1][0], self.snake[1][1]] = 1
                self.board[self.head[0], self.head[1]] = 2
                rem = self.snake.pop()
                self.board[rem[0], rem[1]] = 0
        else:
            self.head = self.snake[0].copy()  # did not enter valid move


class SnakeGameGUI(SnakeGame):

    def __init__(self, headless_mode=False):
        super().__init__()
        self.BLUE = (0, 0, 255)
        self.PURPLE = (255, 0, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.SQUARESIZE = 10
        self.WIDTH = self.SQUARESIZE * self.width  # width= 150
        self.HEIGHT = self.SQUARESIZE * self.height  # height= 150
        self.SIZE = (self.WIDTH + 400, self.HEIGHT)  # SIZE = 550x150

        if headless_mode == False:
            self.SCREEN = pygame.display.set_mode(self.SIZE)
            pygame.init()

    def draw_board(self):
        myfont = pygame.font.SysFont("monospace", 50)
        self.SCREEN.fill(self.BLACK)
        for i in range(self.height):
            for j in range(self.width):
                # check for head, body, food
                if self.board[i, j] == 1:
                    loc_size = (j * self.SQUARESIZE, i * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                    pygame.draw.rect(self.SCREEN, self.BLUE, loc_size)
                elif self.board[i, j] == 2:
                    loc_size = (j * self.SQUARESIZE, i * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                    pygame.draw.rect(self.SCREEN, self.PURPLE, loc_size)
                elif self.board[i, j] == -1:
                    loc = (int((j + 0.5) * self.SQUARESIZE), int((i + 0.5) * self.SQUARESIZE))
                    pygame.draw.circle(self.SCREEN, self.RED, loc, self.SQUARESIZE // 2)

        label = myfont.render(f"Score: {self.score}", 1, self.PURPLE)
        self.SCREEN.blit(label, (self.WIDTH + 10, 10))
        loc_size = (self.WIDTH, 0, 3, self.HEIGHT)
        pygame.draw.rect(self.SCREEN, (255, 255, 255), loc_size)
        pygame.display.update()

    def run_game(self, player_ai=None):
        update_rate = 3  # frames/update
        fps = 60
        counter = 0
        vel = self.vel
        myfont = pygame.font.SysFont("monospace", 65)
        self.draw_board()
        pygame.display.update()

        exit_flag = False
        while exit_flag == False and self.game_state == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        vel = [-1, 0]
                    elif event.key == pygame.K_DOWN:
                        vel = [1, 0]
                    elif event.key == pygame.K_LEFT:
                        vel = [0, -1]
                    elif event.key == pygame.K_RIGHT:
                        vel = [0, 1]
                    else:
                        vel = self.vel

            time.sleep(1.0 / fps)
            counter += 1
            if counter >= update_rate:
                self.update_vel(vel)
                self.update_state()
                counter = 0
            self.draw_board()
            pygame.display.update()

        label = myfont.render(f"Game Over!", 1, self.RED)
        self.SCREEN.blit(label, (self.WIDTH + 10, 50))
        pygame.display.update()

        while exit_flag == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True
        pygame.quit()


class SnakeGameAI(SnakeGameGUI):

    def __init__(self, headless_mode=False):
        super().__init__(headless_mode)
        self.reverse = 1  # flag to allow snake to alternate directions

    def rand_move(self):
        return rand.choice([[-1, 0], [1, 0], [0, -1], [0, 1]])

    def get_safe_moves(self, temp_head=None):
        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        unsafe_moves = []

        if temp_head == None:
            temp_head_orig = self.head.copy()
        else:
            temp_head_orig = temp_head.copy()
        # remove unsafe moves
        for move in moves:
            temp_head = temp_head_orig.copy()
            temp_head[0] += move[0]
            temp_head[1] += move[1]

            if temp_head[0] < 0 or temp_head[0] >= self.height:
                unsafe_moves.append(move)
            elif temp_head[1] < 0 or temp_head[1] >= self.width:
                unsafe_moves.append(move)
            elif temp_head in self.snake:
                unsafe_moves.append(move)

        for move in unsafe_moves:
            moves.remove(move)

        return moves

    def safe_move(self):
        moves = self.get_safe_moves()
        if len(moves) == 0:  # no safe moves
            moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        return rand.choice(moves)

    def run_game(self, player_ai=None):
        update_rate = 1
        fps = 60
        counter = 0
        vel = self.vel
        pygame.init()
        myfont = pygame.font.SysFont("monospace", 65)
        self.draw_board()
        pygame.display.update()

        exit_flag = False
        while exit_flag == False and self.game_state == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        vel = [-1, 0]
                    elif event.key == pygame.K_DOWN:
                        vel = [1, 0]
                    elif event.key == pygame.K_LEFT:
                        vel = [0, -1]
                    elif event.key == pygame.K_RIGHT:
                        vel = [0, 1]
                    else:
                        vel = self.vel

            time.sleep(1.0 / fps)
            counter += 1
            if counter >= update_rate:
                if player_ai != None:
                    vel = player_ai()
                self.update_vel(vel)
                self.update_state()
                counter = 0
            self.draw_board()
            pygame.display.update()

        label = myfont.render(f"Game Over!", 1, self.RED)
        self.SCREEN.blit(label, (self.WIDTH + 10, 50))
        pygame.display.update()

        while exit_flag == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True
        pygame.quit()


class SnakeGameAStar(SnakeGameAI):

    def __init__(self, headless_mode=False):
        super().__init__(headless_mode)
        self.path2food = []


    def wiggle_away(self):
        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        unsafe_moves = []
        food_dir = []

        d0 = -self.food[0] + self.head[0]
        if d0 != 0:
            food_dir.append([d0 // abs(d0), 0])
        d1 = -self.food[1] + self.head[1]
        if d1 != 0:
            food_dir.append([0, d1 // abs(d1)])

        # remove unsafe moves
        for move in moves:
            temp_head = self.head.copy()
            temp_head[0] += move[0]
            temp_head[1] += move[1]

            if temp_head[0] < 0 or temp_head[0] >= self.height:
                unsafe_moves.append(move)
            elif temp_head[1] < 0 or temp_head[1] >= self.width:
                unsafe_moves.append(move)
            elif temp_head in self.snake:
                unsafe_moves.append(move)

        for move in unsafe_moves:
            moves.remove(move)

        # move towards food first
        self.reverse *= -1  # to alternate turning direction
        for move in moves[::self.reverse]:
            # for move in moves:
            if move in food_dir:
                return move

        if len(moves) == 0:  # no safe moves
            return [1, 0]
        else:
            return rand.choice(moves)

    def check4food(self, loc):
        if self.food[0] == loc[0] and self.food[1] == loc[1]:
            return True
        else:
            return False

    def empty_spaces(self):
        return [[i, j] for i in range(self.height) for j in range(self.width) if
                self.board[i, j] == 0 or self.board[i, j] == -1]

    def heuristic(self, head):
        # distance to food
        d0 = self.food[0] - head[0]
        d1 = self.food[1] - head[1]
        # pythagoras rule
        return np.sqrt(d0 ** 2 + d1 ** 2)

    def astar_explore(self, temp_head):
        self.explored.append(temp_head)

        moves = self.get_safe_moves(temp_head)

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            h = self.heuristic(head)

            if str(head) not in self.parents.keys():
                self.parents[str(head)] = temp_head

            if head in self.explored:
                continue

            if self.check4food(head):
                self.food_found = True
                return
            if [h, head] not in self.not_explored:
                self.not_explored.insert(0, [h, head])
                self.not_explored.sort()

    def astar_search(self, temp_head=None):
        self.food_found = False
        # not_explored represents open list
        self.not_explored = []
        # explored represents closed list
        self.explored = []
        self.parents = dict()
        if temp_head == None:
            temp_head = self.head.copy()
        orig_head = temp_head.copy()

        moves = self.get_safe_moves(temp_head)

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            h = self.heuristic(head)
            if str(head) not in self.parents.keys():
                self.parents[str(head)] = temp_head
            if self.check4food(head):
                return move
            else:
                self.not_explored.insert(0, [h, head])
                self.not_explored.sort()

        while len(self.not_explored) > 0:
            h_th = self.not_explored.pop(0)
            self.astar_explore(h_th[1])
            if self.food_found:
                break

        if self.food_found:  # back track to move
            loc = self.food
            while self.parents[str(loc)] != orig_head:
                loc = self.parents[str(loc)]
            return [loc[0] - orig_head[0], loc[1] - orig_head[1]]
        elif len(self.explored) > 0:
            loc = self.explored[-1]  # last point
            while self.parents[str(loc)] != orig_head:
                loc = self.parents[str(loc)]
            return [loc[0] - orig_head[0], loc[1] - orig_head[1]]
        else:  # no path to food, no path to far point
            return self.wiggle_away()

    def run_game(self, player_ai=None):
        update_rate = 1
        fps = 60
        counter = 0
        vel = self.vel
        pygame.init()
        myfont = pygame.font.SysFont("monospace", 65)
        self.draw_board()
        pygame.display.update()

        exit_flag = False
        while exit_flag == False and self.game_state == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        vel = [-1, 0]
                    elif event.key == pygame.K_DOWN:
                        vel = [1, 0]
                    elif event.key == pygame.K_LEFT:
                        vel = [0, -1]
                    elif event.key == pygame.K_RIGHT:
                        vel = [0, 1]
                    else:
                        vel = self.vel

            time.sleep(1.0 / fps)
            counter += 1
            if counter >= update_rate:
                if player_ai != None:
                    vel = player_ai()
                self.update_vel(vel)
                self.update_state()
                counter = 0
            self.draw_board()
            pygame.display.update()

        label = myfont.render(f"Game Over!", 1, self.RED)
        self.SCREEN.blit(label, (self.WIDTH + 10, 50))
        pygame.display.update()

        while exit_flag == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True
        pygame.quit()


def main():
    my_game = SnakeGameAStar()
    my_game.run_game(my_game.astar_search)


if __name__ == "__main__":
    main()