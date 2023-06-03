import numpy as np

def get_period(sequence):
    """
    逐渐周期化的01序列数据
    """
    # 从后往前计算3次跳变的长度
    num_jumps = 3
    jump_lengths = np.zeros(num_jumps)
    isone = np.zeros(num_jumps)
    current_jump = 0

    for i in range(len(sequence)-2, -1, -1):
        if sequence[i] != sequence[i+1]:
            if sequence[i] == 1:
                isone[current_jump] = 1
            jump_lengths[current_jump] = i
            current_jump += 1

            if current_jump >= num_jumps:
                break

    # 计算周期长度
    length1 = jump_lengths[0] - jump_lengths[1]
    length2 = jump_lengths[1] - jump_lengths[2]
    period = length1 + length2
    # 计算占空比
    if isone[0] == 0:
        duty_ratio = length2 / period
    else:
        duty_ratio = length1 / period

    return period, duty_ratio