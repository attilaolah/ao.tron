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
            self.__them = None

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
