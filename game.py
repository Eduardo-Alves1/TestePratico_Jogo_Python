from random import randint, choice

# Dimensões da janela do jogo
WIDTH = 800
HEIGHT = 600

# Estado do jogo
jogo_ativo = False
som_ligado = True

# Botões do menu
botao_iniciar = Actor("btniniciar", pos=(80, 50))
botao_sair = Actor("btnsair", pos=(80, 100))
botao_som_desligado = Actor("btnsomdesligado", pos=(80, 150))
botao_som_ligado = Actor("btnsomligado", pos=(80, 150))

# Elementos visuais
jogador = Actor("alien", pos=(400, 300))
fundo = Actor("bg2", pos=(WIDTH // 2, HEIGHT // 2))
fundocopy = Actor("bg2", pos=(WIDTH + WIDTH // 2, HEIGHT // 2))
jogador.pos = (400, 500)

# Barreira inicial e pontuação
img_barreiras = ["arm1", "arm2", "arm3", "arm4"]
barreiras = []
pontos = 0

nova = Actor(choice(img_barreiras), pos=(WIDTH + 50, randint(50, HEIGHT - 50)))
nova.width = 10
nova.height = 10
barreiras.append(nova)


# Desenha todos os elementos da tela
def draw():
    screen.clear()
    if not jogo_ativo:
        screen.draw.text("MENU PRINCIPAL", center=(400, 100), fontsize=50, color="white")
        botao_iniciar.draw()
        botao_sair.draw()
        botao_som_desligado.draw()
        botao_som_ligado.draw()
    else:
        screen.draw.text("JOGO COMEÇOU!", center=(400, 100), fontsize=50, color="white")
        fundo.draw()
        fundocopy.draw()
        jogador.draw()
        for barreira in barreiras:
            barreira.draw()

        screen.draw.text(f"Pontos: {pontos}", topleft=(10, 10), fontsize=30, color="white")


# Detecta cliques do mouse nos botões
def on_mouse_down(pos):
    global jogo_ativo, som_ligado, pontos, barreiras

    if botao_iniciar.collidepoint(pos):
        jogo_ativo = True
        pontos = 0
        barreiras.clear()
        jogador.pos = (400, 500)
    elif botao_som_desligado.collidepoint(pos):
        som_ligado = not som_ligado
        if som_ligado:
            botao_som_ligado.image = "btnsomligado"
        else:
            botao_som_ligado.image = "btnsomdesligado"
    elif botao_sair.collidepoint(pos):
        quit()  # Sai do jogo


# Controla movimentação do jogador via teclado
def teclas():
    if keyboard.up:
        jogador.y -= 5
    if keyboard.down:
        jogador.y += 5
    if keyboard.left:
        jogador.x -= 5
    if keyboard.right:
        jogador.x += 5

    # Impede que o jogador ultrapasse os limites da tela
    jogador.y = max(0, min(jogador.y, HEIGHT))
    jogador.x = max(0, min(jogador.x, WIDTH))


# Gera novas barreiras com posição e imagem aleatória
def criar_barreiras():
    imagem = choice(img_barreiras)
    aleatorio_x = randint(50, HEIGHT - 50)
    barreira = Actor(imagem, pos=(WIDTH + 50, aleatorio_x))

    barreira.width = 50
    barreira.height = 50
    barreira.angle = 90 if imagem else 0

    barreiras.append(barreira)


# Move barreiras e atualiza pontuação ao passar pela tela
def mover_barreiras():
    global pontos
    for barreira in barreiras[:]:
        barreira.x -= 5
        if barreira.right < 0:
            barreiras.remove(barreira)
            pontos += 1


# Atualiza estado do jogo a cada frame
def update():
    global jogo_ativo

    if jogo_ativo:
        teclas()
        fundo.x -= 2
        fundocopy.x -= 2

        # Troca fundo para dar efeito de scroll contínuo
        if fundo.right < 0:
            fundo.left = fundocopy.right
        if fundocopy.right < 0:
            fundocopy.left = fundo.right

        # Cria barreiras aleatoriamente
        if randint(0, 30) == 0:
            criar_barreiras()

        mover_barreiras()

        # Verifica colisão entre o jogador e as barreiras
        for barreira in barreiras:
            if barreira.colliderect(jogador):
                jogo_ativo = False
                print("COLISÃO! Fim de jogo.")
                break
