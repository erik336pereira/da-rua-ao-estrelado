extends Node2D

const VIEW := Vector2(1280, 720)
const LEVEL_LENGTH := 5350.0
const FLOOR_Y := 608.0
const PLAYER_SPEED := 355.0
const GRAVITY := 1720.0
const JUMP_SPEED := -690.0
const SLIDE_MOVE_DURATION := 0.46
const SLIDE_ANIMATION_DURATION := 0.74
const SLIDE_SPEED := 465.0
const KICK_ANIMATION_DURATION := 0.42
const HEADBUTT_ANIMATION_DURATION := 0.38
const MAX_LIVES := 5
const MAX_BALLS := 10

const CREAM := Color("fff1c6")
const INK := Color("102039")
const NAVY := Color("152c50")
const BLUE := Color("198bd1")
const GOLD := Color("ffd45a")
const RED := Color("e94a55")
const GREEN := Color("55c987")
const SKY := Color("82d9ec")
const PIXEL_FONT := {
	"A":["01110","10001","10001","11111","10001","10001","10001"],"B":["11110","10001","10001","11110","10001","10001","11110"],
	"C":["01111","10000","10000","10000","10000","10000","01111"],"D":["11110","10001","10001","10001","10001","10001","11110"],
	"E":["11111","10000","10000","11110","10000","10000","11111"],"F":["11111","10000","10000","11110","10000","10000","10000"],
	"G":["01111","10000","10000","10111","10001","10001","01111"],"H":["10001","10001","10001","11111","10001","10001","10001"],
	"I":["11111","00100","00100","00100","00100","00100","11111"],"J":["00111","00010","00010","00010","10010","10010","01100"],
	"K":["10001","10010","10100","11000","10100","10010","10001"],"L":["10000","10000","10000","10000","10000","10000","11111"],
	"M":["10001","11011","10101","10101","10001","10001","10001"],"N":["10001","11001","10101","10011","10001","10001","10001"],
	"O":["01110","10001","10001","10001","10001","10001","01110"],"P":["11110","10001","10001","11110","10000","10000","10000"],
	"Q":["01110","10001","10001","10001","10101","10010","01101"],"R":["11110","10001","10001","11110","10100","10010","10001"],
	"S":["01111","10000","10000","01110","00001","00001","11110"],"T":["11111","00100","00100","00100","00100","00100","00100"],
	"U":["10001","10001","10001","10001","10001","10001","01110"],"V":["10001","10001","10001","10001","10001","01010","00100"],
	"W":["10001","10001","10001","10101","10101","10101","01010"],"X":["10001","10001","01010","00100","01010","10001","10001"],
	"Y":["10001","10001","01010","00100","00100","00100","00100"],"Z":["11111","00001","00010","00100","01000","10000","11111"],
	"0":["01110","10001","10011","10101","11001","10001","01110"],"1":["00100","01100","00100","00100","00100","00100","01110"],
	"2":["01110","10001","00001","00010","00100","01000","11111"],"3":["11110","00001","00001","01110","00001","00001","11110"],
	"4":["00010","00110","01010","10010","11111","00010","00010"],"5":["11111","10000","10000","11110","00001","00001","11110"],
	"6":["01110","10000","10000","11110","10001","10001","01110"],"7":["11111","00001","00010","00100","01000","01000","01000"],
	"8":["01110","10001","10001","01110","10001","10001","01110"],"9":["01110","10001","10001","01111","00001","00001","01110"],
	"!":["00100","00100","00100","00100","00100","00000","00100"],"?":["01110","10001","00001","00010","00100","00000","00100"],
	":":["00000","00100","00100","00000","00100","00100","00000"],".":["00000","00000","00000","00000","00000","00110","00110"],
	"/":["00001","00010","00010","00100","01000","01000","10000"],"-":["00000","00000","00000","11111","00000","00000","00000"]
}

var state := "menu"
var settings_return_state := "menu"
var master_volume := 1.0
var dragging_volume := false
var player := Vector2(135, FLOOR_Y)
var velocity := Vector2.ZERO
var facing := 1
var lives := 3
var balls := 5
var invulnerable := 0.0
var camera_x := 0.0
var attack_cooldown := 0.0
var attack_flash := 0.0
var slide_time := 0.0
var slide_anim_time := 0.0
var slide_facing := 1
var kick_anim_time := 0.0
var kick_facing := 1
var headbutt_anim_time := 0.0
var headbutt_facing := 1
var jump_pressed := false
var music_player: AudioStreamPlayer
var sfx_player: AudioStreamPlayer
var current_music := ""
var sprite_textures: Dictionary = {}
var animation_clock := 0.0
var move_axis := 0.0
var enemies: Array[Dictionary] = []
var projectiles: Array[Dictionary] = []
var pickups: Array[Dictionary] = []
var platforms: Array[Rect2] = []
var boss_defeated := false
var trophy_spawned := false
var elapsed := 0.0
var score := 0
@export var capture_mode := ""

func _ready() -> void:
	_setup_input()
	_setup_level()
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	for key in ["player", "referee", "goalie", "fan", "red_card_boss", "background", "ground_tile", "underground_tile", "platform_tile", "stadium"]:
		sprite_textures[key] = load("res://assets/sprites/%s.png" % key)
	music_player = AudioStreamPlayer.new()
	music_player.bus = "Master"
	add_child(music_player)
	sfx_player = AudioStreamPlayer.new()
	sfx_player.bus = "Master"
	add_child(sfx_player)
	play_music("menu")
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture="):
			capture_mode = arg.trim_prefix("--capture=")
	if capture_mode != "":
		if capture_mode != "title": start_game()
		invulnerable = 0.0
		if capture_mode == "pause": state = "paused"
		if capture_mode == "gameover":
			state = "game_over"
			play_music("gameover")
		if capture_mode == "victory":
			state = "victory"
			boss_defeated = true
			player = Vector2(LEVEL_LENGTH - 245.0, FLOOR_Y)
			camera_x = clampf(player.x - 400.0, 0.0, LEVEL_LENGTH - VIEW.x)
			play_music("victory")
		if capture_mode == "goalie":
			player = Vector2(1120.0, FLOOR_Y)
			camera_x = player.x - 400.0
			for enemy in enemies:
				if enemy.kind == "goalie": enemy.jump_timer = 0.0
		if capture_mode == "slide":
			player = Vector2(2020.0, FLOOR_Y)
			camera_x = player.x - 400.0
			facing = 1
			slide_time = SLIDE_MOVE_DURATION * 0.54
			slide_anim_time = SLIDE_ANIMATION_DURATION * 0.56
			slide_facing = facing
			attack_flash = 0.28
		if capture_mode == "boss":
			player = Vector2(4320.0, FLOOR_Y)
			camera_x = clampf(player.x - 400.0, 0.0, LEVEL_LENGTH - VIEW.x)
			for enemy in enemies:
				if enemy.kind == "red_card": enemy.timer = 0.0
		if capture_mode == "kick":
			player = Vector2(2020.0, FLOOR_Y)
			camera_x = player.x - 400.0
			facing = 1
			_shoot_ball()
			kick_anim_time = KICK_ANIMATION_DURATION * 0.48
		if capture_mode == "headbutt":
			player = Vector2(2020.0, FLOOR_Y)
			camera_x = player.x - 400.0
			facing = 1
			headbutt_facing = facing
			headbutt_anim_time = HEADBUTT_ANIMATION_DURATION * 0.52
		if capture_mode == "bonus":
			player = Vector2(4310.0, FLOOR_Y)
			camera_x = player.x - 400.0
		if capture_mode == "trophy":
			player = Vector2(4660.0, 510.0)
			camera_x = player.x - 400.0
			boss_defeated = true
			for index in range(enemies.size() - 1, -1, -1):
				if enemies[index].kind == "red_card": enemies.remove_at(index)
			_spawn_trophy()
		call_deferred("_capture_after_frame")

