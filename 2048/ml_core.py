weight = 10


def get_correct_op(input):
    return 2 * input


inputs = [5, 8, 10, 0]

for i in range(10000):
    for ip in inputs:
        predictedOutput = weight * ip
        correctOutput = get_correct_op(ip)

        cost = correctOutput - predictedOutput

        weight += 0.01 * cost

print(weight)
