from graphics import *
import random

TILE_IMAGE = 'tile.gif'
FLAG_IMAGE = 'flag.gif'
MINE_IMAGE = 'mine.gif'
LOSE_IMAGE = 'lose.gif'
SMILEY_IMAGE = 'smiley.gif'
BLANK_CELL = 0
EXPOSED_CELL = 10
MINE_CELL = 13
MAX_ADJACENT_MINES = 8
WIDTH_OF_IMAGES = 32
HEIGHT_OF_IMAGES = 32
LEFT_OFFSET = 100
RIGHT_OFFSET = 100
TOP_OFFSET = 120
BOTTOM_OFFSET = LEFT_OFFSET // 2
X_OFFSET = LEFT_OFFSET
Y_OFFSET = TOP_OFFSET


def game_mode_option_window():
    window_x = 800  # can be changed if value >= 400
    window_y = 800  # can be changed if value >= 650
    difficulties = ['Beginner', 'Intermediate', 'Expert']

    window = GraphWin("Minesweeper level selection", window_x, window_y, autoflush=False)

    # This part calculates  x, y, width, and height values to get the game choice buttons/text  to be in
    # the middle of the window

    v = False
    i = 1.0
    j = 1.0
    width = 360
    height = 120

    while window_x < width:
        width -= window_x
    while window_y < height:
        height -= window_y

    while not v:
        x = window_x // i
        y = window_y // j
        p1 = Point(x, y)
        p2 = Point(x + width, y + height)
        rect = Rectangle(p1, p2)
        center_of_rectangle = rect.getCenter()
        if center_of_rectangle.getX() != window_x // 2:
            i += .01
        if center_of_rectangle.getY() != window_y // 2:
            j += .01
        if window_x // 2 == center_of_rectangle.getX() and window_y // 2 == center_of_rectangle.getY():
            v = True
    # points are finished calculating

    text(center_of_rectangle.getX(), y - 90, 'Minesweeper', 36, window), text(center_of_rectangle.getX(), y - 40,
                                                                              'Please select game mode', 25, window)
    rectangles = []
    print(len(difficulties))
    for i in range(len(difficulties)):
        rect = selection_screen_rectangles_with_text(x, y, width, height, difficulties, difficulties[i], window)
        rect.draw(window)
        rectangles.append(rect)
        y += height

    window.update()
    mouse_click = window.getMouse()
    click = False
    while not click:
        if is_click_in_rectangle(rectangles[0], mouse_click) is True:
            difficulty_selected = difficulties[0]
            click = True
            window.close()
            return rectangles, difficulty_selected

        if is_click_in_rectangle(rectangles[1], mouse_click) is True:
            difficulty_selected = difficulties[1]
            click = True
            window.close()
            return rectangles, difficulty_selected
        if is_click_in_rectangle(rectangles[2], mouse_click) is True:
            difficulty_selected = difficulties[2]
            click = True
            window.close()
            return rectangles, difficulty_selected
        else:
            mouse_click = window.getMouse()


