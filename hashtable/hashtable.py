class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity=MIN_CAPACITY):
        # Your code here
        self.capacity = capacity if capacity >= MIN_CAPACITY else MIN_CAPACITY
        self.table = [None] * (self.capacity)
        self.count = 0
        self.resizing = False


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """

        return len(self.table)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """

        load_factor = self.count/self.capacity

        if not self.resizing:
            if load_factor > 0.7:
                self.resize(int(self.capacity * 2))
            elif load_factor < 0.2 and self.capacity != MIN_CAPACITY:
                self.resize(int(self.capacity / 2))
        
        return load_factor


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        pass


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """

        h = 5381
        for x in key:
            h = (h * 33) + ord(x)
        return h


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """

        i = self.hash_index(key)

        if self.table[i] == None:
            self.table[i] == HashTableEntry(key, value)
        else: 
            current_node = self.table[i]

            if current_node.key == key:
                current_node.value = value
            else: 
                while current_node.next != None:
                    if current_node.next.key == key:
                        current_node.next.value = value
                        return
                    current_node = current_node.next
                current_node.next = HashTableEntry(key, value)

        self.count += 1
        self.get_load_factor()

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """

        i = self.hash_index(key)

        if self.table[i] != None:
            current_node = self.table[i]
            if current_node.key == key:
                self.table[i] = current_node.next
                self.count -= 1
                self.get_load_factor()
                return
            while current_node.next != None:
                if current_node.next.key == key:
                    current_node.next = current_node.next.next
                    self.count -= 1
                    self.get_load_factor()
                    return
            print('Error: Key not found')
        else:
            print('Error: Key not found')


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """

        i = self.hash_index(key)

        if self.table[i] == None:
            return self.table[i]

        if self.table[i].key != key:
            current_node = self.table[i]
            while current_node != None:
                if current_node.key == key:
                    return current_node.value
                else:
                    current_node = current_node.next
            return current_node
        else:
            return self.table[i].value


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """

        new_table = HashTable(new_capacity)

        new_table.resizing = True

        for n in self.table:
            if n != None and n.next == None:
                new_table.put(n.key, n.value)
            else:
                current_node = n
                while current_node != None:
                    new_table.put(current_node.key, current_node.value)
                    current_node = current_node.next

        self.capacity = new_table.capacity
        self.table = new_table.table
        self.count = new_table.count

if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
