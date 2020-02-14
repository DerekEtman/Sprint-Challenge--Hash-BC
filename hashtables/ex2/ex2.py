#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    # Grabbing each element from ticket and putting them into the table with source and dest
    for i in tickets:
        print(f"source: {i.source}, dest: {i.destination}")
        # Inserting source and dest into the hashtable
        hash_table_insert(hashtable, i.source, i.destination)

    route[0] = hash_table_retrieve(hashtable, "NONE")
    for j in range(1,length):
        route[j] = hash_table_retrieve(hashtable, route[j-1])
        print(f"printing route: {route[j]}")

    for x in route:
        if x is "NONE":
            route.remove(x)


    
    print(f"current route: {route}")
    return route
