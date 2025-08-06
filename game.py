from random import randint, choice
from pygame import Rect
import time  # Usado para controlar o tempo após colisão

# --- Configurações da janela ---
WIDTH = 800
HEIGHT = 600

# --- Estados globais ---
jogo_ativo = False        # Indica se o jogo está em andamento
game_over = False         # Indica se o jogo terminou
colidiu = False           # Marca se houve uma colisão
som_ligado = True         # Controla se o som está ativado
musica_atual = None       # Armazena a música atual tocando
pontos = 0                # Pontuação do jogador
tempo_colisao = 0         # Guarda o tempo da colisão para exibir o impacto

# --- Atores principais ---
jogador = Actor("alien", pos=(400, 500))                    # Jogador
fundo = Actor("bg2", pos=(WIDTH // 2, HEIGHT // 2))         # Fundo principal
fundocopy = Actor("bg2", pos=(WIDTH + WIDTH // 2, HEIGHT // 2))  # Cópia para criar efeito de scroll infinito
menu_background = Actor("menu_background", pos=(WIDTH // 2, HEIGHT // 2))  # Fundo do menu

# --- Botões do menu e game over ---
botao_iniciar = Actor("btniniciar", pos=(80, 50))
botao_sair = Actor("btnsair", pos=(80, 100))
botao_som = Actor("btnsomligado", pos=(80, 150))
botao_tentar = Actor("btniniciar", pos=(WIDTH // 2, HEIGHT // 2 + 80))   # Usado para tentar novamente
botao_menu = Actor("btnsair", pos=(WIDTH // 2, HEIGHT // 2 + 140))       # Retorna ao menu principal

# --- Lista de barreiras e imagens disponíveis ---
img_barreiras = ["arm1", "arm2", "arm3", "arm4"]
barreiras = []

# --- Funções de controle do jogo ---

# Reinicia o jogo
def reiniciar_jogo():
    global jogo_ativo, game_over, colidiu, pontos, barreiras
    jogo_ativo = True
    game_over = False
    colidiu = False
    pontos = 0
    barreiras.clear()
    jogador.pos = (400, 500)
    jogador.image = "alien"
    atualizar_musica()

# Volta ao menu inicial
def voltar_menu():
    global jogo_ativo, game_over, colidiu, pontos, barreiras
    jogo_ativo = False
    game_over = False
    colidiu = False
    pontos = 0
    barreiras.clear()
    jogador.pos = (400, 500)
    jogador.image = "alien"
    atualizar_musica()

# Desenha os elementos na tela
def draw():
    screen.clear()

    if jogo_ativo:
        # Desenha o fundo, jogador, barreiras e pontuação
        fundo.draw()
        fundocopy.draw()
        jogador.draw()
        for barreira in barreiras:
            barreira.draw()
        screen.draw.text(f"Pontos: {pontos}", topleft=(10, 10), fontsize=30, color="white")

    elif game_over:
        # Exibe a tela de game over
        fundo.draw()
        fundocopy.draw()
        jogador.draw()
        for barreira in barreiras:
            barreira.draw()
        screen.draw.text("TENTAR NOVAMENTE", center=(WIDTH // 2, HEIGHT // 2 - 40), fontsize=60, color="lime")
        screen.draw.text(f"Pontos: {pontos}", topleft=(10, 10), fontsize=30, color="white")
        botao_tentar.draw()
        botao_menu.draw()

    else:
        # Exibe o menu inicial
        menu_background.draw()
        screen.draw.text("RUN ALIEN", center=(400, 100), fontsize=50, color="white")
        botao_iniciar.draw()
        botao_sair.draw()
        botao_som.draw()

# Detecta cliques do mouse nos botões
def on_mouse_down(pos):
    global som_ligado

    if game_over:
        if botao_tentar.collidepoint(pos):
            reiniciar_jogo()
        elif botao_menu.collidepoint(pos):
            voltar_menu()

    elif not jogo_ativo:
        if botao_iniciar.collidepoint(pos):
            reiniciar_jogo()
        elif botao_sair.collidepoint(pos):
            exit()
        elif botao_som.collidepoint(pos):
            # Alterna som ligado/desligado
            som_ligado = not som_ligado
            botao_som.image = "btnsomligado" if som_ligado else "btnsomdesligado"
            atualizar_musica()

# Lê as teclas pressionadas para mover o jogador
def teclas():
    if keyboard.up:
        jogador.y = max(jogador.height//2, jogador.y - 5)
    if keyboard.down:
        jogador.y = min(HEIGHT - jogador.height//2, jogador.y + 5)
    if keyboard.left:
        jogador.x = max(jogador.width//2, jogador.x - 5)
    if keyboard.right:
        jogador.x = min(WIDTH - jogador.width//2, jogador.x + 5)

# Cria uma barreira com imagem aleatória e posição vertical randômica
def criar_barreiras():
    imagem = choice(img_barreiras)
    pos_y = randint(50, HEIGHT - 50)
    barreira = Actor(imagem, pos=(WIDTH + 50, pos_y))
    barreira.angle = 90
    barreiras.append(barreira)

# Move as barreiras para a esquerda e remove as que saíram da tela
def mover_barreiras():
    global pontos
    for barreira in barreiras[:]:
        barreira.x -= 5
        if barreira.right < 0:
            barreiras.remove(barreira)
            pontos += 1  # Ganha ponto ao desviar

# Atualiza o jogo a cada frame
def update():
    global jogo_ativo, game_over, colidiu, tempo_colisao

    if jogo_ativo:
        teclas()

        # Scroll infinito do fundo
        fundo.x -= 2
        fundocopy.x -= 2
        if fundo.right < 0:
            fundo.left = fundocopy.right
        if fundocopy.right < 0:
            fundocopy.left = fundo.right

        # Criação aleatória de barreiras
        if randint(0, 30) == 0:
            criar_barreiras()

        mover_barreiras()

        # Verifica colisão com barreiras
        for barreira in barreiras:
            jogador_rect_reduzido = Rect(jogador.x - 20, jogador.y - 20, 40, 40)
            barreira_rect_reduzido = Rect(barreira.x - 20, barreira.y - 20, 40, 40)
            if barreira_rect_reduzido.colliderect(jogador_rect_reduzido) and not colidiu:
                colidiu = True
                tempo_colisao = time.time()
                jogador.image = "colisao_alien"
                if som_ligado:
                    sounds.colidir_music.play()
                break

    elif colidiu and not game_over:
        # Aguarda 1 segundo após colisão para mostrar tela de fim de jogo
        if time.time() - tempo_colisao >= 1.0:
            game_over = True
            jogo_ativo = False

# Controla a música do jogo conforme estado (menu ou jogo)
def atualizar_musica():
    global musica_atual
    if not som_ligado:
        sounds.stop()
        musica_atual = None
        return

    nova_musica = "game_music" if jogo_ativo else "menu_music"

    if musica_atual != nova_musica:
        music.stop()
        music.play(nova_musica)
        musica_atual = nova_musica

# --- Início do jogo ---
atualizar_musica()
