# 👽 Run Alien - Jogo em PgZero

**Run Alien** é um jogo 2D simples feito com [PgZero](https://pygame-zero.readthedocs.io/en/stable/), onde você controla um alienígena tentando escapar de barreiras que se movem em sua direção. O jogador deve desviar dos obstáculos e acumular pontos. O jogo possui um menu interativo com botões, música e efeitos sonoros.

## 🎮 Demonstração


---

## 🚀 Como jogar

- Use as **setas do teclado** para mover o alien (↑ ↓ ← →).
- Desvie das barreiras para sobreviver.
- A cada barreira evitada, você ganha **1 ponto**.
- Se colidir com uma barreira, verá a tela de "Tentar Novamente".
- Você pode optar por **tentar de novo** ou **voltar ao menu**.

---

## 🛠️ Funcionalidades

- 🎨 Menu principal com botões de Iniciar, Sair e Ativar/Desativar Som.
- 🎵 Música dinâmica de fundo (menu e jogo).
- 🔊 Efeito sonoro ao colidir com obstáculos.
- 🌌 Rolagem infinita do fundo (efeito de movimento).
- 🧱 Barreiras aleatórias com imagens variadas.
- 📈 Sistema de pontuação.

---

## 📦 Requisitos

- **Python 3.x**
- **PgZero** (pygame-zero)

## 💻 Ambiente Virtual (Recomendado)

Para isolar o projeto e garantir que tudo funcione corretamente, crie um ambiente virtual:

### Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Windows (CMD):

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt




▶️ Como executar o jogo

pgzrun run_alien.py


🗂️ Estrutura recomendada do projeto

run-alien/
├── run_alien.py
├── README.md
├── images/
│   ├── alien.png
│   ├── bg2.png
│   ├── arm1.png
│   ├── arm2.png
│   └── ... etc.
├── sounds/
│   ├── menu_music.wav
│   ├── game_music.wav
│   └── colidir_music.wav
