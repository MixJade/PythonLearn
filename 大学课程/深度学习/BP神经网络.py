from math import exp


def initialize_network():
    """
    初始化权值矩阵

    :return: 自定义的权值矩阵(最后一个参数为偏导)
    """
    network = list()
    hidden_layer = [{'weights': [-1, 1, 0]}, {'weights': [1, 1, 0]}]
    network.append(hidden_layer)
    output_layer = [{'weights': [1, 1, 0]}, {'weights': [-1, 1, 0]}]
    network.append(output_layer)
    return network


def activate(weights, inputs):
    """
    计算神经元的激活值（加权合）

    :param weights: 权值矩阵
    :param inputs: 输入值
    :return: 经权值矩阵输入到神经元的值
    """
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation


def transfer(activation):
    """
    激活函数

    :param activation: 经权值矩阵到神经元的输入
    :return: 保留两位小数的结果
    """
    transfer_result = 1.0 / (1.0 + exp(-activation))
    transfer_result = float('%.2f' % transfer_result)  # 贴合书上保留两位小数
    return transfer_result


def forward_propagate(network, row):
    """
    计算神经网络的正向传播

    :param network: 神经网络
    :param row: 输入值
    :return: 最终输出值
    """
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            activation = float('%.2f' % activation)  # 贴合书上保留两位小数
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
            print(neuron)
        inputs = new_inputs
    return inputs


def transfer_derivative(output):
    """
    对激活函数进行求导

    :param output: 当前神经元的输出
    :return: 激活函数的导数
    """
    return output * (1.0 - output)


def backward_propagate_error(network, expected):
    """
    反向传播误差信息，并存储在神经元中

    :param network: 神经网络
    :param expected: 期待值(单列矩阵)
    """
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network) - 1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['duty'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            duty_result = errors[j] * transfer_derivative(neuron['output'])
            duty_result = float('%.4f' % duty_result)  # 贴合书上保留四位小数
            neuron['duty'] = duty_result


def update_weights(network, row, l_rate):
    """
    根据误差，更新网络权重

    :param network: 神经网络
    :param row: 输入值
    :param l_rate: 学习速率
    """
    for i in range(len(network)):
        inputs = row
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * neuron['duty'] * inputs[j]
            neuron['weights'][-1] += l_rate * neuron['duty']


if __name__ == '__main__':
    # 初始化权值矩阵
    print("初始化权值矩阵")
    network01 = initialize_network()
    for layer01 in network01:
        print(layer01)

    # 前馈计算
    print("\n前馈计算")
    row01 = [1, -1]
    output01 = forward_propagate(network01, row01)
    for i002 in range(len(output01)):
        output01[i002] = format(output01[i002], '.2f')  # 贴合书上保留四位小数
    print("最终输出:\n", output01)

    # 反向传播
    print("\n反向传播")
    expected01 = [1, 0]  # 期待值
    backward_propagate_error(network01, expected01)
    for layer01 in network01:
        print(layer01)

    # 更新权重
    update_weights(network01, row01, 0.1)

    print("\n最终权值矩阵为:")
    for layorNum in range(len(network01)):
        for neuron01 in network01[layorNum]:
            print(neuron01['weights'][:-1])
