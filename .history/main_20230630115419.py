import pygame
import os
import random

pygame.init()

musica_de_fundo = pygame.mixer.music.load(os.path.join("sounds","musica_fundo.mp3"))
pygame.mixer.music.play(-1)

TELA_LARGURA = 1000
TELA_ALTURA = 800

IMAGEM_PREDIO = pygame.image.load(os.path.join("imgs","prédio.png"))
IMAGEM_CHAO = pygame.image.load(os.path.join("imgs","chao.png"))
IMAGEM_BACKGROUND = pygame.image.load(os.path.join("imgs","bg1.png"))
IMAGENS_PASSARO = [
    pygame.image.load(os.path.join("imgs","p1.png")),
    pygame.image.load(os.path.join("imgs","p2.png")),
    pygame.image.load(os.path.join("imgs","p3.png")),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial black", 50,)


class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 20
    VELOCIDADE_ROTACAO = 25
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.y, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Prédio:
    DISTANCIA = 400
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.PREDIO_TOP0 = pygame.transform.flip(IMAGEM_PREDIO, False, True)
        self.PREDIO_BASE = IMAGEM_PREDIO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.PREDIO_TOP0.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.PREDIO_TOP0, (self.x, self.pos_topo))
        tela.blit(self.PREDIO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.PREDIO_TOP0)
        base_mask = pygame.mask.from_surface(self.PREDIO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, prédios, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for prédio in prédios:
        prédio.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (0,0,0))
    tela.blit(texto,(TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    prédios = [Prédio(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_prédio = False
        remover_prédios = []
        for prédio in prédios:
            for i, passaro in enumerate(passaros):
                if prédio.colidir(passaro):
                    passaros.pop(i)
                if not prédio.passou and passaro.x > prédio.x:
                    prédio.passou = True
                    adicionar_prédio = True
            prédio.mover()
            if prédio.x + prédio.PREDIO_TOP0.get_width() < 0:
                remover_prédios.append(prédio)
        if adicionar_prédio:
            pontos += 1
            prédios.append(Prédio(600))
        for prédio in remover_prédios:
            prédios.remove(prédio)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela,passaros, prédios, chao, pontos)

if __name__=="__main__":
    main()      