func _setup_input() -> void:
	_bind_key("move_left", [KEY_A, KEY_LEFT])
	_bind_key("move_right", [KEY_D, KEY_RIGHT])
	_bind_key("jump", [KEY_SPACE, KEY_W, KEY_UP])
	_bind_key("headbutt", [KEY_J])
	_bind_key("slide", [KEY_K])
	_bind_key("kick", [KEY_L])
	_bind_key("pause", [KEY_ESCAPE, KEY_P])
	_bind_key("start", [KEY_ENTER, KEY_SPACE])
	_bind_key("capture_screenshot", [KEY_F12])
	_bind_key("restart", [KEY_R])

func _bind_key(action: String, codes: Array) -> void:
	if not InputMap.has_action(action):
		InputMap.add_action(action)
	for code in codes:
		var event := InputEventKey.new()
		event.keycode = code
		if not InputMap.action_get_events(action).any(func(existing): return existing is InputEventKey and existing.keycode == code):
			InputMap.action_add_event(action, event)

func _setup_level() -> void:
	platforms = [
		Rect2(620, 522, 190, 22), Rect2(1010, 455, 188, 22),
		Rect2(1530, 520, 230, 22), Rect2(1980, 444, 170, 22),
		Rect2(2530, 510, 220, 22), Rect2(3030, 432, 200, 22),
		Rect2(3560, 500, 220, 22), Rect2(4115, 520, 210, 22),
		Rect2(4630, 510, 210, 22)
	]
	_spawn_level()

func _spawn_level() -> void:
	enemies = [
		_make_enemy("referee", 790, 2),
		_make_enemy("goalie", 1470, 2),
		_make_enemy("fan", 2180, 2),
		_make_enemy("referee", 2940, 2),
		_make_enemy("goalie", 3670, 3),
		_make_enemy("red_card", 4545, 7)
	]
	pickups = [
		{"kind":"ball", "pos":Vector2(1010, FLOOR_Y - 22), "taken":false},
		{"kind":"heart", "pos":Vector2(1740, FLOOR_Y - 22), "taken":false},
		{"kind":"ball", "pos":Vector2(2650, FLOOR_Y - 22), "taken":false},
		{"kind":"heart", "pos":Vector2(3370, FLOOR_Y - 22), "taken":false},
		{"kind":"ball", "pos":Vector2(4070, FLOOR_Y - 22), "taken":false},
		{"kind":"heart", "pos":Vector2(4310, 496), "taken":false}
	]
	projectiles.clear()
	boss_defeated = false
	trophy_spawned = false

func _spawn_trophy() -> void:
	if trophy_spawned: return
	trophy_spawned = true
	pickups.append({"kind":"trophy", "pos":Vector2(4735, 494), "taken":false})

func _make_enemy(kind: String, x: float, hp: int) -> Dictionary:
	return {"kind":kind, "pos":Vector2(x, FLOOR_Y), "hp":hp, "max_hp":hp,
		"dir":-1, "timer":0.8, "stun":0.0, "patrol":x, "phase":0.0,
		"vy":0.0, "jump_timer":0.9, "attack_time":0.0, "melee_timer":0.0, "slide_hit":false}

func start_game() -> void:
	state = "playing"
	player = Vector2(135, FLOOR_Y)
	velocity = Vector2.ZERO
	facing = 1
	lives = 3
	balls = 5
	score = 0
	invulnerable = 1.8
	attack_cooldown = 0.0
	attack_flash = 0.0
	slide_time = 0.0
	slide_anim_time = 0.0
	kick_anim_time = 0.0
	headbutt_anim_time = 0.0
	elapsed = 0.0
	_spawn_level()
	play_music("level")

func _process(delta: float) -> void:
	# Keep scene animation running through the victory state so the stadium celebration continues.
	animation_clock += delta
	if state == "playing":
		_update_game(delta)
	queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if state in ["settings", "controls"]:
		if event.is_action_pressed("pause") or event.is_action_pressed("start"):
			_close_settings()
			return
		if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
			if state == "settings" and Rect2(440,386,400,74).has_point(event.position):
				dragging_volume = event.pressed
				if event.pressed: _set_volume_from_mouse(event.position.x)
			elif event.pressed and Rect2(440,494,400,58).has_point(event.position): _close_settings()
			elif state == "controls" and event.pressed and Rect2(440,518,400,44).has_point(event.position): _close_settings()
		if state == "settings" and event is InputEventMouseMotion and dragging_volume and (event.button_mask & MOUSE_BUTTON_MASK_LEFT) != 0:
			_set_volume_from_mouse(event.position.x)
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_handle_menu_click(event.position)
		return
	if event.is_action_pressed("start"):
		if state in ["menu", "game_over", "victory"]:
			start_game()
			return
	if event.is_action_pressed("pause"):
		if state == "playing":
			state = "paused"
		elif state == "paused":
			state = "playing"
		return
	if event.is_action_pressed("capture_screenshot"):
		_capture_current_screen()
		return
	if event.is_action_pressed("restart") and state == "paused":
		start_game()
		return
	if state == "paused" and event.is_action_pressed("start"):
		state = "playing"
		return
	if state != "playing":
		return
	if event.is_action_pressed("jump"):
		jump_pressed = true
	if event.is_action_pressed("headbutt"):
		_melee_attack("headbutt")
	if event.is_action_pressed("slide"):
		_melee_attack("slide")
	if event.is_action_pressed("kick"):
		_shoot_ball()

func _handle_menu_click(position: Vector2) -> void:
	if state == "menu":
		if Rect2(80,443,270,62).has_point(position): start_game()
		elif Rect2(80,510,200,44).has_point(position): _open_settings()
		elif Rect2(292,510,200,44).has_point(position): _open_controls()
	elif state == "paused":
		if Rect2(322,440,190,52).has_point(position): state = "playing"
		elif Rect2(545,440,190,52).has_point(position): _open_settings()
		elif Rect2(768,440,190,52).has_point(position): _open_controls()
	elif state in ["game_over", "victory"]:
		if Rect2(360,440,250,56).has_point(position): start_game()
		elif Rect2(640,440,250,56).has_point(position): _return_to_menu()

func _open_settings() -> void:
	settings_return_state = state
	state = "settings"
	dragging_volume = false

func _open_controls() -> void:
	settings_return_state = state
	state = "controls"

func _close_settings() -> void:
	state = settings_return_state
	dragging_volume = false

func _set_volume_from_mouse(mouse_x: float) -> void:
	_set_master_volume(clampf((mouse_x - 470.0) / 340.0, 0.0, 1.0))

func _set_master_volume(value: float) -> void:
	master_volume = clampf(value, 0.0, 1.0)
	var master_bus := AudioServer.get_bus_index("Master")
	AudioServer.set_bus_mute(master_bus, master_volume <= 0.001)
	AudioServer.set_bus_volume_db(master_bus, linear_to_db(maxf(master_volume, 0.001)))

