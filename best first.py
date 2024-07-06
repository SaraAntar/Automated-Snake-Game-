import math, random, pygame, sys, copy

class cube(object):
    # dimensions of window
    rows = 20
    w = 500

    # attributes of fruit
    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    # movement function of fruit
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = ((self.pos[0] + self.dirnx) % 20, (self.pos[1] + self.dirny) % 20)

    # drawing the snake and fruit
    def draw(self, surface, eyes=False, food=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        if food:
            centre = dis // 2
            radius = 10
            pygame.draw.circle(surface, self.color, (i * dis + centre + 1, j * dis + centre + 1), radius)
        else:
            pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    # attributes of snake
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos, color=(102, 178, 255))
        self.body.append(self.head)
        self.last_dir = ""
        self.curr_dir = "right"
        self.dirnx = 1
        self.dirny = 0

    # movement function of snake
    def move(self, control=""):
        # if the user pressed on the quit button the game will stop and quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        keys = pygame.key.get_pressed()
        # determining the dimensions of the path according to the directions
        if control != self.curr_dir:
            self.last_dir = self.curr_dir
            if control == "left":
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.curr_dir = "left"

            elif control == "right":
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.curr_dir = "right"

            elif control == "up":
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.curr_dir = "up"

            elif control == "down":
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.curr_dir = "down"

            else:
                for key in keys:
                    if keys[pygame.K_LEFT] and self.curr_dir != "left":
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        self.curr_dir = "left"

                    elif keys[pygame.K_RIGHT] and self.curr_dir != "right":
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        self.curr_dir = "right"

                    elif keys[pygame.K_UP] and self.curr_dir != "up":
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        self.curr_dir = "up"

                    elif keys[pygame.K_DOWN] and self.curr_dir != "down":
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        self.curr_dir = "down"
        print(self.dirnx)
        print(self.dirny)

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:  # out of left bound
                    c.pos = (19, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= 19:  # out of right bound
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= 19:  # out of bottom bound
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:  # out of top bound
                    c.pos = (c.pos[0], 19)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos, color=(102, 178, 255))
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        for i in range(len(self.body)):
            if i:
                self.body[i].color = (255, 255, 255)

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1]), color=self.color))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1]), color=self.color))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1), color=self.color))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1), color=self.color))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawScore(score):
    score_font = pygame.font.SysFont('Raleway', 20, bold=True)
    score_surface = score_font.render('Score : ' + str(score), True, pygame.Color(153, 255, 51))
    score_rect = score_surface.get_rect()
    score_rect.topleft = (width - 120, 10)
    win.blit(score_surface, score_rect)


def drawPressKeyMsg():
    press_font = pygame.font.SysFont('Raleway', 255)
    pressKeySurf = press_font.render('Press a key to play.', True, (255, 255, 255))
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.midtop = (250, 350)
    win.blit(pressKeySurf, pressKeyRect)


