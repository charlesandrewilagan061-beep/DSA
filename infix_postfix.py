
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, data):
        node = Node(data)
        node.next = self.top
        self.top = node
        self.size += 1

    def pop(self):
        if self.top is None:
            raise ValueError("The stack is empty.")
        removed = self.top.data
        self.top = self.top.next
        self.size -= 1
        return removed

    def peek(self):
        if self.top is None:
            raise ValueError("The stack is empty.")
        return self.top.data

    def is_empty(self):
        return self.top is None

    def to_list(self):
        items = []
        current = self.top
        while current:
            items.append(current.data)
            current = current.next
        items.reverse()
        return items

    def __len__(self):
        return self.size


OPERATORS = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
RIGHT_ASSOCIATIVE = {'^'}


def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch.isspace():
            i += 1
        elif ch.isalnum() or ch == '.':
            start = i
            while i < len(expression) and (expression[i].isalnum() or expression[i] == '.'):
                i += 1
            tokens.append(expression[start:i])
        elif ch in OPERATORS or ch in '()':
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(f'Invalid character "{ch}" in the expression.')
    return tokens


def infix_to_postfix(expression):
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError('Please enter an infix expression.')

    stack = Stack()
    output = []
    steps = []
    expect_operand = True

    for token in tokens:
        if token == '(':
            if not expect_operand:
                raise ValueError('Missing operator before "(".')
            stack.push(token)
            action = 'Push "(" onto the stack'
        elif token == ')':
            if expect_operand:
                raise ValueError('Missing operand before ")" (or empty parentheses).')
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            if stack.is_empty():
                raise ValueError('Mismatched parentheses: extra ")".')
            stack.pop()
            action = 'Pop operators until "(" and discard the pair'
        elif token in OPERATORS:
            if expect_operand:
                raise ValueError(f'Missing operand before "{token}".')
            while (not stack.is_empty() and stack.peek() != '('
                   and (OPERATORS[stack.peek()] > OPERATORS[token]
                        or (OPERATORS[stack.peek()] == OPERATORS[token]
                            and token not in RIGHT_ASSOCIATIVE))):
                output.append(stack.pop())
            stack.push(token)
            expect_operand = True
            action = f'Pop higher/equal precedence operators, then push "{token}"'
        else:
            if not expect_operand:
                raise ValueError(f'Missing operator before "{token}".')
            output.append(token)
            expect_operand = False
            action = 'Operand: send to output'

        steps.append({
            'token': token,
            'action': action,
            'stack': ' '.join(stack.to_list()),
            'output': ' '.join(output),
        })

    if expect_operand:
        raise ValueError('The expression ends with an operator.')

    while not stack.is_empty():
        top = stack.pop()
        if top == '(':
            raise ValueError('Mismatched parentheses: missing ")".')
        output.append(top)
        steps.append({
            'token': '—',
            'action': f'End of input: pop "{top}" to output',
            'stack': ' '.join(stack.to_list()),
            'output': ' '.join(output),
        })

    return ' '.join(output), steps
