
# Name: Nicole Boose
# OSU Email: boosen@gmail.com
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08-15-2023
# Description: This is a file that contains a hash map class defined using open addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Inserts into a hash table
        """
        # Check table load
        # I was declaring capacity in the wrong place! It should be after we check if a resize is needed
        table_load = self.table_load()
        if table_load >= 0.5:
            self.resize_table(2 * self._capacity)

        # Capture capacity and calculate initial index
        capacity = self._capacity
        initial_index = self._hash_function(key) % capacity
        # Also initialize quad index for probing and iterator
        quad_index = initial_index
        j = 1
        # While not empty
        while self._buckets.get_at_index(quad_index) is not None:
            # If the keys match
            if self._buckets.get_at_index(quad_index).key == key:
                # Check if we've hit a tombstone. If we have, alter tombstone value and size
                if self._buckets.get_at_index(quad_index).is_tombstone:
                    self._buckets.set_at_index(quad_index, HashEntry(key, value))
                    self._buckets.get_at_index(quad_index).is_tombstone = False
                    self._size += 1
                    # Once that's done we can end this function
                    return
                # If keys match and not a tombstone, just change the index value but not the size
                if not self._buckets.get_at_index(quad_index).is_tombstone:
                    self._buckets.set_at_index(quad_index, HashEntry(key, value))
                    return
            # If we don't get a key match, just continue with probe
            quad_index = (initial_index + j ** 2) % capacity
            j += 1
        # What if we hit a none spot? Then the key is not in the map and we just insert it
        self._buckets.set_at_index(quad_index, HashEntry(key, value))
        self._size += 1

    def table_load(self) -> float:
        """
        Gets the table's load factor
        """
        # This is same as other file and exploration
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Counts number of empty buckets and returns that to the user. Does not count
        tombstones as empty
        """
        # Since we aren't working with LL's, we can take advantage of the fact that capacity - size = available slots
        num_empty = self._capacity - self._size
        return num_empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table to the value of new_capacity.
        """
        # If our new capacity is less than the num of elements we have, then that cannot work and we return
        if new_capacity < self._size:
            return
        # If new capacity isn't prime, amend that
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Set up a temp hash map to hold our old values
        temp = HashMap(capacity=new_capacity, function=self._hash_function)

        # Iterate through our Class map and put each key-value pair into our temp table
        for each in self:
            temp.put(each.key, each.value)
        # Now clear out buckets (I guess you can also use self.clear() but if I can make code self-contained I will)
        for slot in range(new_capacity):
            self._buckets.append(None)
        # Set size of class map down to 0 since it's empty now
        self._size = 0
        # Set all class map characteristics equal to temp map characteristics
        self._buckets = temp._buckets
        self._size = temp._size
        self._capacity = temp._capacity

    def get(self, key: str) -> object:
        """
        Gets value associated with a key
        """
        # Get original indices and iterator
        initial_index = self._hash_function(key) % self._capacity
        j = 1
        quad_index = initial_index
        # While we haven't run out of data
        while self._buckets.get_at_index(quad_index) is not None:
            # If our index data isn't a tombstone and the keys match, return associated value
            if not self._buckets.get_at_index(quad_index).is_tombstone and \
                    self._buckets.get_at_index(quad_index).key == key:

                return self._buckets.get_at_index(quad_index).value
            # Otherwise keep iterating
            quad_index = (initial_index + j**2) % self._capacity
            j += 1
        # If we hit a 'none' value, the key isn't in our array and we return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if a key is in a hash table
        """
        # Take advantage of the existence of the get function since it's already done the work for us
        if self.get(key) is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """
        Removes a key-value pair from the hash table
        """
        # Initialize index and iterator
        index = self._hash_function(key) % self._capacity
        j = 1
        quad_index = index
        # While we iterate through and find indices that aren't empty
        while self._buckets.get_at_index(quad_index) is not None:
            # If we hit one where the keys are equal and it's not a tombstone (want to skip those)
            if self._buckets.get_at_index(quad_index).key == key and\
                    not self._buckets.get_at_index(quad_index).is_tombstone:
                self._buckets.get_at_index(quad_index).is_tombstone = True
                self._size -= 1
            # Else, continue
            quad_index = (index + j**2) % self._capacity
            j += 1
        # If we hit a none, then we conclude that the hash table does not contain that key, and we return None
        return None

    def clear(self) -> None:
        """
        Clears the hash table
        """
        old_capacity = self._capacity
        self._buckets = DynamicArray()
        # Must maintain capacity
        for each in range(old_capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns an array of tuples that are comprised of keys and values
        """
        # Init new array
        key_val_arr = DynamicArray()
        # Iterate through hash map
        for entry in self:
            # If our entry is not none and it's not a tombstone, add to our array
            if entry is not None and not entry.is_tombstone:
                key_val_tuple = (entry.key, entry.value)
                key_val_arr.append(key_val_tuple)
        return key_val_arr


    def __iter__(self):
        """
        Iterator element for the Dynamic array that holds the hash table/data
        """
        self.index = 0
        # I am a dummy and was returning self.index not just 'self' :/
        return self

    def __next__(self):
        """
        Traverses the Dynamic Array that holds the hash table using the iterator
        """
        try:
            # Init value to None
            value = None
            # Skip over the non-used buckets
            while value is None or value.is_tombstone:
                value = self._buckets.get_at_index(self.index)
                self.index += 1
        # If we hit a used bucket, stop the iteration and return the value
        except DynamicArrayException:
            raise StopIteration
        return value


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)