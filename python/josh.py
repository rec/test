import tkinter


color_table = ['', 'red', 'black', 'yellow']

logo_pattern_11_by_11 = [
    [1, 2, 3, 2, 2, 3, 2, 2, 3, 2, 1],
    [1, 2, 3, 2, 2, 3, 2, 2, 3, 2, 1],
    [2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2],
    [2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [2, 2, 3, 2, 2, 2, 2, 2, 3, 2, 2],
    [1, 2, 3, 3, 2, 2, 2, 3, 3, 2, 1],
    [1, 2, 2, 3, 3, 2, 3, 3, 2, 2, 1],
    [1, 1, 2, 2, 3, 3, 3, 2, 2, 1, 1]]

def josh_logo_draw():
    """
    counter that runs from range (1, 11) vertically and horizontally
    done with a nested drawing of squares in range(1, 11)
    to access my fake matrix of colors, represented by 1, 2 and 3.
    """

    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, width=550, height=550)
    canvas.pack()

    for row in range(11):
        for column in range(11):
            x = column * 50
            y = row * 50
            color = logo_pattern_11_by_11[row][column]
            canvas.create_rectangle(x, y, x+50, y+50, fill=color_table[color], width=0)
            #print(y,row*column)  #used this to debug


if __name__ == '__main__':
    josh_logo_draw()
