
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0


    def insert_at_head(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
        self.size += 1

    def insert_at_tail(self, data):
        node = Node(data)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self.size += 1

    def insert_at_index(self, index, data):
        if index < 0 or index > self.size:
            raise ValueError(f"Index {index} is out of range (valid: 0 to {self.size}).")
        if index == 0:
            self.insert_at_head(data)
            return
        node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        node.next = current.next
        current.next = node
        self.size += 1

    
    def delete_head(self):
        if self.head is None:
            raise ValueError("The list is empty.")
        removed = self.head.data
        self.head = self.head.next
        self.size -= 1
        return removed

    def delete_tail(self):
        if self.head is None:
            raise ValueError("The list is empty.")
        if self.head.next is None:
            return self.delete_head()
        current = self.head
        while current.next.next:
            current = current.next
        removed = current.next.data
        current.next = None
        self.size -= 1
        return removed

    def delete_value(self, data):
        
        if self.head is None:
            raise ValueError("The list is empty.")
        if self.head.data == data:
            self.delete_head()
            return
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return
            current = current.next
        raise ValueError(f'Value "{data}" was not found in the list.')

    def delete_at_index(self, index):
        if index < 0 or index >= self.size:
            raise ValueError(
                f"Index {index} is out of range"
                + (f" (valid: 0 to {self.size - 1})." if self.size else " (the list is empty).")
            )
        if index == 0:
            return self.delete_head()
        current = self.head
        for _ in range(index - 1):
            current = current.next
        removed = current.next.data
        current.next = current.next.next
        self.size -= 1
        return removed

   
    def search(self, data):
        
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def reverse(self):
        previous = None
        current = self.head
        while current:
            current.next, previous, current = previous, current, current.next
        self.head = previous

    def clear(self):
        self.head = None
        self.size = 0

    def to_list(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items

    def __len__(self):
        return self.size
