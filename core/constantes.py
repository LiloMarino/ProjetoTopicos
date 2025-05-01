from pathlib import Path

import pygame

# Tamanhos
TAMANHO_TELA = (1024, 1024)
TAMANHO_SPRITE = (32, 32)

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# Caminhos de imagem
PATH_COELHO = ASSETS_DIR / "cueio.png"
PATH_LOBO = ASSETS_DIR / "lobo.png"
PATH_CENOURA = ASSETS_DIR / "cenoura.png"
PATH_AMBIENTE = ASSETS_DIR / "ambiente.png"
PATH_AMBIENTE_MASK = ASSETS_DIR / "ambiente_mask.png"

# Caminhos de config NEAT
NEAT_CONFIG_COELHO = BASE_DIR / "core" / "neat-config-coelho.ini"
NEAT_CONFIG_LOBO = BASE_DIR / "core" / "neat-config-lobo.ini"

# Imagens globais (inicialmente None)
IMG_COELHO = None
IMG_LOBO = None
IMG_CENOURA = None


def init_constantes():
    """Inicializa e carrega as imagens após o display ser criado."""
    global IMG_COELHO, IMG_LOBO, IMG_CENOURA

    IMG_COELHO = pygame.transform.scale(
        pygame.image.load(PATH_COELHO).convert_alpha(), TAMANHO_SPRITE
    )

    IMG_LOBO = pygame.transform.scale(
        pygame.image.load(PATH_LOBO).convert_alpha(), TAMANHO_SPRITE
    )

    IMG_CENOURA = pygame.transform.scale(
        pygame.image.load(PATH_CENOURA).convert_alpha(), TAMANHO_SPRITE
    )
