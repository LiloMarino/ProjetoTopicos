from pathlib import Path

import pygame

# Tamanhos
TAMANHO_TELA = (800, 600)
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


# Função auxiliar para carregar imagens com transparência e escala
def carregar_sprite(caminho: Path) -> pygame.Surface:
    return pygame.transform.scale(
        pygame.image.load(caminho).convert_alpha(), TAMANHO_SPRITE
    )


# Carregamento das imagens
IMG_COELHO = carregar_sprite(PATH_COELHO)
IMG_LOBO = carregar_sprite(PATH_LOBO)
IMG_CENOURA = carregar_sprite(PATH_CENOURA)
IMG_AMBIENTE = pygame.image.load(PATH_AMBIENTE).convert()
IMG_AMBIENTE_MASK = pygame.mask.from_surface(IMG_AMBIENTE)
