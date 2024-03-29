# coding=utf-8
# @Time    : 2021/11/16 16:30
# @Software: PyCharm
import os
import random

import pygame

size: tuple[int, int] = 300, 500  # 设置窗口尺寸
width, height = 300, 533
FPS = 30
# Setup 设置
pygame.init()
Screen = pygame.display.set_mode(size)  # 显示窗口
pygame.display.set_caption("小鸟管道（空格运行)")  # 设置标题
CLOCK = pygame.time.Clock()  # 时间模块
IMAGES = {}  # 创建字典
BIRDS_IMG = {}  # 随机颜色的小鸟
PIPES_IMG = {}  # 随机颜色的管道
for image in os.listdir("picture"):
    name, extension = os.path.splitext(image)
    path = os.path.join("picture", image)
    IMAGES[name] = pygame.image.load(path)

START = pygame.mixer.Sound("audio/start.wav")  # 开场音效
DIE = pygame.mixer.Sound("audio/die.wav")  # 死亡音效
HIT = pygame.mixer.Sound("audio/hit.wav")  # 撞击音效
SCORE = pygame.mixer.Sound("audio/score.wav")  # 得分音效
FLAP = pygame.mixer.Sound("audio/flap.wav")  # 翅膀音效
# 位置
FLOOR_Y = height - IMAGES["floor"].get_height()


def main():
    while True:
        START.play()  # 播放音效
        IMAGES['bgpic'] = IMAGES[random.choice(['day', 'night'])]
        color = random.choice(['red', 'blue', 'yellow'])
        BIRDS_IMG['birds'] = [IMAGES[color + '-up'], IMAGES[color + '-mid'], IMAGES[color + '-down']]
        pipe = IMAGES[random.choice(['green-pipe', 'red-pipe'])]
        PIPES_IMG['pipes'] = [pipe, pygame.transform.flip(pipe, False, True)]  # 上下管道

        menu_window()  # 菜单窗口
        result = game_window()  # 游戏窗口
        end_window(result)  # 结束窗口


def menu_window():
    floor_gap = IMAGES['floor'].get_width() - width
    floor_x = 0
    guide_x = (width - IMAGES["guide"].get_width()) / 2
    guide_y = (FLOOR_Y - IMAGES["guide"].get_height()) / 2
    bird_x = width * 0.2
    bird_y = (height - BIRDS_IMG["birds"][0].get_height()) / 2
    bird_y_vel = 1  # 帧与帧之间向下移动 1 个像素
    bird_y_range = [bird_y - 8, bird_y + 8]  # 小鸟移动范围
    idx = 0
    frames = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]

    while True:  # 判断事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # 跳转，开始下一个游戏界面
        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0
        bird_y += bird_y_vel
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel *= -1
        idx += 1
        idx %= len(frames)
        Screen.blit(IMAGES["bgpic"], (0, 0))
        Screen.blit(IMAGES["floor"], (floor_x, FLOOR_Y))
        Screen.blit(IMAGES["guide"], (guide_x, guide_y))
        Screen.blit(BIRDS_IMG["birds"][frames[idx]], (bird_x, bird_y))
        pygame.display.update()
        CLOCK.tick(FPS)
        # 刷新频率


