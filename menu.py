import arcade
import button as bt
import sys


class Introduction:
    def __init__(self, w, h):
        self.width = w
        self.heigth = h
        self.status = True
        self.background = arcade.load_texture("images/background.jpg")
        self.button_list = [bt.Button("Start", self.width // 2, self.heigth // 2 + 30, self.act_start),
                            bt.Button("Exit", self.width // 2, self.heigth // 2 - 20, self.act_exit)]

    def draw(self):
        arcade.draw_texture_rectangle(self.width // 2, self.heigth // 2,
                                      self.width, self.heigth, self.background)
        for button in self.button_list:
            button.draw()
        return self.status

    def check_release_buttons(self):
        return bt.check_mouse_release_for_buttons(self.button_list)

    def check_press_buttons(self, pos_x, pos_y):
        return bt.check_mouse_press_for_buttons(pos_x, pos_y, self.button_list)

    def act_start(self):
        self.status = False

    def act_exit(self):
        sys.exit(0)