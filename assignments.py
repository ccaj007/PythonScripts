
class MaxSizeList():

    def __init__(self,size):
        self.size = size
        self.list = []

    def push(self, value):
        self.list.append(value)
        if self.size < len(self.list):
            self.list.pop(0)

    def get_list(self):
        return self.list

    def __str__(self):
        return ' '.join(self.list)

