def generatePairs(input_array):
    pairs = []

    # Iterate through each element in the input array
    for i in range(len(input_array)):
        for j in range(i + 1, len(input_array)):
            # Create a pair without repetition
            pair = (input_array[i], input_array[j])
            pairOpposite = (input_array[j], input_array[i])
            pairs.append(pair)
            pairs.append(pairOpposite)
    return pairs

# Example usage:
# input_array = ['a', 'b', 'c']
# result = generatePairs(input_array)
# print(result)

def generate2dArray(input_array):
    num_rows = len(input_array)
    my_2d_array = [[0] * num_rows for _ in range(num_rows)]
    return my_2d_array