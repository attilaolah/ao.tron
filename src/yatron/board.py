class Board(object):
    """Representation of the current state of the tron board."""

    # Default constants:
    W = WALL  = '#'
    F = FLOOR = ' '
    M = ME    = '1'
    T = THEM  = '2'

    def __init__(self, dimensions, lines, syntax=None):
        # Set up dimensions and lines (with height and withd for convenience):
        self.dimensions = \
            self.height, self.width = dimensions
        self.lines = lines
        # Set up custom syntax if supplied:
        if syntax is not None:
            self.W = self.WALL  = syntax['WALL']
            self.F = self.FLOOR = syntax['FLOOR']
            self.M = self.ME    = syntax['ME']
            self.T = self.THEM  = syntax['THEM']
        # Set up some lazyness for the properties:
        self.__board = \
            self.__me = \
            self.__them = \
            self.__distance = None

    @property
    def board(self):
        """Returns the tron board in plain text. Useful for debugging."""
        if self.__board is None:
            self.__board = '\n'.join(reversed([
                ''.join(line) for line in self.lines]))
        return self.__board

    def __repr__(self):
        """Useful when debugging."""
        return '<Board ({0}x{1})>'.format(*self.dimensions)

    def __iter__(self):
        """Iterates over the board, yielding block values and coordinates."""
        for y, line in enumerate(self.lines):
            for x, block in enumerate(line):
                yield block, (x, y)

    def __getitem__(self, coords):
        """Returns the block with coordinates."""
        return self.lines[coords[1]][coords[0]]

    @property
    def me(self):
        """Returns the coordinates of `ME` on the board."""
        if self.__me is None:
            for block, coords in self:
                if block == self.ME:
                    self.__me = coords
                    break
        return self.__me
    m = me

    @property
    def them(self):
        """Returns coordinates of `THEM` on the board."""
        if self.__them is None:
            for block, coords in self:
                if block == self.THEM:
                    self.__them = coords
                    break
        return self.__them
    t = them

    def possibilities(self, coords):
        """Returns the coordinates of spaces around `coords`."""
        x, y = coords
        area = ((x, y-1), (x, y+1), (x+1, y), (x-1, y))
        return tuple(block for block in area if self[block] == self.FLOOR)

    @property
    def distance(self):
        """Calculates the distance between the two players.

        If the players are isolated, returns None, otherwise the number of
        blocks needed to travel from our position to the opponent's position,
        minus one.

        """
        if self.__distance is None:
            borders = self.possibilities(self.them)
            fields, counter = [self.me], 1
            flood = []
            while True:
                next = []
                for field in fields:
                    for x in self.possibilities(field):
                        if x in borders:
                            self.__distance = counter
                            return counter
                        if x not in flood:
                            flood.append(x)
                            next.append(x)
                counter += 1
                if next == []:
                    self.__distance = -1
                    return -1
                fields = next
            # At this point, it looks like we're isolated.
        return self.__distance
