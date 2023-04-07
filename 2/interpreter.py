class Interpreter:
    def __init__(self):
        self.scope = dict()
        self.operations = "+-*/"
        self.local_scope = []

    def execVal(self, tree, local_scope=None):
        try:
            tree_type = tree.type
            children = tree.children
        except AttributeError:
            if local_scope:
                if tree in self.local_scope[-1].keys():
                    tree_type = "variable"
                    children = self.local_scope[-1][tree]
                else:
                    i = 0
                    for _s in reversed(self.local_scope):
                        i = i - 1
                        if tree in _s.keys():
                            tree_type = "variable"
                            children = self.local_scope[i][tree]
                            continue

                if tree_type is None:
                    if tree in self.scope.keys():
                        tree_type = "variable"
                        children = self.scope[tree]
                    else:
                        return tree

            else:
                if tree in self.scope.keys():
                    tree_type = "variable"
                    children = self.scope[tree]
                else:
                    return tree

        if tree_type == "variable":
            return children

        if tree_type == "arg":
            return children[0]

        if tree_type == "array_init":
            _args = list()
            args = children[0].children

            for arg in args:
                if arg != ",":
                    _args.append(arg.children[0])

            return _args

        if tree_type in self.operations:
            if local_scope:
                left_op = self.execVal(children[0], True)
                right_op = self.execVal(children[1], True)
            else:
                left_op = self.execVal(children[0])
                right_op = self.execVal(children[1])

            if tree_type == "+":
                return left_op + right_op
            if tree_type == "-":
                return left_op - right_op
            if tree_type == "*":
                return left_op * right_op
            if tree_type == "/":
                if right_op == 0:
                    raise SyntaxError("Division by zero")
                return left_op / right_op

    def execLoop(self, tree):
        try:
            tree_type = tree.type
            children = tree.children
            self.local_scope.append({})
        except AttributeError:
            return tree

        if children[0].type == "init":
            self.local_scope[-1][children[0].children[1]] = self.execVal(children[0].children[-1])
            var = self.local_scope[-1][children[0].children[1]]
        else:
            self.local_scope[-1][children[0].children[0]] = self.execVal(children[0].children[-1])
            var = self.local_scope[-1][children[0].children[0]]

        condition = self.execVal(children[1].children[-1])
        condition_sign = children[1].children[1]
        change_val = children[2].children[-1].type

        if change_val == "increment":
            if condition_sign == "<=":
                for _var in range(var, condition, 1):
                    self.local_scope[-1][children[0].children[1]] = _var
                    self.exec(tree.children[3], True)
                self.local_scope.pop()
                return
            elif condition_sign == "<":
                for _var in range(var, condition - 1, 1):
                    self.local_scope[-1][children[0].children[1]] = _var
                    self.exec(tree.children[3], True)
                self.local_scope.pop()
                return
        elif change_val == "decrement":
            if condition_sign == ">=":
                for _var in range(condition, var, -1):
                    self.local_scope[-1][children[0].children[1]] = _var
                    self.exec(tree.children[3], True)
                self.local_scope.pop()
                return
            elif condition_sign == ">":
                for _var in range(condition - 1, var, -1):
                    self.local_scope[-1][children[0].children[1]] = _var
                    self.exec(tree.children[3], True)
                self.local_scope.pop()
                return

    def execConditional(self, tree, local_scope=None):
        try:
            tree_type = tree.type
            children = tree.children
        except AttributeError:
            return tree

        _cond = children[0]

        if _cond.children[1] == "==":
            if local_scope:
                if self.execVal(_cond.children[0], True) == self.execVal(_cond.children[2], True):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()

            else:
                if self.execVal(_cond.children[0]) == self.execVal(_cond.children[2]):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()

        if _cond.children[1] == "<=":
            if local_scope:
                if self.execVal(_cond.children[0], True) <= self.execVal(_cond.children[2], True):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()

            else:
                if self.execVal(_cond.children[0]) <= self.execVal(_cond.children[2]):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()

        if _cond.children[1] == "<":
            if local_scope:
                if self.execVal(_cond.children[0], True) < self.execVal(_cond.children[2], True):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()
                    return
            else:
                if self.execVal(_cond.children[0]) < self.execVal(_cond.children[2]):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()
                    return

        if _cond.children[1] == ">=":
            if local_scope:
                if self.execVal(_cond.children[0], True) >= self.execVal(_cond.children[2], True):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()
                    return
            else:
                if self.execVal(_cond.children[0]) >= self.execVal(_cond.children[2]):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()
                    return

        if _cond.children[1] == ">":
            if local_scope:
                if self.execVal(_cond.children[0], True) > self.execVal(_cond.children[2], True):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()
                    return
            else:
                if self.execVal(_cond.children[0]) > self.execVal(_cond.children[2]):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()
                    return

        if _cond.children[1] == "!=":
            if local_scope:
                if self.execVal(_cond.children[0], True) != self.execVal(_cond.children[2], True):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()
                    return
            else:
                if self.execVal(_cond.children[0]) != self.execVal(_cond.children[2]):
                    self.local_scope.append({})
                    self.exec(children[1], True)
                    self.local_scope.pop()
                    return

        if len(children) > 2:
            if _cond.children[1] == "==":
                if local_scope:
                    if self.execVal(_cond.children[0], True) != self.execVal(_cond.children[2], True):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()
                        return
                else:
                    if self.execVal(_cond.children[0]) != self.execVal(_cond.children[2]):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()
                        return

            if _cond.children[1] == "<=":
                if local_scope:
                    if self.execVal(_cond.children[0], True) > self.execVal(_cond.children[2], True):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

                else:
                    if self.execVal(_cond.children[0]) > self.execVal(_cond.children[2]):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

            if _cond.children[1] == "<":
                if local_scope:
                    if self.execVal(_cond.children[0], True) >= self.execVal(_cond.children[2], True):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

                else:
                    if self.execVal(_cond.children[0]) >= self.execVal(_cond.children[2]):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

            if _cond.children[1] == ">=":
                if local_scope:
                    if self.execVal(_cond.children[0], True) < self.execVal(_cond.children[2], True):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

                else:
                    if self.execVal(_cond.children[0]) < self.execVal(_cond.children[2]):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

            if _cond.children[1] == ">":
                if local_scope:
                    if self.execVal(_cond.children[0], True) <= self.execVal(_cond.children[2], True):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

                else:
                    if self.execVal(_cond.children[0]) <= self.execVal(_cond.children[2]):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

            if _cond.children[1] == "!=":
                if local_scope:
                    if self.execVal(_cond.children[0], True) == self.execVal(_cond.children[2], True):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

                else:
                    if self.execVal(_cond.children[0]) == self.execVal(_cond.children[2]):
                        self.local_scope.append({})
                        self.exec(children[3], True)
                        self.local_scope.pop()

    def exec(self, tree, local_scope=None):
        try:
            tree_type = tree.type
            children = tree.children
            local_scope = local_scope
        except AttributeError:
            return tree

        if tree_type == "func_call":

            if local_scope:
                if children[0] == "printf":
                    print(self.execVal(children[1].children[0], True))
                    return
            else:
                if children[0] == "printf":
                    print(self.execVal(children[1].children[0]))
                    return

        if tree_type == "init":
            if local_scope:
                self.local_scope[-1][children[1]] = self.execVal(children[-1])
            else:
                self.scope[children[1]] = self.execVal(children[-1])
            return

        if tree_type == "assign":
            if local_scope:
                if children[0] in self.local_scope[-1].keys():
                    self.local_scope[-1].update({children[0]: self.execVal(children[-1], True)})
                else:
                    i = 0
                    for _s in reversed(self.local_scope):
                        i = i - 1
                        if children[0] in _s.keys():
                            self.local_scope[i].update({children[0]: self.execVal(children[-1], True)})
                            continue
            else:
                self.scope.update({children[0]: self.execVal(children[-1])})
            return

        if tree_type == "for":
            self.execLoop(tree)
            return

        if tree_type == "if":
            if local_scope:
                self.execConditional(tree, True)
            else:
                self.execConditional(tree)
            return

        for child in children:
            if child != "=":
                if local_scope:
                    self.exec(child, True)
                else:
                    self.exec(child)
