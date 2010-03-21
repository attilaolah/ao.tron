import os
import operator
import random
import sys


DIRECTIONS = (NORTH, EAST, SOUTH, WEST) = (N, S, E, W) = 1, 2, 3, 4

ME    = '1'
THEM  = '2'
FLOOR = ' '
WALL  = '#'


def move(direction):
    print direction
    sys.stdout.flush()


def generate():
    """Generate board objects, once per turn.

    This method returns a generator which you may iterate over.
    Make sure to call tron.move() exactly once for every board
    generated, or your bot will not work.

    """

    while True:

        # Read until we hit an empty string:
        line, lines = sys.stdin.readline(), []
        if line == '':
            break

        # Extract the dimensions:
        width, height = map(int, line[:-1].split())

        # Generate board lines:
        for i in xrange(height):
            lines.append(tuple(sys.stdin.readline()[:width]))

        # Yield a new Board object for each iteration:
        yield Board((width, height), tuple(reversed(lines)))


class Board(object):
    """The Tron Board."""

    # Copy the module-level constants to the board class for convenience:
    DIRECTIONS = (NORTH, EAST, SOUTH, WEST) = (N, S, E, W) = DIRECTIONS
    ME, THEM, WALL, FLOOR = ME, THEM, WALL, FLOOR

    # Also copy the move function:
    move = staticmethod(move)

    def __init__(self, dimensions, data):
        # Set up dimensions and data (with height and withd for convenience):
        self.dimensions = \
            self.width, self.height = dimensions
        self.data = data
        # Set up some lazyness for the properties:
        self.__board = \
            self.__me = \
            self.__them = \
            self.__distance = \
            self.__path = \
            self.__flight = \
            self.__charge = \
            self.__chase = \
            self.__flee = None

    @property
    def board(self):
        """Returns the tron board in plain text. Useful for debugging."""

        if self.__board is None:
            self.__board = '\n'.join(reversed([
                ''.join(line) for line in self.data]))

        return self.__board

    def __repr__(self):
        """Useful when debugging."""

        return '<Board (%dx%d)>' % self.dimensions

    def __iter__(self):
        """Iterates over the board, yielding block values and coordinates."""

        for y, line in enumerate(self.data):
            for x, block in enumerate(line):
                yield block, (x, y)

    def __getitem__(self, coords):
        """Returns the block with coordinates."""

        return self.data[coords[1]][coords[0]]

    @property
    def me(self):
        """Returns the coordinates of `ME` on the board."""

        # Check for cached value:
        if self.__me is None:
            for block, coords in self:
                if block == ME:
                    self.__me = coords
                    break

        # Return cached value:
        return self.__me

    m = me

    @property
    def them(self):
        """Returns coordinates of `THEM` on the board."""

        # Check for cached value:
        if self.__them is None:
            for block, coords in self:
                if block == THEM:
                    self.__them = coords
                    break

        # Return cached value:
        return self.__them

    t = them

    def surround(self, coords):
        """Returns the four surrounding blocks for `doords`."""

        x, y = coords

        return ((x, y+1), (x+1, y), (x, y-1), (x-1, y))


    def possibilities(self, coords):
        """Returns the coordinates of spaces around `coords`."""

        x, y = coords

        return tuple(block for block in self.surround(
            coords) if self[block] == FLOOR)

    def direction(self, coords):
        """Returns the direction to go the the adjacent `coords`."""

        if coords in self.surround(self.me):
            # XXX This is not compatible with Python 2.5, so we work it around:
            # return self.surround(self.me).index(coords) + 1
            return [i for i, x in enumerate(self.surround(
                self.me)) if x == coords][0] + 1

    @property
    def distance(self):
        """Calculates the distance between the two players.

        If the players are isolated, returns None, otherwise the number of
        blocks needed to travel from our position to the opponent's position,
        minus one.

        """

        # Check for cached value:
        if self.__distance is None:

            if self.them in self.surround(self.me):
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

        # Return the cached value:
        return self.__distance

    @property
    def path(self):
        """Returns one of the shortest paths between us on the opponent."""
        return (self.distance, self.__path)[1]

    @property
    def flight(self):
        """Thsi is the absolute distance between us and the opponent.

        Note that walls are not taken account of. We may even be separated.
        This is just a cheap call to see if we're far away on a huge map.

        """

        # Check for cached value:
        if self.__flight is None:
            self.__flight = sum(map(abs, map(operator.sub, self.me, self.them)))

        # Return the cached value:
        return self.__flight

    @property
    def chase(self):
        """Chases the enemy.

        Note that this will call `self.path`, which may be quite expensive on
        huge boards. Use it with caution. If you need a cheaper version, try
        `self.charge`.

        """

        # Check for cached value:
        if self.__chase is None:
            self.__chase = self.path and self.path[0] or None

        # Return the cached value:
        return self.__chase

    @property
    def charge(self):
        """Charges towards the enemy.

        This call is very cheap, but it does not check for the shortest path;
        It doesn't even check if we're separated from the enemy or not. Use it
        when you're far from the enemy and want to get closer as quickly as
        possible.

        """

        # Check for cached value:
        if self.__charge is None:
            x, y = self.me
            xl, yl = map(operator.lt, self.me, self.them)

            fields = {
                (True, True): ((x+1, y), (x, y+1), (x, y-1), (x-1, y)),
                (True, False): ((x+1, y), (x, y-1), (x-1, y), (x, y+1)),
                (False, True): ((x-1, y), (x, y+1), (x+1, y), (x, y-1)),
                (False, False): ((x-1, y), (x, y-1), (x+1, y), (x, y+1)),
            }[xl, yl]

            for field in fields:
                if field in self.possibilities(self.me):
                    self.__charge = field
                    return field

            # It looks like we're trapped, so let's return None.
            self.__charge = -1
            return None

        if self.__charge == -1:
            return None

        # Return the cached value:
        return self.__charge

    @property
    def flee(self):
        """Flee from the enemy.

        This call is very cheap, but it does not check for the shortest path;
        It doesn't even check if we're separated from the enemy or not. Use it
        when you want to run away as quickly as possible.

        """

        # Check for cached value:
        if self.__flee is None:
            x, y = self.me
            xg, yg = map(operator.gt, self.me, self.them)

            fields = {
                (True, True): ((x+1, y), (x, y+1), (x, y-1), (x-1, y)),
                (True, False): ((x+1, y), (x, y-1), (x-1, y), (x, y+1)),
                (False, True): ((x-1, y), (x, y+1), (x+1, y), (x, y-1)),
                (False, False): ((x-1, y), (x, y-1), (x+1, y), (x, y+1)),
            }[xg, yg]

            for field in fields:
                if field in self.possibilities(self.me):
                    self.__flee = field
                    return field

            # It looks like we're trapped, so let's return None.
            self.__flee = -1
            return None

        if self.__flee == -1:
            return None

        # Return the cached value:
        return self.__flee

    @property
    def random(self):
        """Returns a random valid move."""

        return self.possibilities(self.me) and random.choice(
            self.possibilities(self.me)) or self.surround(self.me)[0]
