# BeWell
# made for Recess Hacks 3.0
# by Evan Gorman and Jason Li

import json
import pygame
import string
import sys
from pygame import gfxdraw
from roundrects import *

FADE_LENGTH = 20

class Text:
    def __init__(self, text, font, color):
        self.surface = font.render(text, True, color)
        self.width, self.height = font.size(text)

class Image:
    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()

def scale_surface_to_width(surface, new_width):
    width, height = surface.get_size()
    return pygame.transform.smoothscale(surface, (new_width, int(height / width * new_width)))

def scale_surface_to_height(surface, new_height):
    width, height = surface.get_size()
    return pygame.transform.smoothscale(surface, (int(width / height * new_height), new_height))

def home():
    fade_alpha = FADE_LENGTH
    fade_in = pygame.Surface((1280, 720))
    fade_in.fill((0, 0, 0))

    activities_alpha = 0
    tracking_alpha = 0

    overlay = pygame.Surface((640, 720), pygame.SRCALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                global fade_frame
                fade_frame = screen.copy()

                if activities_alpha == 10:
                    return "activities"
                elif tracking_alpha == 10:
                    return "tracking"

        if fade_alpha > 0:
            fade_alpha -= 1
        else:
            pos = pygame.mouse.get_pos()

            if pos[0] < 640:
                if activities_alpha < 10:
                    activities_alpha += 1

                if tracking_alpha > 0:
                    tracking_alpha -= 1
            else:
                if activities_alpha > 0:
                    activities_alpha -= 1

                if tracking_alpha < 10:
                    tracking_alpha += 1

        """
        left = 640 - (images["logo"].width + text["title"].width + 25) // 2
        top = 100 - images["logo"].height // 2
        screen.blit(images["logo"].surface, (left, top))
        screen.blit(text["title"].surface, (left + images["logo"].width + 25, top))
        """

        screen.blit(images["sudoku"].surface, (0, 0), (300, 0, 640, 720))
        screen.blit(images["running"].surface, (640, 0), (300, 0, 640, 720))

        overlay.fill((0, 0, 0, int(80 * (activities_alpha / 10))))
        screen.blit(overlay, (0, 0))
        overlay.fill((0, 0, 0, int(80 * (tracking_alpha / 10))))
        screen.blit(overlay, (640, 0))

        overlay.fill((0, 0, 0, 0))
        overlay.blit(text["activities"].surface, (80, 640 - text["activities"].height))
        overlay.set_alpha(activities_alpha / 10 * 255)
        screen.blit(overlay, (0, 0))

        overlay.fill((0, 0, 0, 0))
        overlay.blit(text["tracking"].surface, (560 - text["tracking"].width, 640 - text["tracking"].height))
        overlay.set_alpha(tracking_alpha / 10 * 255)
        screen.blit(overlay, (640, 0))

        overlay.set_alpha(255)

        fade_in.set_alpha(fade_alpha / FADE_LENGTH * 255)
        screen.blit(fade_in, (0, 0))

        pygame.display.flip()
        clock.tick(60)

def tracking():
    fade_alpha = FADE_LENGTH
    fade_in = pygame.Surface((1280, 720))
    fade_in.fill((0, 0, 0))

    goals_alpha = 0
    logging_alpha = 0
    data_alpha = 0
    reminders_alpha = 0
    back_size = 50

    overlay = pygame.Surface((640, 360), pygame.SRCALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                global fade_frame
                fade_frame = screen.copy()

                if goals_alpha == 10:
                    return "goals"
                elif logging_alpha == 10:
                    return "logging"
                elif data_alpha == 10:
                    return "data"
                elif reminders_alpha == 10:
                    return "reminders"
                elif back_size == 80:
                    return "home"

        if fade_alpha > 0:
            fade_alpha -= 1
        else:
            pos = pygame.mouse.get_pos()

            if pos[0] < 120 and 300 <= pos[1] <= 420:
                if goals_alpha > 0:
                    goals_alpha -= 1

                if logging_alpha > 0:
                    logging_alpha -= 1

                if data_alpha > 0:
                    data_alpha -= 1

                if reminders_alpha > 0:
                    reminders_alpha -= 1

                if back_size < 80:
                    back_size += 3
            else:
                if pos[0] < 640:
                    if pos[1] < 360:
                        if goals_alpha < 10:
                            goals_alpha += 1

                        if logging_alpha > 0:
                            logging_alpha -= 1

                        if data_alpha > 0:
                            data_alpha -= 1

                        if reminders_alpha > 0:
                            reminders_alpha -= 1
                    else:
                        if goals_alpha > 0:
                            goals_alpha -= 1

                        if logging_alpha > 0:
                            logging_alpha -= 1

                        if data_alpha < 10:
                            data_alpha += 1

                        if reminders_alpha > 0:
                            reminders_alpha -= 1
                else:
                    if pos[1] < 360:
                        if goals_alpha > 0:
                            goals_alpha -= 1

                        if logging_alpha < 10:
                            logging_alpha += 1

                        if data_alpha > 0:
                            data_alpha -= 1

                        if reminders_alpha > 0:
                            reminders_alpha -= 1
                    else:
                        if goals_alpha > 0:
                            goals_alpha -= 1

                        if logging_alpha > 0:
                            logging_alpha -= 1

                        if data_alpha > 0:
                            data_alpha -= 1

                        if reminders_alpha < 10:
                            reminders_alpha += 1

                if back_size > 50:
                    back_size -= 3

        screen.blit(images["checkboxes"].surface, (0, 0), (0, 0, 640, 360))
        screen.blit(images["calendar"].surface, (640, 0))
        screen.blit(images["graph"].surface, (0, 360))
        screen.blit(images["clock"].surface, (640, 360), (0, 50, 640, 360))

        overlay.fill((0, 0, 0, int(80 * (goals_alpha / 10))))
        screen.blit(overlay, (0, 0))
        overlay.fill((0, 0, 0, int(80 * (logging_alpha / 10))))
        screen.blit(overlay, (640, 0))
        overlay.fill((0, 0, 0, int(80 * (data_alpha / 10))))
        screen.blit(overlay, (0, 360))
        overlay.fill((0, 0, 0, int(80 * (reminders_alpha / 10))))
        screen.blit(overlay, (640, 360))

        overlay.fill((0, 0, 0, 0))
        overlay.blit(text["goals"].surface, (80, 80))
        overlay.set_alpha(goals_alpha / 10 * 255)
        screen.blit(overlay, (0, 0))

        overlay.fill((0, 0, 0, 0))
        overlay.blit(text["logging"].surface, (560 - text["logging"].width, 80))
        overlay.set_alpha(logging_alpha / 10 * 255)
        screen.blit(overlay, (640, 0))

        overlay.fill((0, 0, 0, 0))
        overlay.blit(text["data"].surface, (80, 280 - text["data"].height))
        overlay.set_alpha(data_alpha / 10 * 255)
        screen.blit(overlay, (0, 360))

        overlay.fill((0, 0, 0, 0))
        overlay.blit(text["reminders"].surface, (560 - text["reminders"].width, 280 - text["reminders"].height))
        overlay.set_alpha(reminders_alpha / 10 * 255)
        screen.blit(overlay, (640, 360))

        overlay.set_alpha(255)

        screen.blit(pygame.transform.smoothscale(images["back"].surface, (back_size, back_size)), (60 - back_size // 2, 360 - back_size // 2))

        fade_in.set_alpha(fade_alpha / FADE_LENGTH * 255)
        screen.blit(fade_in, (0, 0))

        pygame.display.flip()
        clock.tick(60)

def add_goal():
    fade_alpha = 20
    fade_in = pygame.Surface((1280, 720))
    fade_in.fill((0, 0, 0))

    activity_focused = False
    activity_contents = ""

    amount_number_focused = False
    amount_number_contents = ""

    amount_unit_focused = False
    amount_unit_contents = ""

    frequency_amount_focused = False
    frequency_amount_contents = ""

    frequency_every_focused = False
    frequency_every_contents = ""

    duration_focused = False
    duration_contents = ""

    while True:
        clicked = False
        wheel_down = False
        wheel_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked = True
            elif event.type == pygame.KEYDOWN:
                if activity_focused:
                    if event.key == pygame.K_BACKSPACE and activity_contents:
                        activity_contents = activity_contents[:-1]
                    elif len(activity_contents) < 8 and (event.unicode.isalpha() or event.unicode in string.digits + string.punctuation):
                        activity_contents += event.unicode
                elif amount_number_focused:
                    if event.key == pygame.K_BACKSPACE and amount_number_contents:
                        amount_number_contents = amount_number_contents[:-1]
                    elif len(amount_number_contents) < 3 and (event.unicode in "123456789" or (amount_number_contents and event.unicode in "0.")):
                        amount_number_contents += event.unicode
                elif amount_unit_focused:
                    if event.key == pygame.K_BACKSPACE and amount_unit_contents:
                        amount_unit_contents = amount_unit_contents[:-1]
                    elif len(amount_unit_contents) < 8 and (event.unicode.isalpha() or event.unicode in string.digits + string.punctuation):
                        amount_unit_contents += event.unicode
                elif frequency_amount_focused:
                    if event.key == pygame.K_BACKSPACE and frequency_amount_contents:
                        frequency_amount_contents = frequency_amount_contents[:-1]
                    elif len(frequency_amount_contents) < 3 and (event.unicode in "123456789" or (frequency_amount_contents and event.unicode == "0")):
                        frequency_amount_contents += event.unicode
                elif frequency_every_focused:
                    if event.key == pygame.K_BACKSPACE and frequency_every_contents:
                        frequency_every_contents = frequency_every_contents[:-1]
                    elif len(frequency_every_contents) < 3 and (event.unicode in "123456789" or (frequency_every_contents and event.unicode == "0")):
                        frequency_every_contents += event.unicode
                elif duration_focused:
                    if event.key == pygame.K_BACKSPACE and duration_contents:
                        duration_contents = duration_contents[:-1]
                    elif len(duration_contents) < 3 and (event.unicode in "123456789" or (duration_contents and event.unicode == "0")):
                        duration_contents += event.unicode

        if fade_alpha > 0:
            fade_alpha -= 1
        
        pos = pygame.mouse.get_pos()

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, colors["blue"], pygame.Rect(0, 0, 1280, 50))
        aa_round_rect(screen, pygame.Rect(640 - (text["add-goal"].width + 60) // 2, 0, text["add-goal"].width + 60, 100), colors["blue"], rad=15)
        screen.blit(text["add-goal"].surface, (640 - text["add-goal"].width // 2, 50 - text["add-goal"].height // 2))

        screen.blit(text["activity"].surface, (154 - text["activity"].width // 2, 150))
        screen.blit(text["amount"].surface, (410 - text["amount"].width // 2, 150))
        screen.blit(text["frequency"].surface, (666 - text["frequency"].width // 2, 150))
        screen.blit(text["duration"].surface, (922 - text["duration"].width // 2, 150))

        activity_text = Text(activity_contents, fonts["option"], colors["black"])
        box = (144 - activity_text.width // 2, 210, activity_text.width + 20, activity_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(activity_text.surface, (154 - activity_text.width // 2, 220))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                activity_focused = True
            else:
                activity_focused = False

        activity_exists = activity_contents
        if activity_contents and activity_contents not in data["activities"]:
            screen.blit(text["activity-warning"].surface, (154 - text["activity-warning"].width // 2, 275))
            activity_exists = False

        amount_number_text = Text(amount_number_contents, fonts["option"], colors["black"])
        amount_unit_text = Text(amount_unit_contents, fonts["option"], colors["black"])
        amount_width = amount_number_text.width + 50 + amount_unit_text.width
        
        box = (410 - amount_width // 2, 210, amount_number_text.width + 20, amount_number_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(amount_number_text.surface, (420 - amount_width // 2, 220))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                amount_number_focused = True
            else:
                amount_number_focused = False

        box = (440 - amount_width // 2 + amount_number_text.width, 210, amount_unit_text.width + 20, amount_unit_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(amount_unit_text.surface, (450 - amount_width // 2 + amount_number_text.width, 220))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                amount_unit_focused = True
            else:
                amount_unit_focused = False

        screen.blit(text["unit-format"].surface, (410 - text["unit-format"].width // 2, 275))

        if amount_unit_contents and (not activity_exists or (amount_unit_contents and amount_unit_contents not in data["activities"][activity_contents]["units"])):
            screen.blit(text["unit-warning"].surface, (410 - text["unit-warning"].width // 2, 300))

        frequency_amount_text = Text(frequency_amount_contents, fonts["option"], colors["black"])
        frequency_amount_width = frequency_amount_text.width + 30 + text["frequency-middle"].width
        box = (666 - frequency_amount_width // 2, 210, frequency_amount_text.width + 20, frequency_amount_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(frequency_amount_text.surface, (676 - frequency_amount_width // 2, 220))
        screen.blit(text["frequency-middle"].surface, (696 - frequency_amount_width // 2 + frequency_amount_text.width, 220))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                frequency_amount_focused = True
            else:
                frequency_amount_focused = False

        frequency_every_text = Text(frequency_every_contents, fonts["option"], colors["black"])
        box = (666 - frequency_amount_width // 2, 290, frequency_every_text.width + 20, frequency_every_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(frequency_every_text.surface, (676 - frequency_amount_width // 2, 300))
        screen.blit(text["days"].surface, (696 - frequency_amount_width // 2 + frequency_every_text.width, 300))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                frequency_every_focused = True
            else:
                frequency_every_focused = False

        duration_text = Text(duration_contents, fonts["option"], colors["black"])
        duration_width = duration_text.width + 30 + text["days"].width
        box = (922 - duration_width // 2, 210, duration_text.width + 20, duration_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(duration_text.surface, (932 - duration_width // 2, 220))
        screen.blit(text["days"].surface, (952 - duration_width // 2 + duration_text.width, 220))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                duration_focused = True
            else:
                duration_focused = False

        aa_round_rect(screen, pygame.Rect(1120 - text["add"].width, 201, text["add"].width + 60, 100), colors["blue"], rad=15)
        screen.blit(text["add"].surface, (1150 - text["add"].width, 251 - text["add"].height // 2))

        fade_in.set_alpha(fade_alpha / FADE_LENGTH * 255)
        screen.blit(fade_in, (0, 0))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("BeWell")
    clock = pygame.time.Clock()

    colors = {
        "white": pygame.Color("#ffffff"),
        "black": pygame.Color("#434343"),
        "gray": pygame.Color("#e6e6e6"),
        "blue": pygame.Color("#86c0cc")
    }

    fonts = {
        "title": pygame.font.Font("fonts/Nunito-Regular.ttf", 100),
        "label": pygame.font.Font("fonts/BebasNeue-Regular.ttf", 75),
        "label-small": pygame.font.Font("fonts/BebasNeue-Regular.ttf", 40),
        "option": pygame.font.Font("fonts/NotoSans-Regular.ttf", 25),
        "tiny": pygame.font.Font("fonts/NotoSans-Regular.ttf", 15)
    }

    text = {
        "title": Text("BeWell", fonts["title"], colors["white"]),
        "file-not-found": Text("Error: data.json not found.", fonts["label"], colors["white"]),
        "activities": Text("ACTIVITIES", fonts["label"], colors["white"]),
        "tracking": Text("GOAL TRACKING", fonts["label"], colors["white"]),
        "goals": Text("GOALS", fonts["label"], colors["white"]),
        "logging": Text("LOGGING", fonts["label"], colors["white"]),
        "data": Text("DATA", fonts["label"], colors["white"]),
        "reminders": Text("REMINDERS", fonts["label"], colors["white"]),
        "add-goal": Text("ADD GOAL", fonts["label"], colors["white"]),
        "activity": Text("ACTIVITY", fonts["label-small"], colors["black"]),
        "amount": Text("AMOUNT", fonts["label-small"], colors["black"]),
        "frequency": Text("FREQUENCY", fonts["label-small"], colors["black"]),
        "duration": Text("DURATION", fonts["label-small"], colors["black"]),
        "activity-warning": Text("(activity will be created)", fonts["tiny"], colors["black"]),
        "unit-format": Text("(number, unit)", fonts["tiny"], colors["black"]),
        "unit-warning": Text("(unit will be created)", fonts["tiny"], colors["black"]),
        "frequency-middle": Text("time(s) every", fonts["option"], colors["black"]),
        "days": Text("day(s)", fonts["option"], colors["black"]),
        "add": Text("ADD", fonts["label-small"], colors["white"]),
    }

    images = {
        "logo": Image(scale_surface_to_width(pygame.image.load("images/logo.png"), 150)),
        "back": Image(pygame.image.load("images/back.png")),
        "sudoku": Image(scale_surface_to_height(pygame.image.load("images/sudoku.webp"), 720)),
        "running": Image(scale_surface_to_height(pygame.image.load("images/running.jpeg"), 720)),
        "books": Image(scale_surface_to_width(pygame.image.load("images/books.jpeg"), 640)),
        "walking": Image(scale_surface_to_width(pygame.image.load("images/walking.jpeg"), 640)),
        "checkboxes": Image(scale_surface_to_width(pygame.image.load("images/checkboxes.jpeg"), 640)),
        "calendar": Image(pygame.transform.smoothscale(pygame.image.load("images/calendar.png"), (640, 360))),
        "graph": Image(pygame.transform.smoothscale(pygame.image.load("images/graph.png"), (640, 360))),
        "clock": Image(scale_surface_to_width(pygame.image.load("images/clock.jpeg"), 640))
    }

    menus = {
        "home": home,
        "tracking": tracking,
        "goals": add_goal
    }

    try:
        with open("data.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((0, 0, 0))
            screen.blit(text["file-not-found"].surface, (80, 80))

            pygame.display.flip()
            clock.tick(60)

    next_menu = "home"
    while True:
        next_menu = menus[next_menu]()

        for alpha in range(FADE_LENGTH, 0, -1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((0, 0, 0))
            fade_frame.set_alpha(alpha / FADE_LENGTH * 255)
            screen.blit(fade_frame, (0, 0))

            pygame.display.flip()
            clock.tick(60)
