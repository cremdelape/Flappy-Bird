# Importng the Libraries
from sprites import *
import os
import random

# Initialising the pygame module
pg.init()

# Launch the game window at the ceter of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'


# noinspection PyAttributeOutsideInit
class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.playing = True  # Check game window open or close
        self.running = True  # Check if a singular game loop is going on
        self.temp = 0
        self.scroll_count = 0
        self.score = 0
        self.load_data()

    def load_data(self):
        self.bg = pg.image.load('gallery/sprites/background.png').convert()
        self.die_sound = pg.mixer.Sound('gallery/audio/die.wav')
        self.point_sound = pg.mixer.Sound('gallery/audio/point.wav')
        self.flap_sound = pg.mixer.Sound('gallery/audio/wing.wav')

    def start(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.movables = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.add_pipe()
        pg.mixer.music.load('gallery/audio/game.ogg')
        self.run()

    def run(self):
        pg.mixer.music.play(loops=-1)
        while self.running:
            self.clock.tick(32)
            self.event()
            self.update()
            self.draw()

    def add_pipe(self):
        gap_ht = random.randrange(30, HEIGHT - GAP - 30)
        pipe1 = Pipe('t', gap_ht)
        pipe2 = Pipe('b', gap_ht)
        self.movables.add(pipe1, pipe2)
        self.all_sprites.add(pipe1, pipe2)

    def update(self):
        # Check to see if the player hits the edges
        if self.player.y <= 0 or self.player.y >= HEIGHT:
            self.die_sound.play()
            self.running = False
            pg.mixer.fadeout(500)
        # Window scroll
        for pipe in self.movables:
            pipe.x -= GAME_SPEED
            if pipe.rect.right <= 0:
                pipe.kill()
        self.scroll_count += GAME_SPEED
        # Adding more pipes
        if self.scroll_count >= DISTANCE:
            self.add_pipe()
            self.point_sound.play()
            self.score += 1
            self.scroll_count = 0
        # DIE!!
        for pipe in self.movables:
            if self.player.hitbox.colliderect(pipe.rect):
                self.die_sound.play()
                self.running = False
                pg.mixer.fadeout(500)

        self.all_sprites.update()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
            # Check if the player is flapping
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_RALT:
                    self.flap_sound.play()
                    self.player.vel = FLAP_POWER
                    if 0 < self.player.rot < 45:
                        self.player.rot_speed = ROTEY
                    if 270 < self.player.rot < 360:
                        self.player.rot_speed = ROTEY * 2.5
                    self.player.flapped = True

    def draw_text(self, size, text, colour, x):
        self.font = pg.font.SysFont('Comic Sans MS', size)
        text_surface = self.font.render(text, 1, colour)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, x))
        self.screen.blit(text_surface, text_rect)

    def check_highscore(self):
        with open('High Score', 'r+') as score_file:
            try:
                self.high_score = int(score_file.read())
            except IOError and ValueError:
                self.high_score = 0

        if self.score > self.high_score:
            with open('High Score', 'r+') as score_file:
                score_file.write(str(self.score))
            self.high_score = self.score
            return True
        else:
            return False

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text(32, f'{self.score}', WHITE, 20)
        # pg.draw.rect(self.screen, RED, self.player.hitbox, 2)
        # pg.draw.rect(self.screen, GREEN, self.player.rect, 2)

        pg.display.flip()

    def wait(self):
        self.waiting = True
        while self.waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.playing = False
                    self.waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.running = True
                        self.playing = True
                        self.waiting = False

    def start_screen(self):
        pg.mixer.music.load('gallery/audio/screen.ogg')
        pg.mixer.music.play(loops=-1)
        self.running = True
        self.screen.fill(LIGHTBLUE)
        self.draw_text(60, 'WELCOME', WHITE, HEIGHT * 0.25)
        self.draw_text(32, 'Press ENTER to play again', WHITE, HEIGHT * 0.5)
        pg.display.flip()
        self.wait()
        pg.mixer.music.fadeout(500)

    def go_screen(self):
        if not self.playing:
            return
        pg.mixer.music.load('gallery/audio/screen.ogg')
        pg.mixer.music.play(loops=-1)
        self.screen.fill(LIGHTBLUE)
        self.draw_text(60, 'GAME OVER', WHITE, HEIGHT * 0.5)
        self.draw_text(32, f'{self.score}', WHITE, 20)
        self.draw_text(32, 'Press ENTER to play again', WHITE, HEIGHT * 0.75)
        if self.check_highscore():
            self.draw_text(42, 'New High Score!', YELLOW, HEIGHT * 0.25)
        else:
            self.draw_text(40, f'High Score {self.high_score}', WHITE, HEIGHT * 0.25)
            self.draw_text(22, 'It is never too late', RED, HEIGHT * 0.6)
            self.draw_text(22, 'TO GIVE UP!', RED, HEIGHT * 0.7)
        pg.display.flip()
        self.wait()
        pg.mixer.music.fadeout(500)


game = Game()
game.start_screen()
while game.playing:
    game.__init__()
    game.start()
    game.go_screen()
