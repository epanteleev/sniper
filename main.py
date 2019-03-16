import arcade
import os
import sys

import menu

SPRITE_SCALING = 1

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Isometric Example"

VIEWPORT_MARGIN = 200
MOVEMENT_SPEED = 5


def read_sprite_list(grid, sprite_list):
    for row in grid:
        for grid_location in row:
            if grid_location.tile is not None:
                tile_sprite = arcade.Sprite(grid_location.tile.source, SPRITE_SCALING)
                tile_sprite.center_x = grid_location.center_x * SPRITE_SCALING
                tile_sprite.center_y = grid_location.center_y * SPRITE_SCALING
                # print(f"{grid_location.tile.source} -- ({tile_sprite.center_x:4}, {tile_sprite.center_y:4})")
                sprite_list.append(tile_sprite)



class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title,fullscreen=True)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.all_sprites_list = None

        # Set up the player
        self.player_sprite = None
        self.wall_list = None
        self.floor_list = None
        self.objects_list = None
        self.player_list = None
        self.view_bottom = 0
        self.view_left = 0
        self.my_map = None
        self.introduction = menu.Introduction(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.is_menu = True

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.objects_list = arcade.SpriteList()

        self.my_map = arcade.read_tiled_map('dungeon.tmx')

        # Set up the player
        self.player_sprite = arcade.Sprite("images/character.png", 0.4)
        px, py = arcade.isometric_grid_to_screen(self.my_map.width // 2,
                                                 self.my_map.height // 2,
                                                 self.my_map.width,
                                                 self.my_map.height,
                                                 self.my_map.tilewidth,
                                                 self.my_map.tileheight)

        self.player_sprite.center_x = px * SPRITE_SCALING
        self.player_sprite.center_y = py * SPRITE_SCALING
        self.player_list.append(self.player_sprite)

        read_sprite_list(self.my_map.layers["Floor"], self.floor_list)
        # read_sprite_list(self.my_map.layers["Walls"], self.wall_list)
        read_sprite_list(self.my_map.layers["Furniture"], self.wall_list)

        # Set the background color
        if self.my_map.backgroundcolor is None:
            arcade.set_background_color(arcade.color.BLACK)
        else:
            arcade.set_background_color(self.my_map.backgroundcolor)

        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        arcade.start_render()
        if self.is_menu and self.is_menu:
            self.introduction.draw()
            return

        # Draw all the sprites.
        self.floor_list.draw()
        self.player_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            sys.exit(0)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        self.player_sprite.update()

        if self.is_menu and self.is_menu:
            self.is_menu = self.introduction.draw()
            return

        changed = False

        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_mouse_press(self, x, y, button_, modifiers):
        if self.introduction.check_press_buttons(x, y):
            return

    def on_mouse_release(self, x, y, button_, key_modifiers):
        self.introduction.check_release_buttons()


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()