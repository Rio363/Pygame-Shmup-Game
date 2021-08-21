import pygame
from sprites import *

pygame.init()
pygame.mixer.init()
screenSize = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

font_name = pygame.font.match_font("Arial")

mobs_and_mobsDeathTime = {}


def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	txt_surf = font.render(text, True, WHITE)
	txt_rect = txt_surf.get_rect(midtop=[x, y])
	surf.blit(txt_surf, txt_rect)


def draw_shield_bar(surf, pos_x, pos_y, current_shield):
	if current_shield <= 0:
		current_shield = 0
	COLOR = GREEN
	if current_shield < 25:
		COLOR = RED
	elif current_shield < 65:
		COLOR = YELLOW

	BAR_LENGTH = 100
	BAR_HEIGHT = 20
	SHIELD_LENGTH = (current_shield / 100) * BAR_LENGTH
	SHIELD_HEIGHT = 20

	pygame.draw.rect(surf, COLOR, (pos_x, pos_y, SHIELD_LENGTH, SHIELD_HEIGHT))
	pygame.draw.rect(surf, WHITE, (pos_x, pos_y, BAR_LENGTH, BAR_HEIGHT), True)


def draw_numbers(surf, value, centerx, y, size=19):
	value = int(value)
	distance = 0
	# to make more centered
	if len(str(value)) >= 4:
		centerx = centerx - size + 1

	for num in range(len(str(value))):
		distance += size + 1
		if size != 19:
			surf.blit(pygame.transform.scale(nums_lst[int(str(value)[num])], (size, size)), (centerx + distance, y))
		else: # for the score
			surf.blit(nums_lst[int(str(value)[num])], (centerx + distance, y))


def draw_lives(surf, lives):
	count_x, count_y = 268, 20
	draw_numbers(screen, player.lives, count_x, count_y)
	surf.blit(player_mini, (330, 15))
	surf.blit(x_sprite, (310, 21))


def hit_points_animator(info_dict):
	now = pygame.time.get_ticks()
	for mob, death_time in info_dict.items():
		draw_text(screen, str(int(100 - mob.radius)), 25, mob.rect.centerx, mob.rect.centery)
		# draw_numbers(screen, int(100 - mob.radius), mob.rect.centerx, mob.rect.y)
		if now - death_time > 500:
			del info_dict[mob]
			return


def difficulty_manager():
	# Increase difficulty	
	if score > 2500:
		mob_count = 20
		POWER_UP_DROP_DOWN_PCT = 0.8
	if score > 7000:
		mob_count = 25
		POWER_UP_DROP_DOWN_PCT = 0.75
	if score > 12000:
		mob_count = 31
		if random.random() > 0.99 and len(gray_mobs) < 2:
			ImmortalMob(all_sprites, gray_mobs, mobs)
	if score > 18000:
		mob_count = 40
	if score > 25000:
		mob_count = 60
		if random.random() > 0.99 and len(gray_mobs) < 4:
			ImmortalMob(all_sprites, gray_mobs, mobs)
	if score > 50000:
			mob_count = 80
			if random.random() > 0.98 and len(gray_mobs) < 4:
				ImmortalMob(all_sprites, gray_mobs, mobs)


splash_screen = True
running = True

def create_mob(count=1):
	for mob in range(count):
		Mob(all_sprites, mobs)

def show_splash_screen():
	screen.blit(background_img, (0, 0))
	draw_text(screen, "Shmup Game", 30, WIDTH / 2, HEIGHT / 4)
	draw_text(screen, "Arrow keys to move, Space to shoot", 22, WIDTH / 2, HEIGHT / 2)
	draw_text(screen, f"Highest Score {score_data['best_score']}", 20, WIDTH / 2, 20)
	draw_text(screen, "Press Any Key", 24, WIDTH / 2, HEIGHT - HEIGHT / 4)

	pygame.display.flip()

	waiting = True
	while waiting:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT \
			 	or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pygame.quit()

			if event.type == pygame.KEYUP:
				waiting = False


# Play Music
pygame.mixer.music.play(loops=-1)


while running:
	if splash_screen:
		show_splash_screen()
		score = 0
		all_sprites = pygame.sprite.Group()

		mobs = pygame.sprite.Group()
		gray_mobs = pygame.sprite.Group()

		mob_count = 10
		for mob in range(mob_count):
			m = Mob()
			all_sprites.add(m)
			mobs.add(m)

		bullets = pygame.sprite.Group()
		power_ups_group = pygame.sprite.Group()

		player = Player(all_sprites, bullets)
		all_sprites.add(player)

		splash_screen = False

	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT \
		 or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				# Test Something
				pass

	screen.fill(BLACK)
	screen.blit(background_img, (0, 0))
	all_sprites.update()
	all_sprites.draw(screen)
	# draw_text(screen, str(score), 25, WIDTH / 2, 20)
	# draw_text(screen, str(int(player.shield)) + "%", 18, 35, 38)
	draw_numbers(screen, score, WIDTH / 2 - 30, 20)
	draw_numbers(screen, player.shield, -2, 40, 13)

	draw_lives(screen, player.lives)
	draw_shield_bar(screen,15, 15, player.shield)
	difficulty_manager()

	# Check Collisions between Mobs/Bullets
	hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
	for hit in hits:
		# Reduce mob strength
		hit.mob_strength -= random.randint(5, 10)
		if hit.mob_strength <= 0:

			# Add mob and death time to dict
			mobs_and_mobsDeathTime[hit] = pygame.time.get_ticks()

			hit.kill()
			Explosion("m", hit, all_sprites)
			
			# Add Score
			score += int(100 - hit.radius)
	
			# Play Explosion sound
			random.choice(expl_sounds).play()
		
			# Power ups
			if random.random() > POWER_UP_DROP_DOWN_PCT and score > 2000:
				PowerUp(hit.rect.centerx, hit.rect.centery, all_sprites, power_ups_group)
		else:
			Explosion("s", hit, all_sprites)


	# Check Collisions between Player/Mob
	hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	for hit in hits:
		# Reduce Shield -- if player is not invinsible
		if not player.invincible:
			player.shield -= hit.damage_points
		# Reduce lives if less than 0
		if player.shield <= 0:
			# Move player off screen for some time
			player.hide()
			
			player.lives -= 1
			player.shield = 100 if player.lives > 0 else 0
			Explosion("p", hit, all_sprites)
			player_expl_snd.play()

		death_expl = Explosion("m", hit, all_sprites)
		random.choice(expl_sounds).play()	



	# Collect Power_ups
	hits = pygame.sprite.spritecollide(player, power_ups_group, True)
	for hit in hits:
		if hit.pow_type == "shield":
			player.shield += random.randint(10, 35)
			if player.shield > 100:
				player.shield = 100
			power_ups_snds[1].play()

		elif hit.pow_type == "bolt":
			player.use_bolt()
			power_ups_snds[0].play()

		elif hit.pow_type == "star":
			player.use_star()
			power_ups_snds[2].play()

	# Make sure mobs are always == mob_count
	if len(mobs) < mob_count:
		create_mob()

	hit_points_animator(mobs_and_mobsDeathTime)

	# check for new best scores	
	if score > score_data["best_score"]:
		score_data["best_score"] = score

	if player.lives <= 0 and not death_expl.alive():
		splash_screen = True


	pygame.display.flip()

pygame.quit()
