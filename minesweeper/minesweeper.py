import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for element in self.knowledge:
            element.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge

                A cell and its neighbouring number of mines given, in cell and count respectively,
                so the sentence would go something like this - 

                Initialise a new sentence, with count as the count, and the set of cells being nearby cells.
                1. mark that the cell has been clicked.
                2. mark the cell as safe, as if it was not, then it was already game over. 
                3. Add the new sentence which I just formed upar, in the AI knowledge base.
                    Make sure to only add the cells to the set whose state is undetermined.
                4. Now comes the riyal shit. inference needs to be made, if they can be made, based 
                    on the pre-existing and new sentences in the knowledge base.
                    1. If a sentences has count = 0, then each cell in the sentence is safe, and remove 
                    those cells from any other sentence too.
                    2. If a sentence has count = number of elements in it, then each cell is a mine, 
                    then mark each cell as a mine, and also remove each cell from any other sentence, 
                    and also update its count.
                    3. Also, if the intersection of two sets is not an empty set, then subtract 
                        the sets and also subtract their count (number of mines), from larger set - smaller set.
                    4. repeat, until, ? until when????
                        For now, I seriously think that two for loops will do the trick
                        - For each element1 in the KB list:
                            For each element2 in the KB list:
                                Do your shite....
        """
        # Mark the cell as a move that has been made.
        self.moves_made.add(cell)
        
        # Mark the cell as safe
        self.safes.add(cell)
        #Also make sure that this element is removed from every sentence in the knowledge base
            #Need to make a copy of the set as an element can not be removed from a set if the set is being iterated upon
        for element in self.knowledge:
            if cell in element.cells:
                element.cells.remove(cell)

    
        # add the new sentence in the knowledge base    
        '''
            1. get all the nearby cells. 
            2. eliminate all the nearby cells which are already in safe or in mines or already made moves.
                while eliminating already known mines, also update the count(number of nearby mines...)
           3. then form a new sentence, with count as number of mines, and the sentence. 
        '''

        new_cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                    if 0 <= i < self.height and 0 <= j < self.width:
                        # check if the neighbouring cell is a known mine
                        if (i, j) in self.mines
                            # Lower the mine count 
                            count -= 1
                            continue
                        #check if the neighbouring cell is a known safe cell (includes the cells which are already a made move)
                        elif (i, j) in self.safes:
                            continue
                        else:
                            new_cells.add((i, j))

        new_sentence = Sentence()
        new_sentence.cells = new_cells
        new_sentence.count = count

        self.knowledge.append(new_sentence)

 '''
 Knowledge base - list of sentences
 sentences - object with a (set of cells) + (a count)
 for each sentence1 in element in the list called knowledge base,
 for each sentence2 in element in list called knowledge base,
    if sentence1 intersection sentence2 is not 0:
        then subset wala set subtract kro, count new karo, and then new sentence add karo...
 '''


        # ALSO
        # Everytime the knowledge base is changes, then it means that there is a possibility of new inferences
        # So each time KB is changes, the inference algo should repeat over it.
        for element1 in self.knowlege:
            for element2 in self.knowledge:
                if element1.cells = element2.cells:
                    continue
                elif element1.cells.issubset(element2.cells):
                    new_cells = element1.cells.difference(element2.cells)
                    new_count = element1.count - element2.count
                    new_sentence = Sentence()
                    new_sentence.cells = new_cells
                    new_sentence.count = new_count
                elif element2.cells.issubset(element1.cells):
                    new_cells = element2.cells.difference(element1.cells)
                    new_count = element2.count - element1.count
                    new_sentence = Sentence()
                    new_sentence.cells = new_cells
                    new_sentence.count = new_count

        # To infer that a given cell is mine
        for element1 in self.knowledge:
            # if count = no of cells, add all the cells to known mines. 
            if len(element1.cells) == element1.count:
                for element2 in element1.cells:
                    self.mines.append(element2)

            if element1.count == 0:
                for element2 in element1.cells:
                    self.safes.append(element2)

                
        # to infer that a given set of cells is safe
            
        raise NotImplementedError   

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # WRONG
        # Should also consider the case that self.safes is empty

        if not self.safes:
            return None
        else:  
            for element in self.safes:
                if element not in self.moves_made:
                    return element
                else:
                    return None


        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines

            1) Cells that have not already been choosen - not in self.moves_made
            2) not known to be mine - not in self.mines

            I need to figure out how to get the list of all such elements... 
            Maybe done by - 
            1. Getting a list of all elements.
            2. Eliminate all elements which are 
                1. Moves_made
                2. known_mines
            3. Select a random element out of the list.
            I can do one thing - get the cells from the knowledge base, and then select any one at random from the damn sets.
            Wait wait wait, To get the cells, I do have the height and the width of the board, I can just create all the cells by myself wtf -_-
        """
        for i in range(self.height):
            clear_cells = []
            for j in range(self.width):
                if (i, j) in self.moves_made:
                    continue
                elif (i, j) in self.mines:
                    continue
                else:
                    clear_cells.append(i, j)
                
                return random.choice(clear_cells)
        


        raise NotImplementedError
