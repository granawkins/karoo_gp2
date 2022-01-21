from karoo_gp import Operator, Terminal
import ast

operator_ref = {ast.Add: '+',
                ast.Sub: '-',
                ast.Mult: '*',
                ast.Div: '/',
                ast.Pow: '**',
                ast.USub: '-'}

class Branch:
    """An recursive tree element with a node, parent and children"""

    #################
    #  INITIALIZE   #
    #################

    def __init__(self, node, tree_type, parent=None):
        self.node = node
        self.tree_type = tree_type
        self.parent = parent
        self.children = None

    @classmethod
    def generate(cls, rng, operators, terminals, tree_type, depth, parent=None):
        """Return a randomly generated branch (recursive)"""

        # Grow trees flip a coin for operator/terminal (except root)
        if tree_type == 'g' and parent is not None:
            terminal = rng.choice([True, False])
        else:
            terminal = False

        # Create terminal or operator
        if terminal or depth == 0:
            node = rng.choice(terminals.get())
            branch = cls(node, tree_type, parent=parent)
        else:
            node = rng.choice(operators.get())
            branch = cls(node, tree_type, parent=parent)

            # Generate children
            args = (rng, operators, terminals, tree_type, depth-1)
            branch.children = [cls.generate(*args, parent=branch) for c in range(node.arity)]
        return branch

    def duplicate(self):
        dup = Branch(self.node, self.tree_type, self.parent)
        if self.children:
            dup.children = [c.duplicate() for c in self.children]
        return dup

    def update_tree_type(self, tree_type):
        self.tree_type = tree_type
        if self.children:
            for c in self.children:
                c.update_tree_type(tree_type)

    @classmethod
    def load(cls, expr, tree_type):
        if isinstance(expr, ast.Name):
            node = Terminal(expr.id)
            branch = Branch(node, tree_type)
        elif isinstance(expr, ast.Num):
            node = Terminal(expr.value)
            branch = Branch(node, tree_type)
        else:
            if type(expr) == ast.Expression:
                expr = expr.body
            symbol = operator_ref[type(expr.op)]
            node = Operator(symbol)
            branch = Branch(node, tree_type)
            if isinstance(expr, ast.UnaryOp):
                branch.children = [cls.load(expr.left, tree_type)]
            elif isinstance(expr, ast.BinOp):
                branch.children = [cls.load(expr.left, tree_type), cls.load(expr.right, tree_type)]
            else:
                raise ValueError("Unrecognized op type in load:", expr.op)
        return branch

    #################
    #    DISPLAY    #
    #################

    def __repr__(self):
        return f"<Branch: {self.node.__repr__()}>"

    def parse(self):
        """Return full list of symbols (recursive)"""
        if not self.children:
            return self.node.symbol
        elif len(self.children) == 1:
            return f"{self.node.symbol}{self.children[0].parse()}"
        elif len(self.children) == 2:
            return f"{self.children[0].parse()}{self.node.symbol}{self.children[1].parse()}"

    def save(self):
        if not self.children:
            return self.node.symbol
        elif len(self.children) == 1:
            return f"({self.node.save}{self.children[0].save()})"
        elif len(self.children) == 2:
            return f"({self.children[0].save()}{self.node.symbol}{self.children[1].save()})"


    #################
    #   NAVIGATE    #
    #################

    def depth(self):
        if self.children:
            return 1 + max([c.depth() for c in self.children])
        else:
            return 1

    def n_children(self):
        """Return the total number of children (excluding root) as an int (recursive)"""
        if not self.children:
            return 1
        else:
            n_ch = sum([c.n_children() for c in self.children])
            n = n_ch if not self.parent else n_ch + 1
            return n

    def get_child(self, n):
        """Returns the child in the nth position as the 0th element of a 2-tuple (recursive)"""
        if n == 0:
            return self, n
        elif not self.children:
            return False, n-1
        else:
            n = n - 1
            for child in self.children:
                target, new_n = child.get_child(n)
                n = new_n
                if target:
                    return target, n
            return False, n

    def set_child(self, n, branch):
        """Replace the child in the nth position with supplied branch (recursive)"""
        for i, child in enumerate(self.children):
            n -= 1
            if n == 0:
                self.children[i] = branch
                return True, n
            if child.children:
                target, new_n = child.set_child(n, branch)
                if target:
                    return True, n
                else:
                    n = new_n
        return False, n

    #################
    #    EVOLVE     #
    #################

    def mutate(self, rng, operators, terminals, recursive=False):
        """Updates own value from a provided list of operators or terminals (optionally recursive)"""
        if type(self.node) == Operator:
            self.node = rng.choice(operators.get())
        elif type(self.node) == Terminal:
            self.node = rng.choice(terminals.get())
        if recursive and self.children:
            for child in self.children:
                child.mutate(rng, operators, terminals, recursive=True)