def selection_screen_rectangles_with_text(x, y, width, height, difficulty_list, difficulty_text, win):
    rectangle = draw_rectangles(x, y, x + width, y + height)
    text_x_position = x + height + (height // 2)
    text_y_position = y + (height // 2)
    for i in range(len(difficulty_list)):
        text(text_x_position, text_y_position, difficulty_text, 28, win)
    return rectangle


def text(x, y, text_wanted, size, win):
    text_colors = ['FireBrick', 'Coral', 'Moccasin', 'DarkSlateBlue', 'PaleVioletRed', 'DarkSeaGreen', 'SteelBlue']
    text_points = Point(x, y)
    text_wanted = Text(text_points, text_wanted)
    text_wanted.setSize(size)
    text_wanted.draw(win)
    choose_random_color_idx = random.randint(0, len(text_colors) - 1)
    text_wanted.setTextColor(text_colors[choose_random_color_idx])


def game_mode_selected(rectangle, mouse_click):
    game_mode = False
    while not game_mode:
        for i in range(len(rectangle)):
            if is_click_in_rectangle(rectangle[i], mouse_click):
                game_mode = True
                return i


def is_click_in_rectangle(rectangle, mouse_click):
    point_1 = rectangle.getP1()
    point_2 = rectangle.getP2()

    if point_1.getX() < mouse_click.getX() < point_2.getX() and point_1.getY() < mouse_click.getY() < point_2.getY():
        return True
    return False


def game_mode_rows(game_type):
    if game_type == 'Beginner':
        rows = 9
        return rows
    if game_type == 'Intermediate':
        rows = 16
        return rows
    if game_type == 'Expert':
        rows = 16
        return rows


def game_mode_columns(game_type):
    if game_type == 'Beginner':
        columns = 9
        return columns
    if game_type == 'Intermediate':
        columns = 16
        return columns
    if game_type == 'Expert':
        columns = 30
        return columns


def game_mode_mines(game_type):
    if game_type == 'Beginner':
        num_mines = 10
        return num_mines
    if game_type == 'Intermediate':
        num_mines = 40
        return num_mines
    if game_type == 'Expert':
        num_mines = 99
        return num_mines


def create_minesweeper_matrix(rows, columns):
    matrix_list = []
    for i in range(rows):
        matrix_list.append([])
        for j in range(columns):
            matrix_list[i].append(0)
    return matrix_list


def print_game_board(minesweeper_matrix):
    for i in range(len(minesweeper_matrix)):
        for j in range(len(minesweeper_matrix[i])):
            print(str(minesweeper_matrix[i][j]).rjust(4), '', end='')
        print()


def populate_with_mines(game_board_matrix, number_of_mines):
    i = 0
    while i < number_of_mines:
        row = random.randint(0, len(game_board_matrix) - 1)
        col = random.randint(0, len(game_board_matrix[0]) - 1)
        if game_board_matrix[row][col] != MINE_CELL:
            game_board_matrix[row][col] = MINE_CELL
            i += 1


def update_neighbor_count(game_board_markers, row, column):
    count = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if 0 <= row + i <= len(game_board_markers) - 1 and 0 <= column + j <= len(game_board_markers[0]) - 1 and \
                            game_board_markers[row + i][column + j] == MINE_CELL:
                count += 1
    if game_board_markers[row][column] >= MINE_CELL:
        count = MINE_CELL
    return count


def add_mine_counts(game_board_markers):
    for i in range(len(game_board_markers)):
        for j in range(len(game_board_markers[i])):
            game_board_markers[i][j] = update_neighbor_count(game_board_markers, i, j)


def draw_rectangles(upper_x, upper_y, lower_x, lower_y):
    point_1 = Point(upper_x, upper_y)
    point_2 = Point(lower_x, lower_y)
    rectangle = Rectangle(point_1, point_2)
    return rectangle


def draw_the_grid(rows, columns, win):
    rectangle_list = []
    x = LEFT_OFFSET
    width_of_rect = TOP_OFFSET + WIDTH_OF_IMAGES

    for i in range(rows):
        rectangle_list.append([])
        y_2 = RIGHT_OFFSET + i * BOTTOM_OFFSET
        for j in range(columns):
            x_2 = width_of_rect + j * BOTTOM_OFFSET
            rectangle = draw_rectangles(x, BOTTOM_OFFSET, x_2, y_2)
            rectangle.draw(win)
            rectangle_list[i].append(rectangle)
            x = x_2
        x = LEFT_OFFSET

    return rectangle_list


def drawings(rectangle_points, wanted_text, type_of_image, win):
    x = rectangle_points.getP1().getX() + WIDTH_OF_IMAGES // 2 + WIDTH_OF_IMAGES // 4
    y = rectangle_points.getP2().getY() - HEIGHT_OF_IMAGES // 2 - HEIGHT_OF_IMAGES // 4
    points = Point(x, y)
    text_wanted = Text(points, wanted_text)
    text_wanted.draw(win)
    image = Image(points, type_of_image)
    image.draw(win)
    return image


def draw_board_images(visual_grid, numerical_grid, rows, columns, win):
    x = LEFT_OFFSET
    y = RIGHT_OFFSET
    width_of_rectangles = TOP_OFFSET + WIDTH_OF_IMAGES
    height_of_rectangles = BOTTOM_OFFSET - HEIGHT_OF_IMAGES

    for i in range(rows):
        text_y_axis = y + (BOTTOM_OFFSET - y) // 2
        text_x_axis = LEFT_OFFSET - WIDTH_OF_IMAGES // 4
        text(text_x_axis, text_y_axis, i, 12, win)
        y += RIGHT_OFFSET

    for i in range(columns):
        text_y_axis = HEIGHT_OF_IMAGES + height_of_rectangles // 2
        text_x_axis = x + (width_of_rectangles - x) // 2

        text(text_x_axis, text_y_axis, i, 12, win)

        x += LEFT_OFFSET

    tile_list = []
    mine_list = []

    for i in range(len(numerical_grid)):
        tile_list.append([])
        mine_list.append([])
        for j in range(len(numerical_grid[i])):
            if numerical_grid[i][j] == MINE_CELL:
                rectangle_points = visual_grid[i][j]
                mine_cell = drawings(rectangle_points, '', MINE_IMAGE, win)
                tile_cell = drawings(rectangle_points, '', TILE_IMAGE, win)
                tile_list[i].append(tile_cell)
                mine_list[i].append(tile_cell)
            if numerical_grid[i][j] != BLANK_CELL and numerical_grid[i][j] != MINE_CELL:
                rectangle_points = visual_grid[i][j]
                mines_adjacent_text = drawings(rectangle_points, numerical_grid[i][j], '', win)
                tile_cell = drawings(rectangle_points, '', TILE_IMAGE, win)
                tile_list[i].append(tile_cell)
            if numerical_grid[i][j] == BLANK_CELL:
                rectangle_points = visual_grid[i][j]
                tile_cell = drawings(rectangle_points, '', TILE_IMAGE, win)
                tile_list[i].append(tile_cell)

    win.update()

    return tile_list, mine_list


def remove_image(rectangles, tile_list, numerical_grid, mines, row, col, mouse_click):
    bomb_clicked = False
    row_clicked = ((mouse_click.getY()) // BOTTOM_OFFSET) - 1
    col_clicked = ((mouse_click.getX()) // 50) - 2
    if -1 < row_clicked < row and -1 < col_clicked <= col - 1:
        cell, total, expose = expose_cell(rectangles[row_clicked][col_clicked], row_clicked, col_clicked,
                                          numerical_grid, tile_list, mines,
                                          mouse_click)
        if cell:
            bomb_clicked = True
        return bomb_clicked, total, expose


def expose_cell(rectangle, row, col, numerical_grid, tile_list, mines, mouse_click):
    game_over = False
    v = is_click_in_rectangle(rectangle, mouse_click)
    total = 0
    exposed = False

    if v and numerical_grid[row][col] == MINE_CELL:
        game_over = True
        for i in range(len(mines)):
            for j in range(len(mines[i])):
                mines[i][j].undraw()

    if v and numerical_grid[row][col] == BLANK_CELL:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= row + i <= len(numerical_grid) - 1 and 0 <= col + j <= len(numerical_grid[0]) - 1:
                    z = check_neighbor_is_zero_and_un_draw(numerical_grid, tile_list, row + i, col)
                    q = check_neighbor_is_zero_and_un_draw(numerical_grid, tile_list, row, col + j)
                    r = check_neighbor_is_zero_and_un_draw(numerical_grid, tile_list, row + i, col + j)
                    sum = z + q + r
                    total += sum

    if v and numerical_grid[row][col] == EXPOSED_CELL:
        exposed = True

    if v and numerical_grid[row][col] != BLANK_CELL and numerical_grid[row][col] != MINE_CELL:
        numerical_grid[row][col] = EXPOSED_CELL
        tile_list[row][col].undraw()
    return game_over, total, exposed


def check_neighbor_is_zero_and_un_draw(numerical_grid, tile_list, row, col):
    i = 0
    if numerical_grid[row][col] == 0:
        tile_list[row][col].undraw()
        numerical_grid[row][col] = EXPOSED_CELL
        i = 1
    return i


def is_game_over(rectangles, tile_list, numerical_grid, mines, window, row, col, num_mines):
    i = 0
    number_of_possible_clicks = row * col - num_mines
    did_they_win = False
    while i < number_of_possible_clicks:
        mouse_click = window.getMouse()
        bomb_click, total, expose = remove_image(rectangles, tile_list, numerical_grid, mines, row, col,
                                                 mouse_click)
        if bomb_click:
            i = number_of_possible_clicks
        if total > 0:
            number_of_possible_clicks -= total
            continue
        if not expose:
            i += 1
    if bomb_click:
        return did_they_win
    else:
        did_they_win = True
        return did_they_win


def game_over(did_they_win,window_x,window_y, window):
    points_for_image = Point((window_x + 40) - window_x, (window_y + 40) - window_y)
    points_for_text = Point((window_x + 40) - window_x,  (window_y + 100) - window_y)
    if did_they_win:
        image = Image(points_for_image, SMILEY_IMAGE)
        text_wanted = Text(points_for_text, 'You won!')
        image.draw(window)
        text_wanted.draw(window)
        window.getMouse()
        window.close()
    else:
        image = Image(points_for_image,LOSE_IMAGE)
        text_wanted = Text(points_for_text, 'You lost!')
        image.draw(window)
        text_wanted.draw(window)
        window.getMouse()
        window.close()

def main():
    game_mode_rectangles, game_type = game_mode_option_window()
    window_x = 0
    window_y = 0
    game_mode = ''
    if game_type == 'Beginner':
        window_x = 600
        window_y = 540
        game_mode = 'Minesweeper:Beginner'
    if game_type == 'Intermediate':
        window_x = 990
        window_y = 916
        game_mode = "Minesweeper:Intermediate"
    if game_type == 'Expert':
        window_x = 1680
        window_y = 916
        game_mode = 'Minesweeper:Expert'

    win = GraphWin(game_mode, window_x, window_y, autoflush=False)
    rows = game_mode_rows(game_type)
    columns = game_mode_columns(game_type)
    num_mines = game_mode_mines(game_type)
    minesweeper_matrix = create_minesweeper_matrix(rows, columns)
    populate_with_mines(minesweeper_matrix, num_mines)
    add_mine_counts(minesweeper_matrix)
    print_game_board(minesweeper_matrix)
    visual_grid = draw_the_grid(rows, columns, win)
    tiles, mines = draw_board_images(visual_grid, minesweeper_matrix, rows, columns, win)
    did_they_win = is_game_over(visual_grid, tiles, minesweeper_matrix, mines, win, rows, columns, num_mines)
    game_over(did_they_win, window_x,window_y, win)
    win.close
main()