import math

position = [19, 19]  # out of range of the board
player, opponent = "", ""
time = 0
captured_W, captured_B = 0, 0
board = [["."] * 19 for _ in range(19)]
maxDepth = 1
center = 9  # center of rows and cols


def game_is_over(imaging_captured_W: int, imaging_captured_B: int) -> bool:
    global player
    if (player == "b" and imaging_captured_W + captured_W >= 10) or (player == "w" and imaging_captured_B + captured_B >= 10):
        return True
    return False


def white_is_first_step_or_second_step(board: list) -> int:
    count_W = 0
    count_B = 0
    for i in range(19):
        for j in range(19):
            if board[i][j] == "w":
                count_W += 1
            elif board[i][j] == "b":
                count_B += 1
    if count_W == 0 and count_B == 0:
        return 0  # it's first step
    elif count_W == 1 and count_B == 1:
        return 1  # it's second step
    return -1


def surrounding_empty(x: int, y: int, board: list) -> bool:
    global maxDepth
    for i in range(x - maxDepth, x + maxDepth + 1):
        for j in range(y - maxDepth, y + maxDepth + 1):
            if (0 <= i < 19 and 0 <= j < 19 and board[i][j] != "."):
                return False
    return True


def after_move(x: int, y: int, board: list, imaging_captured_W: int, imaging_captured_B: int) -> list:
    # update imaging_captured_W, imaging_captured_B, return updated board
    # Check rows
    if (y - 3 >= 0 and board[x][y] != "." and board[x][y - 1] != "." and board[x][y - 2] != "." and board[x][y - 3] != "."):
        if (board[x][y] != board[x][y - 1] and board[x][y] == board[x][y - 3] and board[x][y - 1] == board[x][y - 2]):
            if board[x][y] == "b":
                imaging_captured_W += 2
            else:
                imaging_captured_B += 2
            board[x][y - 1] = "."
            board[x][y - 2] = "."

    if (y + 3 < 19 and board[x][y] != "." and board[x][y + 1] != "." and board[x][y + 2] != "." and board[x][y + 3] != "."):
        if (board[x][y] != board[x][y + 1] and board[x][y] == board[x][y + 3] and board[x][y + 1] == board[x][y + 2]):
            # print(x, y, board[x][y], board[x][y + 1],
            #       board[x][y + 2], board[x][y + 3])
            if board[x][y] == "b":
                imaging_captured_W += 2
            else:
                imaging_captured_B += 2
            board[x][y + 1] = "."
            board[x][y + 2] = "."

    # Check columns
    if (x - 3 >= 0 and board[x][y] != "." and board[x - 1][y] != "." and board[x - 2][y] != "." and board[x - 3][y] != "."):
        if (board[x][y] != board[x - 1][y] and board[x][y] == board[x - 3][y] and board[x - 1][y] == board[x - 2][y]):
            if board[x][y] == "b":
                imaging_captured_W += 2
            else:
                imaging_captured_B += 2
            board[x - 1][y] = "."
            board[x - 2][y] = "."

    if (x + 3 < 19 and board[x][y] != "." and board[x + 1][y] != "." and board[x + 2][y] != "." and board[x + 3][y] != "."):
        if (board[x][y] != board[x + 1][y] and board[x][y] == board[x + 3][y] and board[x + 1][y] == board[x + 2][y]):
            if board[x][y] == "b":
                imaging_captured_W += 2
            else:
                imaging_captured_B += 2
            board[x + 1][y] = "."
            board[x + 2][y] = "."

    # Check diagonals
    if (x - 3 >= 0 and y - 3 >= 0 and board[x][y] != "." and board[x - 1][y - 1] != "." and board[x - 2][y - 2] != "." and board[x - 3][y - 3] != "."):
        if (board[x][y] != board[x - 1][y - 1] and board[x][y] == board[x - 3][y - 3] and board[x - 1][y - 1] == board[x - 2][y - 2]):
            if board[x][y] == "b":
                imaging_captured_W += 2
            else:
                imaging_captured_B += 2
            board[x - 1][y - 1] = "."
            board[x - 2][y - 2] = "."

    if (x - 3 >= 0 and y + 3 < 19 and board[x][y] != "." and board[x - 1][y + 1] != "." and board[x - 2][y + 2] != "." and board[x - 3][y + 3] != "."):
        if (board[x][y] != board[x - 1][y + 1] and board[x][y] == board[x - 3][y + 3] and board[x - 1][y + 1] == board[x - 2][y + 2]):
            if board[x][y] == "b":
                imaging_captured_W += 2
            else:
                imaging_captured_B += 2
            board[x - 1][y + 1] = "."
            board[x - 2][y + 2] = "."

    if (x + 3 < 19 and y - 3 >= 0 and board[x][y] != "." and board[x + 1][y - 1] != "." and board[x + 2][y - 2] != "." and board[x + 3][y - 3] != "."):
        if (board[x][y] != board[x + 1][y - 1] and board[x][y] == board[x + 3][y - 3] and board[x + 1][y - 1] == board[x + 2][y - 2]):
            if board[x][y] == "b":
                imaging_captured_W += 2
            else:
                imaging_captured_B += 2
            board[x + 1][y - 1] = "."
            board[x + 2][y - 2] = "."

    if (x + 3 < 19 and y + 3 < 19 and board[x][y] != "." and board[x + 1][y + 1] != "." and board[x + 2][y + 2] != "." and board[x + 3][y + 3] != "."):
        if (board[x][y] != board[x + 1][y + 1] and board[x][y] == board[x + 3][y + 3] and board[x + 1][y + 1] == board[x + 2][y + 2]):
            if board[x][y] == "b":
                imaging_captured_W += 2
            else:
                imaging_captured_B += 2
            board[x + 1][y + 1] = "."
            board[x + 2][y + 2] = "."

    return board, imaging_captured_W, imaging_captured_B


def find_stone_shapes(input: list, attacker: str) -> int:
    # input[0] == "b" or "w"
    # input[0] == attacker: length == 5, 4, 3, 2
    # input[0] != attacker: length == 4, 3
    if attacker == "b":
        defender = "w"
    else:
        defender = "b"
    if input[0] == attacker:
        if len(input) == 5:
            win = [attacker, attacker, attacker, attacker, attacker]
            if input == win:
                return 10
            shapes_seven = [
                [attacker, ".", attacker, attacker, attacker],
                [attacker, attacker, ".", attacker, attacker],
                [attacker, attacker, attacker, ".", attacker]
            ]
            if input in shapes_seven:
                return 1
            return 0
        if len(input) == 4:
            special = [attacker, defender, defender, attacker]
            if input == special:
                return 9
            shapes_six_attack_l1 = [
                [attacker, ".", attacker, attacker],
                [attacker, attacker, ".", attacker]
            ]
            if input in shapes_six_attack_l1:
                return 1
            if input == [attacker, attacker, attacker, attacker]:
                return 2
            return 0
        if len(input) == 3:
            if input == [attacker, attacker, attacker]:
                return 1
            return 0
        if len(input) == 2:
            if input == [attacker, attacker]:
                return 1
    else:
        if len(input) == 4:
            if input == [defender, defender, defender, defender]:
                return -1
            return 0
        if len(input) == 3:
            if input == [defender, defender, defender]:
                return -1
            return 0
    return 0


