import pygame
from os import path
import shelve

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snds")

pygame.mixer.init()

TITLE = "Shump!"
WIDTH, HEIGHT = 380, 600
FPS = 60
ICON_IMG = pygame.image.load(path.join(img_dir, "playerLife1_orange.png"))

score_data = shelve.open("data")
score_data.setdefault("best_score", 0)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

POWER_UP_DROP_DOWN_PCT = 0.9


# Load All Graphics...
background_img = pygame.image.load(path.join(img_dir, "background.png"))
player_sprite = pygame.image.load(path.join(img_dir, "playerShip1_orange.png"))


meteor_sprites = [pygame.image.load(path.join(img_dir, "meteors", img)) \
	for img in [f"meteorBrown_big{n}.png" for n in range(1, 5)] \
	+ [f"meteorBrown_med{n}.png" for n in range(1, 3)] \
	+ [f"meteorBrown_small{n}.png" for n in range(1,3)]
]
gray_meteor_sprites = [pygame.image.load(path.join(img_dir, "meteors", img)) \
	for img in [f"meteorGrey_big{n}.png" for n in range(1,3)] \
	+ [f"meteorGrey_med{n}.png" for n in range(1,3)] \
	+ [f"meteorGrey_small{n}.png" for n in range(1,3)]
]
lazer = pygame.image.load(path.join(img_dir, "laserRed16.png"))

mob_expl_lst = [pygame.image.load(path.join(img_dir, "expl", img)) for img in \
		[f"regularExplosion0{n}.png" for n in range(9)] ]

player_expl_lst = [pygame.image.load(path.join(img_dir, "player_expl", img)) for img in [f"sonicExplosion0{n}.png" for n in range(9)]]

nums_lst = [pygame.image.load(path.join(img_dir, "nums", num_img)) for num_img in \
		[f"numeral{n}.png" for n in range(10)]]

sparks = [pygame.image.load(path.join(img_dir, img)) for img in ["laserRed09.png", "laserRed08.png", "laserRed10.png"]]

power_ups = [pygame.image.load(path.join(img_dir, img)) for img in ["bolt_gold.png", "shield_gold.png", "star_gold.png"]]
player_mini = pygame.image.load(path.join(img_dir, "playerLife1_orange.png"))
x_sprite = pygame.image.load(path.join(img_dir, "numeralX.png"))

# Load All Sounds...
lazer_sounds = [pygame.mixer.Sound(path.join(snd_dir, snd)) for snd in ["bullet_snd1.wav", "bullet_snd2.wav"]] 
[snd.set_volume(0.1) for snd in lazer_sounds]
expl_sounds = [pygame.mixer.Sound(path.join(snd_dir, snd)) for snd in ["explosion1.wav", "explosion2.wav"]]
[snd.set_volume(0.2) for snd in expl_sounds]

player_expl_snd = pygame.mixer.Sound(path.join(snd_dir, "player_expl_snd.ogg"))

power_ups_snds = [pygame.mixer.Sound(path.join(snd_dir, snd)) for snd in ["power_up3.wav", "power_up4.wav", "power_up2.wav"]]
power_ups_snds[-1].set_volume(0.1)

# Music
pygame.mixer.music.load(path.join(snd_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4)