def redrawWindow(lose=False):
    win.fill((0, 0, 0))
    s.draw(win)
    snack.draw(win, food=True)

    drawScore(len(s.body) - 1)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def showGameOverScreen():
    gameOverFont = pygame.font.SysFont("courier new", 150)
    gameSurf = gameOverFont.render('Game', True, pygame.Color(255, 255, 255))
    overSurf = gameOverFont.render('Over', True, pygame.Color(255, 255, 255))
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (width / 2, 10)
    overRect.midtop = (width / 2, gameRect.height + 10 + 25)

    win.blit(gameSurf, gameRect)
    win.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def checkForKeyPress():
    if len(pygame.event.get(pygame.QUIT)) > 0:
        pygame.quit()
        sys.exit()
    keyUpEvents = pygame.event.get(pygame.KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    return keyUpEvents[0].key


def best_first_search():
    global s, snack, visited
    curr_posx = s.body[0].pos[0]
    curr_posy = s.body[0].pos[1]
    nodes = []  # 0: left, 1: right, 2: up, 3: down
    p = ((curr_posx - 1) % 20, curr_posy)
    nodes.append(('left', manhattan_dis((curr_posx - 1, curr_posy), snack.pos, size=rows), p))
    p = ((curr_posx + 1) % 20, curr_posy)
    nodes.append(('right', manhattan_dis((curr_posx + 1, curr_posy), snack.pos, size=rows), p))
    p = (curr_posx, (curr_posy - 1) % 20)
    nodes.append(('up', manhattan_dis((curr_posx, curr_posy - 1), snack.pos, size=rows), p))
    p = (curr_posx, (curr_posy + 1) % 20)
    nodes.append(('down', manhattan_dis((curr_posx, curr_posy + 1), snack.pos, size=rows), p))
    if set(nodes[:][2]) <= set(list(map(lambda z: z.pos, s.body))):
        s.move()
        return
    i = 0
    print()
    best = []
    dist = []
    for p in nodes:
        prio = 0
        if (len(s.body) > 2):
            temp = [((curr_posx + 1) % 20, (curr_posy + 1) % 20), ((curr_posx + 1) % 20, (curr_posy - 1) % 20)]
            if set(temp) <= set(list(map(lambda z: z.pos, s.body))):
                if p[0] == "right":
                    prio += 1
                elif (p[0] == "up" and s.curr_dir == "right" and s.last_dir == "up") or (
                        p[0] == "down" and s.curr_dir == "right" and s.last_dir == "down"):
                    prio += 1
            temp = [((curr_posx - 1) % 20, (curr_posy + 1) % 20), ((curr_posx - 1) % 20, (curr_posy - 1) % 20)]
            if set(temp) <= set(list(map(lambda z: z.pos, s.body))):
                if p[0] == "left":
                    prio += 1
                elif (p[0] == "up" and s.curr_dir == "left" and s.last_dir == "up") or (
                        p[0] == "down" and s.curr_dir == "left" and s.last_dir == "down"):
                    prio += 1
            temp = [((curr_posx + 1) % 20, (curr_posy + 1) % 20), ((curr_posx - 1) % 20, (curr_posy + 1) % 20)]
            if set(temp) <= set(list(map(lambda z: z.pos, s.body))):
                if p[0] == "down":
                    prio += 1
                elif (p[0] == "left" and s.curr_dir == "down" and s.last_dir == "left") or (
                        p[0] == "right" and s.curr_dir == "down" and s.last_dir == "right"):
                    prio += 1
            temp = [((curr_posx + 1) % 20, (curr_posy - 1) % 20), ((curr_posx - 1) % 20, (curr_posy - 1) % 20)]
            if set(temp) <= set(list(map(lambda z: z.pos, s.body))):
                if p[0] == "up":
                    prio += 1
                elif (p[0] == "left" and s.curr_dir == "up" and s.last_dir == "left") or (
                        p[0] == "right" and s.curr_dir == "up" and s.last_dir == "right"):
                    prio += 1
            cy = 0
            if curr_posy > 16 and curr_posy < 19:
                cy = 19 - curr_posy
            elif curr_posy < 17:
                cy = 3
            bottom = [q for q in list(map(lambda z: z.pos, s.body)) if
                      q[0] == curr_posx and q[1] - curr_posy < cy and curr_posy < q[1]]
            for i in range(3 - cy):
                if (curr_posx, i) in list(map(lambda z: z.pos, s.body)): bottom.append((curr_posx, i))
            print("bottom " + str(bottom))
            cy = 0
            if curr_posy > 0 and curr_posy < 3:
                cy = curr_posy
            elif curr_posy > 2:
                cy = 3
            top = [q for q in list(map(lambda z: z.pos, s.body)) if
                   q[0] == curr_posx and curr_posy - q[1] < cy and curr_posy > q[1]]
            for i in range(19, 16 + cy, -1):
                if (curr_posx, i) in list(map(lambda z: z.pos, s.body)): top.append((curr_posx, i))
            print("top " + str(top))
            cx = 0
            if curr_posx > 0 and curr_posx < 3:
                cx = curr_posx
            elif curr_posx > 2:
                cx = 3
            left = [q for q in list(map(lambda z: z.pos, s.body)) if
                    q[1] == curr_posy and curr_posx - q[0] < cx and curr_posx > q[0]]
            for i in range(19, 16 + cx, -1):
                if (i, curr_posy) in list(map(lambda z: z.pos, s.body)): left.append((i, curr_posy))
            print("left " + str(left))
            cx = 0
            if curr_posx > 16 and curr_posx < 19:
                cx = 19 - curr_posx
            elif curr_posx < 17:
                cx = 3
            right = [q for q in list(map(lambda z: z.pos, s.body)) if
                     q[1] == curr_posy and q[0] - curr_posx < cx and curr_posx < q[0]]
            for i in range(3 - cx):
                if (i, curr_posy) in list(map(lambda z: z.pos, s.body)): right.append((i, curr_posy))
            print("right " + str(right))
            temp = []
            if p[0] == "up":
                if len(top) and s.curr_dir != "down":
                    prio += len(top)
                    for q in top:
                        temp.append(manhattan_dis((curr_posx, curr_posy), q, size=rows))
                    dist.append(("up", min(temp)))
            elif p[0] == "down":
                if len(bottom) and s.curr_dir != "up":
                    prio += len(bottom)
                    for q in bottom:
                        temp.append(manhattan_dis((curr_posx, curr_posy), q, size=rows))
                    dist.append(("down", min(temp)))
            elif p[0] == "left":
                if len(left) and s.curr_dir != "right":
                    prio += len(left)
                    for q in left:
                        temp.append(manhattan_dis((curr_posx, curr_posy), q, size=rows))
                    dist.append(("left", min(temp)))
            elif p[0] == "right":
                if len(right) and s.curr_dir != "left":
                    prio += len(right)
                    for q in right:
                        temp.append(manhattan_dis((curr_posx, curr_posy), q, size=rows))
                    dist.append(("right", min(temp)))
            if p[2] in list(map(lambda z: z.pos, s.body)):
                prio += 1
        best.append((p[0], p[1], p[2], prio))
    if len(dist):
        print(dist)
        mindist = min(dist, key=lambda t: t[1])
        print(mindist)
        temp = [x[0] for x in dist if x[1] == mindist[1]]
        print(temp)
        for j in temp:
            print(j)
            near = best.pop([y[0] for y in best].index(j))
            print(near)
            best.append((near[0], near[1], near[2], near[3] + 1))
    best = sorted(best, key=lambda t: (t[3], t[1]))
    print(best)
    for p in best:
        print(i)
        if p[0] == "left" and s.curr_dir != "right" and p not in visited:
            print("A")
            s.move(control="left")
            visited.add(p)
            return
        elif p[0] == "right" and s.curr_dir != "left" and p not in visited:
            print("B")
            s.move(control="right")
            visited.add(p)
            return
        elif p[0] == "up" and s.curr_dir != "down" and p not in visited:
            print("C")
            s.move(control="up")
            visited.add(p)
            return
        elif p[0] == "down" and s.curr_dir != "up" and p not in visited:
            print("D")
            s.move(control="down")
            visited.add(p)
            return
        i += 1
    s.move()


def manhattan_dis(p, q, size=0):
    dx = min(abs(q[0] - p[0]), size - abs(q[0] - p[0]))
    dy = min(abs(q[1] - p[1]), size - abs(q[1] - p[1]))
    return dx + dy


def main():
    global width, rows, s, snack, win, visited
    pygame.init()
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption('Snake Game Bot')
    startx = random.randint(0, rows - 1)
    starty = random.randint(0, rows - 1)
    s = snake((255, 255, 51), (startx, starty))
    snack = cube(randomSnack(rows, s), color=(255, 51, 51))
    flag = True
    cost = 0
    clock = pygame.time.Clock()
    visited = set({})

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        best_first_search()
        if s.body[0].pos == snack.pos:
            visited = set({})
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(255, 51, 51))
        if s.body[0].pos in list(map(lambda z: z.pos, s.body[1:])):
            redrawWindow(lose=True)
            print('Score: ', len(s.body) - 1)
            showGameOverScreen()
            startx = random.randint(0, rows - 1)
            starty = random.randint(0, rows - 1)
            s.reset((startx, starty))
            snack = cube(randomSnack(rows, s), color=(255, 51, 51))

        redrawWindow()

main()