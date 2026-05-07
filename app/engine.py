"""Durable Snake: snake game with 3 retries and aggressive speedup.

Copyright (c) 2026 Alexandre Roman. All rights reserved.
"""

import random
import time

from badge import *

from badge_app import (
    DualScreenSession,
    load_score,
    read_stick_4way,
    save_score,
    ticks_add,
    with_led_override,
)
import badge_ui as ui


CELL = 4
COLS = 32
PLAY_TOP = 10
PLAY_LEFT = 0
ROWS = (64 - PLAY_TOP) // CELL  # 13

FRAME_MS = 30
START_STEP_MS = 170
MIN_STEP_MS = 38
SPEEDUP_NUM = 1
SPEEDUP_DEN = 13

EAT_BURST_FRAMES = 4
MILESTONE_MS = 500
MILESTONE_INTERVAL = 10
MILESTONE_STROBE_MS = 90

DEATH_FLASHES = 3
DEATH_FLASH_ON_MS = 90
DEATH_FLASH_OFF_MS = 70
DEATH_RETRACT_MS = 28

CONTINUE_TICK_MS = 200

TITLE_TICK_MS = 130
TITLE_SNAKE_LEN = 5

GAMEOVER_TICK_MS = 240

LIVES_START = 3
LIVES_ROW_BRIGHT = 220

SCORE_PATH = "/durable_snake_score.json"


def compute_interval(food_count):
    interval = START_STEP_MS
    n = food_count
    while n > 0:
        if interval <= MIN_STEP_MS:
            return MIN_STEP_MS
        decrement = interval * SPEEDUP_NUM // SPEEDUP_DEN
        if decrement < 1:
            decrement = 1
        interval -= decrement
        n -= 1
    if interval < MIN_STEP_MS:
        return MIN_STEP_MS
    return interval


def random_free_cell(snake_set):
    while True:
        cell = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if cell not in snake_set:
            return cell


def fresh_snake():
    cx = COLS // 2
    cy = ROWS // 2
    snake = [(cx + 1, cy), (cx, cy), (cx - 1, cy)]
    return snake, set(snake)


def new_run():
    snake, snake_set = fresh_snake()
    return {
        "snake": snake,
        "snake_set": snake_set,
        "dir": (1, 0),
        "next_dir": (1, 0),
        "food": random_free_cell(snake_set),
        "food_count": 0,
        "speed_count": 0,
        "step_ms": START_STEP_MS,
        "last_step": time.ticks_ms(),
        "last_frame": 0,
        "burst": None,
        "milestone_until": None,
        "inverted": False,
        "lives": LIVES_START,
        "reason": "Quit",
    }


def restart_after_continue(game):
    snake, snake_set = fresh_snake()
    game["snake"] = snake
    game["snake_set"] = snake_set
    game["dir"] = (1, 0)
    game["next_dir"] = (1, 0)
    game["food"] = random_free_cell(snake_set)
    game["speed_count"] = 0
    game["step_ms"] = START_STEP_MS
    game["last_step"] = time.ticks_ms()
    game["last_frame"] = 0
    game["burst"] = None
    game["milestone_until"] = None
    game["inverted"] = False
    game["reason"] = "Quit"


def turn(game, x_dir, y_dir):
    if x_dir:
        proposed = (x_dir, 0)
    elif y_dir:
        proposed = (0, y_dir)
    else:
        return
    cur = game["dir"]
    if proposed[0] == -cur[0] and proposed[1] == -cur[1]:
        return
    game["next_dir"] = proposed


def step(game, now):
    if time.ticks_diff(now, game["last_step"]) < game["step_ms"]:
        return True
    game["last_step"] = now
    game["dir"] = game["next_dir"]

    dx, dy = game["dir"]
    head = game["snake"][0]
    new_head = ((head[0] + dx) % COLS, (head[1] + dy) % ROWS)

    eating = new_head == game["food"]
    snake = game["snake"]
    snake_set = game["snake_set"]
    tail = None

    if not eating:
        tail = snake.pop()
        snake_set.discard(tail)

    if new_head in snake_set:
        game["reason"] = "Snake bite"
        if tail is not None:
            snake.append(tail)
            snake_set.add(tail)
        return False

    snake.insert(0, new_head)
    snake_set.add(new_head)

    if eating:
        old_food = game["food"]
        game["food_count"] += 1
        game["speed_count"] += 1
        game["step_ms"] = compute_interval(game["speed_count"])
        game["burst"] = (old_food[0], old_food[1], EAT_BURST_FRAMES)
        if game["food_count"] % MILESTONE_INTERVAL == 0:
            game["milestone_until"] = ticks_add(now, MILESTONE_MS)
        game["food"] = random_free_cell(snake_set)
        try:
            tone(880, 40)
        except Exception:
            pass

    return True


def cell_box(cx, cy):
    oled_draw_box(
        PLAY_LEFT + cx * CELL,
        PLAY_TOP + cy * CELL,
        CELL,
        CELL,
    )