func _return_to_menu() -> void:
	state = "menu"
	player = Vector2(135, FLOOR_Y)
	velocity = Vector2.ZERO
	camera_x = 0.0
	play_music("menu")

func _update_game(delta: float) -> void:
	elapsed += delta
	invulnerable = maxf(0.0, invulnerable - delta)
	attack_cooldown = maxf(0.0, attack_cooldown - delta)
	attack_flash = maxf(0.0, attack_flash - delta)
	slide_time = maxf(0.0, slide_time - delta)
	slide_anim_time = maxf(0.0, slide_anim_time - delta)
	kick_anim_time = maxf(0.0, kick_anim_time - delta)
	headbutt_anim_time = maxf(0.0, headbutt_anim_time - delta)
	var axis := Input.get_axis("move_left", "move_right")
	move_axis = axis
	if axis != 0.0 and slide_anim_time <= 0.0 and kick_anim_time <= 0.0 and headbutt_anim_time <= 0.0:
		facing = int(signf(axis))
	if slide_time > 0.0:
		var slide_progress := 1.0 - clampf(slide_time / SLIDE_MOVE_DURATION, 0.0, 1.0)
		var eased_speed := 0.72 + 0.28 * sin(slide_progress * PI)
		velocity.x = float(slide_facing) * SLIDE_SPEED * eased_speed
	else:
		velocity.x = 0.0 if slide_anim_time > 0.0 else axis * PLAYER_SPEED
	if jump_pressed and slide_anim_time <= 0.0 and kick_anim_time <= 0.0 and is_on_floor_or_platform():
		velocity.y = JUMP_SPEED
		play_sfx("jump")
	jump_pressed = false
	var prev_y := player.y
	velocity.y = minf(velocity.y + GRAVITY * delta, 1000.0)
	player.x = clampf(player.x + velocity.x * delta, 24.0, LEVEL_LENGTH - 50.0)
	player.y += velocity.y * delta
	if player.y >= FLOOR_Y:
		player.y = FLOOR_Y
		velocity.y = 0.0
	for platform in platforms:
		if velocity.y >= 0.0 and prev_y <= platform.position.y and player.y >= platform.position.y and player.y <= platform.position.y + 18.0 and player.x + 19 > platform.position.x and player.x - 19 < platform.end.x:
			player.y = platform.position.y
			velocity.y = 0.0
	for pickup in pickups:
		if pickup.taken: continue
		if player.distance_to(pickup.pos) < 48.0:
			pickup.taken = true
			score += 1000 if pickup.kind == "trophy" else 100
			if pickup.kind == "ball": balls = mini(MAX_BALLS, balls + 3)
			elif pickup.kind == "heart": lives = mini(MAX_LIVES, lives + 1)
			play_sfx("pickup")
	_update_enemies(delta)
	_update_projectiles(delta)
	if player.x > LEVEL_LENGTH - 165.0 and boss_defeated:
		state = "victory"
		play_music("victory")
	if player.y > VIEW.y + 120:
		_take_damage(Vector2(player.x, FLOOR_Y))
	camera_x = clampf(player.x - 400.0, 0.0, LEVEL_LENGTH - VIEW.x)

func is_on_floor_or_platform() -> bool:
	if player.y >= FLOOR_Y - 0.5: return true
	for platform in platforms:
		if absf(player.y - platform.position.y) < 1.0 and player.x + 18 > platform.position.x and player.x - 18 < platform.end.x:
			return true
	return false

func _melee_attack(kind: String) -> void:
	if attack_cooldown > 0.0: return
	if kick_anim_time > 0.0: return
	if kind == "slide" and (slide_anim_time > 0.0 or not is_on_floor_or_platform()): return
	attack_cooldown = 0.48 if kind == "headbutt" else 0.88
	attack_flash = 0.19 if kind == "headbutt" else 0.32
	if kind == "slide":
		slide_time = SLIDE_MOVE_DURATION
		slide_anim_time = SLIDE_ANIMATION_DURATION
		slide_facing = facing
		velocity.x = float(slide_facing) * SLIDE_SPEED * 0.72
		for enemy in enemies:
			enemy.slide_hit = false
	else:
		headbutt_facing = facing
		headbutt_anim_time = HEADBUTT_ANIMATION_DURATION
	play_sfx("attack")
	if kind == "headbutt":
		for enemy in enemies:
			var dx: float = enemy.pos.x - player.x
			if absf(dx) < 72.0 and absf(enemy.pos.y - player.y) < 92 and signf(dx) == facing:
				_damage_enemy(enemy, 1)

func _shoot_ball() -> void:
	if balls <= 0 or attack_cooldown > 0.18 or slide_anim_time > 0.0 or kick_anim_time > 0.0: return
	balls -= 1
	attack_cooldown = 0.28
	kick_facing = facing
	kick_anim_time = KICK_ANIMATION_DURATION
	projectiles.append({"kind":"ball", "pos":player + Vector2(kick_facing * 34, -42), "vel":Vector2(kick_facing * 680, -75), "life":2.2})
	play_sfx("kick")

func _update_enemies(delta: float) -> void:
	for i in range(enemies.size() - 1, -1, -1):
		var enemy := enemies[i]
		enemy.timer = float(enemy.timer) - delta
		enemy.stun = maxf(0.0, float(enemy.stun) - delta)
		enemy.attack_time = maxf(0.0, float(enemy.attack_time) - delta)
		enemy.melee_timer = maxf(0.0, float(enemy.melee_timer) - delta)
		enemy.phase = float(enemy.phase) + delta
		var dx: float = player.x - enemy.pos.x
		var kind: String = enemy.kind
		if enemy.stun <= 0.0:
			if kind == "goalie":
				enemy.pos.x += clampf(dx, -1.0, 1.0) * (150.0 if absf(dx) > 115 else 52.0) * delta
				enemy.jump_timer = float(enemy.jump_timer) - delta
				if enemy.pos.y >= FLOOR_Y - 0.5 and absf(dx) < 620.0 and enemy.jump_timer <= 0.0:
					enemy.vy = -520.0
					enemy.jump_timer = 1.5
				enemy.vy = minf(float(enemy.vy) + GRAVITY * delta, 1000.0)
				enemy.pos.y += float(enemy.vy) * delta
				if enemy.pos.y >= FLOOR_Y:
					enemy.pos.y = FLOOR_Y
					enemy.vy = 0.0
			elif kind == "fan":
				enemy.pos.x += sin(float(enemy.phase) * 1.7) * 70.0 * delta
			else:
				if kind == "red_card" and absf(dx) < 145.0:
					if enemy.melee_timer <= 0.0:
						enemy.attack_time = 0.5
						enemy.melee_timer = 1.1
						if absf(player.y-enemy.pos.y) < 90.0:
							_take_damage(enemy.pos)
				else:
					var attack_range := 650.0 if kind == "red_card" else 470.0
					if absf(dx) < attack_range and enemy.timer <= 0.0:
						var direction := 1 if dx > 0 else -1
						var color_kind := "boss_card" if kind == "red_card" else "card"
						var speed := 390.0 if kind == "red_card" else 300.0
						var projectile_height := -108.0 if kind == "red_card" else -66.0
						projectiles.append({"kind":color_kind, "pos":enemy.pos + Vector2(0,projectile_height), "vel":Vector2(direction * speed, -40.0), "life":3.3})
						enemy.timer = 1.35 if kind == "red_card" else 2.3
						if kind == "red_card": enemy.attack_time = 0.52
		if kind == "referee" or kind == "fan":
			if enemy.pos.x < enemy.patrol - 90 or enemy.pos.x > enemy.patrol + 90:
				enemy.dir = -int(enemy.dir)
			enemy.pos.x += float(enemy.dir) * 48.0 * delta
		enemy.pos.x = clampf(enemy.pos.x, 35, LEVEL_LENGTH - 35)
		if slide_time > 0.0 and not enemy.slide_hit:
			var slide_dx: float = enemy.pos.x-player.x
			var slide_reach := 112.0 if kind == "red_card" else 76.0
			if absf(slide_dx) < slide_reach and absf(enemy.pos.y-player.y) < 96.0 and signf(slide_dx) == slide_facing:
				enemy.slide_hit = true
				_damage_enemy(enemy, 1)
		if enemy.hp <= 0:
			score += 500 if kind == "red_card" else 150
			if kind == "red_card":
				boss_defeated = true
				_spawn_trophy()
			enemies.remove_at(i)
			continue
		if absf(dx) < (108.0 if kind == "red_card" else 43.0) and absf(player.y-enemy.pos.y) < 76 and invulnerable <= 0.0:
			_take_damage(enemy.pos)

