"""
Main Script
"""
from controller import *

pygame.display.set_caption(GAME_NAME, GAME_NAME)

pygame.mixer.init()


# TODO pygame FPS counter

controller = Controller()
clock = pygame.time.Clock()

running = True

while running:

    clock.tick_busy_loop(120)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == BLOWUP:
            controller.game.death()
        elif event.type == RESET:
            if len(controller.game.particles) > 0:
                pygame.event.post(RESET_EVENT)
            else:
                controller.game.reset()
        elif event.type == BLEND:
            if event.tile.color_counter < COLOR_BLEND_STEPS:
                colors = event.colors
                event.tile.absorb_bullet(colors)
                ev = pygame.event.Event(BLEND, {'tile': event.tile, 'colors': colors})
                pygame.event.post(ev)
            else:
                controller.game.shoot_enemy_bullet(event.tile)
        elif event.type == PLAY_GAME_MUSIC:
            pygame.mixer.music.load('./sounds/music.wav')
            pygame.mixer.music.play(-1)
        elif event.type == JOYBUTTONDOWN:
            print(event.button)
        elif event.type == JOYBUTTONUP:
            print(event.button)
        elif event.type == VIDEORESIZE:
            print(event)
        elif event.type == VIDEOEXPOSE:
            print(event)


    if controller.mode == MODE_GAME:
        # Get input
        pressed = pygame.key.get_pressed()
        controller.get_joystick_pressed()

        # Game logic
        if controller.game.get_physics_mode() == 'Horizontal':
            if not controller.game.player_on_floor:
                controller.game.on_floor_sound_guard = True

            controller.game.is_on_floor()

            if controller.game.player_on_floor and controller.game.on_floor_sound_guard:
                pygame.mixer.Sound.play(FALL_SOUND)
                controller.game.on_floor_sound_guard = False

        controller.update_game()

        if not controller.game.dropping_down and not controller.game.falling_up:
            if controller.game.get_physics_mode() == 'Horizontal':
                controller.game.gravity_check()
            controller.game.vertical_collision_check()
            controller.game.scroll_master_control()
            controller.game.horizontal_collision_check()
        elif controller.game.dropping_down:
            controller.game.destroy_down_bridge()
        elif controller.game.falling_up:
            controller.game.destroy_up_bridge()

        # Draw screen
        controller.game.player.morph_update()
        controller.game.bullets.update()
        controller.game.bullet_collision()
        controller.game.particles.update()
        controller.game.backgrounds.update(controller.game.speed, controller.game.scroll_direction)
        controller.game.stars.update(controller.game.speed, controller.game.scroll_direction)
        controller.game.calculate_star_parameters()
        controller.game.flash_objects()
        controller.game.render_screen()

    elif controller.mode == MODE_EDITOR:
        controller.get_joystick_pressed()
        controller.update_editor()
        controller.editor.flash_editor_cursors()
        controller.editor.render_screen()

    elif controller.mode == MODE_MENU:
        controller.get_joystick_pressed()
        controller.update_menu()
        controller.menu.flash_text_buttons()
        controller.menu.all_stars.update(1, 'Right')
        controller.menu.update_stars_and_moon()
        controller.menu.render_screen()

    else:
        assert False

    pygame.display.flip()

pygame.quit()
