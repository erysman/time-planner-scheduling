from .type import TimeRange


def generatePairs(array):
    pairs = []

    # Iterate through each element in the input array
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            pair = (array[i], array[j])
            pairOpposite = (array[j], array[i])
            pairs.append(pair)
            pairs.append(pairOpposite)
    return pairs


def generate2dArray(array):
    num_rows = len(array)
    my_2d_array = [[0] * num_rows for _ in range(num_rows)]
    return my_2d_array


def areRangesOverlapping(rangeA: TimeRange, rangeB: TimeRange):
    areRangesJustOverlapping = (
        rangeA.timeRangeStart <= rangeB.timeRangeStart
        and rangeA.timeRangeEnd >= rangeB.timeRangeStart
    ) or (
        rangeA.timeRangeStart >= rangeB.timeRangeStart
        and rangeA.timeRangeStart <= rangeB.timeRangeEnd
    )
    areRangesNested = (
        rangeA.timeRangeStart >= rangeB.timeRangeStart
        and rangeA.timeRangeEnd <= rangeB.timeRangeEnd
    ) or (
        rangeB.timeRangeStart >= rangeA.timeRangeStart
        and rangeB.timeRangeEnd <= rangeA.timeRangeEnd
    )
    return areRangesJustOverlapping or areRangesNested