func _update_projectiles(delta: float) -> void:
	for i in range(projectiles.size() - 1, -1, -1):
		var shot := projectiles[i]
		shot.life = float(shot.life) - delta
		shot.pos += shot.vel * delta
		if shot.kind == "ball":
			for enemy in enemies:
				var target_offset := Vector2(0,-96) if enemy.kind == "red_card" else Vector2(0,-45)
				var hit_radius := 78.0 if enemy.kind == "red_card" else 43.0
				if shot.pos.distance_to(enemy.pos + target_offset) < hit_radius:
					_damage_enemy(enemy, 2)
					shot.life = 0.0
		else:
			if shot.pos.distance_to(player + Vector2(0,-40)) < 44.0 and invulnerable <= 0.0:
				_take_damage(shot.pos)
		if shot.life <= 0 or shot.pos.x < camera_x-160 or shot.pos.x > camera_x+VIEW.x+200:
			projectiles.remove_at(i)

func _damage_enemy(enemy: Dictionary, amount: int) -> void:
	enemy.hp = int(enemy.hp) - amount
	enemy.stun = 0.32
	enemy.pos.x += signf(enemy.pos.x - player.x) * 18.0
	play_sfx("hit")

func _take_damage(source: Vector2) -> void:
	if invulnerable > 0.0 or state != "playing": return
	lives -= 1
	invulnerable = 1.5
	velocity.y = -360.0
	velocity.x = -signf(player.x - source.x) * 250.0
	play_sfx("hurt")
	if lives <= 0:
		state = "game_over"
		play_music("gameover")

func play_music(track: String) -> void:
	if current_music == track and music_player.playing: return
	var path := "res://assets/audio/%s.wav" % track
	if not ResourceLoader.exists(path): return
	var stream := load(path) as AudioStreamWAV
	if stream:
		stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		music_player.stream = stream
		music_player.volume_db = -13.0
		music_player.play()
		current_music = track

func play_sfx(name: String) -> void:
	var path := "res://assets/audio/%s.wav" % name
	if not ResourceLoader.exists(path): return
	sfx_player.stream = load(path)
	sfx_player.volume_db = -5.0
	sfx_player.play()

func _draw() -> void:
	if state == "menu":
		_draw_menu()
		return
	_draw_world()
	_draw_hud()
	if state == "settings": _draw_settings()
	elif state == "controls": _draw_controls()
	elif state == "paused": _draw_pause_menu()
	elif state == "game_over": _draw_end_menu("FIM DE JOGO", "A torcida ainda acredita em você.", RED)
	elif state == "victory": _draw_end_menu("É CAMPEÃO!", "O estádio abriu os portões.", GREEN)

func _draw_menu() -> void:
	_draw_background(0.0)
	draw_rect(Rect2(0,0,1280,720), Color(0.02,0.05,0.12,0.28))
	_draw_pixel_text("DA RUA AO ESTRELADO",80,128,2,GOLD,Color("7a3240"))
	_draw_pixel_text("AS AVENTURAS",80,166,6,CREAM,Color("813e45"))
	_draw_pixel_text("DE UM JOGADOR",80,229,5,BLUE,Color("142f57"))
	draw_rect(Rect2(80,309,420,4), GOLD)
	draw_string(ThemeDB.fallback_font, Vector2(80,355), "Uma partida inteira separa você do estádio.", HORIZONTAL_ALIGNMENT_LEFT, -1, 20, CREAM)
	draw_string(ThemeDB.fallback_font, Vector2(80,387), "Drible os perigos, guarde a bola e enfrente o chefão.", HORIZONTAL_ALIGNMENT_LEFT, -1, 17, Color("c8d8e8"))
	draw_rect(Rect2(80,443,270,62), GOLD, true)
	_draw_pixel_text_center("ENTER / COMECAR",215,462,2,INK,Color("ffe89d"))
	_draw_menu_button(Rect2(80,510,200,44),"CONFIGURAÇÕES",BLUE)
	_draw_menu_button(Rect2(292,510,200,44),"CONTROLES",GOLD)
	draw_string(ThemeDB.fallback_font, Vector2(80,580), "JOGO DE PLATAFORMA • FUTEBOL • 1 JOGADOR", HORIZONTAL_ALIGNMENT_LEFT, -1, 13, CREAM)
	draw_string(ThemeDB.fallback_font, Vector2(80,657), "JOGO DE PLATAFORMA • FUTEBOL • 1 JOGADOR", HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color("a9bed1"))
	_draw_stadium(0.0, 0.0, true)
	_draw_ball(Vector2(900,475), 1.1)
	_draw_player(Vector2(1075,526), 1, false)

func _draw_world() -> void:
	_draw_background(camera_x)
	_draw_stadium(4450.0, camera_x)
	for platform in platforms:
		var sx := platform.position.x - camera_x
		if sx < -300 or sx > VIEW.x+300: continue
		var platform_texture: Texture2D = sprite_textures.get("platform_tile")
		if platform_texture:
			for tile_index in range(ceili(platform.size.x/32.0)):
				draw_texture_rect(platform_texture, Rect2(sx+tile_index*32,platform.position.y,32,12), false)
				draw_rect(Rect2(sx+tile_index*32,platform.position.y+12,32,10), Color("805136"))
		else:
			draw_rect(Rect2(sx,platform.position.y,platform.size.x,platform.size.y), Color("d5a65b"), true)
	_draw_ground(camera_x)
	_draw_stadium_apron(camera_x)
	for pickup in pickups:
		if pickup.taken: continue
		var p: Vector2 = pickup.pos - Vector2(camera_x,0)
		if p.x < -60 or p.x > VIEW.x+60: continue
		if pickup.kind == "ball":
			_draw_ball(p, 0.62)
		elif pickup.kind == "heart":
			_draw_pickup_heart(p)
		elif pickup.kind == "trophy":
			var trophy_bob := sin(animation_clock*3.5)*3.0
			_draw_trophy(p+Vector2(0,trophy_bob))
			draw_rect(Rect2(p.x-25,p.y-30+trophy_bob,3,3),CREAM)
			draw_rect(Rect2(p.x+22,p.y-20+trophy_bob,3,3),GOLD)
		else:
			_draw_pickup_heart(p)
	for enemy in enemies:
		var ep: Vector2 = enemy.pos - Vector2(camera_x,0)
		if ep.x > -100 and ep.x < VIEW.x+100: _draw_enemy(enemy, ep)
	for shot in projectiles:
		var sp: Vector2 = shot.pos - Vector2(camera_x,0)
		if shot.kind == "ball": _draw_ball(sp, 0.52)
		else:
			var card_color := RED if shot.kind == "boss_card" else GOLD
			draw_set_transform(sp, -0.35, Vector2.ONE)
			draw_rect(Rect2(-14,-18,28,36), card_color, true)
			draw_string(ThemeDB.fallback_font, Vector2(-5,6), "!", HORIZONTAL_ALIGNMENT_CENTER, 12, 18, INK)
			draw_set_transform(Vector2.ZERO)
	_draw_player(player - Vector2(camera_x,0), facing, invulnerable > 0 and int(elapsed*15)%2==0)
	if boss_defeated:
		_draw_stadium_celebration(camera_x)

