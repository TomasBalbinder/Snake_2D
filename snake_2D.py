'''First game with uses framework Pyglet'''


import random
import pyglet
from pyglet.window import key

window = pyglet.window.Window(width=1000, height=1000)
pyglet.gl.glClearColor(0.5,0,2,1)


load_flower = pyglet.image.load("flower.png")
load_snake_begin = pyglet.image.load("snake1.png")
load_snake_center = pyglet.image.load("snake2.png")
load_snake_end = pyglet.image.load("snake3.png")
load_background = pyglet.image.load("background.png")

for img in (load_snake_begin, load_snake_center, load_snake_end, load_flower, load_background):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2


flower = pyglet.sprite.Sprite(load_flower)
snake_begin = pyglet.sprite.Sprite(load_snake_begin)
snake_end = pyglet.sprite.Sprite(load_snake_end)
background = pyglet.sprite.Sprite(load_background)

snake = [snake_begin, snake_end]

interval = 1/1
score = 0


flower.position = 150, 150
snake_begin.x = 450
snake_begin.y = 450
background.position = 500, 500

snake_end.x = snake_begin.x
snake_end.y = snake_begin.y - 100

snake_extension = False


def orientation(symbol, modifier):
    global snake_extension

    if symbol == key.D:
        snake_begin.rotation = snake_begin.rotation + 90
        if snake_begin.rotation > 270 :
            snake_begin.rotation = 0

    if symbol == key.A:
        snake_begin.rotation = snake_begin.rotation - 90
        if snake_begin.rotation < 0:
            snake_begin.rotation = 270


def snake_move(t):
    global snake_extension, end, label, score, interval

    if snake_extension:
        snake_extension = False
        new_part = pyglet.sprite.Sprite(load_snake_center)
        new_part.x = snake_begin.x
        new_part.y = snake_begin.y
        new_part.rotation = snake_begin.rotation
        snake.insert(1, new_part)

    else:
        for idx_changing in reversed(range(1, len(snake))):

            idx_source = idx_changing - 1
            changing_part = snake[idx_changing]
            source_part = snake[idx_source]
            changing_part.x = source_part.x
            changing_part.y = source_part.y
            changing_part.rotation = source_part.rotation


    if snake_begin.rotation == 0:
        snake_begin.y = snake_begin.y + 100

    if snake_begin.rotation == 90:
        snake_begin.x = snake_begin.x + 100

    if snake_begin.rotation == 180:
        snake_begin.y = snake_begin.y - 100

    if snake_begin.rotation == 270:
        snake_begin.x = snake_begin.x - 100

    for i in snake[1:]:
        if snake_begin.position == i.position:
            exit("game over")

    if snake_begin.x < 0 or snake_begin.y < 0 or snake_begin.x > 1000 or snake_begin.y > 1000 :
        exit("game over")


    coordinates_x = []
    coordinates_y = []

    if snake_begin.position == flower.position:

        score = score + 1
        label.text = f"Score {str(score)}"
        pyglet.clock.unschedule(snake_move)

        interval = interval * 0.9
        pyglet.clock.schedule_interval(snake_move, interval)

        snake_extension = True
        flower.opacity = 0

        for x, y in zip(range(50, 950, 100), range(50, 950, 100)):
            coordinates_x.append(x)
            coordinates_y.append(y)

        flower.x = random.choice(coordinates_x)
        flower.y = random.choice(coordinates_y)
        flower.opacity = 500



label = pyglet.text.Label(f'Score {str(score)}',

                          font_name='Times New Roman',
                          font_size=25,
                          x=100, y=980,
                          anchor_x='center', anchor_y='center')

mandarinka = pyglet.clock.schedule_interval(snake_move, 1/1)

def display():

    window.clear()
    background.draw()
    flower.draw()
    for i in snake:
        i.draw()
    label.draw()


window.push_handlers(
                     on_draw=display,
                     on_key_press=orientation)

pyglet.app.run()
