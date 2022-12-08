import hashlib
import datetime

class Block:
    def __init__(self, data, previous_hash):
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        
        sha = hashlib.sha256()
        hash_str = "We are going to encode this string of data!".encode('utf-8')
        sha.update(hash_str)
        self.hash = sha.hexdigest()

        self.next = None

    def __str__(self):
        return "Timestamp: {}\nData: {}\nSHA256 Hash: {}\nPrevious Hash: {}".format(self.timestamp, self.data, self.hash, self.previous_hash)

class BlockChain:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        if index >= self.size or index < 0:
            raise IndexError("BlockChain index out of range")
        curr = self.head
        for i in range(index):
            curr = curr.next
        return curr

    def __iter__(self):
        self.curr = self.head
        return self

    def __next__(self):
        if self.curr is None:
            raise StopIteration()
        curr = self.curr
        self.curr = self.curr.next
        return curr

    def append(self, data):
        if data is None:
            return
        if not self.head:
            self.head = Block(data, 0)
            self.tail = self.head
        else:
            self.tail.next = Block(data, self.tail.hash)
            self.tail = self.tail.next
        self.size += 1

    def contains(self, data):
        if data is None:
            return False
        curr = self.head
        while curr:
            if curr.data == data:
                return True
            curr = curr.next
        return False

    def get(self, data):
        if data is None:
            return None
        curr = self.head
        while curr:
            if curr.data == data:
                return curr
            curr = curr.next
        return None

    def print_chain(self):
        curr = self.head
        while curr:
            print(curr)
            curr = curr.next

def main():
    block_chain = BlockChain()
    block_chain.append("Some Information")
    block_chain.append("Another piece of information")
    block_chain.print_chain()
    print("Size:", len(block_chain))
    print("Contains 'Some Information':", block_chain.contains("Some Information"))
    print("Contains 'None':", block_chain.contains("None"))
    print("Timestamp of second block:", block_chain[1].timestamp)
    print("Iterate over blocks:")
    for block in block_chain:
        print(block)

if __name__ == '__main__':
    main()
