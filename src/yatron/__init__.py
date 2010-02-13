from sys import stdout


def printmove(direction):
    """Prints the current move to the standard output."""
    print direction
    stdout.flush()

# The default move function is `printmove`.
move = printmove