def is_target(board: list, x: int, y: int, target_1: str, target_2: str) -> bool:
    return 0 <= x < 19 and 0 <= y < 19 and (board[x][y] == target_1 or board[x][y] == target_2)


def scan_whole_board(board: list, color: str) -> list:
    if color == "b":
        anti = "w"
    else:
        anti = "b"
    # [win, four_open, four_open_jump, four_close, four_close_jump, three_open, three_open_jump, three_close, three_close_jump, two_open, two_close(be_captured), four_defend, four_defend_half, three_defend, three_defend_half, special(capture)]
    count_stone_shapes = [0] * 16
    # horizontal lines
    for i in range(19):
        start = 0
        while start < 19:
            while board[i][start] == "." and start + 1 < 19:
                start += 1
            if board[i][start] == color:  # attacker, input length is 5/4/3/2
                res = 0

                if start + 4 < 19:  # input length == 5
                    input = board[i][start: start + 5]
                    res = find_stone_shapes(input, color)

                    if res == 10:  # win
                        count_stone_shapes[0] += 1
                        start += 5
                        continue

                    if res == 1:  # jump four
                        # four_open_jump
                        if start - 1 >= 0 and start + 5 < 19 and board[i][start - 1] == "." and board[i][start + 5] == ".":
                            count_stone_shapes[2] += 1
                            start += 6
                            continue
                        # four_close_jump
                        if (((start - 1 >= 0 and board[i][start - 1] == anti) or start - 1 < 0) and (start + 5 < 19 and board[i][start + 5] == ".")) or ((start - 1 >= 0 and board[i][start - 1] == ".") and (start + 5 >= 19 or (start + 5 < 19 and board[i][start + 5] == anti))):
                            count_stone_shapes[4] += 1
                            start += 6
                            continue

                if start + 3 < 19:  # input length == 4
                    input = board[i][start: start + 4]
                    res = find_stone_shapes(input, color)

                    if res == 9:  # special
                        count_stone_shapes[15] += 1
                        start += 4
                        continue
                    if res == 1:  # jump three
                        # three_open_jump
                        if start - 1 >= 0 and start + 4 < 19 and board[i][start - 1] == "." and board[i][start + 4] == ".":
                            count_stone_shapes[6] += 1
                            start += 5
                            continue
                        if (((start - 1 >= 0 and board[i][start - 1] == anti) or start - 1 < 0) and (start + 4 < 19 and board[i][start + 4] == ".")) or ((start - 1 >= 0 and board[i][start - 1] == ".") and (start + 4 >= 19 or (start + 4 < 19 and board[i][start + 4] == anti))):  # three_close_jump
                            count_stone_shapes[8] += 1
                            start += 5
                            continue
                    if res == 2:  # four
                        # four_open
                        if start - 1 >= 0 and start + 4 < 19 and board[i][start - 1] == "." and board[i][start + 4] == ".":
                            count_stone_shapes[1] += 1
                            start += 5
                            continue
                        if (((start - 1 >= 0 and board[i][start - 1] == anti) or start - 1 < 0) and (start + 4 < 19 and board[i][start + 4] == ".")) or ((start - 1 >= 0 and board[i][start - 1] == ".") and (start + 4 >= 19 or (start + 4 < 19 and board[i][start + 4] == anti))):  # four_close
                            count_stone_shapes[3] += 1
                            start += 5
                            continue

                if start + 2 < 19:  # input length == 3
                    input = board[i][start: start + 3]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # three
                        # three_open
                        if start - 1 >= 0 and start + 3 < 19 and board[i][start - 1] == "." and board[i][start + 3] == ".":
                            count_stone_shapes[5] += 1
                            start += 4
                            continue
                        if (((start - 1 >= 0 and board[i][start - 1] == anti) or start - 1 < 0) and (start + 3 < 19 and board[i][start + 3] == ".")) or ((start - 1 >= 0 and board[i][start - 1] == ".") and (start + 3 >= 19 or (start + 3 < 19 and board[i][start + 3] == anti))):  # three_close
                            count_stone_shapes[7] += 1
                            start += 4
                            continue

                if start + 1 < 19:  # input length == 2
                    input = board[i][start: start + 2]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # two
                        # two open
                        if start - 1 >= 0 and start + 2 < 19 and board[i][start - 1] == "." and board[i][start + 2] == ".":
                            count_stone_shapes[9] += 1
                            start += 3
                            continue
                        if (((start - 1 >= 0 and board[i][start - 1] == anti) or start - 1 < 0) and (start + 2 < 19 and board[i][start + 2] == ".")) or ((start - 1 >= 0 and board[i][start - 1] == ".") and (start + 2 >= 19 or (start + 2 < 19 and board[i][start + 2] == anti))):  # two_close
                            count_stone_shapes[10] += 1
                            start += 3
                            continue

            else:  # not attacker, input length is 4/3
                if start + 3 < 19:  # input length == 4
                    input = board[i][start: start + 4]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: four
                        # four defend
                        if start - 1 >= 0 and start + 4 < 19 and board[i][start - 1] == color and board[i][start + 4] == color:
                            count_stone_shapes[11] += 1
                            start += 5
                            continue
                        if (((start - 1 >= 0 and board[i][start - 1] == color) or start - 1 < 0) and (start + 4 < 19 and board[i][start + 4] == ".")) or ((start - 1 >= 0 and board[i][start - 1] == ".") and (start + 4 >= 19 or (start + 4 < 19 and board[i][start + 4] == color))):  # four_defend_half
                            count_stone_shapes[12] += 1
                            start += 5
                            continue

                if start + 2 < 19:  # input length == 3
                    input = board[i][start: start + 3]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: three
                        # three defend
                        if start - 1 >= 0 and start + 3 < 19 and board[i][start - 1] == color and board[i][start + 3] == color:
                            count_stone_shapes[13] += 1
                            start += 4
                            continue
                        if (((start - 1 >= 0 and board[i][start - 1] == color) or start - 1 < 0) and (start + 3 < 19 and board[i][start + 3] == ".")) or ((start - 1 >= 0 and board[i][start - 1] == ".") and (start + 3 >= 19 or (start + 3 < 19 and board[i][start + 3] == color))):  # three_defend_half
                            count_stone_shapes[14] += 1
                            start += 4
                            continue

            start += 1

    # vertical
    for j in range(19):
        start = 0
        while start < 19:
            while board[start][j] == "." and start + 1 < 19:
                start += 1
            if board[start][j] == color:  # attacker, input length is 5/4/3/2
                res = 0

                if start + 4 < 19:  # input length == 5
                    input = [board[start][j], board[start + 1][j], board[start + 2][j], board[start + 3]
                             [j], board[start + 4][j]]
                    res = find_stone_shapes(input, color)

                    if res == 10:  # win
                        count_stone_shapes[0] += 1
                        start += 5
                        continue

                    if res == 1:  # jump four
                        # four_open_jump
                        if start - 1 >= 0 and start + 5 < 19 and board[start - 1][j] == "." and board[start + 5][j] == ".":
                            count_stone_shapes[2] += 1
                            start += 6
                            continue
                        # four_close_jump
                        if (((start - 1 >= 0 and board[start - 1][j] == anti) or start - 1 < 0) and (start + 5 < 19 and board[start + 5][j] == ".")) or ((start - 1 >= 0 and board[start - 1][j] == ".") and (start + 5 >= 19 or (start + 5 < 19 and board[start + 5][j] == anti))):
                            count_stone_shapes[4] += 1
                            start += 6
                            continue

                if start + 3 < 19:  # input length == 4
                    input = [board[start][j], board[start + 1][j], board[start + 2][j], board[start + 3]
                             [j]]
                    res = find_stone_shapes(input, color)

                    if res == 9:  # special
                        count_stone_shapes[15] += 1
                        start += 4
                        continue
                    if res == 1:  # jump three
                        # three_open_jump
                        if start - 1 >= 0 and start + 4 < 19 and board[start - 1][j] == "." and board[start + 4][j] == ".":
                            count_stone_shapes[6] += 1
                            start += 5
                            continue
                        if (((start - 1 >= 0 and board[start - 1][j] == anti) or start - 1 < 0) and (start + 4 < 19 and board[start + 4][j] == ".")) or ((start - 1 >= 0 and board[start - 1][j] == ".") and (start + 4 >= 19 or (start + 4 < 19 and board[start + 4][j] == anti))):  # three_close_jump
                            count_stone_shapes[8] += 1
                            start += 5
                            continue
                    if res == 2:  # four
                        # four_open
                        if start - 1 >= 0 and start + 4 < 19 and board[start - 1][j] == "." and board[start + 4][j] == ".":
                            count_stone_shapes[1] += 1
                            start += 5
                            continue
                        if (((start - 1 >= 0 and board[start - 1][j] == anti) or start - 1 < 0) and (start + 4 < 19 and board[start + 4][j] == ".")) or ((start - 1 >= 0 and board[start - 1][j] == ".") and (start + 4 >= 19 or (start + 4 < 19 and board[start + 4][j] == anti))):  # four_close
                            count_stone_shapes[3] += 1
                            start += 5
                            continue

                if start + 2 < 19:  # input length == 3
                    input = [board[start][j], board[start + 1]
                             [j], board[start + 2][j]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # three
                        # three_open
                        if start - 1 >= 0 and start + 3 < 19 and board[start - 1][j] == "." and board[start + 3][j] == ".":
                            count_stone_shapes[5] += 1
                            start += 4
                            continue
                        if (((start - 1 >= 0 and board[start - 1][j] == anti) or start - 1 < 0) and (start + 3 < 19 and board[start + 3][j] == ".")) or ((start - 1 >= 0 and board[start - 1][j] == ".") and (start + 3 >= 19 or (start + 3 < 19 and board[start + 3][j] == anti))):  # three_close
                            count_stone_shapes[7] += 1
                            start += 4
                            continue

                if start + 1 < 19:  # input length == 2
                    input = [board[start][j], board[start + 1][j]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # two
                        # two open
                        if start - 1 >= 0 and start + 2 < 19 and board[start - 1][j] == "." and board[start + 2][j] == ".":
                            count_stone_shapes[9] += 1
                            start += 3
                            continue
                        if (((start - 1 >= 0 and board[start - 1][j] == anti) or start - 1 < 0) and (start + 2 < 19 and board[start + 2][j] == ".")) or ((start - 1 >= 0 and board[start - 1][j] == ".") and (start + 2 >= 19 or (start + 2 < 19 and board[start + 2][j] == anti))):  # two_close
                            count_stone_shapes[10] += 1
                            start += 3
                            continue

            else:  # not attacker, input length is 4/3
                if start + 3 < 19:  # input length == 4
                    input = [board[start][j], board[start + 1][j], board[start + 2][j], board[start + 3]
                             [j]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: four
                        # four defend
                        if start - 1 >= 0 and start + 4 < 19 and board[start - 1][j] == color and board[start + 4][j] == color:
                            count_stone_shapes[11] += 1
                            start += 5
                            continue
                        if (((start - 1 >= 0 and board[start - 1][j] == color) or start - 1 < 0) and (start + 4 < 19 and board[start + 4][j] == ".")) or ((start - 1 >= 0 and board[start - 1][j] == ".") and (start + 4 >= 19 or (start + 4 < 19 and board[start + 4][j] == color))):  # four_defend_half
                            count_stone_shapes[12] += 1
                            start += 5
                            continue

                if start + 2 < 19:  # input length == 3
                    input = [board[start][j], board[start + 1]
                             [j], board[start + 2][j]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: three
                        # three defend
                        if start - 1 >= 0 and start + 3 < 19 and board[start - 1][j] == color and board[start + 3][j] == color:
                            count_stone_shapes[13] += 1
                            start += 4
                            continue
                        if (((start - 1 >= 0 and board[start - 1][j] == color) or start - 1 < 0) and (start + 3 < 19 and board[start + 3][j] == ".")) or ((start - 1 >= 0 and board[start - 1][j] == ".") and (start + 3 >= 19 or (start + 3 < 19 and board[start + 3][j] == color))):  # three_defend_half
                            count_stone_shapes[14] += 1
                            start += 4
                            continue

            start += 1

    # diagonal
    for i in range(1, 19):
        start = 0
        while i - start >= 0 and start < 19:
            while board[i - start][start] == "." and i - (start + 1) >= 0:
                start += 1
            if board[i - start][start] == color:  # attacker, input length is 5/4/3/2
                res = 0

                if i - (start + 4) >= 0 and start + 4 < 19:  # input length == 5
                    input = [board[i - start][start], board[i - (start + 1)][start + 1], board[i - (start + 2)][start + 2], board[i - (start + 3)]
                             [start + 3], board[i - (start + 4)][start + 4]]
                    res = find_stone_shapes(input, color)

                    if res == 10:  # win
                        count_stone_shapes[0] += 1
                        start += 5
                        continue

                    if res == 1:  # jump four
                        # four_open_jump
                        if is_target(board, i - (start - 1), start - 1, ".", ".") and is_target(board, i - (start + 5), start + 5, ".", "."):
                            count_stone_shapes[2] += 1
                            start += 6
                            continue
                        # four_close_jump
                        if (not is_target(board, i - (start - 1), start - 1, ".", color) and is_target(board, i - (start + 5), start + 5, ".", ".")) or (is_target(board, i - (start - 1), start - 1, ".", color) and not is_target(board, i - (start + 5), start + 5, ".", color)):
                            count_stone_shapes[4] += 1
                            start += 6
                            continue

                if i - (start + 3) >= 0 and start + 3 < 19:  # input length == 4
                    input = [board[i - start][start], board[i - (start + 1)][start + 1], board[i - (start + 2)][start + 2], board[i - (start + 3)]
                             [start + 3]]
                    res = find_stone_shapes(input, color)

                    if res == 9:  # special
                        count_stone_shapes[15] += 1
                        start += 4
                        continue
                    if res == 1:  # jump three
                        # three_open_jump
                        if is_target(board, i - (start - 1), start - 1, ".", ".") and is_target(board, i - (start + 4), start + 4, ".", "."):
                            count_stone_shapes[6] += 1
                            start += 5
                            continue
                        if (not is_target(board, i - (start - 1), start - 1, ".", color) and is_target(board, i - (start + 4), start + 4, ".", ".")) or (is_target(board, i - (start - 1), start - 1, ".", color) and not is_target(board, i - (start + 5), start + 5, ".", color)):  # three_close_jump
                            count_stone_shapes[8] += 1
                            start += 5
                            continue
                    if res == 2:  # four
                        # four_open
                        if is_target(board, i - (start - 1), start - 1, ".", ".") and is_target(board, i - (start + 4), start + 4, ".", "."):
                            count_stone_shapes[1] += 1
                            start += 5
                            continue
                        if (not is_target(board, i - (start - 1), start - 1, ".", color) and is_target(board, i - (start + 4), start + 4, ".", ".")) or (is_target(board, i - (start - 1), start - 1, ".", color) and not is_target(board, i - (start + 4), start + 4, ".", color)):  # four_close
                            count_stone_shapes[3] += 1
                            start += 5
                            continue

                if i - (start + 2) >= 0 and start + 2 < 19:  # input length == 3
                    input = [board[i - start][start], board[i -
                                                            (start + 1)][start + 1], board[i - (start + 2)][start + 2]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # three
                        # three_open
                        if is_target(board, i - (start - 1), start - 1, ".", ".") and is_target(board, i - (start + 3), start + 3, ".", "."):
                            count_stone_shapes[5] += 1
                            start += 4
                            continue
                        if (not is_target(board, i - (start - 1), start - 1, ".", color) and is_target(board, i - (start + 3), start + 3, ".", ".")) or (is_target(board, i - (start - 1), start - 1, ".", color) and not is_target(board, i - (start + 3), start + 3, ".", color)):   # three_close
                            count_stone_shapes[7] += 1
                            start += 4
                            continue

                if i - (start + 1) >= 0 and start + 1 < 19:  # input length == 2
                    input = [board[i - start][start],
                             board[i - (start + 1)][start + 1]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # two
                        # two open
                        if is_target(board, i - (start - 1), start - 1, ".", ".") and is_target(board, i - (start + 2), start + 2, ".", "."):
                            count_stone_shapes[9] += 1
                            start += 3
                            continue
                        if (not is_target(board, i - (start - 1), start - 1, ".", color) and is_target(board, i - (start + 2), start + 2, ".", ".")) or (is_target(board, i - (start - 1), start - 1, ".", ".") and not is_target(board, i - (start + 2), start + 2, ".", color)):   # two_close
                            count_stone_shapes[10] += 1
                            start += 3
                            continue

            else:  # not attacker, input length is 4/3
                if i - (start + 3) >= 0 and start + 3 < 19:  # input length == 4
                    input = [board[i - start][start], board[i - (start + 1)][start + 1], board[i - (start + 2)][start + 2], board[i - (start + 3)]
                             [start + 3]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: four
                        # four defend
                        if is_target(board, i - (start - 1), start - 1, color, color) and is_target(board, i - (start + 4), start + 4, color, color):
                            count_stone_shapes[11] += 1
                            start += 5
                            continue
                        if (is_target(board, i - (start - 1), start - 1, ".", anti) and is_target(board, i - (start + 4), start + 4, color, color)) or (is_target(board, i - (start - 1), start - 1, color, color) and is_target(board, i - (start + 4), start + 4, ".", anti)):  # four_defend_half
                            count_stone_shapes[12] += 1
                            start += 5
                            continue

                if i - (start + 2) >= 0 and start + 2 < 19:  # input length == 3
                    input = [board[i - start][start], board[i -
                                                            (start + 1)][start + 1], board[i - (start + 2)][start + 2]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: three
                        # three defend
                        if is_target(board, i - (start - 1), start - 1, color, color) and is_target(board, i - (start + 3), start + 3, color, color):
                            count_stone_shapes[13] += 1
                            start += 4
                            continue
                        if (is_target(board, i - (start - 1), start - 1, ".", anti) and is_target(board, i - (start + 3), start + 3, color, color)) or (is_target(board, i - (start - 1), start - 1, color, color) and is_target(board, i - (start + 3), start + 3, ".", anti)):  # three_defend_half
                            count_stone_shapes[14] += 1
                            start += 4
                            continue

            start += 1

        start = 0
        while i + start < 19 and start < 19:
            while board[i + start][start] == "." and i + (start + 1) < 19:
                start += 1
            if board[i + start][start] == color:  # attacker, input length is 5/4/3/2
                res = 0

                if i + (start + 4) < 19 and start + 4 < 19:  # input length == 5
                    input = [board[i + start][start], board[i + (start + 1)][start + 1], board[i + (start + 2)][start + 2], board[i + (start + 3)]
                             [start + 3], board[i + (start + 4)][start + 4]]
                    res = find_stone_shapes(input, color)

                    if res == 10:  # win
                        count_stone_shapes[0] += 1
                        start += 5
                        continue

                    if res == 1:  # jump four
                        # four_open_jump
                        if is_target(board, i + (start - 1), start - 1, ".", ".") and is_target(board, i + (start + 5), start + 5, ".", "."):
                            count_stone_shapes[2] += 1
                            start += 6
                            continue
                        # four_close_jump
                        if (not is_target(board, i + (start - 1), start - 1, ".", color) and is_target(board, i + (start + 5), start + 5, ".", ".")) or (is_target(board, i + (start - 1), start - 1, ".", color) and not is_target(board, i + (start + 5), start + 5, ".", color)):
                            count_stone_shapes[4] += 1
                            start += 6
                            continue

                if i + (start + 3) < 19 and start + 3 < 19:  # input length == 4
                    input = [board[i + start][start], board[i + (start + 1)][start + 1], board[i + (start + 2)][start + 2], board[i + (start + 3)]
                             [start + 3]]
                    res = find_stone_shapes(input, color)

                    if res == 9:  # special
                        count_stone_shapes[15] += 1
                        start += 4
                        continue
                    if res == 1:  # jump three
                        # three_open_jump
                        if is_target(board, i + (start - 1), start - 1, ".", ".") and is_target(board, i + (start + 4), start + 4, ".", "."):
                            count_stone_shapes[6] += 1
                            start += 5
                            continue
                        if (not is_target(board, i + (start - 1), start - 1, ".", color) and is_target(board, i + (start + 4), start + 4, ".", ".")) or (is_target(board, i + (start - 1), start - 1, ".", color) and not is_target(board, i + (start + 5), start + 5, ".", color)):  # three_close_jump
                            count_stone_shapes[8] += 1
                            start += 5
                            continue
                    if res == 2:  # four
                        # four_open
                        if is_target(board, i + (start - 1), start - 1, ".", ".") and is_target(board, i + (start + 4), start + 4, ".", "."):
                            count_stone_shapes[1] += 1
                            start += 5
                            continue
                        if (not is_target(board, i + (start - 1), start - 1, ".", color) and is_target(board, i + (start + 4), start + 4, ".", ".")) or (is_target(board, i + (start - 1), start - 1, ".", color) and not is_target(board, i + (start + 4), start + 4, ".", color)):  # four_close
                            count_stone_shapes[3] += 1
                            start += 5
                            continue

                if i + (start + 2) < 19 and start + 2 < 19:  # input length == 3
                    input = [board[i + start][start], board[i +
                                                            (start + 1)][start + 1], board[i + (start + 2)][start + 2]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # three
                        # three_open
                        if is_target(board, i + (start - 1), start - 1, ".", ".") and is_target(board, i + (start + 3), start + 3, ".", "."):
                            count_stone_shapes[5] += 1
                            start += 4
                            continue
                        if (not is_target(board, i + (start - 1), start - 1, ".", color) and is_target(board, i + (start + 3), start + 3, ".", ".")) or (is_target(board, i + (start - 1), start - 1, ".", color) and not is_target(board, i + (start + 3), start + 3, ".", color)):   # three_close
                            count_stone_shapes[7] += 1
                            start += 4
                            continue

                if i + (start + 1) < 19 and start + 1 < 19:  # input length == 2
                    input = [board[i + start][start],
                             board[i + (start + 1)][start + 1]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # two
                        # two open
                        if is_target(board, i + (start - 1), start - 1, ".", ".") and is_target(board, i + (start + 2), start + 2, ".", "."):
                            count_stone_shapes[9] += 1
                            start += 3
                            continue
                        if (not is_target(board, i + (start - 1), start - 1, ".", color) and is_target(board, i + (start + 2), start + 2, ".", ".")) or (is_target(board, i + (start - 1), start - 1, ".", ".") and not is_target(board, i + (start + 2), start + 2, ".", color)):   # two_close
                            count_stone_shapes[10] += 1
                            start += 3
                            continue

            else:  # not attacker, input length is 4/3
                if i + (start + 3) < 19 and start + 3 < 19:  # input length == 4
                    input = [board[i + start][start], board[i + (start + 1)][start + 1], board[i + (start + 2)][start + 2], board[i + (start + 3)]
                             [start + 3]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: four
                        # four defend
                        if is_target(board, i + (start - 1), start - 1, color, color) and is_target(board, i + (start + 4), start + 4, color, color):
                            count_stone_shapes[11] += 1
                            start += 5
                            continue
                        if (is_target(board, i + (start - 1), start - 1, ".", anti) and is_target(board, i + (start + 4), start + 4, color, color)) or (is_target(board, i + (start - 1), start - 1, color, color) and is_target(board, i + (start + 4), start + 4, ".", anti)):  # four_defend_half
                            count_stone_shapes[12] += 1
                            start += 5
                            continue

                if i + (start + 2) < 19 and start + 2 < 19:  # input length == 3
                    input = [board[i + start][start], board[i +
                                                            (start + 1)][start + 1], board[i + (start + 2)][start + 2]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: three
                        # three defend
                        if is_target(board, i + (start - 1), start - 1, color, color) and is_target(board, i + (start + 3), start + 3, color, color):
                            count_stone_shapes[13] += 1
                            start += 4
                            continue
                        if (is_target(board, i + (start - 1), start - 1, ".", anti) and is_target(board, i + (start + 3), start + 3, color, color)) or (is_target(board, i + (start - 1), start - 1, color, color) and is_target(board, i + (start + 3), start + 3, ".", anti)):  # three_defend_half
                            count_stone_shapes[14] += 1
                            start += 4
                            continue

            start += 1

        start = 0
        while i - start >= 0 and 18 - start >= 0:
            while board[i - start][18 - start] == "." and i - (start + 1) >= 0 and 18 - (start + 1) >= 0:
                start += 1
            if board[i - start][18 - start] == color:  # attacker, input length is 5/4/3/2
                res = 0

                if i - (start + 4) >= 0 and 18 - (start + 4) >= 0:  # input length == 5
                    input = [board[i - start][18 - start], board[i - (start + 1)][18 - (start + 1)], board[i - (start + 2)][18 - (start + 2)], board[i - (start + 3)]
                             [18 - (start + 3)], board[i - (start + 4)][18 - (start + 4)]]
                    res = find_stone_shapes(input, color)

                    if res == 10:  # win
                        count_stone_shapes[0] += 1
                        start += 5
                        continue

                    if res == 1:  # jump four
                        # four_open_jump
                        if is_target(board, i - (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i - (start + 5), 18 - (start + 5), ".", "."):
                            count_stone_shapes[2] += 1
                            start += 6
                            continue
                        # four_close_jump
                        if (not is_target(board, i - (start - 1), 18 - (start - 1), ".", color) and is_target(board, i - (start + 5), 18 - (start + 5), ".", ".")) or (is_target(board, i - (start - 1), 18 - (start - 1), ".", color) and not is_target(board, i - (start + 5), 18 - (start + 5), ".", color)):
                            count_stone_shapes[4] += 1
                            start += 6
                            continue

                if i - (start + 3) >= 0 and 18 - (start + 3) >= 0:  # input length == 4
                    input = [board[i - start][18 - start], board[i - (start + 1)][18 - (start + 1)], board[i - (start + 2)][18 - (start + 2)], board[i - (start + 3)]
                             [18 - (start + 3)]]
                    res = find_stone_shapes(input, color)

                    if res == 9:  # special
                        count_stone_shapes[15] += 1
                        start += 4
                        continue
                    if res == 1:  # jump three
                        # three_open_jump
                        if is_target(board, i - (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i - (start + 4), 18 - (start + 4), ".", "."):
                            count_stone_shapes[6] += 1
                            start += 5
                            continue
                        if (not is_target(board, i - (start - 1), 18 - (start - 1), ".", color) and is_target(board, i - (start + 4), 18 - (start + 4), ".", ".")) or (is_target(board, i - (start - 1), 18 - (start - 1), ".", color) and not is_target(board, i - (start + 5), 18 - (start + 5), ".", color)):  # three_close_jump
                            count_stone_shapes[8] += 1
                            start += 5
                            continue
                    if res == 2:  # four
                        # four_open
                        if is_target(board, i - (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i - (start + 4), 18 - (start + 4), ".", "."):
                            count_stone_shapes[1] += 1
                            start += 5
                            continue
                        if (not is_target(board, i - (start - 1), 18 - (start - 1), ".", color) and is_target(board, i - (start + 4), 18 - (start + 4), ".", ".")) or (is_target(board, i - (start - 1), 18 - (start - 1), ".", color) and not is_target(board, i - (start + 4), 18 - (start + 4), ".", color)):  # four_close
                            count_stone_shapes[3] += 1
                            start += 5
                            continue

                if i - (start + 2) >= 0 and 18 - (start + 2) >= 0:  # input length == 3
                    input = [board[i - start][18 - start], board[i -
                                                                 (start + 1)][18 - (start + 1)], board[i - (start + 2)][18 - (start + 2)]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # three
                        # three_open
                        if is_target(board, i - (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i - (start + 3), 18 - (start + 3), ".", "."):
                            count_stone_shapes[5] += 1
                            start += 4
                            continue
                        if (not is_target(board, i - (start - 1), 18 - (start - 1), ".", color) and is_target(board, i - (start + 3), 18 - (start + 3), ".", ".")) or (is_target(board, i - (start - 1), 18 - (start - 1), ".", color) and not is_target(board, i - (start + 3), 18 - (start + 3), ".", color)):   # three_close
                            count_stone_shapes[7] += 1
                            start += 4
                            continue

                if i - (start + 1) >= 0 and 18 - (start + 1) >= 0:  # input length == 2
                    input = [board[i - start][18 - start],
                             board[i - (start + 1)][18 - (start + 1)]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # two
                        # two open
                        if is_target(board, i - (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i - (start + 2), 18 - (start + 2), ".", "."):
                            count_stone_shapes[9] += 1
                            start += 3
                            continue
                        if (not is_target(board, i - (start - 1), 18 - (start - 1), ".", color) and is_target(board, i - (start + 2), 18 - (start + 2), ".", ".")) or (is_target(board, i - (start - 1), 18 - (start - 1), ".", ".") and not is_target(board, i - (start + 2), 18 - (start + 2), ".", color)):   # two_close
                            count_stone_shapes[10] += 1
                            start += 3
                            continue

            else:  # not attacker, input length is 4/3
                if i - (start + 3) >= 0 and 18 - (start + 3) >= 0:  # input length == 4
                    input = [board[i - start][18 - start], board[i - (start + 1)][18 - (start + 1)], board[i - (start + 2)][18 - (start + 2)], board[i - (start + 3)]
                             [18 - (start + 3)]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: four
                        # four defend
                        if is_target(board, i - (start - 1), 18 - (start - 1), color, color) and is_target(board, i - (start + 4), 18 - (start + 4), color, color):
                            count_stone_shapes[11] += 1
                            start += 5
                            continue
                        if (is_target(board, i - (start - 1), 18 - (start - 1), ".", anti) and is_target(board, i - (start + 4), 18 - (start + 4), color, color)) or (is_target(board, i - (start - 1), 18 - (start - 1), color, color) and is_target(board, i - (start + 4), 18 - (start + 4), ".", anti)):  # four_defend_half
                            count_stone_shapes[12] += 1
                            start += 5
                            continue

                if i - (start + 2) >= 0 and 18 - (start + 2) >= 0:  # input length == 3
                    input = [board[i - start][18 - start], board[i -
                                                                 (start + 1)][18 - (start + 1)], board[i - (start + 2)][18 - (start + 2)]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: three
                        # three defend
                        if is_target(board, i - (start - 1), 18 - (start - 1), color, color) and is_target(board, i - (start + 3), 18 - (start + 3), color, color):
                            count_stone_shapes[13] += 1
                            start += 4
                            continue
                        if (is_target(board, i - (start - 1), 18 - (start - 1), ".", anti) and is_target(board, i - (start + 3), 18 - (start + 3), color, color)) or (is_target(board, i - (start - 1), 18 - (start - 1), color, color) and is_target(board, i - (start + 3), 18 - (start + 3), ".", anti)):  # three_defend_half
                            count_stone_shapes[14] += 1
                            start += 4
                            continue

            start += 1

        start = 0
        while i + start < 19 and 18 - start >= 0:
            while board[i + start][18 - start] == "." and i + (start + 1) < 19 and 18 - (start + 1) >= 0:
                start += 1
            if board[i + start][18 - start] == color:  # attacker, input length is 5/4/3/2
                res = 0

                if i + (start + 4) < 19 and 18 - (start + 4) >= 0:  # input length == 5
                    input = [board[i + start][18 - start], board[i + (start + 1)][18 - (start + 1)], board[i + (start + 2)][18 - (start + 2)], board[i + (start + 3)]
                             [18 - (start + 3)], board[i + (start + 4)][18 - (start + 4)]]
                    res = find_stone_shapes(input, color)

                    if res == 10:  # win
                        count_stone_shapes[0] += 1
                        start += 5
                        continue

                    if res == 1:  # jump four
                        # four_open_jump
                        if is_target(board, i + (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i + (start + 5), 18 - (start + 5), ".", "."):
                            count_stone_shapes[2] += 1
                            start += 6
                            continue
                        # four_close_jump
                        if (not is_target(board, i + (start - 1), 18 - (start - 1), ".", color) and is_target(board, i + (start + 5), 18 - (start + 5), ".", ".")) or (is_target(board, i + (start - 1), 18 - (start - 1), ".", color) and not is_target(board, i + (start + 5), 18 - (start + 5), ".", color)):
                            count_stone_shapes[4] += 1
                            start += 6
                            continue

                if i + (start + 3) < 19 and 18 - (start + 3) >= 0:  # input length == 4
                    input = [board[i + start][18 - start], board[i + (start + 1)][18 - (start + 1)], board[i + (start + 2)][18 - (start + 2)], board[i + (start + 3)]
                             [18 - (start + 3)]]
                    res = find_stone_shapes(input, color)

                    if res == 9:  # special
                        count_stone_shapes[15] += 1
                        start += 4
                        continue
                    if res == 1:  # jump three
                        # three_open_jump
                        if is_target(board, i + (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i + (start + 4), 18 - (start + 4), ".", "."):
                            count_stone_shapes[6] += 1
                            start += 5
                            continue
                        if (not is_target(board, i + (start - 1), 18 - (start - 1), ".", color) and is_target(board, i + (start + 4), 18 - (start + 4), ".", ".")) or (is_target(board, i + (start - 1), 18 - (start - 1), ".", color) and not is_target(board, i + (start + 5), 18 - (start + 5), ".", color)):  # three_close_jump
                            count_stone_shapes[8] += 1
                            start += 5
                            continue
                    if res == 2:  # four
                        # four_open
                        if is_target(board, i + (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i + (start + 4), 18 - (start + 4), ".", "."):
                            count_stone_shapes[1] += 1
                            start += 5
                            continue
                        if (not is_target(board, i + (start - 1), 18 - (start - 1), ".", color) and is_target(board, i + (start + 4), 18 - (start + 4), ".", ".")) or (is_target(board, i + (start - 1), 18 - (start - 1), ".", color) and not is_target(board, i + (start + 4), 18 - (start + 4), ".", color)):  # four_close
                            count_stone_shapes[3] += 1
                            start += 5
                            continue

                if i + (start + 2) < 19 and 18 - (start + 2) >= 0:  # input length == 3
                    input = [board[i + start][18 - start], board[i +
                                                                 (start + 1)][18 - (start + 1)], board[i + (start + 2)][18 - (start + 2)]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # three
                        # three_open
                        if is_target(board, i + (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i + (start + 3), 18 - (start + 3), ".", "."):
                            count_stone_shapes[5] += 1
                            start += 4
                            continue
                        if (not is_target(board, i + (start - 1), 18 - (start - 1), ".", color) and is_target(board, i + (start + 3), 18 - (start + 3), ".", ".")) or (is_target(board, i + (start - 1), 18 - (start - 1), ".", color) and not is_target(board, i + (start + 3), 18 - (start + 3), ".", color)):   # three_close
                            count_stone_shapes[7] += 1
                            start += 4
                            continue

                if i + (start + 1) < 19 and 18 - (start + 1) >= 0:  # input length == 2
                    input = [board[i + start][18 - start],
                             board[i + (start + 1)][18 - (start + 1)]]
                    res = find_stone_shapes(input, color)

                    if res == 1:  # two
                        # two open
                        if is_target(board, i + (start - 1), 18 - (start - 1), ".", ".") and is_target(board, i + (start + 2), 18 - (start + 2), ".", "."):
                            count_stone_shapes[9] += 1
                            start += 3
                            continue
                        if (not is_target(board, i + (start - 1), 18 - (start - 1), ".", color) and is_target(board, i + (start + 2), 18 - (start + 2), ".", ".")) or (is_target(board, i + (start - 1), 18 - (start - 1), ".", ".") and not is_target(board, i + (start + 2), 18 - (start + 2), ".", color)):   # two_close
                            count_stone_shapes[10] += 1
                            start += 3
                            continue

            else:  # not attacker, input length is 4/3
                if i + (start + 3) < 19 and 18 - (start + 3) >= 0:  # input length == 4
                    input = [board[i + start][18 - start], board[i + (start + 1)][18 - (start + 1)], board[i + (start + 2)][18 - (start + 2)], board[i + (start + 3)]
                             [18 - (start + 3)]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: four
                        # four defend
                        if is_target(board, i + (start - 1), 18 - (start - 1), color, color) and is_target(board, i + (start + 4), 18 - (start + 4), color, color):
                            count_stone_shapes[11] += 1
                            start += 5
                            continue
                        if (is_target(board, i + (start - 1), 18 - (start - 1), ".", anti) and is_target(board, i + (start + 4), 18 - (start + 4), color, color)) or (is_target(board, i + (start - 1), 18 - (start - 1), color, color) and is_target(board, i + (start + 4), 18 - (start + 4), ".", anti)):  # four_defend_half
                            count_stone_shapes[12] += 1
                            start += 5
                            continue

                if i + (start + 2) < 19 and 18 - (start + 2) >= 0:  # input length == 3
                    input = [board[i + start][18 - start], board[i +
                                                                 (start + 1)][18 - (start + 1)], board[i + (start + 2)][18 - (start + 2)]]
                    res = find_stone_shapes(input, color)

                    if res == -1:  # defend: three
                        # three defend
                        if is_target(board, i + (start - 1), 18 - (start - 1), color, color) and is_target(board, i + (start + 3), 18 - (start + 3), color, color):
                            count_stone_shapes[13] += 1
                            start += 4
                            continue
                        if (is_target(board, i + (start - 1), 18 - (start - 1), ".", anti) and is_target(board, i + (start + 3), 18 - (start + 3), color, color)) or (is_target(board, i + (start - 1), 18 - (start - 1), color, color) and is_target(board, i + (start + 3), 18 - (start + 3), ".", anti)):  # three_defend_half
                            count_stone_shapes[14] += 1
                            start += 4
                            continue

            start += 1

    return count_stone_shapes


def heuristic(board: list, imaging_captured_W: int, imaging_captured_B: int) -> int:
    # observer (upper level) has put the piece
    global player
    # connecting_value = 0
    # counts_B = scan_whole_board(board, "b")
    # counts_W = scan_whole_board(board, "w")
    # weight = [3, 6, 10, 6, 7, 10, 5, 4, 6, 6, 6, 3, 1, 2, 6, 1, 2, 2, 1, 2]
    # connecting_value_B = counts_B[0] * 1 + counts_B[1] * 5 + counts_B[2] * 10 + counts_B[3] * \
    #     30 + counts_B[4] * 80 + counts_B[5] * 500 + \
    #     counts_B[6] * 100000
    # connecting_value_W = counts_W[0] * 1 + counts_W[1] * 5 + counts_W[2] * 10 + counts_W[3] * \
    #     30 + counts_W[4] * 80 + counts_W[5] * 500 + \
    #     counts_W[6] * 1000
    count = scan_whole_board(board, player)
    weight = [float(10**15), float(10**12), float(10**8) * 0.8, float(10**4), float(10**4) * 0.8, float(10**3), float(10**3)
              * 0.8,  float(10**7) * 0.8, float(10**2) * 0.8, float(10), -float(10**10), float(10**14), float(10**13), float(10**5), float(10**11), float(10**5)]

    connecting_value = 0
    for i in range(len(weight)):
        connecting_value += weight[i] * count[i]
    if player == "b":
        if imaging_captured_W + captured_W >= 10:
            connecting_value += float(10**15)
        else:
            connecting_value += float(imaging_captured_W -
                                      imaging_captured_B) * 0.5 * 10**6
    else:
        if imaging_captured_B + captured_B >= 10:
            connecting_value += float(10**15)
        else:
            connecting_value += float(imaging_captured_B -
                                      imaging_captured_W) * 0.5 * 10**6

    return connecting_value


def square_positions(width: int, center_x: int, center_y: int) -> set:
    res = set()
    for j in range(width + 1):
        if 0 <= center_x - width < 19:
            if 0 <= center_y - j < 19:
                res.add((center_x - width, center_y - j))
            if 0 <= center_y + j < 19:
                res.add((center_x - width, center_y + j))
        if 0 <= center_x + width < 19:
            if 0 <= center_y - j < 19:
                res.add((center_x + width, center_y - j))
            if 0 <= center_y + j < 19:
                res.add((center_x + width, center_y + j))

    for i in range(width + 1):
        if 0 <= center_y - width < 19:
            if 0 <= center_x - i < 19:
                res.add((center_x - i, center_y - width))
            if 0 <= center_x + i < 19:
                res.add((center_x + i, center_y - width))
        if 0 <= center_y + width < 19:
            if 0 <= center_x - i < 19:
                res.add((center_x - i, center_y + width))
            if 0 <= center_x + i < 19:
                res.add((center_x + i, center_y + width))

    return res


def minimax(board: list, depth: int, alpha, beta, is_maximizing: bool, imaging_captured_W: int, imaging_captured_B: int, prev_x: int, prev_y: int) -> int:
    # Check if the game is over or depth limit has been reached
    # print(depth)
    # "leaf" in the tree
    if depth == 0 or game_is_over(imaging_captured_W, imaging_captured_B):
        # return heuristic value
        # global player
        # if (player == "w" and not is_maximizing) or (player == "b" and is_maximizing):
        #     observer = "w"
        # else:
        #     observer = "b"
        return heuristic(board, imaging_captured_W, imaging_captured_B)
    global position

    if player == "w":
        white_steps = white_is_first_step_or_second_step(board)

        if white_steps == 0:
            # it's white first step, just put it on the center and return
            board[center][center] = player
            position = [center, center]
            return

        if white_steps == 1:
            # it's white second step, put it on the center-left-by-2 if it's empty
            if board[center][center - 3] == ".":
                board[center][center - 3] = player
                position = [center, center - 3]
                return
            # otherwise, put it on the center-right-by-2
            else:
                board[center][center + 3] = player
                position = [center, center + 3]
                return

    # Maximizing player
    if is_maximizing:
        best_score = -math.inf

        for width in range(19):
            candidates = square_positions(width, prev_x, prev_y)
            for i, j in candidates:
                if board[i][j] == '.':

                    # if surrounding_empty(i, j, board):
                    #     score = heuristic(player, 0, 0)

                    # else:
                    old_board = [list(item) for item in board]
                    old_imaging_captured_W = imaging_captured_W
                    old_imaging_captured_B = imaging_captured_B

                    board[i][j] = player
                    board, imaging_captured_W, imaging_captured_B = after_move(
                        i, j, board, imaging_captured_W, imaging_captured_B)
                    score = minimax(board, depth - 1, alpha, beta, False,
                                    imaging_captured_W, imaging_captured_B, i, j)

                    board = [list(item) for item in old_board]
                    imaging_captured_W = old_imaging_captured_W
                    imaging_captured_B = old_imaging_captured_B

                    if score > best_score:
                        best_score = score
                        if depth == maxDepth:
                            position = [i, j]
                            # print(board[position[0]][position[1]])
                            # print(position)

                    if best_score >= beta:
                        return best_score
                    alpha = max(alpha, best_score)

        return best_score

    # Minimizing player
    else:
        best_score = math.inf

        for width in range(19):
            candidates = square_positions(width, prev_x, prev_y)
            for i, j in candidates:
                if board[i][j] == '.':

                    # if surrounding_empty(i, j, board):
                    #     score = heuristic(player, 0, 0)

                    # else:
                    old_board = [list(item) for item in board]
                    old_imaging_captured_W = imaging_captured_W
                    old_imaging_captured_B = imaging_captured_B

                    board[i][j] = opponent
                    board, imaging_captured_W, imaging_captured_B = after_move(
                        i, j, board, imaging_captured_W, imaging_captured_B)
                    score = minimax(board, depth - 1, alpha, beta, True,
                                    imaging_captured_W, imaging_captured_B, i, j)

                    board = [list(item) for item in old_board]
                    imaging_captured_W = old_imaging_captured_W
                    imaging_captured_B = old_imaging_captured_B

                    best_score = min(score, best_score)

                    if best_score <= alpha:
                        return best_score
                    beta = min(beta, best_score)

        return best_score


def find_empty(board: list) -> list:
    res = [0, 0]
    for i in range(19):
        for j in range(19):
            if board[i][j] == ".":
                res[0] = i
                res[1] = j
                return res
    return res


def main():
    file = open("input.txt", "r")

    # first line
    line = file.readline()
    line = line.strip()
    global player, opponent
    if line == "BLACK":
        player = "b"
        opponent = "w"
    else:
        player = "w"
        opponent = "b"
    # second line
    line = file.readline()
    global time
    time = (float)(line.strip())
    # third line
    line = file.readline()
    global captured_W, captured_B
    captured_B, captured_W = line.strip().split(",")
    captured_W = int(captured_W)
    captured_B = int(captured_B)

    # fellowing lines
    global board
    for i in range(19):
        line = file.readline()
        for j in range(19):
            board[i][j] = line[j]

    imaging_captured_W, imaging_captured_B = 0, 0

    # print(player)
    # print(time)
    # print(captured_W)
    # print(captured_B)
    # print(board)

    row = [19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    col = ["A", "B", "C", "D", "E", "F", "G", "H", "J",
           "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]

    if time <= float(0.01):
        res = find_empty(board)
        f = open("output.txt", "w")
        f.write(str(row[res[0]]) + col[res[1]])
        f.close()

    else:
        global maxDepth
        if time >= float(150):
            maxDepth = 2

        minimax(board, maxDepth, -math.inf, math.inf, True,
                imaging_captured_W, imaging_captured_B, 9, 9)

        f = open("output.txt", "w")
        f.write(str(row[position[0]]) + col[position[1]])
        f.close()


if __name__ == "__main__":
    main()
