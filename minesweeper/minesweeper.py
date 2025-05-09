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
        if len(self.cells) == self.count:
            print(f"All cells are mines: {self.cells}")
            return self.cells
        else:
            print("No known mines in this sentence.")

            return set()

    def known_safes(self):
        if self.count == 0:
            print(f"All cells are safes: {self.cells}")

            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


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
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Updates the AI's knowledge base given that a safe cell has been revealed,
        along with the number of nearby mines.
        """
        # Step 1 & 2: Record the move and mark the cell as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Step 3: Gather neighboring cells and adjust count based on known mines
        neighbors = self._get_neighbors(cell)
        adjusted_count = count - sum(1 for neighbor in neighbors if neighbor in self.mines)

        # Create and add a new sentence based on the adjusted information
        sentence = Sentence(neighbors - self.safes - self.mines, adjusted_count)
        if sentence.cells:
            self.knowledge.append(sentence)

        # Step 4: Update knowledge and infer new safe cells or mines
        self._update_knowledge_with_inferences()

    def _get_neighbors(self, cell):
        """Helper function to return valid neighboring cells of a given cell."""
        i, j = cell
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        return {(i + di, j + dj) for di, dj in directions if 0 <= i + di < self.height and 0 <= j + dj < self.width}

    def _update_knowledge_with_inferences(self):
        """Updates the knowledge base by marking known mines and safe cells."""
        updated = True
        while updated:
            updated = False
            mines_to_add = set()
            safes_to_add = set()

            for sentence in self.knowledge:
                mines_to_add.update(sentence.known_mines())
                safes_to_add.update(sentence.known_safes())

            for mine in mines_to_add - self.mines:
                self.mark_mine(mine)
                updated = True
            for safe in safes_to_add - self.safes:
                self.mark_safe(safe)
                updated = True

            new_inferences = self._infer_from_existing_sentences()
            if new_inferences:
                self.knowledge.extend(new_inferences)
                updated = True

            self.knowledge = [sentence for sentence in self.knowledge if sentence.cells]

    def _infer_from_existing_sentences(self):
        """Generates new sentences based on subset relations in existing knowledge."""
        new_sentences = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2 and sentence2.cells.issubset(sentence1.cells):
                    inferred_cells = sentence1.cells - sentence2.cells
                    inferred_count = sentence1.count - sentence2.count
                    inferred_sentence = Sentence(inferred_cells, inferred_count)
                    if inferred_sentence not in self.knowledge and inferred_sentence not in new_sentences:
                        new_sentences.append(inferred_sentence)
        return new_sentences

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cells = {(i, j) for i in range(self.height) for j in range(self.width)}
        possible_moves = all_cells - self.moves_made - self.mines

        if possible_moves:
            return random.choice(list(possible_moves))
        return None
