from karoo_gp import Branch
from sympy import sympify

DEFAULT_TREE = dict(depth=3,
                    tree_type='g')

class Tree:
    """Wrapper for a root Branch with group-level attrs and methods"""
    def __init__(self, root):
        self.root = root
        self.fitness = None

    @classmethod
    def generate(cls, rng, operators, terminals, params={}):
        depth = params.get('depth', DEFAULT_TREE['depth'])
        tree_type = params.get('tree_type', DEFAULT_TREE['tree_type'])
        root = Branch.generate(rng, operators, terminals, tree_type, depth)
        return cls(root)

    def parse(self):
        return self.root.parse()

    def sym(self):
        return sympify(self.root.parse())

    def __repr__(self):
        fit_repr = f" fitness: {str(round(self.fitness, 2))}" if self.fitness else ''
        sym_repr = str(self.sym())
        if len(sym_repr) > 16:
            sym_repr = sym_repr[:13] + "..."
        return f"<Tree: '{sym_repr}'{fit_repr}>"

    def point_mutate(self, rng, operators, terminals):
        """Mutates the node of a random branch"""
        r = self.root
        c = rng.randint(0, r.n_children())
        child, _ = r.get_child(c)
        child.mutate(rng, operators, terminals)

    def full_mutate(self, rng, operators, terminals):
        """Mutates all nodes of a random branch and its children"""
        r = self.root
        c = rng.randint(0, r.n_children())
        child, _ = r.get_child(c)
        child.mutate(rng, operators, terminals, recursive=True)

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
