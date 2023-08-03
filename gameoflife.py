import tkinter as tk
import copy
from random import randrange


class Buttons(tk.Button):
    def __init__(self, parent, options, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.options = options
        self.bou_clear = None
        for i, elt in enumerate(self.options):
            if i == len(self.options)-1:
                self.entry = Entry(parent)
            self.bou = tk.Button(parent, **elt)
            self.bou.pack()
            if elt['text'] == 'clear':
                self.bou_clear = self.bou


class Entry(tk.Entry, tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)
        tk.Label.__init__(self, parent, *args, **kwargs)

        tk.Label(parent, text='Width : ').pack()
        self.entry1 = tk.Entry(parent, width=10)
        self.entry1.pack()
        tk.Label(parent, text='Weight : ').pack()
        self.entry2 = tk.Entry(parent, width=10)
        self.entry2.pack()


class Window:

    """Main window"""

    def __init__(self, parent, **kwargs):

        """
        Construct attributes for the graphic window
        :param parent: class tkinter.Tk, root window
        :param kwargs:
                    width : int, canvas width
                    height : int, canvas height
                    cote : int, size of the squares
        """

        self.parent = parent
        self.width = kwargs['width']
        self.height = kwargs['height']
        self.cote = kwargs['cote']
        # List of dictionaries containing options for the buttons
        self.options = [{'text': 'start', 'command': self.start},
                        {'text': 'stop', 'command': self.stop},
                        {'text': 'step-by-step', 'command': self.stepbystep, 'repeatinterval': 100,
                         'repeatdelay': 300},
                        {'text': 'forwards', 'command': self.forwards, 'repeatinterval': 100,
                         'repeatdelay': 300},
                        {'text': 'backwards', 'command': self.backwards, 'repeatinterval': 100,
                         'repeatdelay': 300},
                        {'text': 'clear', 'command': self.clear, 'state': 'normal'},
                        {'text': 'random', 'command': self.randomly},
                        {'text': 'ok', 'command': self.get_entries}]
        # Matrix
        self.cell = [[0 for row in range(self.height)] for col in
                     range(self.width)]
        self.state = [[0 for row in range(self.height)] for col in
                      range(self.width)]
        self.temp = [[0 for row in range(self.height)] for col in
                     range(self.width)]

        self.states_list = []  # List of all state
        self.index = 0  # Index of the list
        self.flag = 0  # Flag
        self.num = 0  # Event type

        self.canvas()
        # Creates buttons
        self.bou = Buttons(self.parent, self.options)
        self.draw_square()

    def canvas(self):

        """Create the canvas and bind left click on it"""

        self.can = tk.Canvas(self.parent, width=(self.width * self.cote),
                             height=(self.height * self.cote),
                             highlightthickness=0)
        self.can.bind('<Button-1>', self.manager)
        self.can.bind('<B1-Motion>', self.manager)
        self.can.bind('<Button-3>', self.manager)
        self.can.bind('<B3-Motion>', self.manager)
        self.can.pack(side='left')

    def manager(self, event):

        """
        Event manager
        Modifies the states of the selected cells
        Works for click and motion event
        :param event: tk.Event, event
        """

        # Saves the number of the button pressed
        if event.num == '??':  # Motion return '??'
            pass
        else:
            self.num = event.num
        x, y = event.x // self.cote, event.y // self.cote  # Set x, y to detect which square selected
        # Passes if the mouse detect event outside the canvas to avoid index out of range
        if x > (self.width - 1) or y > (self.height - 1):
            pass
        else:
            # if right click
            if self.num == 1:
                self.state[x][y] = 1
                self.temp[x][y] = 1
                col = 'blue'
                self.can.itemconfig(self.cell[x][y], fill=col)
            # if left click
            if self.num == 3:
                self.state[x][y] = 0
                self.temp[x][y] = 0
                col = 'white'
                self.can.itemconfig(self.cell[x][y], fill=col)

    def randomly(self):
        self.clear()
        for i in range(self.width * self.height // 4):
            x, y = randrange(self.width), randrange(self.height)
            self.state[x][y] = 1
            col = 'blue'
            self.can.itemconfig(self.cell[x][y], fill=col)

    def get_entries(self):
        self.clear()
        width, height = self.bou.entry.entry1.get(), self.bou.entry.entry2.get()
        if not width:
            width = int(self.can.cget('width')) // self.cote
        if not height:
            height = int(self.can.cget('height')) // self.cote
        width, height = int(width), int(height)
        self.can.config(width=width*self.cote, height=height*self.cote)
        self.width, self.height = width, height
        self.cell = [[0 for row in range(self.height)] for col in
                     range(self.width)]
        self.state = [[0 for row in range(self.height)] for col in
                      range(self.width)]
        self.temp = [[0 for row in range(self.height)] for col in
                     range(self.width)]
        self.draw_square()

    def start(self):

        """Action of start button
        Launch the animation automatically"""

        self.flag = 1
        self.launch()

    def stop(self):

        """Action of stop button
        Stop the animation"""

        self.flag = 0

    def stepbystep(self):

        """Action of step-by-step button
        Launch step-by-step the animation"""

        self.flag = 2
        self.launch()

    def backwards(self):

        """Action of backwards button
        Go to the previous frame"""

        if self.index > 0:
            self.index -= 1
            state = self.states_list[self.index]
            self.draw(state)

    def forwards(self):

        """Action of forwards button
        Go to the next frame if backwards button has been used"""

        if self.index < len(self.states_list) - 1:
            self.index += 1
            state = self.states_list[self.index]
            self.draw(state)

    def clear(self):

        """Clear the window"""

        self.stop()
        self.states_list = []
        self.index = 0
        self.state = [[0 for row in range(self.height)] for col in
                      range(self.width)]
        self.temp = [[0 for row in range(self.height)] for col in
                     range(self.width)]
        self.draw(self.state)

    def draw_square(self):

        """Draws the squares inside the canvas"""

        for y in range(self.height):
            for x in range(self.width):
                self.cell[x][y] = \
                    self.can.create_rectangle((x*self.cote, y*self.cote,
                                              (x+1)*self.cote,
                                              (y+1)*self.cote),
                                              outline='grey', fill='white')
        self.display_frame()

    def draw(self, state):

        """
        Colors each cells in blue or white according its states
        :param state: list, matrix of states
        """

        for y in range(self.height):
            for x in range(self.width):
                if state[x][y]:
                    col = 'blue'
                else:
                    col = 'white'
                self.can.itemconfig(self.cell[x][y], fill=col)
        self.config_info()  # Configure the frame counter

    def launch(self):

        """Saves state in the list and calculates the next state
         of each cells with the function 'calculate' and draw it"""

        #################################################################
        # CAUTION :                                                     #
        # Need to use copy.deepcopy() because each elt in the list are  #
        # a reference to self.state and if self.state is modified each  #
        # elt are they too                                              #
        #################################################################

        # Saves the first state in the list
        if not self.states_list:
            states = copy.deepcopy(self.state)
            self.states_list.append(states)
            self.index = len(self.states_list) - 1  # set index at last index
        # Calculate the next state
        rules(self.width, self.height, self.state, self.temp)
        # Draw it
        self.draw(self.state)
        # Save each state in the list
        states = copy.deepcopy(self.state)
        self.states_list.append(states)
        self.index = len(self.states_list) - 1  # set index at last index
        self.config_info()  # Configure the frame counter
        if self.flag:
            if self.flag == 2:
                self.flag = 0
            else:
                self.parent.after(100, self.launch)
        # Activates or deactivates clear button
        if self.flag:
            self.bou.bou_clear.configure(state='disabled')
        else:
            self.bou.bou_clear.configure(state='active')

    def display_frame(self):

        """Display the number of current frame"""

        self.info = self.can.create_text(10, 10, text=str(self.index),
                                         fill='red', font=10)

    def config_info(self,):

        """Configure the frame counter"""

        # Moves the position of the number so that you can always see
        # the whole number
        if self.index >= 100:
            self.can.coords(self.info, 15, 10)
        if self.index >= 1000:
            self.can.coords(self.info, 20, 10)
        if self.index >= 10000:
            self.can.coords(self.info, 25, 10)
        # Configure the text according to self.index
        self.can.itemconfig(self.info, text=self.index)


def neighbors_alive(state, width, height, x, y):

    """
    Calculates all alive neighbors of a cell
    :param state: list, list of states
    :param width: int, width of the canvas
    :param height: int, height of the canvas
    :param x: int, row number
    :param y: int, column number
    :return: nb_neighbors : int, number of neighbors
    """

    # Each cell has 8 neighbors
    nb_neighbors = 0
    if state[(x - 1) % width][(y + 1) % height]:
        nb_neighbors += 1
    if state[x][(y + 1) % height]:
        nb_neighbors += 1
    if state[(x + 1) % width][(y + 1) % height]:
        nb_neighbors += 1
    if state[(x + 1) % width][y]:
        nb_neighbors += 1
    if state[(x + 1) % width][(y - 1) % height]:
        nb_neighbors += 1
    if state[x][(y - 1) % height]:
        nb_neighbors += 1
    if state[(x - 1) % width][(y - 1) % height]:
        nb_neighbors += 1
    if state[(x - 1) % width][y]:
        nb_neighbors += 1

    return nb_neighbors


def rules(width, height, state, temp):

    """
    Rules for the game of life
    :param width: int, width of the canvas
    :param height: int, height of the canvas
    :param state: list, list of states
    :param temp: list, list of temporary states
    """

    # Set temporary state according to the rules
    for y in range(height):
        for x in range(width):
            nb_neighbors = neighbors_alive(state, width, height, x, y)
            # Rule 1 - Death by loneliness
            if state[x][y] and nb_neighbors < 2:
                temp[x][y] = 0
            # Rule 2 - Any cell with 2 or 3 neighbors survives.
            if state[x][y] and (nb_neighbors == 2 or nb_neighbors == 3):
                temp[x][y] = 1
            # Rule 3 - Death by asphyxiation
            if state[x][y] and nb_neighbors > 3:
                temp[x][y] = 0
            # Rule 4 - Birth
            if not state[x][y] and nb_neighbors == 3:
                temp[x][y] = 1

    # Changes the state of each cell according to its temporary state
    for y in range(height):
        for x in range(width):
            state[x][y] = temp[x][y]


def main():

    """Main program"""

    # Sets sizes
    width = 30
    height = 30
    cote = 15
    # Creates root
    root = tk.Tk()
    root.title('jeu de la vie')
    # Creates window
    Window(root, width=width, height=height, cote=cote)
    # Mainloop
    root.mainloop()


if __name__ == '__main__':
    main()
