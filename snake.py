"""
Snake Problem
=============

Question
--------

Write a program that calculates how many different ways a snake of
length 16 can be laid out on a 4x4 grid.


Example
-------

Given a grid like so::

    +---------+---------+---------+---------+
    |         |         |         |         |
    |    0    |    1    |    2    |    3    |
    |         |         |         |         |
    +---------+---------+---------+---------+
    |         |         |         |         |
    |    4    |    5    |    6    |    7    |
    |         |         |         |         |
    +---------+---------+---------+---------+
    |         |         |         |         |
    |    8    |    9    |   10    |   11    |
    |         |         |         |         |
    +---------+---------+---------+---------+
    |         |         |         |         |
    |   12    |   13    |   14    |   15    |
    |         |         |         |         |
    +---------+---------+---------+---------+


one path would be
``[0, 1, 2, 3, 7, 6, 5, 4, 8, 9, 10, 11, 15, 14, 13, 12]``::

    +---------+---------+---------+---------+
    |  Start  |         |         |         |
    |    0---------1---------2---------3    |
    |         |         |         |    |    |
    +---------+---------+---------+----|----+
    |         |         |         |    |    |
    |    4---------5---------6---------7    |
    |    |    |         |         |         |
    +----|----+---------+---------+---------+
    |    |    |         |         |         |
    |    8---------9---------10-------11    |
    |         |         |         |    |    |
    +---------+---------+---------+----|----+
    |   End   |         |         |    |    |
    |    12-------13--------14--------15    |
    |         |         |         |         |
    +---------+---------+---------+---------+


and another ``[5, 6, 10, 9, 8, 4, 0, 1, 2, 3, 7, 11, 15, 14, 13, 12]``::

    +---------+---------+---------+---------+
    |         |         |         |         |
    |    0---------1---------2---------3    |
    |    |    |         |         |    |    |
    +----|----+---------+---------+----|----+
    |    |    |  Start  |         |    |    |
    |    4    |    5---------6    |    7    |
    |    |    |         |    |    |    |    |
    +----|----+---------+----|----+----|----+
    |    |    |         |    |    |    |    |
    |    8---------9--------10    |   11    |
    |         |         |         |    |    |
    +---------+---------+---------+----|----+
    |  End    |         |         |    |    |
    |   12--------13--------14--------15    |
    |         |         |         |         |
    +---------+---------+---------+---------+

There are many more but what is the total of all possible unique paths?


Rules
-----

* Do not output all the paths, just the total path count.  A single
  number is all that is required as output of this program.

* Diagonal movements are not allowed.

* Use Python 3.8+ and the standard modules only.  No Numpy or any third
  party modules.


Tips
----

* The answers for smaller square grids:

    * 1x1 grid (snake length 1) has 1 path.
    * 2x2 grid (snake length 4) has 8 paths.
    * 3x3 grid (snake length 9) has 40 paths.

* Consider performance when writing your solution.

* We will test your solution with square grids of different sizes.

"""

import math
import time
import itertools
import traceback

version = '1.0'
symmetric_snakes = False

class event_log:
    """A simple logger, designed to form the basis for a non-interactive UI"""
    def __init__(self):
        self.perf_counter_reference = time.perf_counter() # use time.perf_counter() because time.time() is not recommended for measuring small intervals (e.g. can count backwards!)
        self.start_time = time.time() # start time is the number of seconds since 1st Jan 1970, roughly corresponding to the first airing of Monty Python
        self.events = {}
    def record_event(self, event_name, display=True):
        elapsed_time = time.perf_counter() - self.perf_counter_reference
        event_time = self.start_time + elapsed_time
        self.events[event_name] = event_time
        if display: print(event_name.ljust(60), time.ctime(event_time))

def brute_force_count(edge_length):
    """Generate all possible permutations of grid squares and count how many of these form a valid path."""
    count = 0
    snake_length = edge_length ** 2
    coordinates = [i for i in range(snake_length)]
    set_of_all_paths = itertools.permutations(coordinates)
    for path in set_of_all_paths:
        if is_valid(path, edge_length, snake_length):
            count += 1
            # could also store the path at this stage
            
