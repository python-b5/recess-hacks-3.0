# BeWell
# made for Recess Hacks 3.0
# by Evan Gorman and Jason Li

import calendar
import datetime
import json
import math
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

def save():
    with open("data.json", "w+") as file:
        json.dump(data, file, indent=4)

def home():
    global fade_frame

    fade_alpha = FADE_LENGTH
    fade_in = pygame.Surface((1280, 720))
    fade_in.fill((0, 0, 0))

    goals_alpha = 0
    logs_alpha = 0

    overlay = pygame.Surface((640, 720), pygame.SRCALPHA)

    while True:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked = True

        if fade_alpha > 0:
            fade_alpha -= 1
            clicked = False
        else:
            pos = pygame.mouse.get_pos()

            if pos[0] < 640:
                if goals_alpha < 10:
                    goals_alpha += 1

                if logs_alpha > 0:
                    logs_alpha -= 1
            else:
                if goals_alpha > 0:
                    goals_alpha -= 1

                if logs_alpha < 10:
                    logs_alpha += 1

        screen.blit(images["checkboxes"].surface, (0, 0), (300, 0, 640, 720))
        screen.blit(images["calendar"].surface, (640, 0))

        overlay.fill((0, 0, 0, int(80 * (goals_alpha / 10))))
        screen.blit(overlay, (0, 0))
        overlay.fill((0, 0, 0, int(80 * (logs_alpha / 10))))
        screen.blit(overlay, (640, 0))

        overlay.fill((0, 0, 0, 0))
        overlay.blit(text["goals"].surface, (80, 640 - text["goals"].height))
        overlay.set_alpha(goals_alpha / 10 * 255)
        screen.blit(overlay, (0, 0))

        overlay.fill((0, 0, 0, 0))
        overlay.blit(text["logs"].surface, (560 - text["logs"].width, 640 - text["logs"].height))
        overlay.set_alpha(logs_alpha / 10 * 255)
        screen.blit(overlay, (640, 0))

        overlay.set_alpha(255)

        fade_in.set_alpha(fade_alpha / FADE_LENGTH * 255)
        screen.blit(fade_in, (0, 0))

        pygame.display.flip()
        clock.tick(60)

        if clicked:
            if goals_alpha == 10:
                fade_frame = screen.copy()
                return "goals"
            elif logs_alpha == 10:
                fade_frame = screen.copy()
                return "logs"

