#importando as bibliotecas
import pathlib
import pygame
from pygame.locals import *
import random


#declarando as variaveis da janela / jogo
screen_largura = 400
screen_altura = 800

SPEED = 10
GRAVIDADE = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * screen_largura
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

#passarinho hitbox
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#sprites do passarinho batendo as asas juntos
        self.images = [pygame.image.load(caminho_p_Blue_up_bird).convert_alpha(),
                      pygame.image.load(caminho_p_Blue_mid_bird).convert_alpha(),
                      pygame.image.load(caminho_p_Blue_down_bird).convert_alpha()]
        
#SPEED do passarinho
        self.SPEED = SPEED


        self.current_image = 0

        self.image = pygame.image.load(caminho_p_Blue_up_bird).convert_alpha()

#mascara da hitbox do passaro, p melhorar a colisao
        self.mask = pygame.mask.from_surface(self.image)

#poe o passaro no meio da janela
        self.rect = self.image.get_rect()
        self.rect[0] = screen_largura / 2
        self.rect[1] = screen_altura / 2

#passa as 3 sprites fazendo a animacao do passaro batendo as asas
    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

#GRAVIDADE do jogo, é oq faz o passaro voltar a cair depois do pulo, n deixa ele subir infinitamente
        self.SPEED += GRAVIDADE

#faz o passaro cair e subir de acordo com cada atualizacao da tela
        self.rect[1] += self.SPEED

    def pulin(self):
        self.SPEED = -SPEED

#canos do jogo
class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(caminho_p_cano).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos


        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = screen_altura - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


#coloca o chao e faz a animacao do chao ficar em loop
class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(caminho_p_chao).convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = screen_altura - GROUND_HEIGHT


    def update(self):
        self.rect[0] -= GAME_SPEED

#funcao pra verificar se o sprite esta fora da tela
def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

#cria os canos aleatoriamente na tela
def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, screen_altura - size - PIPE_GAP)
    return (pipe, pipe_inverted)

#inicia a janela
pygame.init()

#determina o tamanho da janela
screen = pygame.display.set_mode((screen_largura, screen_altura))

#indica pro programa onde estao os sprites
caminho_p_fundo_dia = pathlib.Path(r"C:\Users\Biel\Desktop\PROJETITOS\FLAPPY BIRD\sprites\background-day.png")
caminho_p_Blue_mid_bird = pathlib.Path(r"C:\Users\Biel\Desktop\PROJETITOS\FLAPPY BIRD\sprites\bluebird-midflap.png")
caminho_p_Blue_down_bird = pathlib.Path(r"C:\Users\Biel\Desktop\PROJETITOS\FLAPPY BIRD\sprites\bluebird-downflap.png")
caminho_p_Blue_up_bird = pathlib.Path(r"C:\Users\Biel\Desktop\PROJETITOS\FLAPPY BIRD\sprites\bluebird-upflap.png")
caminho_p_chao = pathlib.Path(r'C:\Users\Biel\Desktop\PROJETITOS\FLAPPY BIRD\sprites\base.png')
caminho_p_cano = pathlib.Path(r'C:\Users\Biel\Desktop\PROJETITOS\FLAPPY BIRD\sprites\pipe-green.png')

#coloca o background na janela e converte pro tamando
fundo = pygame.image.load(caminho_p_fundo_dia)
fundo = pygame.transform.scale(fundo, (screen_largura, screen_altura))

#grupos p serem puxado, (tipo uma variavel)
bird_group = pygame.sprite.Group()
Bird = Bird()
bird_group.add(Bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(screen_largura * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


#limita o fps do passarinho, pra n ficar mt rapido ele batendo as asas 
clock = pygame.time.Clock()

#codigo p fechar o jogo se clicar no X
while True:
    clock.tick(25)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

#reconhece a tecla pra fazer o passaro pular
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                Bird.pulin()

#indica onde vai ficar o background
    screen.blit(fundo, (0, 0))

#indica se um chao sumiu da tela e cria outro
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

#indica se um cano sumiu da tela e cria outro
    if is_off_screen(pipe_group.sprites()[0]):  
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(screen_largura * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])  


#atualiza infinitamente os componentes dos grupos
    bird_group.update()
    ground_group.update()
    pipe_group.update()

#desenha os componentes do grupo
    bird_group.draw(screen)
    ground_group.draw(screen)
    pipe_group.draw(screen)

#faz a colisao do passarinho, game over
    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        input()
        break


#faz a tela atualizar infinitamente
    pygame.display.update()