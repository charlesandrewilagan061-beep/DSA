class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinaryTree:
    """Binary search tree: smaller keys go left, larger keys go right."""

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key):
        if self.search(self.root, key) is not None:
            raise ValueError(f'{key} is already in the tree.')
        node = Node(key)
        if self.root is None:
            self.root = node
        else:
            current = self.root
            while True:
                if key < current.key:
                    if current.left is None:
                        current.left = node
                        break
                    current = current.left
                else:
                    if current.right is None:
                        current.right = node
                        break
                    current = current.right
        self.size += 1

    def search(self, root, key):
        """Return the node holding key, or None when it is not in the tree."""
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def search_path(self, key):
        """Keys visited while looking for key (used to highlight the path)."""
        path = []
        current = self.root
        while current is not None:
            path.append(current.key)
            if current.key == key:
                break
            current = current.left if key < current.key else current.right
        return path

    def post_traversal(self, start, traversal):
        """Left, Right, Root. traversal is a string that grows as nodes are visited."""
        if start:
            traversal = self.post_traversal(start.left, traversal)
            traversal = self.post_traversal(start.right, traversal)
            traversal += str(start.key) + '-'
        return traversal

    def delete_node(self, root, key):
        """Delete key from the tree under root and return the new root of that part."""
        if root is None:
            return root
        if key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            # one child or no child
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            # two children: copy the in-order successor, then delete it
            successor = root.right
            while successor.left is not None:
                successor = successor.left
            root.key = successor.key
            root.right = self.delete_node(root.right, successor.key)
        return root

    def delete(self, key):
        if self.search(self.root, key) is None:
            raise ValueError(f'{key} was not found in the tree.')
        self.root = self.delete_node(self.root, key)
        self.size -= 1

    def __len__(self):
        return self.size

    def clear(self):
        self.root = None
        self.size = 0

    def layout(self):
        """Give every node an (x, y) slot for drawing. Returns (nodes, edges, depth)."""
        nodes = []
        edges = []
        counter = [0]

        def walk(node, depth):
            if node is None:
                return None
            left = walk(node.left, depth + 1)
            x = counter[0]
            counter[0] += 1
            item = {'key': node.key, 'x': x, 'depth': depth}
            nodes.append(item)
            right = walk(node.right, depth + 1)
            if left:
                edges.append((item, left))
            if right:
                edges.append((item, right))
            return item

        walk(self.root, 0)
        depth = max((n['depth'] for n in nodes), default=0)
        return nodes, edges, depth