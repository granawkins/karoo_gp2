import ast, math
from sympy import sympify
from karoo_gp import Branch

DEFAULT_TREE = dict(depth=3,
                    tree_type='g')

class Tree:
    """Wrapper for a root Branch with group-level attrs and methods"""
    def __init__(self, root, fitness=None):
        self.root = root
        self.fitness = fitness

    @classmethod
    def generate(cls, rng, operators, terminals, params={}):
        depth = params.get('depth', DEFAULT_TREE['depth'])
        tree_type = params.get('tree_type', DEFAULT_TREE['tree_type'])
        root = Branch.generate(rng, operators, terminals, tree_type, depth)
        if tree_type == 'r':
            root.update_tree_type('g')
        return cls(root)

    def save(self):
        return f"{self.root.tree_type}{self.root.parse}"

    @classmethod
    def load(cls, saved):
        tree_type = saved[1]
        expr = saved[1:]
        parsed = ast.parse(expr, mode='eval')
        root = Branch.load(parsed, tree_type)
        return cls(root)

    def duplicate(self):
        root = self.root.duplicate()
        return Tree(root, self.fitness)

    def depth(self):
        return self.root.depth()

    def parse(self, **kwargs):
        return self.root.parse(**kwargs)

    def sym(self):
        return sympify(self.root.parse())

    def __repr__(self):
        fit_repr = f" fitness: {str(round(self.fitness, 2))}" if self.fitness else ''
        sym_repr = str(self.sym())
        if len(sym_repr) > 16:
            sym_repr = sym_repr[:13] + "..."
        return f"<Tree: '{sym_repr}'{fit_repr}>"

    def display(self, width=60, symbol_max_len=3):
        output = ''
        last_children = [(self.root, width)]  # Nodes for next depth as (branch, branch_width) tuples
        for i in range(self.root.depth()):
            depth_output = ''          # Text to be printed for this depth
            depth_children = []  # Children from items in this depth

            # Iterate through children of the last depth
            for (branch, branch_width) in last_children:
                symbol = ' ' if branch is None else str(branch.node.symbol)[:symbol_max_len]
                this_output = symbol.center(branch_width)

                this_children = []      # Children from this item
                cum_width = 0           # Cumulative character-width of all subtrees
                cum_cols = 0            # Cumulative maximum node-width of all subtrees
                # If no children, propogate the empty spaces below terminal
                if not branch or not branch.children:
                    cum_cols += 1
                    cum_width += branch_width
                    this_children.append((None, branch_width))
                # If children, fill-in this_output with '_' to first/last child label
                else:
                    children_cols = [c.n_cols() for c in branch.children]
                    total_cols = sum(children_cols)
                    for child, child_cols in zip(branch.children, children_cols):
                        # Convert each child's 'cols' into character spacing
                        cum_cols += child_cols
                        cum_ratio = cum_cols / total_cols
                        target_width = math.ceil(cum_ratio * branch_width) - cum_width
                        remaining_width = branch_width - cum_width
                        child_width = min(target_width, remaining_width)
                        # Add record and update tracked values
                        this_children.append((child, child_width))
                        cum_width += child_width
                    # Add lines to the output
                    start_padding = this_children[0][1] // 2          # Midpoint of first child
                    end_padding = branch_width - (this_children[-1][1] // 2)  # ..of last child
                    with_line = ''
                    for i, v in enumerate(this_output):
                        with_line += '_' if (i > start_padding and i < end_padding and v == ' ') else v
                    this_output = with_line
                depth_output += this_output
                depth_children += this_children
            last_children = depth_children
            if last_children:
                depth_output += '\n'
            output += depth_output
        return output

    ##############
    #   EVOLVE   #
    ##############

    def point_mutate(self, rng, operators, terminals):
        """Mutates the node of a random branch"""
        r = self.root
        c = rng.randint(0, r.n_children())
        child, _ = r.get_child(c)
        child.mutate(rng, operators, terminals)
        self.fitness = None

    def full_mutate(self, rng, operators, terminals):
        """Mutates all nodes of a random branch and its children"""
        r = self.root
        c = rng.randint(0, r.n_children())
        child, _ = r.get_child(c)
        child.mutate(rng, operators, terminals, recursive=True)
        self.fitness = None

    def crossover(self, rng, mate):
        # Copy a non-root branch from spouse
        m_root = mate.root
        m_index = rng.randint(1, m_root.n_children())
        m_branch, _ = m_root.get_child(m_index)
        m_branch = m_branch.duplicate()

        # Create an offspring and replace random non-root branch
        o_root = self.root.duplicate()
        o_index = rng.randint(1, o_root.n_children())
        o_root.set_child(o_index, m_branch)

        return Tree(o_root)
