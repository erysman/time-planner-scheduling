def generatePairs(array):
    pairs = []

    # Iterate through each element in the input array
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            # Create a pair without repetition
            pair = (array[i], array[j])
            pairOpposite = (array[j], array[i])
            pairs.append(pair)
            pairs.append(pairOpposite)
    return pairs

def generate2dArray(array):
    num_rows = len(array)
    my_2d_array = [[0] * num_rows for _ in range(num_rows)]
    return my_2d_array

