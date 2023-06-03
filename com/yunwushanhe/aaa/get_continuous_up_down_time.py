def get_continuous_up_down_time(sequence, dt):
    # sequence = [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1] # input sequence

    max_ones_length = 0
    current_ones_length = 0
    for i in range(len(sequence)):
        if sequence[i] == 1:
            current_ones_length += 1
        else:
            if current_ones_length > max_ones_length:
                max_ones_length = current_ones_length
            current_ones_length = 0
    if current_ones_length > max_ones_length:
        max_ones_length = current_ones_length

    max_zeros_length = 0
    current_zeros_length = 0
    for i in range(len(sequence)):
        if sequence[i] == 0:
            current_zeros_length += 1
        else:
            if current_zeros_length > max_zeros_length:
                max_zeros_length = current_zeros_length
            current_zeros_length = 0
    if current_zeros_length > max_zeros_length:
        max_zeros_length = current_zeros_length


    up_time = max_ones_length * dt / 60
    down_time = max_zeros_length * dt / 60

    return up_time, down_time