""" For loading random batches of n objects from a pickle file without taking up much memory at any one time """
import os
import pickle
import random

def load_batch(filepath, batch_size):
    """ Returns a specified number of objects at random from a pickle file 
    
    No more than (batch_size + 1) objects required to be in memory at once."""
    # First we need to find how many pickled objects there are in the file
    # I don't know any more efficient way to do this than to just load and discard every object in the file
    obj_count = 0
    while True:
        try:
            pickle.load(open(filepath, mode='rb'))
            obj_count += 1
        except:
            break

    if batch_size > obj_count:
        raise RuntimeError('Batch size request exceeds number of objects in file')

    batch_indicies = random.choices(range(batch_size), k=batch_size)

    return_list = []

    i = 0
    while True:
        try:
            loaded_obj = pickle.load(open(filepath, mode='rb'))
            if i in batch_indicies:
                return_list.append(loaded_obj)

            obj_count += 1
        except:
            break

    return return_list
