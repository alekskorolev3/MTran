class SemanticAnalyzer:
    def analyze(self, tree):
        try:
            tree_type = tree.type
            children = tree.children
        except AttributeError:
            return tree

        if tree_type == "init":
            print("init")

        for child in children:
            if child != "=":
                self.analyze(child)
