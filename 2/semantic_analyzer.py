class SemanticAnalyzer:

    def __init__(self):
        self.variables = {}
        self.operations = "+-*/"

    def gettype(self, tree):
        try:
            tree_type = tree.type
            children = tree.children
        except AttributeError:
            return tree

        if tree_type == "arg":
            return type(children[0]).__name__
        if tree_type in self.operations:
            return self.analyze(tree)

    def analyze(self, tree, _type=None):
        try:
            tree_type = tree.type
            children = tree.children
            _type = _type
        except AttributeError:
            return tree

        if tree_type in self.operations or tree_type == "condition":
            left_op = children[0]
            if tree_type == "condition":
                right_op = children[-1]
            else:
                right_op = children[1]

            if left_op in self.variables.keys():
                lt = self.variables.get(left_op).get("type")
            else:
                lt = self.gettype(left_op)

            if right_op in self.variables.keys():
                rt = self.variables.get(right_op).get("type")
            else:
                rt = self.gettype(right_op)

            if lt != rt:
                raise SyntaxError("Mismatch types in " + str(tree_type) + ": " + str(lt) + " and " + str(rt))
            else:
                return lt

        if tree_type == "arg":
            if _type is not None:
                if type(children[0]).__name__ != _type:
                    raise SyntaxError("Type " + str(_type) + " cannot initialize " + str(children[0]))
                return

        if tree_type == "array_init":
            self.analyze(children[0], _type)
            return

        if tree_type == "init_block":
            for child in children:
                if child != ",":
                    if self.gettype(child) != _type:
                        raise SyntaxError("Wrong initialization of array")
            return

        if tree_type == "indexing_op":

            if children[0] in self.variables.keys():
                if self.variables.get(children[0]).get("type") != _type:
                    raise SyntaxError("Mismatch types on initialization")

            if self.gettype(children[1]) != _type:
                raise SyntaxError("Wrong argument type in indexing operation")

            return

        if tree_type == "init":
            self.variables[children[1]] = {"type": children[0], "value": children[1]}

            if len(children) > 2:
                self.analyze(children[-1], children[0])
            return

        if tree_type == "assign":
            self.analyze(children[-1], self.variables.get(children[0]).get("type"))
            return

        for child in children:
            if child != "=":
                self.analyze(child)
