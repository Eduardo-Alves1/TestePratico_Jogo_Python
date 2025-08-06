from random import randint, choice
from pygame import Rect

# --- Configurações da janela ---
WIDTH = 800
HEIGHT = 600

# --- Estados globais ---
jogo_ativo = False
game_over = False
colidiu = False
som_ligado = True
musica_atual = None
pontos = 0

# --- Ator principal e fundos ---
jogador = Actor("alien", pos=(400, 500))
fundo = Actor("bg2", pos=(WIDTH // 2, HEIGHT // 2))
fundocopy = Actor("bg2", pos=(WIDTH + WIDTH // 2, HEIGHT // 2))
menu_background = Actor("menu_background", pos=(WIDTH // 2, HEIGHT // 2))

# --- Botões ---
botao_iniciar = Actor("btniniciar", pos=(80, 50))
botao_sair = Actor("btnsair", pos=(80, 100))
botao_som = Actor("btnsomligado", pos=(80, 150))
botao_tentar = Actor("btniniciar", pos=(WIDTH // 2, HEIGHT // 2 + 80))
botao_menu = Actor("btnsair", pos=(WIDTH // 2, HEIGHT // 2 + 140))  # Voltar ao menu

# --- Barreiras ---
img_barreiras = ["arm1", "arm2", "arm3", "arm4"]
barreiras = []

# --- Funções principais ---

def reiniciar_jogo():
    global jogo_ativo, game_over, colidiu, pontos, barreiras
    jogo_ativo = True
    game_over = False
    colidiu = False
    pontos = 0
    barreiras.clear()
    jogador.pos = (400, 500)
    jogador.image = "alien"  # Voltar imagem padrão
    atualizar_musica()

def voltar_menu():
    global jogo_ativo, game_over, colidiu, pontos, barreiras
    jogo_ativo = False
    game_over = False
    colidiu = False
    pontos = 0
    barreiras.clear()
    jogador.pos = (400, 500)
    jogador.image = "alien"  # Voltar imagem padrão
    atualizar_musica()

def draw():
    screen.clear()
    if jogo_ativo:
        fundo.draw()
        fundocopy.draw()
        jogador.draw()
        for barreira in barreiras:
            barreira.draw()
        screen.draw.text(f"Pontos: {pontos}", topleft=(10, 10), fontsize=30, color="white")
    
    elif game_over:
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
        menu_background.draw()
        screen.draw.text("RUN ALIEN", center=(400, 100), fontsize=50, color="white")
        botao_iniciar.draw()
        botao_sair.draw()
        botao_som.draw()

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
            som_ligado = not som_ligado
            botao_som.image = "btnsomligado" if som_ligado else "btnsomdesligado"
            atualizar_musica()

def teclas():
    if keyboard.up:
        jogador.y = max(jogador.height//2, jogador.y - 5)
    if keyboard.down:
        jogador.y = min(HEIGHT - jogador.height//2, jogador.y + 5)
    if keyboard.left:
        jogador.x = max(jogador.width//2, jogador.x - 5)
    if keyboard.right:
        jogador.x = min(WIDTH - jogador.width//2, jogador.x + 5)

def criar_barreiras():
    imagem = choice(img_barreiras)
    pos_y = randint(50, HEIGHT - 50)
    barreira = Actor(imagem, pos=(WIDTH + 50, pos_y))
    barreira.angle = 90
    barreiras.append(barreira)

def mover_barreiras():
    global pontos
    for barreira in barreiras[:]:
        barreira.x -= 5
        if barreira.right < 0:
            barreiras.remove(barreira)
            pontos += 1

def update():
    global jogo_ativo, game_over, colidiu
    if jogo_ativo:
        teclas()

        # Scroll do fundo
        fundo.x -= 2
        fundocopy.x -= 2

        if fundo.right < 0:
            fundo.left = fundocopy.right
        if fundocopy.right < 0:
            fundocopy.left = fundo.right

        # Criar barreiras
        if randint(0, 30) == 0:
            criar_barreiras()

        mover_barreiras()

        # Detectar colisão
        for barreira in barreiras:
            jogador_rect_reduzido = Rect(jogador.x - 20, jogador.y - 20, 40, 40)
            barreira_rect_reduzido = Rect(barreira.x - 20, barreira.y - 20, 40, 40)
            if barreira_rect_reduzido.colliderect(jogador_rect_reduzido) and not colidiu:
                colidiu = True
                if som_ligado:
                    sounds.colidir_music.play()  # toca som antes
                jogador.image = "colisao_alien"
                jogo_ativo = False
                game_over = True
                # Removi o atualizar_musica() para não cortar o som
                print("COLISÃO! Fim de jogo.")
                break


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

# Inicialização
atualizar_musica()
