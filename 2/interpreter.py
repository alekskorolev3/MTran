class Interpreter:
    def __init__(self):
        self.scope = dict()
        self.operations = "+-*/"

    def execVal(self, tree):
        try:
            tree_type = tree.type
            children = tree.children
        except AttributeError:
            if tree in self.scope.keys():
                tree_type = "variable"
                children = self.scope[tree]
            else:
                return tree

        if tree_type == "variable":
            return children

        if tree_type == "arg":
            return children[0]

        if tree_type in self.operations:
            left_op = self.execVal(children[0])
            right_op = self.execVal(children[1])

            print(left_op, right_op)

            return left_op + right_op

    def execLoop(self, tree):
        try:
            tree_type = tree.type
            children = tree.children
            local_scope = dict()
        except AttributeError:
            return tree

        assign = self.execVal(children[0].children[-1])

        print("here")

    def exec(self, tree):
        try:
            tree_type = tree.type
            children = tree.children
        except AttributeError:
            return tree

        if tree_type == "init":
            self.scope[children[1]] = self.execVal(children[-1])
            return

        if tree_type == "assign":
            self.scope.update({children[0]: self.execVal(children[-1])})
            return

        if tree_type == "for":
            self.execLoop(tree)

        for child in children:
            if child != "=":
                self.exec(child)
