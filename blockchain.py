# sha256 hash blockchain demo
# Data:
# Hash:


import hashlib
import datetime

class Block:
    def __init__(self, data, previous_hash):
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()
        hash_str = "We are going to encode this string of data!".encode('utf-8')
        sha.update(hash_str)
        return sha.hexdigest()

class BlockChain:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        if data == None:
            return
        if not self.head:
            self.head = Block(data, 0)
            self.tail = self.head
        else:
            self.tail.next = Block(data, self.tail.hash)
            self.tail = self.tail.next

    def search(self, data):
        if data == None:
            return False
        curr = self.head
        while curr:
            if curr.data == data:
                return True
            curr = curr.next
        return False

    def get_block(self, data):
        if data == None:
            return None
        curr = self.head
        while curr:
            if curr.data == data:
                return curr
            curr = curr.next
        return None

    def print_list(self):
        curr = self.head
        while curr:
            print("Timestamp: {}\nData: {}\nSHA256 Hash: {}\nPrevious Hash: {}\n".format(curr.timestamp, curr.data, curr.hash, curr.previous_hash))
            curr = curr.next

def main():
    block_chain = BlockChain()
    block_chain.append("Some Information")
    block_chain.append("Another piece of information")
    block_chain.print_list()
    print(block_chain.search("Some Information"))
    print(block_chain.search("None"))
    print(block_chain.get_block("Another piece of information").timestamp)

if __name__ == '__main__':
    main()