func _draw_stadium_celebration(cam: float) -> void:
	var stadium_left := 4350.0 - cam
	if stadium_left < -900.0 or stadium_left > VIEW.x + 100.0:
		return
	var bounce := sin(animation_clock * 3.2) * 4.0
	var title_position := Vector2(stadium_left + 240.0, 222.0 + bounce)
	draw_string(ThemeDB.fallback_font, title_position + Vector2(2, 3), "PORTÕES ABERTOS!", HORIZONTAL_ALIGNMENT_CENTER, 360, 23, Color("17304c"))
	draw_string(ThemeDB.fallback_font, title_position, "PORTÕES ABERTOS!", HORIZONTAL_ALIGNMENT_CENTER, 360, 23, GOLD)
	# Two fixed launch points sit above the left and right sides of the stadium roof.
	_draw_firework(Vector2(stadium_left + 150.0, 248.0), fposmod(animation_clock * 0.72, 1.0), RED)
	_draw_firework(Vector2(stadium_left + 690.0, 248.0), fposmod(animation_clock * 0.72 + 0.5, 1.0), SKY)

func _draw_firework(center: Vector2, phase: float, color: Color) -> void:
	var radius := 5.0 + phase * 28.0
	var alpha := 1.0 - phase
	var burst_color := Color(color.r, color.g, color.b, alpha)
	var directions := [Vector2.UP, Vector2.DOWN, Vector2.LEFT, Vector2.RIGHT, Vector2(-0.7, -0.7), Vector2(0.7, -0.7), Vector2(-0.7, 0.7), Vector2(0.7, 0.7)]
	for direction in directions:
		var ray_end: Vector2 = center + direction * radius
		draw_line(center, ray_end, burst_color, 2.0)
		draw_rect(Rect2(ray_end - Vector2(2, 2), Vector2(4, 4)), Color(GOLD.r, GOLD.g, GOLD.b, alpha), true)
	draw_rect(Rect2(center - Vector2(3, 3), Vector2(6, 6)), Color(CREAM.r, CREAM.g, CREAM.b, alpha), true)

func _draw_background(cam: float) -> void:
	var texture: Texture2D = sprite_textures.get("background")
	if texture == null:
		draw_rect(Rect2(0,0,VIEW.x,VIEW.y), Color("39aadd"))
		return
	var shift := fposmod(cam * 0.14, VIEW.x)
	draw_texture_rect(texture, Rect2(-shift,0,VIEW.x,VIEW.y), false)
	draw_texture_rect(texture, Rect2(VIEW.x-shift,0,VIEW.x,VIEW.y), false)

func _draw_cloud(p: Vector2) -> void:
	draw_circle(p, 21, Color("eaffff"))
	draw_circle(p+Vector2(22,-8), 28, Color("eaffff"))
	draw_circle(p+Vector2(48,2), 19, Color("eaffff"))
	draw_rect(Rect2(p.x-2,p.y,54,18), Color("eaffff"), true)

func _draw_ground(cam: float) -> void:
	var grass_tile: Texture2D = sprite_textures.get("ground_tile")
	var dirt_tile: Texture2D = sprite_textures.get("underground_tile")
	if grass_tile == null or dirt_tile == null:
		draw_rect(Rect2(0,FLOOR_Y,VIEW.x,112), Color("9e633e"))
		return
	var offset := fposmod(cam, 32.0)
	for row in range(4):
		for column in range(42):
			var variant := (column+row*3)%4
			var tile := grass_tile if row == 0 else dirt_tile
			draw_texture_rect_region(tile,Rect2(column*32.0-offset,FLOOR_Y+row*32.0,32,32),Rect2(variant*32,0,32,32))
	var tuft_offset := fposmod(cam,16.0)
	var first_tuft := int(floor(cam/16.0))	
	var tuft_heights := [4,8,3,6,10,4,7,3,9,5,4,8]
	for index in range(82):
		var x := float(index*16)-tuft_offset
		var pattern := posmod(first_tuft+index,tuft_heights.size())
		var height := float(tuft_heights[pattern])
		draw_rect(Rect2(x,FLOOR_Y-height,3,height+3),Color("378950"))
		draw_rect(Rect2(x+1,FLOOR_Y-height,1,maxf(1.0,height-2)),Color("75d369" if pattern%3==0 else "59b85f"))
		if pattern==4 or pattern==9:
			draw_rect(Rect2(x+4,FLOOR_Y-4,2,2),Color("ffe58a"))

func _draw_stadium(world_x: float, cam: float, menu: bool = false) -> void:
	if menu:
		var stadium_texture: Texture2D = sprite_textures.get("stadium")
		if stadium_texture:
			draw_texture_rect(stadium_texture,Rect2(735,315,530,227),false)
		_draw_pixel_text_center("ESTADIO",1000,275,3,GOLD,Color("7a3240"))
		return
	var x := world_x - cam - 100.0
	if x < -900 or x > VIEW.x+250: return
	var stadium_texture: Texture2D = sprite_textures.get("stadium")
	if stadium_texture:
		draw_texture_rect(stadium_texture,Rect2(x,248,840,360),false)
	draw_rect(Rect2(x+322,286,196,34),NAVY,true)
	draw_rect(Rect2(x+322,286,196,3),GOLD,true)
	draw_rect(Rect2(x+322,317,196,3),GOLD,true)
	_draw_pixel_text_center("ESTADIO",x+420,293,2,GOLD,Color("7a3240"))

func _draw_stadium_apron(cam: float) -> void:
	var stadium_left := 4350.0 - cam
	var apron_left := stadium_left + 645.0
	var apron_right := stadium_left + 840.0
	if apron_right < -40.0 or apron_left > VIEW.x + 40.0: return
	var visible_left := maxf(-12.0, apron_left)
	var visible_right := minf(VIEW.x + 12.0, apron_right)
	draw_rect(Rect2(visible_left,FLOOR_Y-13.0,visible_right-visible_left,13.0),Color("43526a"),true)
	draw_rect(Rect2(visible_left,FLOOR_Y-13.0,visible_right-visible_left,3.0),Color("b8c9c5"),true)
	var seam := visible_left + 20.0
	while seam < visible_right:
		draw_rect(Rect2(seam,FLOOR_Y-9.0,3.0,5.0),Color("718193"),true)
		seam += 34.0

