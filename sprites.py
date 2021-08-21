from settings import *
import random


class Player(pygame.sprite.Sprite):
	def __init__(self, all_sprites_group, bullets_group):
		super().__init__()
		self.image = pygame.transform.scale(player_sprite.convert(), (50, 38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10

		self.lives = 1

		self.speedx = 0
		self.speedy = 0

		self.all_sprites_group = all_sprites_group
		self.bullets_group = bullets_group

		self.press_time = 0
		self.shot_wait_time = 200 # For shooting


		self.shield = 100

		self.invincible = False
		self.invincible_start_time = 0
		self.invincible_keep_time = 3000

		self.visible = True
		self.hiding_time = 0
		self.hiding_length = 1500

		self.bullet_count = 1
		self.bolt_hit_time = 0
		self.bolt_keep_time = 5000

		self.star_active = False
		self.star_hit_time = 0
		self.star_keep_time = 5000

	def hide(self):
		self.visible = False
		self.hiding_time = pygame.time.get_ticks()
		self.rect.y = HEIGHT + 200

	def use_bolt(self):
		self.bullet_count = 2
		self.bolt_hit_time = pygame.time.get_ticks()

	def use_star(self):
		self.star_active = True
		self.star_hit_time = pygame.time.get_ticks()
		self.shot_wait_time = 100
		if self.lives < 2:
			self.shot_wait_time = 75

	def shoot(self):
		self.lazer_sound = random.choice([lazer_sounds[0], lazer_sounds[0], lazer_sounds[0], lazer_sounds[0], lazer_sounds[1]])
		self.lazer_sound.play()
		self.press_time = pygame.time.get_ticks()

		if self.bullet_count == 1:
			b = Bullet(self.rect.centerx, self.rect.top)
			self.all_sprites_group.add(b)
			self.bullets_group.add(b)

		elif self.bullet_count == 2:
			b = Bullet(self.rect.centerx - 15, self.rect.top)
			self.all_sprites_group.add(b)
			self.bullets_group.add(b)
			b = Bullet(self.rect.centerx + 15, self.rect.top)
			self.all_sprites_group.add(b)
			self.bullets_group.add(b)

	def update(self):
		now = pygame.time.get_ticks()
		if self.visible:
			now = pygame.time.get_ticks()

			self.speedx = 0
			self.speedy = 0
			keys = pygame.key.get_pressed()

			# Character Movement
			if keys[pygame.K_LEFT]:
				if self.rect.left > 0:
					self.speedx = -5
			if keys[pygame.K_RIGHT]:
				if self.rect.right < WIDTH:
					self.speedx = 5
			if keys[pygame.K_UP]:
				if self.rect.top > HEIGHT - 150:
					self.speedy = -5
			if keys[pygame.K_DOWN]:
				if self.rect.bottom < HEIGHT - 10:
					self.speedy = 5

			self.rect.x += self.speedx
			self.rect.y += self.speedy

			# Bullet Movement
			if keys[pygame.K_SPACE]:
				if now - self.press_time > self.shot_wait_time:
					self.shoot()
		else: # visible = False
			if now - self.hiding_time > self.hiding_length:
				self.visible = True
				self.invincible = True
				self.invincible_start_time = now
				self.rect.centerx = WIDTH / 2
				self.rect.bottom = HEIGHT - 10

		if now - self.invincible_start_time > self.invincible_keep_time:
			self.invincible = False

		if self.bullet_count != 1:
			if now - self.bolt_hit_time > self.bolt_keep_time:
				self.bullet_count = 1

		if self.star_active:
			if now - self.star_hit_time > self.star_keep_time:
				self.star_hit_time = now
				self.star_active = False
				self.shot_wait_time = 250

		if self.lives < 2 and not self.star_active:
			self.shot_wait_time = 100


class Mob(pygame.sprite.Sprite):
	def __init__(self, *groups):
		super().__init__(groups)
		self.image_orig = random.choice(meteor_sprites).convert()
		self.image = self.image_orig.copy()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		# mob.radius
		if self.rect.width > 100:
			self.radius = self.rect.width * 0.77 / 2
		elif self.rect.width < 60:
			self.radius = self.rect.width * 0.80 / 2
		elif self.rect.width < 100:
			self.radius = self.rect.width * 0.75 / 2

		# Mob hit points
		self.mob_strength = random.randint(6, 24)

		# pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
		self.rect.bottom = random.randint(-120, -50)
		self.rect.left = random.randint(0, WIDTH - self.rect.width)
		self.speedy = random.randint(1, 10)
		self.speedx = random.randint(-2, 2)

		self.rot_angle = 0
		self.rot_speed = random.randint(-8, 8)
		self.rot_wait_time = 50
		self.last_rotation_time = pygame.time.get_ticks()
		self.damage_points = self.radius * 2


	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_rotation_time > self.rot_wait_time:
			self.last_rotation_time = now
			self.rot_angle = (self.rot_angle + self.rot_speed) % 360
			old_center = self.rect.center
			self.image = pygame.transform.rotate(self.image_orig, self.rot_angle)
			self.image.set_colorkey(BLACK)
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()

		self.rect.y += self.speedy
		self.rect.x += self.speedx

		# Check borders
		if self.rect.top > HEIGHT +10 or self.rect.right < 0 \
				or self.rect.left > WIDTH:
				self.kill()

class ImmortalMob(pygame.sprite.Sprite):
	def __init__(self, *groups):
		super().__init__(groups)
		self.image_orig = random.choice(gray_meteor_sprites).convert()
		self.image = self.image_orig.copy()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		# mob.radius
		if self.rect.width > 100:
			self.radius = self.rect.width * 0.77 / 2
		elif self.rect.width < 60:
			self.radius = self.rect.width * 0.80 / 2
		elif self.rect.width < 100:
			self.radius = self.rect.width * 0.75 / 2

		# Mob hit points
		self.mob_strength = 150

		# pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
		self.rect.bottom = random.randint(-120, -50)
		self.rect.left = random.randint(0, WIDTH - self.rect.width)
		self.speedy = random.randint(2, 10)
		self.speedx = random.randint(-5, 5)

		self.rot_angle = 0
		self.rot_speed = random.randint(-8, 8)
		self.rot_wait_time = 50
		self.last_rotation_time = pygame.time.get_ticks()
		self.damage_points = self.radius * 3


	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_rotation_time > self.rot_wait_time:
			self.last_rotation_time = now
			self.rot_angle = (self.rot_angle + self.rot_speed) % 360
			old_center = self.rect.center
			self.image = pygame.transform.rotate(self.image_orig, self.rot_angle)
			self.image.set_colorkey(BLACK)
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()

		self.rect.y += self.speedy
		self.rect.x += self.speedx

		# Check borders
		if self.rect.top > HEIGHT + 10:
			self.kill()
		if self.rect.left < 0:
			self.speedx *= -1
			return
		if self.rect.right > WIDTH:
			self.speedx *= -1
			return


class Bullet(pygame.sprite.Sprite):
	def __init__(self, player_centerx, player_top):
		super().__init__()
		self.image = pygame.transform.scale(lazer.convert(), (8, 33))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = player_top
		self.rect.centerx = player_centerx
		self.speedy = -10


	def update(self):
		self.rect.y += self.speedy

		# Kill Bullet if out of top border
		if self.rect.bottom < -10:
			self.kill()


class Explosion(pygame.sprite.Sprite):
	def __init__(self, expl_type, obj, *groups):
		super().__init__(groups)
		self.obj_rect = obj.rect

		self.expl_size = int(obj.radius * 3 if obj.radius * 3 < 100 else 100)
		self.expl_lst = mob_expl_lst

		self.last_update = pygame.time.get_ticks()
		self.anim_wait = random.randint(25, 100)
		self.anim_speed = 1

		if expl_type == "p": # for player expl
			self.expl_size = 200
			self.expl_lst = player_expl_lst
		elif expl_type == "s": # for sparks
			self.expl_size = 40
			self.anim_wait = 60
			self.expl_lst = sparks


		self.frame = 0
		self.image = pygame.transform.scale(self.expl_lst[self.frame], (self.expl_size, self.expl_size))
		self.rect = self.image.get_rect(center=[self.obj_rect.centerx, self.obj_rect.centery])


	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.anim_wait:
			self.last_update = now
			self.frame += self.anim_speed
			self.image = pygame.transform.scale(self.expl_lst[self.frame], (self.expl_size, self.expl_size))
			self.rect = self.image.get_rect(center=[self.obj_rect.centerx, self.obj_rect.centery])

		if self.frame + self.anim_speed >= len(self.expl_lst):
			self.kill()


class PowerUp(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, *groups):
		super().__init__(groups)

		choice = random.choice([0, 1, 2])
		self.pow_type = "bolt" # Increases bullet count
		if choice == 1:
			self.pow_type = "shield"
		elif choice == 2:
			self.pow_type = "star" # increases bullet speed

		self.image = power_ups[choice]
		self.rect = self.image.get_rect(center=[pos_x, pos_y])

		self.speedy = random.randint(2, 8)

	def update(self):
		self.rect.y += self.speedy