def goals():
    fade_alpha = 20
    fade_in = pygame.Surface((1280, 720))
    fade_in.fill((0, 0, 0))

    current_date = datetime.datetime.now()
    scroll_y = 0

    while True:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and scroll_y > 0:
                    scroll_y -= 1
                elif event.key == pygame.K_DOWN and scroll_y < len(data["goals"]) - 4:
                    scroll_y += 1

        if fade_alpha > 0:
            fade_alpha -= 1
            clicked = False

        pos = pygame.mouse.get_pos()

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, colors["blue"], pygame.Rect(0, 0, 1280, 50))
        aa_round_rect(screen, pygame.Rect(640 - (text["goals"].width + 60) // 2, 0, text["goals"].width + 60, 100), colors["blue"], rad=15)
        screen.blit(text["goals"].surface, (640 - text["goals"].width // 2, 50 - text["goals"].height // 2))

        next_menu = None

        screen.blit(text["back"].surface, (10, -17))
        if clicked and pos[0] < 15 + text["back"].width and pos[1] < 50:
            next_menu = "home"

        pygame.draw.rect(screen, colors["gray"], pygame.Rect(100, 150, 855, 520))

        if data["goals"]:
            for i, goal in enumerate(data["goals"][scroll_y:scroll_y + 5]):
                if goal["type"] == "normal":
                    desc = Text(
                        f"{goal['activity']} for {goal['amount']['number']} {goal['amount']['unit']} {goal['frequency']['amount']} time(s) every {goal['frequency']['every']} day(s)",
                        fonts["body"], colors["black"]
                    )

                    start = datetime.datetime.strptime(goal['duration']['start'], "%Y-%m-%d")
                    end = datetime.datetime.strptime(goal['duration']['end'], "%Y-%m-%d")

                    if current_date > end:
                        complete = True
                        total_days = (end - start).days

                        for portion in range(math.ceil(total_days / goal["frequency"]["every"])):
                            portion_start = goal["frequency"]["every"] * portion
                            count = 0

                            for days in range(portion_start, min(total_days, portion_start + goal["frequency"]["every"])):
                                date = (start + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
                                if goal["activity"] in data["logs"]:
                                    for day, times in data["logs"][goal["activity"]].items():
                                        if date == day:
                                            for time in times:
                                                if goal["amount"]["unit"] in times[time] and times[time][goal["amount"]["unit"]] >= goal["amount"]["number"]:
                                                    count += 1

                            if count < goal["frequency"]["amount"]:
                                complete = False
                                break

                        if complete:
                            progress = text["progress-complete"]
                        else:
                            progress = text["progress-failed"]
                    else:
                        progress = Text(
                            f"Days remaining: {(datetime.datetime.strptime(goal['duration']['end'], '%Y-%m-%d') - current_date).days + 2}",
                            fonts["body"], colors["black"]
                        )
                elif goal["type"] == "custom":
                    desc = Text(goal["text"], fonts["body"], colors["black"])
                    progress = text["progress-custom"]

                screen.blit(text["x"].surface, (120, 208 + 90 * i))
                screen.blit(desc.surface, (140 + text["x"].width, 189 + 90 * i))
                screen.blit(progress.surface, (140 + text["x"].width, 229 + 90 * i))

                if clicked and 115 <= pos[0] < 125 + text["x"].width and 203 + 90 * i <= pos[1] < 213 + 90 * i + text["x"].height:
                    del data["goals"][scroll_y + i]
                    if scroll_y >= len("goals") - 4:
                        scroll_y = 0
        else:
            screen.blit(text["no-goals"].surface, (120, 189))

        box = (1120 - text["add-goal-button"].width, 540, text["add-goal-button"].width + 60, 100)
        aa_round_rect(screen, pygame.Rect(*box), colors["blue"], rad=15)
        screen.blit(text["add-goal-button"].surface, (1150 - text["add-goal-button"].width, 590 - text["add-goal-button"].height // 2))

        if clicked and box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
            next_menu = "add-goal"

        screen.blit(text["scroll-guide"].surface, (1150 - text["add-goal-button"].width // 2 - text["scroll-guide"].width // 2, 670 - text["scroll-guide"].height))

        fade_in.set_alpha(fade_alpha / FADE_LENGTH * 255)
        screen.blit(fade_in, (0, 0))

        pygame.display.flip()
        clock.tick(60)

        if next_menu:
            global fade_frame
            fade_frame = screen.copy()
            return next_menu

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

    custom_focused = False
    custom_contents = ""

    while True:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked = True
            elif event.type == pygame.KEYDOWN:
                if activity_focused:
                    if event.key == pygame.K_BACKSPACE and activity_contents:
                        activity_contents = activity_contents[:-1]
                    elif len(activity_contents) < 8 and (event.unicode.isalpha() or event.unicode in string.digits + string.punctuation + " "):
                        activity_contents += event.unicode
                elif amount_number_focused:
                    if event.key == pygame.K_BACKSPACE and amount_number_contents:
                        amount_number_contents = amount_number_contents[:-1]
                    elif len(amount_number_contents) < 5 and (event.unicode in "123456789" or (amount_number_contents and event.unicode in "0.")):
                        amount_number_contents += event.unicode
                elif amount_unit_focused:
                    if event.key == pygame.K_BACKSPACE and amount_unit_contents:
                        amount_unit_contents = amount_unit_contents[:-1]
                    elif len(amount_unit_contents) < 8 and (event.unicode.isalpha() or event.unicode in string.digits + string.punctuation + " "):
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
                elif custom_focused:
                    if event.key == pygame.K_BACKSPACE and custom_contents:
                        custom_contents = custom_contents[:-1]
                    elif len(custom_contents) < 36 and (event.unicode.isalpha() or event.unicode in string.digits + string.punctuation + " "):
                        custom_contents += event.unicode

        if fade_alpha > 0:
            fade_alpha -= 1
            clicked = False
        
        pos = pygame.mouse.get_pos()

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, colors["blue"], pygame.Rect(0, 0, 1280, 50))
        aa_round_rect(screen, pygame.Rect(640 - (text["add-goal"].width + 60) // 2, 0, text["add-goal"].width + 60, 100), colors["blue"], rad=15)
        screen.blit(text["add-goal"].surface, (640 - text["add-goal"].width // 2, 50 - text["add-goal"].height // 2))

        next_menu = None

        screen.blit(text["back"].surface, (10, -17))
        if clicked and pos[0] < 15 + text["back"].width and pos[1] < 50:
            next_menu = "goals"

        screen.blit(text["activity"].surface, (154 - text["activity"].width // 2, 150))
        screen.blit(text["amount"].surface, (410 - text["amount"].width // 2, 150))
        screen.blit(text["frequency"].surface, (666 - text["frequency"].width // 2, 150))
        screen.blit(text["duration"].surface, (922 - text["duration"].width // 2, 150))

        activity_text = Text(activity_contents, fonts["body"], colors["black"])
        box = (144 - activity_text.width // 2, 210, activity_text.width + 20, activity_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(activity_text.surface, (154 - activity_text.width // 2, 220))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                activity_focused = True
            else:
                activity_focused = False

        activity_exists = activity_contents
        if activity_contents and activity_contents not in data["logs"]:
            screen.blit(text["activity-warning"].surface, (154 - text["activity-warning"].width // 2, 284))
            activity_exists = False

        amount_number_text = Text(amount_number_contents, fonts["body"], colors["black"])
        amount_unit_text = Text(amount_unit_contents, fonts["body"], colors["black"])
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

        screen.blit(text["unit-format"].surface, (410 - text["unit-format"].width // 2, 284))

        if activity_exists and amount_unit_contents and not any(
            any(amount_unit_contents in data["logs"][activity_contents][date][time] for time in data["logs"][activity_contents][date])
            for date in data["logs"][activity_contents]
        ):
            screen.blit(text["unit-warning"].surface, (410 - text["unit-warning"].width // 2, 309))

        frequency_amount_text = Text(frequency_amount_contents, fonts["body"], colors["black"])
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

        frequency_every_text = Text(frequency_every_contents, fonts["body"], colors["black"])
        box = (666 - frequency_amount_width // 2, 290, frequency_every_text.width + 20, frequency_every_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(frequency_every_text.surface, (676 - frequency_amount_width // 2, 300))
        screen.blit(text["days"].surface, (696 - frequency_amount_width // 2 + frequency_every_text.width, 300))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                frequency_every_focused = True
            else:
                frequency_every_focused = False

        duration_text = Text(duration_contents, fonts["body"], colors["black"])
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

        custom_text = Text(custom_contents, fonts["body"], colors["black"])
        box = (100, 560 - custom_text.height // 2, 848, custom_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(custom_text.surface, (110, 570 - custom_text.height // 2))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                custom_focused = True
            else:
                custom_focused = False

        active = activity_contents and amount_number_contents and amount_unit_contents and frequency_amount_contents and frequency_every_contents and duration_contents
        box = (1120 - text["add"].width, 201, text["add"].width + 60, 100)
        aa_round_rect(screen, pygame.Rect(*box), colors["blue"] if active else colors["gray"], rad=15)
        screen.blit(text["add"].surface, (1150 - text["add"].width, 251 - text["add"].height // 2))

        if clicked and active and box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
            date = datetime.datetime.now()
            data["goals"].append({
                "type": "normal",
                "activity": activity_contents,
                "amount": {
                    "number": int(amount_number_contents) if amount_number_contents.isdigit() else float(amount_number_contents),
                    "unit": amount_unit_contents
                },
                "frequency": {
                    "amount": int(frequency_amount_contents),
                    "every": int(frequency_every_contents)
                },
                "duration": {
                    "start": date.strftime("%Y-%m-%d"),
                    "end": (date + datetime.timedelta(days=int(duration_contents) - 1)).strftime("%Y-%m-%d")
                }
            })

            with open("new_data.json", "w+") as file:
                json.dump(data, file, indent=4)

            next_menu = "goals"

        box = (1120 - text["add-custom"].width, 520, text["add-custom"].width + 60, 100)
        aa_round_rect(screen, pygame.Rect(*box), colors["blue"] if custom_contents else colors["gray"], rad=15)
        screen.blit(text["add-custom"].surface, (1150 - text["add-custom"].width, 570 - text["add-custom"].height // 2))

        if clicked and custom_contents and box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
            data["goals"].append({"type": "custom", "text": custom_contents})

            with open("new_data.json", "w+") as file:
                json.dump(data, file, indent=4)

            next_menu = "goals"

        fade_in.set_alpha(fade_alpha / FADE_LENGTH * 255)
        screen.blit(fade_in, (0, 0))

        pygame.display.flip()
        clock.tick(60)

        if next_menu:
            global fade_frame
            fade_frame = screen.copy()
            return next_menu

def create_logs_display(date):
    logs_lines = [Text("{date:%A}, {date:%B} {date.day}, {date.year}".format(date=date), fonts["body-bold"], colors["black"])]

    for activity, days in data["logs"].items():
        iso = date.strftime("%Y-%m-%d")
        if iso in days:
            times = days[iso]
            if times and any(times[time] for time in times):
                logs_lines.append(None)
                logs_lines.append(Text(activity, fonts["body-bold"], colors["black"]))

                for time, log in times.items():
                    log_str = time + ": "
                    for unit, amount in log.items():
                        log_str += f"{amount} {unit}, "

                    logs_lines.append(Text(log_str[:-2], fonts["body"], colors["black"]))
    
    if len(logs_lines) == 1:
        logs_lines.append(None)
        logs_lines.append(text["no-logs"])

    logs_surface = pygame.Surface((679, len(logs_lines) * 40), pygame.SRCALPHA)
    logs_surface.fill((0, 0, 0, 0))

    for i, line in enumerate(logs_lines):
        if line:
            logs_surface.blit(line.surface, (0, 40 * i))

    return Image(logs_surface), len(logs_lines)

def logs():
    fade_alpha = 20
    fade_in = pygame.Surface((1280, 720))
    fade_in.fill((0, 0, 0))

    current_date = datetime.datetime.now()
    year = current_date.year
    month = current_date.month
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

    logs_display, logs_height = create_logs_display(current_date)
    scroll_y = 0

    can_add = True

    while True:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and scroll_y > 0:
                    scroll_y -= 1
                elif event.key == pygame.K_DOWN and scroll_y < logs_height - 13:
                    scroll_y += 1

        if fade_alpha > 0:
            fade_alpha -= 1
            clicked = False

        pos = pygame.mouse.get_pos()

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, colors["blue"], pygame.Rect(0, 0, 1280, 50))
        aa_round_rect(screen, pygame.Rect(640 - (text["logs"].width + 60) // 2, 0, text["logs"].width + 60, 100), colors["blue"], rad=15)
        screen.blit(text["logs"].surface, (640 - text["logs"].width // 2, 50 - text["logs"].height // 2))

        next_menu = None

        screen.blit(text["back"].surface, (10, -17))
        if clicked and pos[0] < 15 + text["back"].width and pos[1] < 50:
            next_menu = "home"

        screen.blit(text["<"].surface, (115 - text["<"].width // 2, 187 - text["<"].height // 2))
        screen.blit(text[">"].surface, (215 - text[">"].width // 2, 187 - text["<"].height // 2))
        year_text = Text(str(year), fonts["body"], colors["black"])
        screen.blit(year_text.surface, (165 - year_text.width // 2, 187 - year_text.height // 2))

        screen.blit(text["<"].surface, (265 - text["<"].width // 2, 187 - text["<"].height // 2))
        screen.blit(text[">"].surface, (415 - text[">"].width // 2, 187 - text["<"].height // 2))
        screen.blit(text[months[month - 1]].surface, (340 - text[months[month - 1]].width // 2, 187 - text[months[month - 1]].height // 2))

        if clicked and 172 <= pos[1] <= 202:
            if 100 <= pos[0] <= 130:
                year -= 1
                if year < 1970:
                    year = current_date.year
            elif 200 <= pos[0] <= 230:
                year += 1
                if year > current_date.year:
                    year = 1970
            elif 250 <= pos[0] <= 280:
                month -= 1
                if month < 1:
                    month = 12
            elif 400 <= pos[0] <= 430:
                month += 1
                if month > 12:
                    month = 1

        screen.blit(text["s"].surface, (115 - text["s"].width // 2, 237 - text["s"].height // 2))
        screen.blit(text["m"].surface, (165 - text["m"].width // 2, 237 - text["m"].height // 2))
        screen.blit(text["t"].surface, (215 - text["t"].width // 2, 237 - text["t"].height // 2))
        screen.blit(text["w"].surface, (265 - text["w"].width // 2, 237 - text["w"].height // 2))
        screen.blit(text["t"].surface, (315 - text["t"].width // 2, 237 - text["t"].height // 2))
        screen.blit(text["f"].surface, (365 - text["f"].width // 2, 237 - text["f"].height // 2))
        screen.blit(text["s"].surface, (415 - text["s"].width // 2, 237 - text["s"].height // 2))

        x, days = calendar.monthrange(year, month)
        x = (x + 1) % 7
        y = 0
        days_drawn = 0

        while y < 5:
            while x < 7 and days_drawn < days:
                days_drawn += 1
                if days_drawn == current_date.day and year == current_date.year and month == current_date.month:
                    gfxdraw.aacircle(screen, 115 + 50 * x, 287 + 50 * y, 15, colors["black"])
                    gfxdraw.filled_circle(screen, 115 + 50 * x, 287 + 50 * y, 15, colors["black"])
                    radius = 12
                else:
                    radius = 15

                date = f"{year}-{month:02}-{days_drawn:02}"
                color = colors["blue"] if any(date in data["logs"][activity] for activity in data["logs"]) else colors["gray"]
                gfxdraw.aacircle(screen, 115 + 50 * x, 287 + 50 * y, radius, color)
                gfxdraw.filled_circle(screen, 115 + 50 * x, 287 + 50 * y, radius, color)

                if clicked and 100 + 50 * x <= pos[0] <= 130 + 50 * x and 272 + 50 * y <= pos[1] <= 302 + 50 * y:
                    logs_display, logs_height = create_logs_display(datetime.date(year, month, days_drawn))
                    scroll_y = 0

                    if year == current_date.year and month == current_date.month and days_drawn == current_date.day:
                        can_add = True
                    else:
                        can_add = False
                
                x += 1

            x = 0
            y += 1

        pygame.draw.rect(screen, colors["gray"], pygame.Rect(481, 160, 699, 500))
        screen.blit(logs_display.surface.subsurface(0, scroll_y * 40, 679, min(logs_display.height, 480)), (491, 170))

        box = (235 - text["add-log-button"].width // 2, 527, text["add-log-button"].width + 60, 70)
        aa_round_rect(screen, pygame.Rect(*box), colors["blue"] if can_add else colors["gray"], rad=15)
        screen.blit(text["add-log-button"].surface, (265 - text["add-log-button"].width // 2, 562 - text["add-log-button"].height // 2))

        if clicked and can_add and box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
            next_menu = "add-log"

        screen.blit(text["scroll-guide"].surface, (265 - text["scroll-guide"].width // 2, 617))

        fade_in.set_alpha(fade_alpha / FADE_LENGTH * 255)
        screen.blit(fade_in, (0, 0))

        pygame.display.flip()
        clock.tick(60)

        if next_menu:
            global fade_frame
            fade_frame = screen.copy()
            return next_menu

def add_log():
    fade_alpha = 20
    fade_in = pygame.Surface((1280, 720))
    fade_in.fill((0, 0, 0))

    activity_focused = False
    activity_contents = ""

    amounts = [
        {
            "number": {"focused": False, "contents": ""},
            "unit": {"focused": False, "contents": ""}
        } for _ in range(4)
    ]

    while True:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked = True
            elif event.type == pygame.KEYDOWN:
                if activity_focused:
                    if event.key == pygame.K_BACKSPACE and activity_contents:
                        activity_contents = activity_contents[:-1]
                    elif len(activity_contents) < 8 and (event.unicode.isalpha() or event.unicode in string.digits + string.punctuation + " "):
                        activity_contents += event.unicode

                for amount in amounts:
                    if amount["number"]["focused"]:
                        if event.key == pygame.K_BACKSPACE and amount["number"]["contents"]:
                            amount["number"]["contents"] = amount["number"]["contents"][:-1]
                        elif len(amount["number"]["contents"]) < 5 and (event.unicode in "123456789" or (amount["number"]["contents"] and event.unicode in "0.")):
                            amount["number"]["contents"] += event.unicode
                    elif amount["unit"]["focused"]:
                        if event.key == pygame.K_BACKSPACE and amount["unit"]["contents"]:
                            amount["unit"]["contents"] = amount["unit"]["contents"][:-1]
                        elif len(amount["unit"]["contents"]) < 8 and (event.unicode.isalpha() or event.unicode in string.digits + string.punctuation + " "):
                            amount["unit"]["contents"] += event.unicode

        if fade_alpha > 0:
            fade_alpha -= 1
            clicked = False

        pos = pygame.mouse.get_pos()

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, colors["blue"], pygame.Rect(0, 0, 1280, 50))
        aa_round_rect(screen, pygame.Rect(640 - (text["add-log"].width + 60) // 2, 0, text["add-log"].width + 60, 100), colors["blue"], rad=15)
        screen.blit(text["add-log"].surface, (640 - text["add-log"].width // 2, 50 - text["add-log"].height // 2))

        next_menu = None

        screen.blit(text["back"].surface, (10, -17))
        if clicked and pos[0] < 15 + text["back"].width and pos[1] < 50:
            next_menu = "logs"

        screen.blit(text["activity"].surface, (320 - text["activity"].width // 2, 304))
        screen.blit(text["amounts"].surface, (640 - text["amounts"].width // 2, 184))

        activity_text = Text(activity_contents, fonts["body"], colors["black"])
        box = (310 - activity_text.width // 2, 364, activity_text.width + 20, activity_text.height + 20)
        pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
        screen.blit(activity_text.surface, (320 - activity_text.width // 2, 374))

        if clicked:
            if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                activity_focused = True
            else:
                activity_focused = False

        if activity_contents and activity_contents not in data["logs"]:
            screen.blit(text["activity-warning"].surface, (320 - text["activity-warning"].width // 2, 425))

        for i, amount in enumerate(amounts):
            amount_number_text = Text(amount["number"]["contents"], fonts["body"], colors["black"])
            amount_unit_text = Text(amount["unit"]["contents"], fonts["body"], colors["black"])
            amount_width = amount_number_text.width + 50 + amount_unit_text.width
            
            box = (640 - amount_width // 2, 244 + 80 * i, amount_number_text.width + 20, amount_number_text.height + 20)
            pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
            screen.blit(amount_number_text.surface, (650 - amount_width // 2, 254 + 80 * i))

            if clicked:
                if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                    amount["number"]["focused"] = True
                else:
                    amount["number"]["focused"] = False

            box = (670 - amount_width // 2 + amount_number_text.width, 244 + 80 * i, amount_unit_text.width + 20, amount_unit_text.height + 20)
            pygame.draw.rect(screen, colors["gray"], pygame.Rect(*box))
            screen.blit(amount_unit_text.surface, (680 - amount_width // 2 + amount_number_text.width, 254 + 80 * i))

            if clicked:
                if box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
                    amount["unit"]["focused"] = True
                else:
                    amount["unit"]["focused"] = False

        screen.blit(text["unit-format"].surface, (640 - text["unit-format"].width // 2, 558))

        active = activity_contents and any(amount["number"]["contents"] and amount["unit"]["contents"] for amount in amounts)
        box = (930 - text["add-log-button"].width // 2, 335, text["add-log-button"].width + 60, 100)
        aa_round_rect(screen, pygame.Rect(*box), colors["blue"] if active else colors["gray"], rad=15)
        screen.blit(text["add-log-button"].surface, (960 - text["add-log-button"].width // 2, 385 - text["add-log-button"].height // 2))

        if clicked and active and box[0] <= pos[0] <= box[0] + box[2] and box[1] <= pos[1] <= box[1] + box[3]:
            if activity_contents not in data["logs"]:
                data["logs"][activity_contents] = {}

            date = datetime.datetime.now()

            iso = date.strftime("%Y-%m-%d")
            if date not in data["logs"][activity_contents]:
                data["logs"][activity_contents][iso] = {}
            
            data["logs"][activity_contents][iso][date.strftime("%I:%M %p")] = {
                amount["unit"]["contents"]:(int(amount["number"]["contents"]) if amount["number"]["contents"].isdigit() else float(amount["number"]["contents"]))
                for amount in amounts if amount["unit"]["contents"] and amount["number"]["contents"]
            }

            next_menu = "logs"

        fade_in.set_alpha(fade_alpha / FADE_LENGTH * 255)
        screen.blit(fade_in, (0, 0))

        pygame.display.flip()
        clock.tick(60)

        if next_menu:
            global fade_frame
            fade_frame = screen.copy()
            return next_menu

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("BeWell")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))
    clock = pygame.time.Clock()

    colors = {
        "white": pygame.Color("#ffffff"),
        "black": pygame.Color("#434343"),
        "gray": pygame.Color("#e6e6e6"),
        "blue": pygame.Color("#86c0cc")
    }

    fonts = {
        "label": pygame.font.Font("fonts/BebasNeue-Regular.ttf", 75),
        "label-small": pygame.font.Font("fonts/BebasNeue-Regular.ttf", 40),
        "body": pygame.font.Font("fonts/NotoSans-Regular.ttf", 25),
        "body-bold": pygame.font.Font("fonts/NotoSans-SemiBold.ttf", 25),
        "body-small": pygame.font.Font("fonts/NotoSans-Regular.ttf", 15)
    }

    text = {
        "title": Text("BeWell", fonts["title"], colors["white"]),
        "invalid": Text("Error: Invalid data.json!", fonts["label"], colors["white"]),
        "goals": Text("GOALS", fonts["label"], colors["white"]),
        "logs": Text("LOGS", fonts["label"], colors["white"]),
        "back": Text("<", fonts["label"], colors["white"]),
        "x": Text("X", fonts["body-bold"], colors["black"]),
        "progress-complete": Text("Complete!", fonts["body"], colors["black"]),
        "progress-failed": Text("Failed...", fonts["body"], colors["black"]),
        "progress-custom": Text("(custom goal; no progress)", fonts["body"], colors["black"]),
        "no-goals": Text("(no goals)", fonts["body"], colors["black"]),
        "add-goal-button": Text("ADD GOAL", fonts["label-small"], colors["white"]),
        "add-goal": Text("ADD GOAL", fonts["label"], colors["white"]),
        "activity": Text("ACTIVITY", fonts["label-small"], colors["black"]),
        "amount": Text("AMOUNT", fonts["label-small"], colors["black"]),
        "frequency": Text("FREQUENCY", fonts["label-small"], colors["black"]),
        "duration": Text("DURATION", fonts["label-small"], colors["black"]),
        "activity-warning": Text("(no logs for this activity)", fonts["body-small"], colors["black"]),
        "unit-format": Text("(number, unit)", fonts["body-small"], colors["black"]),
        "unit-warning": Text("(no logs include this unit)", fonts["body-small"], colors["black"]),
        "frequency-middle": Text("time(s) every", fonts["body"], colors["black"]),
        "days": Text("day(s)", fonts["body"], colors["black"]),
        "add": Text("ADD", fonts["label-small"], colors["white"]),
        "add-custom": Text("ADD CUSTOM", fonts["label-small"], colors["white"]),
        "<": Text("<", fonts["body"], colors["black"]),
        ">": Text(">", fonts["body"], colors["black"]),
        "jan": Text("January", fonts["body"], colors["black"]),
        "feb": Text("February", fonts["body"], colors["black"]),
        "mar": Text("March", fonts["body"], colors["black"]),
        "apr": Text("April", fonts["body"], colors["black"]),
        "may": Text("May", fonts["body"], colors["black"]),
        "jun": Text("June", fonts["body"], colors["black"]),
        "jul": Text("July", fonts["body"], colors["black"]),
        "aug": Text("August", fonts["body"], colors["black"]),
        "sep": Text("September", fonts["body"], colors["black"]),
        "oct": Text("October", fonts["body"], colors["black"]),
        "nov": Text("November", fonts["body"], colors["black"]),
        "dec": Text("December", fonts["body"], colors["black"]),
        "s": Text("S", fonts["body"], colors["black"]),
        "m": Text("M", fonts["body"], colors["black"]),
        "t": Text("T", fonts["body"], colors["black"]),
        "w": Text("W", fonts["body"], colors["black"]),
        "f": Text("F", fonts["body"], colors["black"]),
        "add-log-button": Text("ADD LOG", fonts["label-small"], colors["white"]),
        "scroll-guide": Text("(cursor keys to scroll)", fonts["body-small"], colors["black"]),
        "no-logs": Text("(no logs)", fonts["body"], colors["black"]),
        "add-log": Text("ADD LOG", fonts["label"], colors["white"]),
        "amounts": Text("AMOUNTS", fonts["label-small"], colors["black"])
    }

    images = {
        "logo": Image(scale_surface_to_width(pygame.image.load("images/logo.png"), 150)),
        "checkboxes": Image(scale_surface_to_height(pygame.image.load("images/checkboxes.jpeg"), 720)),
        "calendar": Image(pygame.transform.smoothscale(pygame.image.load("images/calendar.png"), (640, 720))),
    }

    menus = {
        "home": home,
        "goals": goals,
        "add-goal": add_goal,
        "logs": logs,
        "add-log": add_log
    }

    try:
        with open("data.json") as file:
            data = json.load(file)
            if "goals" not in data or "logs" not in data:
                raise json.JSONDecodeError
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save()
                    pygame.quit()
                    sys.exit()

            screen.fill((0, 0, 0))
            screen.blit(text["invalid"].surface, (80, 80))

            pygame.display.flip()
            clock.tick(60)

    next_menu = "home"
    while True:
        next_menu = menus[next_menu]()

        for alpha in range(FADE_LENGTH, 0, -1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save()
                    pygame.quit()
                    sys.exit()

            screen.fill((0, 0, 0))
            fade_frame.set_alpha(alpha / FADE_LENGTH * 255)
            screen.blit(fade_frame, (0, 0))

            pygame.display.flip()
            clock.tick(60)