func _draw_player(p: Vector2, dir: int, blink: bool) -> void:
	if blink: return
	var sprite: Texture2D = sprite_textures.get("player")
	if sprite == null: return
	var frame := 0
	var is_sliding := slide_anim_time > 0.0
	var is_kicking := kick_anim_time > 0.0
	var is_headbutting := headbutt_anim_time > 0.0
	var kick_progress := 0.0
	var headbutt_progress := 0.0
	if is_sliding:
		var slide_progress := 1.0 - clampf(slide_anim_time / SLIDE_ANIMATION_DURATION, 0.0, 1.0)
		if slide_progress < 0.12: frame = 9
		elif slide_progress < 0.30: frame = 10
		elif slide_progress < 0.62: frame = 11
		elif slide_progress < 0.82: frame = 12
		else: frame = 13
	elif is_kicking:
		kick_progress = 1.0 - clampf(kick_anim_time / KICK_ANIMATION_DURATION, 0.0, 1.0)
		if kick_progress < 0.24: frame = 6
		elif kick_progress < 0.68: frame = 7
		else: frame = 8
	elif is_headbutting:
		headbutt_progress = 1.0 - clampf(headbutt_anim_time / HEADBUTT_ANIMATION_DURATION, 0.0, 1.0)
		if headbutt_progress < 0.24: frame = 14
		elif headbutt_progress < 0.68: frame = 15
		else: frame = 16
	elif absf(velocity.y) > 35.0:
		frame = 4
	elif attack_flash > 0.0:
		frame = 5
	elif absf(move_axis) > 0.1:
		frame = 1 + int(animation_clock*11.0)%3
	if is_sliding:
		_draw_ellipse(p+Vector2(0,-2),Vector2(43,7),Color(INK,0.30))
	else:
		draw_rect(Rect2(p.x-18,p.y-3,36,4),Color(INK,0.28))
	var sprite_dir := headbutt_facing if is_headbutting else dir
	draw_set_transform(p,0.0,Vector2(float(sprite_dir),1.0))
	draw_texture_rect_region(sprite,Rect2(-40,-80,80,80),Rect2(frame*32,0,32,32))
	draw_set_transform(Vector2.ZERO)
	if slide_time > 0.0:
		var dust_phase := int(animation_clock*18.0)
		for particle in range(4):
			var behind := 28.0+float((particle*17+dust_phase)%48)
			var dust_x := p.x-float(slide_facing)*behind
			var dust_y := p.y-4.0-float((particle+dust_phase)%3)*5.0
			draw_rect(Rect2(dust_x,dust_y,5,4),Color("c8a46a" if particle%2==0 else "f1d58b"))
		if attack_flash > 0.0:
			var impact_x := p.x+float(slide_facing)*37.0
			draw_rect(Rect2(impact_x,p.y-34,6,18),GOLD)
			draw_rect(Rect2(impact_x-5,p.y-27,16,6),CREAM)
	elif is_kicking and kick_progress >= 0.20 and kick_progress < 0.76:
		var kick_x := p.x+float(kick_facing)*42.0
		draw_rect(Rect2(kick_x,p.y-39,15,4),GOLD)
		draw_rect(Rect2(kick_x+float(kick_facing)*6.0,p.y-31,11,3),CREAM)
	elif is_headbutting and headbutt_progress >= 0.20 and headbutt_progress < 0.78:
		var head_direction := float(headbutt_facing)
		var impact_x := p.x+head_direction*57.0
		var impact_y := p.y-53.0
		if headbutt_progress < 0.40:
			draw_line(Vector2(p.x-head_direction*32.0,impact_y-9.0),Vector2(p.x-head_direction*22.0,impact_y-9.0),GOLD,3.0)
			draw_line(Vector2(p.x-head_direction*34.0,impact_y-2.0),Vector2(p.x-head_direction*25.0,impact_y-2.0),CREAM,2.0)
		else:
			draw_rect(Rect2(impact_x-3.0,impact_y-3.0,6.0,6.0),CREAM)
			draw_line(Vector2(impact_x-10.0,impact_y-9.0),Vector2(impact_x-5.0,impact_y-5.0),GOLD,3.0)
			draw_line(Vector2(impact_x+2.0,impact_y-12.0),Vector2(impact_x+2.0,impact_y-6.0),GOLD,3.0)
			draw_line(Vector2(impact_x+10.0,impact_y-5.0),Vector2(impact_x+5.0,impact_y-3.0),GOLD,3.0)
	elif attack_flash > 0.0:
		var ax := p.x+dir*47
		draw_rect(Rect2(ax-4,p.y-64,8,8),GOLD)
		draw_rect(Rect2(ax-10,p.y-58,7,7),CREAM)

func _draw_enemy(enemy: Dictionary, p: Vector2) -> void:
	var kind: String = enemy.kind
	var is_boss := kind == "red_card"
	var texture_key := "red_card_boss" if is_boss else kind
	var sprite: Texture2D = sprite_textures.get(texture_key)
	if sprite == null: return
	var frame_count := 4
	var frame := int(float(enemy.phase)*7.0)%frame_count
	if is_boss:
		if float(enemy.attack_time)>0.0:
			frame = 1 if float(enemy.attack_time)>0.25 else 2
		else:
			frame = 0 if int(float(enemy.phase)*3.0)%2==0 else 3
	var frame_w := 32 if is_boss else 24
	var frame_h := 40 if is_boss else 32
	var dest := Rect2(-64,-160,128,160) if is_boss else Rect2(-30,-80,60,80)
	if is_boss:
		_draw_ellipse(p+Vector2(0,-2),Vector2(68,11),Color(INK,0.34))
	else:
		draw_rect(Rect2(p.x-20,p.y-3,40,4),Color(INK,0.26))
	var enemy_facing := -1.0 if player.x < enemy.pos.x else 1.0
	draw_set_transform(p,0.0,Vector2(enemy_facing,1.0))
	draw_texture_rect_region(sprite,dest,Rect2(frame*frame_w,0,frame_w,frame_h))
	draw_set_transform(Vector2.ZERO)
	if is_boss or enemy.hp < enemy.max_hp:
		var bar_w := 200.0 if is_boss else 52.0
		var bar_y := p.y-(180.0 if is_boss else 94.0)
		draw_rect(Rect2(p.x-bar_w/2,bar_y,bar_w,8),Color("25334a"))
		draw_rect(Rect2(p.x-bar_w/2,bar_y,bar_w*float(enemy.hp)/float(enemy.max_hp),8),RED)
		if is_boss:
			draw_rect(Rect2(p.x-bar_w/2,bar_y-23,bar_w,18),Color(NAVY,0.96),true)
			draw_string(ThemeDB.fallback_font,Vector2(p.x-100,bar_y-8),"CARTAO VERMELHO",HORIZONTAL_ALIGNMENT_CENTER,200,13,CREAM)

func _draw_ellipse(center: Vector2, radii: Vector2, color: Color) -> void:
	var points := PackedVector2Array()
	for i in range(24):
		var a := TAU * float(i) / 24.0
		points.append(center+Vector2(cos(a)*radii.x,sin(a)*radii.y))
	draw_colored_polygon(points,color)

