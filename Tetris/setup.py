import turtle
import settings
import pygame
import os
import timer
import json


def gen_block(shape, size, rgb=(255, 255, 255)):
    # --- generate and return turtle block ---
    block = turtle.Turtle()
    block.shape(shape)
    block.speed(0)
    block.shapesize(*size)
    block.penup()
    block.hideturtle()
    block.color(rgb)
    # --- return object hidden ---
    return block


def gen_standard_block(rgb=(255, 255, 255)):
    # --- standard block settings (square, (25x25))
    return gen_block(shape="square", size=(settings.BLOCK_SIZE / 20,) * 2, rgb=rgb)


def gen_standard_blocks(count, rgb=(255, 255, 255)):
    # --- generate and return list of standard blocks
    block = gen_standard_block(rgb)  # --- generate block ---
    blocks = [block]  # --- init array ---
    for _ in range(count - 1):
        blocks.append(block.clone())  # --- add clone ---
    return blocks


def gen_timers(count):
    # --- generate and return list of timers ---
    timers = []  # --- init array ---
    for _ in range(count):
        timers.append(timer.Timer())  # --- add new timer ---
    return tuple(timers)


def gen_pen():
    # --- generate object as a pen ---
    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("black")  # --- default color ---
    pen.penup()  # --- return inactive ---
    pen.hideturtle()  # --- return hidden ---
    pen.goto(0, 0)
    return pen


def gen_objects(count=1):
    # --- generate and return a list of turtle default objects ---
    return (turtle.Turtle() for _ in range(count))


def gen_image(wn, file_name, pos=(0, 0)):
    # --- generate and return an image ---
    wn.addshape(file_name)  # --- add shape ---
    img = turtle.Turtle()
    img.penup()
    img.shape(file_name)
    img.speed(0)
    img.goto(*pos)
    img.hideturtle()  # --- return hidden ---
    return img


def setup_wn(size, tracer=(0, 0), title="wn", bg_color="black"):
    # --- generate and return a turtle screen ---
    wn = turtle.Screen()
    wn.title(title)
    wn.bgcolor(bg_color)
    wn.setup(*size)
    wn.colormode(255)
    wn.tracer(*tracer)
    wn.listen()  # --- keyboard binding ---
    return wn


def setup_keyboard_press(wn, values: dict):
    # --- keyboard binding ---
    ### onkey press ###
    for function in values:
        # --- bind each function & its key
        wn.onkeypress(function, values[function])
        if len(values[function]) == 1:
            wn.onkeypress(function, values[function].upper())  # --- include CAPS keyboard


def setup_keyboard(wn, values: dict):
    # --- keyboard binding ---
    ### onkey ###
    for function in values:
        # --- bind each function & its key
        wn.onkey(function, values[function])
        if len(values[function]) == 1:
            wn.onkeypress(function, values[function].upper())  # --- include CAPS keyboard


def create_stats():
    # --- create json file ---
    if os.path.isfile(settings.DATA_PATH):
        with open(settings.DATA_PATH, 'r') as f:
            if "Avg." in f.read():
                return
    # --- write content ---
    with open(settings.DATA_PATH, 'w') as f:
        f.write(
            '{"Avg.":[0],'
            '"Best":[{"Score":0, "Level:":0, "Time":"00:00"}],'
            '"Last":[{"Score":0, "Level:":0, "Time":"00:00"}],'
            '"Count":[0]'
            '}'
        )


def load_colors():
    # --- load colors from resources ---
    with open("Resources/graphics/colors", "r") as f:
        # --- set global settings ---
        settings.rand_colors = [
            [int(x) for x in s.split(',')] for s in f.read().replace(' ', '').split('\n')
        ]


def load_stats():
    # --- load stats from json file ---
    with open("Resources\\Data\\data.json", ) as f:
        data = json.load(f)
        return data


def play(file_name):
    # --- play music file ---
    pygame.init()
    bg_music = pygame.mixer.Sound(file_name)
    bg_music.set_volume(0.2)
    bg_music.play()
