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
            self.__distance = \
            self.__path = None

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
        area = ((x, y-1), (x, y+1), (x-1, y), (x+1, y))
        return tuple(block for block in area if self[block] == self.FLOOR)

    @property
    def distance(self):
        """Calculates the distance between the two players.

        If the players are isolated, returns None, otherwise the number of
        blocks needed to travel from our position to the opponent's position,
        minus one.

        """
        if self.__distance is None:
            x, y = self.me
            if self.them in ((x, y-1), (x, y+1), (x-1, y), (x+1, y)):
                # We're adjacent; set cache to zero and path to empty.
                self.__distance, self.__path = 0, ()
                return 0
            borders = self.possibilities(self.them)
            fields, flood, levels, counter, space = [self.me], [], [], 1, 0
            while True:
                next = []
                for field in fields:
                    for x in self.possibilities(field):
                        if x in borders:
                            # Fond the enemy: set cache to counter value.
                            self.__distance = counter
                            # Also set the shortest path
                            levels.reverse()
                            path = [x]
                            for level in levels:
                                for field in level:
                                    if field in self.possibilities(path[-1]):
                                        path.append(field)
                                        continue
                            self.__path = tuple(reversed(path))
                            # Return the current distance.
                            return counter
                        if x not in flood:
                            flood.append(x)
                            next.append(x)
                counter += 1
                space += len(next)
                if next == []:
                    # No more spaces left: we are isolated; set up path cache.
                    self.__distance, self.__path = -1, ()
                    # We also set our leftover space.
                    self.space = space
                    # Return -1 to indicate isolation.
                    return -1
                levels.append(next)
                fields = next
        return self.__distance

    @property
    def path(self):
        """Returns one of the shortest paths between us on the opponent."""
        return (self.distance, self.__path)[1]
