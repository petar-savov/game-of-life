import json
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from matplotlib.animation import FuncAnimation


def read(board):

    board = [[1 if c == "*" else 0 for c in line] for line in board.split()]
    board = np.array(board)

    return board


def transform(input_board):

    output_board = np.zeros(input_board.shape)

    for i, row in enumerate(input_board):
        for j, _ in enumerate(row):
            neighbours = count_neighbours(pt=(i, j), board=input_board)
            output_board[i, j] = rules(pt_val=input_board[i, j], neighbours=neighbours)

    return output_board


def rules(pt_val, neighbours):

    if pt_val == 1:
        return int(neighbours in [2, 3])

    return int(neighbours == 3)


def count_neighbours(pt, board) -> int:

    x, y = pt[0], pt[1]
    xmin = max(0, x - 1)
    xmax = min(x + 2, board.shape[0])
    ymin = max(0, y - 1)
    ymax = min(y + 2, board.shape[1])

    nearby_points = board[xmin:xmax, ymin:ymax]
    result = nearby_points.sum() - board[pt]
    return result


def display(board):

    plt.imshow(board, cmap="Greys")
    plt.xticks([])
    plt.yticks([])
    plt.show()


def animate(board):

    fig = plt.figure()
    im = plt.imshow(board, cmap="Greys")
    plt.xticks([])
    plt.yticks([])

    def init():
        return (im,)

    def move(i):
        board = im.get_array()
        board = transform(board)
        im.set_array(board)
        return (im,)

    animation = FuncAnimation(fig, move, init_func=init, interval=1000, blit=True)
    plt.show()


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-s", "--shape")
    args = vars(parser.parse_args())
    shape = args["shape"]

    with open("./examples.json") as f:
        examples = json.load(f)

    board = read(examples[shape])
    animate(board)