func _normalize_pixel_text(text: String) -> String:
	return text.to_upper().replace("Ã","A").replace("Á","A").replace("Â","A").replace("É","E").replace("Ê","E").replace("Í","I").replace("Ó","O").replace("Ô","O").replace("Õ","O").replace("Ú","U").replace("Ç","C").replace("•","/")

func _pixel_text_width(text: String, scale: int) -> float:
	return maxf(0.0,float(_normalize_pixel_text(text).length()*6-1)*scale)

func _draw_pixel_text_center(text: String, center_x: float, top: float, scale: int, fill: Color, shadow: Color) -> void:
	_draw_pixel_text(text,center_x-_pixel_text_width(text,scale)/2.0,top,scale,fill,shadow)

func _draw_pixel_text(text: String, left: float, top: float, scale: int, fill: Color, shadow: Color) -> void:
	var normalized := _normalize_pixel_text(text)
	for index in range(normalized.length()):
		var ch := normalized.substr(index,1)
		if ch == " ": continue
		var glyph: Array = PIXEL_FONT.get(ch,PIXEL_FONT["?"])
		for row in range(glyph.size()):
			for column in range(5):
				if glyph[row].substr(column,1) != "1": continue
				var x := left+(index*6+column)*scale
				var y := top+row*scale
				draw_rect(Rect2(x+scale,y+scale,scale,scale),shadow)
				draw_rect(Rect2(x,y,scale,scale),fill)

func _draw_ball(p: Vector2, scale: float) -> void:
	var unit := maxf(1.0,roundf(3.0*scale))
	draw_rect(Rect2(p.x-5*unit,p.y-3*unit,10*unit,6*unit),INK)
	draw_rect(Rect2(p.x-3*unit,p.y-5*unit,6*unit,10*unit),INK)
	draw_rect(Rect2(p.x-4*unit,p.y-3*unit,8*unit,6*unit),CREAM)
	draw_rect(Rect2(p.x-3*unit,p.y-4*unit,6*unit,8*unit),CREAM)
	draw_rect(Rect2(p.x-unit,p.y-2*unit,2*unit,2*unit),INK)
	draw_rect(Rect2(p.x+2*unit,p.y-unit,unit,2*unit),INK)
	draw_rect(Rect2(p.x-3*unit,p.y+unit,2*unit,unit),INK)

func _draw_hud() -> void:
	draw_rect(Rect2(24,20,1232,70),Color(INK,0.88),true)
	draw_string(ThemeDB.fallback_font,Vector2(48,51),"VIDAS",HORIZONTAL_ALIGNMENT_LEFT,-1,13,Color("a9bed1"))
	for i in range(MAX_LIVES):
		var c := RED if i < lives else Color("617087")
		_draw_heart(Vector2(65+i*31,69),c)
	draw_string(ThemeDB.fallback_font,Vector2(250,51),"BOLAS",HORIZONTAL_ALIGNMENT_LEFT,-1,13,Color("a9bed1"))
	for i in range(mini(balls,6)):
		_draw_ball(Vector2(325+i*30,65),0.62)
	if balls > 6:
		draw_string(ThemeDB.fallback_font,Vector2(510,70),"+%d" % (balls-6),HORIZONTAL_ALIGNMENT_LEFT,-1,13,CREAM)
	var progress := clampf(player.x/(LEVEL_LENGTH-160.0),0.0,1.0)
	draw_string(ThemeDB.fallback_font,Vector2(620,51),"CAMINHO AO ESTÁDIO",HORIZONTAL_ALIGNMENT_CENTER,200,12,Color("a9bed1"))
	draw_rect(Rect2(770,57,330,10),Color("51627c"),true)
	draw_rect(Rect2(770,57,330*progress,10),GOLD,true)
	draw_circle(Vector2(770+330*progress,62),8,CREAM)
	draw_string(ThemeDB.fallback_font,Vector2(1110,47),"PONTOS",HORIZONTAL_ALIGNMENT_RIGHT,100,11,Color("a9bed1"))
	draw_string(ThemeDB.fallback_font,Vector2(1110,72),"%06d" % score,HORIZONTAL_ALIGNMENT_RIGHT,100,18,GOLD)
	if not boss_defeated and player.x > 3980:
		draw_string(ThemeDB.fallback_font,Vector2(420,121),"CHEFÃO: CARTÃO VERMELHO",HORIZONTAL_ALIGNMENT_CENTER,440,15,GOLD)

func _draw_trophy(p: Vector2) -> void:
	var outline := Color("80501d")
	var gold := Color("ffd34f")
	var highlight := Color("fff2a0")
	# Pixel handles sit behind the cup and stay attached to its rim.
	draw_rect(Rect2(p.x-20,p.y-17,8,5),outline,true)
	draw_rect(Rect2(p.x-20,p.y-12,5,8),outline,true)
	draw_rect(Rect2(p.x-17,p.y-15,7,3),gold,true)
	draw_rect(Rect2(p.x-17,p.y-12,3,6),gold,true)
	draw_rect(Rect2(p.x+12,p.y-17,8,5),outline,true)
	draw_rect(Rect2(p.x+15,p.y-12,5,8),outline,true)
	draw_rect(Rect2(p.x+10,p.y-15,7,3),gold,true)
	draw_rect(Rect2(p.x+14,p.y-12,3,6),gold,true)
	var cup_outline := PackedVector2Array([
		p+Vector2(-13,-20),p+Vector2(13,-20),p+Vector2(12,-9),p+Vector2(8,-2),
		p+Vector2(4,2),p+Vector2(4,8),p+Vector2(-4,8),p+Vector2(-4,2),
		p+Vector2(-8,-2),p+Vector2(-12,-9)
	])
	draw_colored_polygon(cup_outline,outline)
	var cup_fill := PackedVector2Array([
		p+Vector2(-10,-17),p+Vector2(10,-17),p+Vector2(9,-10),p+Vector2(6,-5),
		p+Vector2(-6,-5),p+Vector2(-9,-10)
	])
	draw_colored_polygon(cup_fill,gold)
	draw_rect(Rect2(p.x-8,p.y-15,6,2),highlight,true)
	draw_rect(Rect2(p.x-2,p.y-11,3,5),Color("e8a92a"),true)
	draw_rect(Rect2(p.x-3,p.y+6,6,6),outline,true)
	draw_rect(Rect2(p.x-2,p.y+6,4,5),gold,true)
	draw_rect(Rect2(p.x-11,p.y+10,22,6),outline,true)
	draw_rect(Rect2(p.x-9,p.y+11,18,3),gold,true)
	draw_rect(Rect2(p.x-7,p.y+11,7,1),highlight,true)

func _draw_pickup_heart(p: Vector2) -> void:
	var pulse := 1.0 + sin(animation_clock*4.0)*0.035
	_draw_heart(p+Vector2(0,2),Color("8c203c"),6.0*pulse)
	_draw_heart(p,RED,5.0*pulse)
	draw_rect(Rect2(p.x-12,p.y-12,5,3),Color("ffb7bd"),true)

func _draw_heart(p: Vector2, color: Color, unit: float = 3.0) -> void:
	var pixels := ["0110110","1111111","1111111","0111110","0011100","0001000"]
	for row in range(pixels.size()):
		for column in range(7):
			if pixels[row].substr(column,1) == "1":
				draw_rect(Rect2(p.x-3.5*unit+column*unit,p.y-3.0*unit+row*unit,unit,unit),color)

