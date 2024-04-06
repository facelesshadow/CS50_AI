import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        """
        PseudoCode for node consistency - 
            for each key in self.domains:
                get the length of that variable...
                remove any values which has letters more or less than the length of that variable...
                use self.domains[v].remove(x) to remove a value x from a variable v's domain.

                crossword.variables - set of all Variables in the puzzle. Each is a Variable object...
                so. self.crossword.variables is a set, for each x in the set, x.length is the length of that variable
                now all the values are in self.domains - a dictionary which maps all the variables to set of its possible words...
        """
        for variable in self.crossword.variables:
            var_len = variable.length
            #now iterate over the whole dictionary of self.domains
            temp = self.domains[variable]
            for element in temp:
                if len(element) != var_len:
                    self.domains[variable].remove(element)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        """
        both x and y are variable objects...
        Arc consistent means - every value in x, has a combination with value in y, which does not cause a conflict
        conflict is when the overlaps places have different letters.
        remove values from x. 
        return true if a revision was made...
        self.domains - a dictionary which maps all the variables to set of its possible words
        """
        revision = False
        if not self.crossword.overlaps[x, y]:
            return revision
        else:
            i, j = self.crossword.overlaps(x, y)
            # now iterate, for each value of y, on each value of x. Do this through self.domain. Remove any value with inconsistency from x's value...
            for y_value in self.domains[y]:
                temp = self.domains[x]
                for x_value in temp:
                    if x_value[i] != y_value[j]:
                        self.domains[x].remove(x_value)
                        revision = True
            
        return revision


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        """
        queue = all arcs in the damn problem... how to get all the arcs?
        for each variable in self.crossword.variable:
             
        """
        if arcs == None:
            arcs = all_arcs()
        
        while arcs:
            temp = arcs
            for element in temp:
                x, y = arcs[element]
                arcs.remove(element)
                if revise(x, y):
                    if len(self.domains[x]) == 0:
                        return False
                    for z in (self.crossword.neighbors(x) - {y}):
                        arcs.add((z, x))

        return True


        raise NotImplementedError


    def all_arcs(self):
        # returns a list of all arcs... each element being a tuple (x,y) where x and y are nodes...
        arcs = []
        for x in self.crossword.varible:
            for y in self.crossword.neighbors(x):
                arcs.append(x, y)

        arcs = set(arcs)
        arcs = list(arcs)

        arcs = temp
        for element in temp:
            a = temp[element][0]
            b = temp[element][1]
            for element2 in temp:
                if temp[element2] == (b, a):
                    arcs.remove(element2)

        return arcs

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        varible_list = list(self.crossword.variable)
        for element in variable_list:
            # not all the variables be present either wtf...
            if element not in assignment:
                return False

            # not all the variables present, may be mapped to something
            if not assignment[element]:
                return False
            
        
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        h_dict = {}
        values = list(self.domains[var])
    
        for value in values:
            h_dict[value] = 0
    

        for neighbor in list(self.crossword.neighbors(var)):
            i,j = self.crossword.overlaps[var, neighbor]
            for element in list(self.domains[neighbor]):
                for element2 in h_dict:
                    if element2[i] = element[j]:
                        h_dict[element2] += 1
        
        # now sort
        sorted_dict = dict(sorted(h_dict.items(), key=lambda item: item[1], reverse))

        return sorted_dict.keys()
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
