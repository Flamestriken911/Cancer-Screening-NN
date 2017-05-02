""" For loading random batches of n objects from a pickle file without taking up much memory at any one time """
import os
import pickle
import random

def load_batch(filepath, batch_size):
    """ Returns a specified number of objects at random from a pickle file 
    
    No more than (batch_size + 1) objects required to be in memory at once."""
    # First we need to find how many pickled objects there are in the file
    # I don't know any more efficient way to do this than to just load and discard every object in the file
    _file = open(filepath, mode='rb')
    obj_count = 0
    while True:
        try:
            pickle.load(_file)
            obj_count += 1
        except:
            break

    _file.close()

    if batch_size > obj_count:
        raise RuntimeError(f'Batch size request, {batch_size} exceeds number of objects in file, {obj_count}')

    batch_indicies = random.choices(range(obj_count), k=batch_size)
    print(batch_indicies)

    return_list = []

    _file = open(filepath, mode='rb')
    i = 0
    while i <= max(batch_indicies):
        obj_current = pickle.load(_file)
        if i in batch_indicies:
            return_list.append(obj_current)

        i += 1

    _file.close()

    return return_list

# NOTE: Un-comment the line below to test the module
# print(load_batch('test2.p',2))