def cell_inner(cx, cy):
    oled_draw_box(
        PLAY_LEFT + cx * CELL + 1,
        PLAY_TOP + cy * CELL + 1,
        CELL - 2,
        CELL - 2,
    )


def draw_burst(game):
    burst = game["burst"]
    if not burst:
        return
    cx, cy, frames_left = burst
    if frames_left <= 0:
        game["burst"] = None
        return
    age = EAT_BURST_FRAMES - frames_left
    half = age + 1
    px = PLAY_LEFT + cx * CELL + CELL // 2
    py = PLAY_TOP + cy * CELL + CELL // 2
    x = px - half
    y = py - half
    size = half * 2
    oled_set_draw_color(2)
    oled_draw_box(x, y, size, 1)
    oled_draw_box(x, y + size - 1, size, 1)
    oled_draw_box(x, y, 1, size)
    oled_draw_box(x + size - 1, y, 1, size)
    oled_set_draw_color(1)
    game["burst"] = (cx, cy, frames_left - 1)


def is_milestone(game, now):
    until = game["milestone_until"]
    if until is None:
        return False
    if time.ticks_diff(until, now) <= 0:
        game["milestone_until"] = None
        return False
    return True


def update_invert(game, now):
    want = is_milestone(game, now)
    if want and not game["inverted"]:
        try:
            oled_invert(True)
        except Exception:
            pass
        game["inverted"] = True
    elif not want and game["inverted"]:
        try:
            oled_invert(False)
        except Exception:
            pass
        game["inverted"] = False


def header_label(game):
    return "L" + str(game["lives"]) + " S" + str(game["food_count"])