def is_valid(path, edge_length, snake_length):
    """Function to check if a given set of coordinates forms a valid path.
    It is helpful to consider the grid as a set of coordinates labelled as in the order that you would read words on a page.
    e.g. 4x4 grid:  1,  2,  3,  4
                    5,  6,  7,  8
                    9,  10, 11, 12
                    13, 14, 15, 16
    The path is a list of these coordinates with a start and end point. It forms a valid snake if each coordinate is either horizontally or vertically adjacent to the next coordinate.
    """
    assert snake_length == len(path), f'Invalid collection of arguments provided to is_valid(): edge_length={edge_length}, snake_length={snake_length}, path={path}'
    assert snake_length == edge_length ** 2, f'Invalid collection of arguments provided to is_valid(): edge_length={edge_length}, snake_length={snake_length}, path={path}'
    # these assertions are probably too fussy, while also not covering all possible problems!
    for i in range(snake_length-1):
        a, b = path[i:i+2] # each step straddles two points on the grid
        gap = abs(a - b)
        horizontally_adjacent = (gap == 1) and ((a // edge_length) == (b // edge_length)) # adjacent if coordinates are 1 space apart and share the same row
        vertically_adjacent = (gap == edge_length)
        adjacent = horizontally_adjacent or vertically_adjacent
        if not adjacent: return(False) # if there is a break in the path then the whole snake is invalid
    return(True) # if there are no breaks in the path then the snake is valid

class node:
    """A node object consists of a label and a list of adjacent nodes.
       The node labels correspond to the order that you would read words on a page.
       e.g. 3x3 grid:  0, 1, 2
                       3, 4, 5
                       6, 7, 8
    """
    def __init__(self, label, edge_length):
        self.label = label
        self.adjacent_nodes = []
        for node in range(edge_length**2):
            a, b = node, label
            gap = abs(a - b)
            horizontally_adjacent = (gap == 1) and ((a // edge_length) == (b // edge_length)) # adjacent if coordinates are 1 space apart and share the same row
            vertically_adjacent = (gap == edge_length)
            adjacent = horizontally_adjacent or vertically_adjacent
            if adjacent: self.adjacent_nodes.append(node)

class grid:
    """Generate an edge_length x edge_length grid of nodes and count the number of paths that lie on this grid."""
    def __init__(self, edge_length):
        self.nodes = [node(i, edge_length) for i in range(edge_length**2)]
        self.find_paths()
    def find_paths(self):
        self.path_count = 0
        for node in self.nodes: # pick each of the possible starting points
            path = [node]
            labels = [node.label] # this list will mirror the 'path' variable - a second list is required to facilitate in operations (the 'adjacent nodes' linked to each node object are integers rather than node objects)
            self.explore_path(path, labels)
    def explore_path(self, path, labels):
        """Recursive function that inspects the end point of an incomplete path to see if it can be extended.
           If a complete path is discovered then increment path_count."""
        if len(path) == len(self.nodes): self.path_count += 1 # check if the path is complete (do this early to ensure that the algorithm works corerctly when edge_length=1)
        else:
            current_node = path[-1] # select the most recently visited node in the path (this will be the one at the end of the path list)
            for adjacent_node in current_node.adjacent_nodes:
                if adjacent_node not in labels:
                    new_path, new_labels = path.copy(), labels.copy() # .copy() is essential to avoid collisions between different branches of the recursive function
                    new_path.append(self.nodes[adjacent_node]) # this relies on the nodes being correctly ordered and enumerated, which is not ideal
                    new_labels.append(adjacent_node)
                    self.explore_path(new_path, new_labels) # notice that this can happen more than one time per function call

def path_count(edge_length: int) -> int:
    """
    Do not change the name, argument, or return type of this function.

    :param edge_length: The number of cells along the edge of a square
                        grid.
    :return: The sum of all possible unique paths on a square grid of
             size: edge_length x edge_length
    """
    count = grid(edge_length).path_count
    if symmetric_snakes: result = count / 2 # divide by two if the start point is indistiguishable from the end point
    else: result = count
    if float(result).is_integer(): return(int(result))
    else: raise ValueError(f'path_count() has calculated a non-integer result: {result}')

def test_program(*args, skip_errors=True):
    """Run path_count() for each of the given arguments and print the results"""
    clock = event_log()
    clock.record_event(f'Snake Counter {version} initiated')
    for arg in args:
        try:
            clock.record_event(f'Calculating: {arg}')
            edge_length = int(arg) # int() allows a wide set of arguments (which may not be desirable) and provides a useful error message if a bogus argument is given
            snake_length = edge_length ** 2
            result = path_count(edge_length=edge_length)
            path_or_paths = 'path' if result == 1 else 'paths'
            clock.record_event(f'{edge_length}x{edge_length} grid (snake length {snake_length}) has {result} {path_or_paths}.')
        except Exception as error:
            if skip_errors: clock.record_event(f'{type(error)}, {error}, {traceback.extract_tb(error.__traceback__)}') # doesn't give as much information as raising the exception but allows program to continue
            else: raise error

if __name__ == '__main__':
    test_program(False, 1, 2.0, math.pi, '4', 'silly string', 5) # run time is reasonable for 5 but not for larger numbers

"""
Discussion
=======

I could see four reasonable approaches.
    1) Brute force - test all of the permutations
    2) Try to build paths iteratively, only visiting adjacent squares
        - better than brute force approach because you can dismiss a very large number of solutions without testing them (big advantage) 
        - the symmetry of the problem means that you only have to test a subset of the possible start and end points (modest advantage)
    3) Generate a formula, likely using some form of inductive reasoning
    4) Try to find a pre-existing solution, likely drawing on results from graph theory
        - notice that the grid forms a bipartite graph

My first attempt at a solution was to implement a naive brute force approach.
This is obviously very far from optimal but it was simple to encode and served some useful purposes:
    - explores the question in more depth
    - produces solutions for small edge lengths which can be used to verify other soltuions
    - provides a solution if other approaches don't bear fruit (e.g. if time runs out)
    - non-solution framework elements could be re-used

Following this I spent a little time trying to develop a formula.
It quickly became apparent that the problem is tricky because some aspects are not as symmetrical as they first appear.
For example, not all edge squares will generate the same number of paths.
Based on this observation I dismissed approaches 3) and 4) as too unreliable as a means to finding a solution within a couple of hours.

I then constructed a recursive algorithm that tries to find all possible paths given an incomplete path.
This could have been improved by limiting the number of starting points and multiplying the answer accordingly.
However, the time investment for generating the improved code did not look worth the payoff.
I'd estimate that limiting the start points probably reduces the number of solutions by ~1/8.
In many applications an improvement of this magnitude would be significant, but in this case the size of the problem increases extremely rapidly.
To provide context: my estimate is that moving from a brute force to iterative solution reduces the number of cases that needed to be tested by more than ((edge_length**2)-3)! (factorial) which is significantly bigger than 8. The 3 in this formula is the (at most) 3 directions that a path could travel in when exiting a square.
"""