"""
Jank Flappy Birb - Buttons (refer to main.py for full header)

Author: Adam Long

License: No license, freedom of use in commerical or non-commerical contexts. I do ask
that you contact me via email (adam.jacob.long@gmail.com) if you plan on using my work
within your own project.
"""

import pygame
from pygame.locals import *
import sys
from src.data import Color_Data

class Clickable_Button:
    pygame.font.init()

    def __init__(self, text, top_left_x, top_left_y, width, height):
        """
        __init__: A constructor defining a button.
        :param text: Text to be centered within the button.
        :param top_left_x: The top-left pixel on the x-plane.
        :param top_left_y: The top-left pixel on the y-plane.
        :param width: The width of the button in pixels.
        :param height: The height of the button in pixels.
        """
        self.text = text
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.width = width
        self.height = height

    def get_text(self):
        """
        get_text: Returns the text of button
        :return: String.
        """
        return self.text

    def set_text(self, text):
        """
        set_text: Sets new button text. *ensure to reblit button.
        :param text: String. Text to assign to button.
        :return: N/A
        """
        self.text = text

    def build_button(self, screen, RGB_color):
        """
        build_button: Builds a button and places it on the display (screen).
        :param screen: A pygame display object to push the button unto.
        :param RGB_color: A RGB formatted color, use Color_Data.py.
        :return: N/A
        """
        font = pygame.font.Font("assets/Fonts/FlappyBirdy.ttf", 50)
        text_object = font.render(self.text, True, Color_Data.BLACK)

        rect_object = pygame.draw.rect(screen, RGB_color, (self.top_left_x, self.top_left_y, self.width, self.height))
        text_coords = text_object.get_rect(center=(rect_object.centerx, rect_object.centery))
        #'center=' is not recognized by my IDE for some reason?
        screen.blit(text_object, text_coords)

    def check_button(self, event):
        """
        check_button: Checks the button for a click.
        :param event: A pygame event object.
        :return: Boolean. If clicked - True. If not clicked - False.
        """
        top_right = self.top_left_x + self.width
        bot_left = self.top_left_y + self.height

        if event.type == MOUSEBUTTONDOWN:
            if (self.top_left_x <= pygame.mouse.get_pos()[0] <= top_right) and \
                    (self.top_left_y <= pygame.mouse.get_pos()[1] <= bot_left):
                return True #clicked
            else:
                return False #not clicked