def draw_play(game, now=None):
    if now is None:
        now = time.ticks_ms()
    oled_clear()
    ui.header("Durable Snake", header_label(game))
    head = game["snake"][0]
    cell_box(head[0], head[1])
    for cx, cy in game["snake"][1:]:
        cell_inner(cx, cy)
    fx, fy = game["food"]
    if (now // 200) & 1:
        cell_box(fx, fy)
    else:
        cell_inner(fx, fy)
    draw_burst(game)
    oled_show()


def lives_row_mask(lives):
    mask = 0
    for i in range(lives):
        mask |= 0x80 >> i
    return mask


def render_score_frame(game):
    rows = [0] * 8
    rows[0] = lives_row_mask(game["lives"])
    food_count = game["food_count"]
    if food_count > 0:
        cycle = (food_count - 1) // 56
        lit = ((food_count - 1) % 56) + 1
        for i in range(lit):
            r = 1 + i // 8
            c = i % 8
            rows[r] |= 0x80 >> c
    return rows


def draw_score_leds(game, now):
    if is_milestone(game, now):
        if (now // MILESTONE_STROBE_MS) & 1:
            led_fill(220)
        else:
            led_clear()
        return
    rows = render_score_frame(game)
    food_count = game["food_count"]
    if food_count <= 0:
        base = LIVES_ROW_BRIGHT
    else:
        cycle = (food_count - 1) // 56
        base = 35 + cycle * 60
        if base > 200:
            base = 200
    led_set_frame(rows, base)


def death_animation(game, session):
    if game["inverted"]:
        try:
            oled_invert(False)
        except Exception:
            pass
        game["inverted"] = False

    for i in range(DEATH_FLASHES):
        led_fill(200)
        try:
            tone(220 - i * 40, 60)
        except Exception:
            pass
        try:
            oled_invert(True)
        except Exception:
            pass
        time.sleep_ms(DEATH_FLASH_ON_MS)
        try:
            oled_invert(False)
        except Exception:
            pass
        led_clear()
        time.sleep_ms(DEATH_FLASH_OFF_MS)

    try:
        no_tone()
    except Exception:
        pass

    snake = game["snake"]
    while len(snake) > 1:
        snake.pop()
        draw_play(game)
        time.sleep_ms(DEATH_RETRACT_MS)

    try:
        haptic_pulse(255, 120, 90)
    except Exception:
        pass


def play_loop(game, session):
    last_food = -1
    last_lives = -1
    led_redraw_at = 0
    draw_play(game)
    draw_score_leds(game, session.now())

    while True:
        now = session.now()
        x_dir, y_dir = read_stick_4way()
        turn(game, x_dir, y_dir)

        if not step(game, now):
            death_animation(game, session)
            return

        update_invert(game, now)

        if game["food_count"] != last_food or game["lives"] != last_lives:
            draw_score_leds(game, now)
            last_food = game["food_count"]
            last_lives = game["lives"]
            led_redraw_at = now
        elif is_milestone(game, now):
            if time.ticks_diff(now, led_redraw_at) >= MILESTONE_STROBE_MS:
                draw_score_leds(game, now)
                led_redraw_at = now

        if session.frame_due(game, now):
            draw_play(game, now)

        if session.quit_pressed():
            game["reason"] = "Quit"
            return

        session.sleep()


def life_run(game):
    session = DualScreenSession(FRAME_MS)
    with_led_override(play_loop, game, session)


def continue_pulse_frame(remaining_lives, phase):
    rows = [0] * 8
    rows[3] = lives_row_mask(remaining_lives)
    rows[4] = rows[3]
    return rows, 60 + phase * 90


def continue_screen(game):
    remaining = game["lives"]
    ui.chrome(
        "Bitten!",
        str(remaining) + " left",
        "OK", "retry",
        "BACK", "stop",
    )
    ui.center(15, "Durable execution")
    ui.center(28, "Score " + str(game["food_count"]))
    ui.center(40, "continue_as_new()")
    oled_show()

    last_tick = time.ticks_ms()
    phase = 0
    rows, bright = continue_pulse_frame(remaining, phase)
    led_set_frame(rows, bright)
    while True:
        if button_pressed(BTN_CONFIRM):
            led_clear()
            return True
        if button_pressed(BTN_BACK):
            led_clear()
            return False
        now = time.ticks_ms()
        if time.ticks_diff(now, last_tick) >= CONTINUE_TICK_MS:
            last_tick = now
            phase = 1 - phase
            rows, bright = continue_pulse_frame(remaining, phase)
            led_set_frame(rows, bright)
        time.sleep_ms(20)


def title_screen(best):
    ui.chrome(
        "Durable Snake",
        "Best " + str(best["total"]),
        "OK", "play",
        "BACK", "quit",
    )
    ui.text(4, 14, "Joystick: turn", 120)
    ui.text(4, 24, "3 lives per run", 120)
    ui.text(4, 34, "Edges wrap, fast pace", 120)
    ui.text(4, 44, "(c) Alexandre Roman", 120)
    oled_show()

    pos = 0
    last_tick = time.ticks_ms()
    led_clear()
    while True:
        if button_pressed(BTN_CONFIRM):
            led_clear()
            return True
        if button_pressed(BTN_BACK):
            led_clear()
            return False
        now = time.ticks_ms()
        if time.ticks_diff(now, last_tick) >= TITLE_TICK_MS:
            last_tick = now
            pos = (pos + 1) % 64
            led_clear()
            for i in range(TITLE_SNAKE_LEN):
                idx = (pos - i) % 64
                r = idx // 8
                c = idx % 8
                level = 90 - i * 18
                if level < 10:
                    level = 10
                led_set_pixel(c, r, level)
        time.sleep_ms(15)


def end_label(reason):
    return {
        "Snake bite": "Out of lives",
        "Quit": "Run quit",
    }.get(reason, reason)


GAME_OVER_X = (
    0b10000001,
    0b01000010,
    0b00100100,
    0b00011000,
    0b00011000,
    0b00100100,
    0b01000010,
    0b10000001,
)


def game_over_screen(score, best, new_best, reason):
    ui.chrome(
        "Game Over",
        "New Best!" if new_best else "Best " + str(best["total"]),
        "OK", "again",
        "BACK", "quit",
    )
    ui.center(15, end_label(reason))
    ui.center(28, "Score " + str(score["total"]))
    ui.center(40, "Length " + str(score["length"]))
    oled_show()

    last_tick = time.ticks_ms()
    bright = 90
    led_set_frame(GAME_OVER_X, bright)
    while True:
        if button_pressed(BTN_CONFIRM):
            led_clear()
            return True
        if button_pressed(BTN_BACK):
            led_clear()
            return False
        now = time.ticks_ms()
        if time.ticks_diff(now, last_tick) >= GAMEOVER_TICK_MS:
            last_tick = now
            bright = 30 if bright > 60 else 110
            led_set_frame(GAME_OVER_X, bright)
        time.sleep_ms(20)


def score_for(game):
    return {
        "total": game["food_count"],
        "length": len(game["snake"]),
    }


def cleanup():
    try:
        oled_invert(False)
    except Exception:
        pass
    try:
        no_tone()
    except Exception:
        pass
    try:
        haptic_off()
    except Exception:
        pass
    led_clear()


def play_run():
    game = new_run()
    while True:
        life_run(game)
        if game["reason"] == "Quit":
            return game
        if game["lives"] <= 1:
            game["lives"] = 0
            return game
        game["lives"] -= 1
        if not with_led_override(continue_screen, game):
            return game
        restart_after_continue(game)


def main():
    best = load_score(SCORE_PATH, {"total": 0, "length": 0})
    if not with_led_override(title_screen, best):
        oled_clear(True)
        cleanup()
        return

    while True:
        game = play_run()
        score = score_for(game)
        new_best = score["total"] > best["total"]
        if new_best:
            best = score
            save_score(SCORE_PATH, best)
        again = with_led_override(game_over_screen, score, best, new_best, game["reason"])
        if not again:
            oled_clear(True)
            cleanup()
            return
