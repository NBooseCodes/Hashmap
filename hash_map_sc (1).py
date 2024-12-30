# Name: Nicole Boose
# OSU Email: boosen@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Portfolio Project (Hash Maps)
# Due Date: 08-15-2023
# Description: This specific file defines a HashMap class that deals with collisions via chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Either overwrites the value at a given node in the bucket with the associated key or adds that
        value to a bucket that is empty
        """

        # First check if table load bigger than 1, if so resize
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)
        # Hash key, get index and specific bucket
        hashed_key = self._hash_function(key)
        index = hashed_key % self._capacity
        bucket = self._buckets.get_at_index(index)
        # Get node associated with the key
        node = bucket.contains(key)
        # If the node exists, overwrite value, else insert and inc size of hashmap
        if node is not None:
            node.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the array self._buckets
        """

        # Initialize a counter
        num_empty_buckets = 0
        # If the bucket length is 0, then it's obviously empty
        for each in range(self._capacity):
            if self._buckets.get_at_index(each).length() == 0:
                # Increment our count
                num_empty_buckets += 1
        # Return the count
        return num_empty_buckets

    def table_load(self) -> float:
        """
        Gets load factor of the table
        """

        # load factor is num elements / num buckets (capacity)
        size = self._size
        cap = self._capacity
        return size / cap

    def clear(self) -> None:
        """
        Clears out the hashmap contents
        """

        # Create a new arr to hold our empty buckets
        clean_buckets = DynamicArray()
        # Append 1 empty linked list object to each bucket in our new arr
        for each in range(self._capacity):
            clean_buckets.append(LinkedList())
        # Set the _buckets member var to clean_buckets arr
        self._buckets = clean_buckets
        # Remember to re-set size to 0 since it's now empty
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes a hash table to give it a new capacity (usually more room but I suppose it could be
        less if you remove a bunch of elements and want to free up some mem space)
        """
        # Check if capacity is valid and if it's prime. If not prime, make it so
        if new_capacity < 1:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Set up a temp storage of our old buckets
        temp = self._buckets  # Dynamic arr of LL's

        # Set capacity to new capacity, size to 0, and self._buckets to new array
        # Also clear out the buckets array
        self._capacity = new_capacity
        self._size = 0
        self._buckets = DynamicArray()
        for each in range(self._capacity):
            self._buckets.append(LinkedList())

        # For each bucket in our temp bucket array
        for i in range(temp.length()):
            bucket = temp.get_at_index(i)
            # Get key and val for each node and put back into the cleared out class bucket array
            for node in bucket:
                key = node.key
                val = node.value
                self.put(key, val)

    def get(self, key: str):
        """
        Gets value at associated key. If no value exists, then we just return None
        """
        # O(1) time complexity

        # Calculate hash value for the key you want
        hashed_key = self._hash_function(key)
        # Find the associated index
        index = hashed_key % self._capacity
        # Locate the bucket associated with that index
        bucket = self._buckets.get_at_index(index)
        # Locate the node you want to access
        node = bucket.contains(key)
        # If that node has a value associated, return the value. If not, return None
        if node is not None:
            return node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if a key is in the hash map
        """
        # O(1)

        if self._size == 0:
            return False
        hashed_key = self._hash_function(key)
        index = hashed_key % self._capacity
        bucket = self._buckets.get_at_index(index)

        if bucket.contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key and its values from a hash table
        """
        # O(1)
        hashed_key = self._hash_function(key)
        index = hashed_key % self._capacity
        bucket = self._buckets.get_at_index(index)
        node = bucket.contains(key)
        if node is not None:
            bucket.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Gets all of the keys and values in a hash table and stores them in an array as a series
        of tuples such that one tuple is of the form (key, value) for each node.
        """
        # O(n)? Or amortized O(n) since some buckets are empty?
        key_val_arr = DynamicArray()
        for each in range(self._capacity):
            bucket = self._buckets.get_at_index(each)
            for node in bucket:
                key = node.key
                val = node.value
                key_val_tuple = (key, val)
                key_val_arr.append(key_val_tuple)

        return key_val_arr


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds mode(s) of a dynamic array using a hash map. Handles ties by appending numerous modes to a new DA.
    Mode array and frequency is returned as a tuple
    """

    # O(n) as far as I can tell

    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    max_element_arr = DynamicArray()
    freq = 1
    max_freq = 1

    for i in range(da.length()):
        key = da[i]
        # If key not in map, reset freq to 1 and put key-val (key-freq) pair in map
        if not map.contains_key(key):
            freq = 1
            map.put(key, freq)
        # Otherwise the key is in the map, so update frequency associated with that key and update map too
        else:
            freq = map.get(key) + 1
            map.put(key, freq)

        # If our current freq = max frequency, append to max_element_arr
        if freq == max_freq:
            max_element_arr.append(key)
        # But if our current frequency is bigger than our max, then clear out the old DA and append key
        # Also reset new max to current freq
        if freq > max_freq:
            max_element_arr = DynamicArray()
            max_element_arr.append(key)
            max_freq = freq
    # Now return
    return max_element_arr, max_freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
