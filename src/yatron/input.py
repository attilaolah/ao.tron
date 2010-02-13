import sys

from yatron.board import Board


def plaintext(infile):
    """Reads the necessary information from :param:`infile`.

    On success, sets up and returns a :class:`yatron.bot.Bot` instance.

    Note: we convert the strings to tuples; iterating over tuples is almost two
    times as fast as iterating over strings.

    """

    raw = (line[:-1] for line in infile.readlines() if line != '\n')
    dimensions = tuple((int(x) for x in raw.next().split()))
    # Note: we need to reverse in order to get the right coordination system.
    lines = tuple(reversed([tuple(line) for line in raw]))

    return Board(dimensions, lines)