func _draw_modal(title: String, subtitle: String, accent: Color) -> void:
	draw_rect(Rect2(0,0,VIEW.x,VIEW.y),Color("061126",0.74))
	draw_rect(Rect2(300,223,680,277),Color("13294b"),true)
	draw_rect(Rect2(300,223,680,7),accent,true)
	var pixel_title := title.replace("É CAMPEÃO!","CAMPEAO!")
	_draw_pixel_text_center(pixel_title,640,278,5,accent,Color("7a2b3b"))
	draw_string(ThemeDB.fallback_font,Vector2(340,374),subtitle,HORIZONTAL_ALIGNMENT_CENTER,600,17,CREAM)
	draw_rect(Rect2(486,417,308,53),accent,true)
	_draw_pixel_text_center("ENTER / CONTINUAR",640,431,2,INK,Color("ffe89d"))

func _draw_pause_menu() -> void:
	draw_rect(Rect2(0,0,VIEW.x,VIEW.y),Color("061126",0.74))
	draw_rect(Rect2(300,205,680,310),Color("13294b"),true)
	draw_rect(Rect2(300,205,680,7),GOLD,true)
	_draw_pixel_text_center("PAUSA",640,248,5,GOLD,Color("7a2b3b"))
	draw_string(ThemeDB.fallback_font,Vector2(340,348),"ESC / P retoma • R reinicia",HORIZONTAL_ALIGNMENT_CENTER,600,17,CREAM)
	_draw_menu_button(Rect2(322,440,190,52),"CONTINUAR",GOLD)
	_draw_menu_button(Rect2(545,440,190,52),"CONFIG",BLUE)
	_draw_menu_button(Rect2(768,440,190,52),"CONTROLES",BLUE)

func _draw_end_menu(title: String, subtitle: String, accent: Color) -> void:
	draw_rect(Rect2(0,0,VIEW.x,VIEW.y),Color("061126",0.74))
	draw_rect(Rect2(300,205,680,310),Color("13294b"),true)
	draw_rect(Rect2(300,205,680,7),accent,true)
	var pixel_title := title.replace("É CAMPEÃO!","CAMPEAO!")
	_draw_pixel_text_center(pixel_title,640,248,5,accent,Color("7a2b3b"))
	draw_string(ThemeDB.fallback_font,Vector2(340,348),subtitle,HORIZONTAL_ALIGNMENT_CENTER,600,17,CREAM)
	_draw_menu_button(Rect2(360,440,250,56),"NOVO JOGO",accent)
	_draw_menu_button(Rect2(640,440,250,56),"MENU PRINCIPAL",BLUE)

func _draw_settings() -> void:
	draw_rect(Rect2(0,0,VIEW.x,VIEW.y),Color("061126",0.78))
	draw_rect(Rect2(300,205,680,370),Color("13294b"),true)
	draw_rect(Rect2(300,205,680,7),GOLD,true)
	_draw_pixel_text_center("CONFIGURACOES",640,246,4,GOLD,Color("7a2b3b"))
	draw_string(ThemeDB.fallback_font,Vector2(340,350),"VOLUME GERAL",HORIZONTAL_ALIGNMENT_CENTER,600,18,CREAM)
	draw_rect(Rect2(460,400,360,58),Color("1b3d64"),true)
	draw_rect(Rect2(470,425,340,12),Color("0b1c36"),true)
	draw_rect(Rect2(470,425,340*master_volume,12),BLUE,true)
	var knob_x := 470.0+340.0*master_volume
	draw_circle(Vector2(knob_x,431),14,GOLD)
	draw_circle(Vector2(knob_x,431),7,CREAM)
	draw_string(ThemeDB.fallback_font,Vector2(470,458),"0%",HORIZONTAL_ALIGNMENT_LEFT,-1,14,CREAM)
	draw_string(ThemeDB.fallback_font,Vector2(810,458),"100%",HORIZONTAL_ALIGNMENT_RIGHT,-1,14,CREAM)
	draw_string(ThemeDB.fallback_font,Vector2(470,482),"Volume: %d%%" % roundi(master_volume*100.0),HORIZONTAL_ALIGNMENT_CENTER,340,15,Color("c8d8e8"))
	_draw_menu_button(Rect2(440,494,400,58),"VOLTAR",GOLD)

func _draw_controls() -> void:
	draw_rect(Rect2(0,0,VIEW.x,VIEW.y),Color("061126",0.78))
	draw_rect(Rect2(300,145,680,430),Color("13294b"),true)
	draw_rect(Rect2(300,145,680,7),GOLD,true)
	_draw_pixel_text_center("CONTROLES",640,184,4,GOLD,Color("7a2b3b"))
	var rows := [["MOVER","A / D ou setas"],["PULAR","Espaço / W / ↑"],["CABEÇADA","J"],["CARRINHO","K"],["CHUTAR BOLA","L"],["PAUSAR","P / Esc"],["INICIAR / VOLTAR","Enter"],["REINICIAR NA PAUSA","R"]]
	for index in range(rows.size()):
		var y := 252.0+index*34.0
		if index%2==0: draw_rect(Rect2(370,y-22,540,30),Color("1b3d64"),true)
		draw_string(ThemeDB.fallback_font,Vector2(390,y),rows[index][0],HORIZONTAL_ALIGNMENT_LEFT,300,16,CREAM)
		draw_string(ThemeDB.fallback_font,Vector2(670,y),rows[index][1],HORIZONTAL_ALIGNMENT_RIGHT,220,16,GOLD)
	_draw_menu_button(Rect2(440,518,400,44),"VOLTAR",GOLD)

func _draw_menu_button(rect: Rect2, label: String, accent: Color) -> void:
	draw_rect(rect,Color("1b3d64"),true)
	draw_rect(Rect2(rect.position.x,rect.position.y,rect.size.x,4),accent,true)
	draw_rect(Rect2(rect.position.x,rect.end.y-3,rect.size.x,3),Color("0b1c36"),true)
	draw_string(ThemeDB.fallback_font,Vector2(rect.position.x+12,rect.position.y+rect.size.y*0.62),label,HORIZONTAL_ALIGNMENT_CENTER,rect.size.x-24,16,CREAM)

func _capture_after_frame() -> void:
	var frames_to_wait := 14 if capture_mode == "goalie" else 2
	for _frame in range(frames_to_wait):
		await get_tree().process_frame
	if capture_mode != "":
		var image := get_viewport().get_texture().get_image()
		var capture_dir := ProjectSettings.globalize_path("res://docs/screenshots")
		DirAccess.make_dir_recursive_absolute(capture_dir)
		var out_path := capture_dir.path_join("%s.png" % capture_mode)
		image.save_png(out_path)
		print("CAPTURE_SAVED=", out_path)
		get_tree().quit()

func _capture_current_screen() -> void:
	var image := get_viewport().get_texture().get_image()
	if image == null: return
	var capture_dir := ProjectSettings.globalize_path("res://docs/screenshots")
	DirAccess.make_dir_recursive_absolute(capture_dir)
	var filename := "gameplay.png"
	match state:
		"menu": filename = "title.png"
		"paused": filename = "pause.png"
		"game_over": filename = "gameover.png"
		"victory": filename = "victory.png"
	var result := image.save_png(capture_dir.path_join(filename))
	if result == OK: print("Screenshot saved: ", filename)
