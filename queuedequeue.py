# Source: GeeksforGeeks
# https://www.geeksforgeeks.org/python/implementation-of-queue-using-linked-list-in-python/

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        new_node = Node(data)

        if self.rear is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

        self.size += 1

    def dequeue(self):
        if self.front is None:
            return None

        removed_data = self.front.data
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        self.size -= 1
        return removed_data

    def to_list(self):
        items = []
        current = self.front

        while current is not None:
            items.append(current.data)
            current = current.next

        return items

    def is_empty(self):
        return self.front is None

    def __len__(self):
        return self.size