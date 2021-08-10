def sum_max(*numbers):
    my_sum = 0
    my_max = 0
    for i in range(0, len(numbers)):
        my_sum += numbers[i]
        if numbers[i] > numbers[my_max]:
            my_max = i
    return my_sum, numbers[my_max]
