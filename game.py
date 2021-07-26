import pygame
from settings import *
from pygame import Vector2
import math
from os import path

from rocket import Rocket
from moon import Moon

# REGLAS:
# - Juego arcade
# - El jugador controla un cohete que debe hacer aterrizar SUAVEMENTE
# - Controla el COHETE con los CURSORES
# - Al cohete le afecta la fuerza de GRAVEDAD
# - EL cohete tiene mucha INERCIA
# - El cohete tiene COMBUSTIBLE, que se gasta al impulsar el cohete
# - Si el combustible se agota, el cohete deja de poder ser controlado
# - El juego acaba MAL si chocamos contra el SUELO
# - El juego acaba BIEN si aterrizamos en la ZONA DE ATERRIZAJE

# MEJORAS 
# - Menú de inicio con el título del juego
# - Interfaz de usuario que muestra la puntuación
# - Pantalla final en caso de terminar la partida que muestra la puntuación conseguida
# - Sonido del motor del cohete cuando se pulsa una tecla, 
#   y otro sonido en caso de chocar contra el suelo
# - Imagen del cohete

# MEJORA EXTRA
# - La puntuación que se obtiene en cada pantalla depende del porcentaje
#   de combusible restante al aterrizar


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.large_font = pygame.font.SysFont('arial', 80)
        self.small_font = pygame.font.SysFont('arial', 32)
        self.load_data()

    def load_data(self):
        root_folder = path.dirname(__file__)
        sound_folder = path.join(root_folder, "sound")
        img_folder = path.join(root_folder, "img")
        self.load_images(img_folder)
        self.load_sounds(sound_folder)

    def load_images(self, img_folder):
        self.rocket_image = pygame.image.load(
            path.join(img_folder, "spaceRocket.png")).convert_alpha()

    def load_sounds(self, sound_folder):
        pygame.mixer.music.load(
            path.join(sound_folder, "engine.ogg"))
        self.crush_fx = pygame.mixer.Sound(
            path.join(sound_folder, "crush.ogg"))
        self.crush_fx.set_volume(0.1)      

    def start(self):
        self.rocket = Rocket(WIDTH/2, 0, self.rocket_image, self.crush_fx)
        self.moon = Moon(HEIGHT//2, 10)
        self.moon.generate_terrain()
        self.run()

    def run(self):
        pygame.mixer.music.play(-1)
        self.playing = True
        while (self.playing):
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        self.game_over_menu()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.rocket.update(self.moon)
        
        if not self.rocket.alive:
            self.playing = False

        if self.rocket.landed:
            self.score += int(100*self.rocket.fuel) #puntuación en función del porcentaje de combustible que queda
            self.start()

    def draw(self):
        self.screen.fill(BLACK)
        self.rocket.draw(self.screen)
        self.moon.draw(self.screen)
        self.draw_UI()
        score_text = self.small_font.render(
            f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (WIDTH//2 + 150, 5))
        pygame.display.flip()

    def draw_UI(self):
        pygame.draw.rect(self.screen, MIDGREY, pygame.Rect(5, 5, 200, 25))
        pygame.draw.rect(self.screen, LIGHTGREY, pygame.Rect(
            7, 7, 196 * self.rocket.fuel, 21))
    
    def main_menu(self):
        title_text = self.large_font.render("LUNAR LANDER", True, WHITE)
        instructions_text = self.small_font.render(
            "Press any key to start", True, LIGHTGREY)
        self.score = 0
        self.screen.fill(BLACK)
        self.screen.blit(
            title_text, (WIDTH//2 - title_text.get_rect().width//2, 25))
        self.screen.blit(
            instructions_text, (
                WIDTH//2 - instructions_text.get_rect().width//2, HEIGHT-50)
        )

        pygame.display.flip()

        in_main_menu = True
        while (in_main_menu):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_main_menu = False
        self.start()

    def game_over_menu(self):
        pygame.mixer.music.stop()
        title_text = self.large_font.render("GAME OVER", True, RED)
        instructions_text = self.small_font.render(
            "Press any key to restart", True, LIGHTGREY)

        self.screen.fill(BLACK)
        self.screen.blit(
            title_text, (WIDTH//2 - title_text.get_rect().width//2, 25))

        score_text = self.small_font.render(
            f"Score: {self.score}", True, WHITE)
        self.screen.blit(
            score_text, (WIDTH//2 - score_text.get_rect().width//2, HEIGHT//2))

        self.screen.blit(
            instructions_text, (
                WIDTH//2 - instructions_text.get_rect().width//2, HEIGHT-50)
        )

        pygame.display.flip()

        in_game_over_menu = True
        while (in_game_over_menu):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_game_over_menu = False
        self.main_menu()


game = Game()
game.main_menu()

