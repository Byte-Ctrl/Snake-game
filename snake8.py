import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

def get_random_color_pair():
    curses.init_pair(10, randint(1, curses.COLORS-1), curses.COLOR_BLACK)
    return curses.color_pair(10)

def display_menu(stdscr, color_pair):
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(5, 5, "Escolha a velocidade:", curses.color_pair(1))
    stdscr.addstr(6, 5, "1 - Muito Lento", curses.color_pair(1))
    stdscr.addstr(7, 5, "2 - Lento", curses.color_pair(1))
    stdscr.addstr(8, 5, "3 - Médio", curses.color_pair(1))
    stdscr.addstr(9, 5, "4 - Rápido", curses.color_pair(1))
    stdscr.addstr(10, 5, "Pressione a tecla correspondente para iniciar...", curses.color_pair(1))
    stdscr.refresh()

    key = stdscr.getch()
    if key == ord('1'):
        return 400
    elif key == ord('2'):
        return 200
    elif key == ord('3'):
        return 100
    elif key == ord('4'):
        return 50
    else:
        return None

def save_score(score):
    with open("snake_scores.txt", "a") as file:
        file.write(str(score) + "\n")

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    sh, sw = stdscr.getmaxyx()
    w = stdscr.subwin(sh-2, sw-2, 1, 1)
    w.keypad(1)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    color_pair = curses.color_pair(1)

    speed = None
    while speed is None:
        speed = display_menu(stdscr, color_pair)

    w.timeout(speed)

    score = 0

    snake = [
        [sh//2, sw//2],
        [sh//2, sw//2-1],
        [sh//2, sw//2-2]
    ]

    food = None
    while food is None:
        food = [
            randint(1, sh-2),
            randint(1, sw-2)
        ]
        if food in snake:
            food = None
    w.addch(food[0], food[1], curses.ACS_PI)

    key = KEY_RIGHT

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        if key in [curses.KEY_RIGHT, ord('d'), ord('D')]:
            key = KEY_RIGHT
        elif key in [curses.KEY_LEFT, ord('a'), ord('A')]:
            key = KEY_LEFT
        elif key in [curses.KEY_UP, ord('w'), ord('W')]:
            key = KEY_UP
        elif key in [curses.KEY_DOWN, ord('s'), ord('S')]:
            key = KEY_DOWN

        if snake[0][0] in [0, sh-3] or \
                snake[0][1] in [0, sw-3] or \
                snake[0] in snake[1:]:
            message = "Game Over! Press 'q' to Quit or 'r' to Restart."
            w.addstr(sh//2, sw//2 - len(message)//2, message)
            save_score(score)
            w.timeout(-1)
            while True:
                choice = w.getch()
                if choice == ord('q'):
                    curses.endwin()
                    quit()
                elif choice == ord('r'):
                    main(stdscr)

        new_head = [snake[0][0], snake[0][1]]

        if key == KEY_DOWN:
            new_head[0] += 1
        if key == KEY_UP:
            new_head[0] -= 1
        if key == KEY_LEFT:
            new_head[1] -= 1
        if key == KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    randint(1, sh-2),
                    randint(1, sw-2)
                ]
                if nf not in snake:
                    food = nf
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
        w.addstr(0, 2, 'Score: ' + str(score), color_pair)
        w.addstr(0, 12, "Mauricio - Dev", curses.color_pair(1))  

curses.wrapper(main)

