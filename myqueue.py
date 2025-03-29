from stack import Stack

class Queue:
    
    def __init__(self):
        self.stack_in = Stack()
        self.stack_out = Stack()

    def enqueue(self, item):
        self.stack_in.push(item)

    def dequeue(self):
        if self.stack_out.is_empty():
            while not self.stack_in.is_empty():
                self.stack_out.push(self.stack_in.pop())
        return self.stack_out.pop()

    def first(self):
        if self.stack_out.is_empty():
            while not self.stack_in.is_empty():
                self.stack_out.push(self.stack_in.pop())
        return self.stack_out.peek()

    def is_empty(self):
        return self.stack_in.is_empty() and self.stack_out.is_empty()

    def size(self):
        return self.stack_in.size() + self.stack_out.size()

    def get_items(self):
        items = []
        while not self.stack_in.is_empty():
            self.stack_out.push(self.stack_in.pop())

        while not self.stack_out.is_empty():
            items.append(self.stack_out.peek())  
            self.stack_in.push(self.stack_out.pop())  

        return items


    def __str__(self):
        return ' <- '.join(map(str, self.get_items()))
