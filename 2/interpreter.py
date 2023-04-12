class Interpreter:
    def __init__(self):
        self.scope = dict()
        self.operations = "+-*/%"
        self.local_scope = []

    def execVal(self, tree, local_scope=None, index=None):
        try:
            tree_type = tree.type
            children = tree.children
            index = index
        except AttributeError:
            if local_scope:
                if tree in self.local_scope[-1].keys():
                    tree_type = "variable"
                    children = self.local_scope[-1][tree]
                elif tree not in self.local_scope[-1].keys():
                    i = 0
                    _break = False
                    for _s in reversed(self.local_scope):
                        i = i - 1
                        if tree in _s.keys():
                            tree_type = "variable"
                            children = self.local_scope[i][tree]
                            _break = True
                            break

                    if tree in self.scope.keys():
                        tree_type = "variable"
                        children = self.scope[tree]
                    elif not _break:
                        return tree

                if tree_type is None:
                    if tree in self.scope.keys():
                        tree_type = "variable"
                        children = self.scope[tree]
                    else:
                        return tree

                if tree in self.scope.keys():
                    tree_type = "variable"
                    children = self.scope[tree]

            else:
                if tree in self.scope.keys():
                    tree_type = "variable"
                    children = self.scope[tree]
                else:
                    if tree in self.local_scope[-1].keys():
                        tree_type = "variable"
                        children = self.local_scope[-1][tree]
                    elif tree not in self.local_scope[-1].keys():
                        i = 0
                        for _s in reversed(self.local_scope):
                            i = i - 1
                            if tree in _s.keys():
                                tree_type = "variable"
                                children = self.local_scope[i][tree]
                                continue
                    else:
                        if tree in self.scope.keys():
                            tree_type = "variable"
                            children = self.scope[tree]
                        else:
                            return tree

        if index is not None:
            if index < len(children):
                return children[index]
            else:
                raise IndexError("List index out of range")

        if tree_type == "variable":
            return children

        if tree_type == "arg":
            if hasattr(children[0], 'type'):
                if children[0].type == "indexing_op":
                    return self.execVal(children[0], True)
            return children[0]

        if tree_type == "array_init":
            _args = list()
            args = children[0].children

            for arg in args:
                if arg != ",":
                    _args.append(arg.children[0])

            return _args

        if tree_type == "indexing_op":
            if local_scope:
                return self.execVal(children[0], True, self.execVal(children[1]))
            else:
                return self.execVal(children[0], None, self.execVal(children[1]))

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
            if tree_type == "%":
                return left_op % right_op
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

    def execWhile(self, tree, _type=None):
        try:
            tree_type = tree.type
            children = tree.children
            self.local_scope.append({})
            _type = _type
        except AttributeError:
            return tree

        if _type:
            _c = children[0]

            children[0] = children[1]
            children[1] = _c

            self.exec(children[1], True)

        var = self.scope[children[0].children[0]]

        condition = self.execVal(children[0].children[-1])
        condition_sign = children[0].children[1]

        if condition_sign == ">":
            while var > condition:
                self.exec(children[1], True)
                var = self.scope[children[0].children[0]]
        if condition_sign == ">=":
            while var >= condition:
                self.exec(children[1], True)
                var = self.scope[children[0].children[0]]
        if condition_sign == "<":
            while var < condition:
                self.exec(children[1], True)
                var = self.scope[children[0].children[0]]
        if condition_sign == "<=":
            while var < condition:
                self.exec(children[1], True)
                var = self.scope[children[0].children[0]]
        if condition_sign == "==":
            while var < condition:
                self.exec(children[1], True)
                var = self.scope[children[0].children[0]]
        if condition_sign == "!=":
            while var < condition:
                self.exec(children[1], True)
                var = self.scope[children[0].children[0]]

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
                left_op = self.execVal(_cond.children[0], True)
                right_op = self.execVal(_cond.children[2], True)
                if left_op > right_op:
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

            if children[0].type == "indexing_op":
                if local_scope:

                    arr = self.execVal(children[0].children[0], True)

                    index = self.execVal(children[0].children[1], True)

                    arr[index] = self.execVal(children[-1], True)

                    if children[0].children[0] in self.local_scope[-1].keys():
                        self.local_scope[-1].update({children[0].children[0]: arr})
                    elif children[0].children[0] not in self.local_scope[-1].keys():
                        i = 0
                        for _s in reversed(self.local_scope):
                            i = i - 1
                            if children[0] in _s.keys():
                                self.local_scope[i].update({children[0]: arr})
                                continue
                        self.scope.update({children[0].children[0]: arr})
                else:
                    arr = self.execVal(children[0].children[0])

                    index = self.execVal(children[0].children[1])

                    arr[index] = self.execVal(children[-1])

                    self.scope.update({children[0].children[0]: arr})
                return
            else:
                if local_scope:
                    if children[0] in self.local_scope[-1].keys():
                        self.local_scope[-1].update({children[0]: self.execVal(children[-1], True)})
                    elif children[0] not in self.local_scope[-1].keys():
                        i = 0
                        for _s in reversed(self.local_scope):
                            i = i - 1
                            if children[0] in _s.keys():
                                self.local_scope[i].update({children[0]: self.execVal(children[-1], True)})
                                continue
                        self.scope.update({children[0]: self.execVal(children[-1])})
                else:
                    self.scope.update({children[0]: self.execVal(children[-1])})
                return

        if tree_type == "for":
            self.execLoop(tree)
            return

        if tree_type == "do_while":
            self.execWhile(tree, True)
            return

        if tree_type == "while":
            self.execWhile(tree)
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
