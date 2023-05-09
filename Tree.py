class Node:
    id = 0

    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.children = []

        if self.parent == None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1

        self.id = Node.id
        Node.id += 1

    def get_data(self):
        return self.data
    
    def set_data(self, new_data):
        self.data = new_data
    
    def get_depth(self):
        return self.depth
    
    #set_depth method is not implimented

    def get_parent(self):
        return self.parent
    
    def set_parent(self, new_parent):
        self.parent = new_parent

    def get_children(self):
        return self.children

    def add_child(self, new_child):
        assert type(new_child) == type(self), f'invalid child arg {new_child}'
        self.children.append(new_child)

    def add_children(self, children):
        for new_child in children:
            self.add_child(new_child)

    def is_leaf(self):
        return len(self.children) == 0



class Tree:
    def __init__(self, root_data):
        self.root = Node(root_data, None)

    def get_root(self):
        return self.root


    def find_by_id(self, id):
        def traverse(node):
            if node.id == id:
                return node
            elif node.is_leaf():
                return -1
            else:
                outs = [traverse(child) for child in node.get_children()]
                for item in outs:
                    if item == abs(item):
                        return item
                return -1

        return traverse(self.root)
    
    
    def add(self, data, parent_id):
        parent = self.find_by_id(parent_id)
        assert parent_id != -1, f'parent with id {parent_id} not found'
        parent.add_child(Node(data, parent))


    def get_nodes_of_depth(self, depth):
        out = []

        def traverse(node):
            if node.depth == depth:
                out.append(node)
                return
            elif node.depth > depth:
                return
            else:
                for child in node.get_children():
                    traverse(child)

        traverse(self.root)

        return out

    


    
        