def game_window():
    score = 0
    FLAP.play()
    floor_gap = IMAGES['floor'].get_width() - width
    floor_x = 0
    bird = Bird(width * 0.2, height * 0.4)
    distance = 160  # 水管间距，难度自拟
    pipe_gap = 160  # 水管上下的间距，难度自拟
    n_paris = 4
    pipe_group = pygame.sprite.Group()
    for i in range(n_paris):
        pipe_y = random.randint(int(height * 0.3), int(height * 0.7))  # 水管出现的范围，难度
        pipe_up = Pipe(width + i * distance, pipe_y, True)
        pipe_down = Pipe(width + i * distance, pipe_y - pipe_gap, False)
        pipe_group.add([pipe_up, pipe_down])  # type: ignore
    while True:
        flap = False
        # 判断事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flap = True
                    FLAP.play()

        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0
        bird.update(flap)
        first_pipe_up = pipe_group.sprites()[0]  # 水管构造
        first_pipe_down = pipe_group.sprites()[1]
        if first_pipe_up.rect.right < 0:
            pipe_y = random.randint(int(height * 0.3), int(height * 0.7))  # 水管出现的范围，难度自拟
            new_pipe_up = Pipe(first_pipe_up.rect.x + n_paris * distance, pipe_y, True)
            new_pipe_down = Pipe(first_pipe_up.rect.x + n_paris * distance, pipe_y - pipe_gap, False)
            pipe_group.add([new_pipe_up, new_pipe_down])  # type: ignore
            first_pipe_up.kill()
            first_pipe_down.kill()
        pipe_group.update()

        if bird.rect.y > FLOOR_Y or bird.rect.y < 0 or pygame.sprite.spritecollideany(bird, pipe_group):
            bird.dying = True
            HIT.play()
            DIE.play()
            result = {'bird': bird, 'pipe_group': pipe_group, 'score': score}
            return result

        if bird.rect.left + first_pipe_up.x_vel < first_pipe_up.rect.centerx < bird.rect.left:
            SCORE.play()
            score += 1

        Screen.blit(IMAGES["bgpic"], (0, 0))
        pipe_group.draw(Screen)
        Screen.blit(IMAGES["floor"], (floor_x, FLOOR_Y))
        show_score(score)
        Screen.blit(bird.image, bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)  # 刷新频率


def end_window(result):
    game_over_x = (width - IMAGES["game-over"].get_width()) / 2
    game_over_y = (FLOOR_Y - IMAGES["game-over"].get_height()) / 2

    bird = result['bird']
    pipe_group = result['pipe_group']

    while True:
        if bird.dying:
            bird.go_die()
        else:  # 判断事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return  # 跳转，开始下一个游戏界面
        bird.go_die()
        Screen.blit(IMAGES["bgpic"], (0, 0))
        pipe_group.draw(Screen)
        Screen.blit(IMAGES["floor"], (0, FLOOR_Y))
        Screen.blit(IMAGES["game-over"], (game_over_x, game_over_y))
        show_score(result['score'])
        Screen.blit(bird.image, bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)  # 刷新频率


def show_score(score):
    score_str = str(score)
    n = len(score_str)
    w = IMAGES['0'].get_width() * 1.1  # 数字之间的间距
    x = (width - n * w) / 2
    y = height * 0.1
    for number in score_str:
        Screen.blit(IMAGES[number], (x, y))
        x += w


class Bird:
    def __init__(self, x, y):
        self.frames = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
        self.idx = 0
        self.images = BIRDS_IMG['birds']
        self.image = self.images[self.frames[self.idx]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = -10  # 速度
        self.max_y_vel = 10
        self.gravity = 1
        self.rotate = 45
        self.max_rotate = -20
        self.rotate_vel = -3
        self.y_vel_after_flap = -10
        self.rotate_after_flap = 45
        self.dying = False

    def update(self, flap=False):
        if flap:
            self.y_vel = self.y_vel_after_flap
            self.rotate = self.rotate_after_flap
        self.y_vel = min(self.y_vel + self.gravity, self.max_y_vel)  # 更新速度
        self.rect.y += self.y_vel
        self.rotate = max(self.rotate + self.rotate_vel, self.max_rotate)
        self.idx += 1
        self.idx %= len(self.frames)
        self.image = self.images[self.frames[self.idx]]
        self.image = pygame.transform.rotate(self.image, self.rotate)

    def go_die(self):
        if self.rect.y < FLOOR_Y:
            self.rotate = -90
            self.rect.y += self.max_y_vel
            self.image = self.images[self.frames[self.idx]]
            self.image = pygame.transform.rotate(self.image, self.rotate)
        else:
            self.dying = False


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, upwards=True):
        pygame.sprite.Sprite.__init__(self)
        if upwards:
            self.image = PIPES_IMG['pipes'][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
        else:
            self.image = PIPES_IMG['pipes'][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y
        self.x_vel = -4

    def update(self):
        self.rect.x += self.x_vel


main()
