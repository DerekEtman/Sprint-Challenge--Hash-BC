#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    # PRoblem: find two items that add up to the limit weight.
    # print(f"{len(weights)}")
    # 
    for i in range(length):
        pairs = hash_table_retrieve(ht, weights[i])
        # print(f"pairs: {pairs}")

        if pairs is None:
            hash_table_insert(ht, limit - weights[i], i)
        else:
            return (i, pairs)

    return None

    # if (length <= 1):
    #     return None
    


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
