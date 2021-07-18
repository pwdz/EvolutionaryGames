import matplotlib.pyplot as plt

print("Filename:")
filename = input()
f = open("fitness/" + filename, "r")
lines = f.readlines()

generation_index = 0
x = []
y1 = []
y2 = []
y3 = []
for line in lines:
    generation_index += 1
    x.append(generation_index)
    numbers = line.split(" ")
    del numbers[-1]

    avg = 0
    max_num = int(numbers[0])
    min_num = int(numbers[0])
    for num in numbers:
        n = int(num)
        avg += n
        if n > max_num:
            max_num = n
        if n < min_num:
            min_num = n
    avg /= len(numbers)

    y1.append(avg)
    y2.append(min_num)
    y3.append(max_num)

    plt.scatter(generation_index, avg, color='blue')
    plt.scatter(generation_index, max_num, color='red')
    plt.scatter(generation_index, min_num, color='green')
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y3)

plt.xlabel("generation number")
plt.ylabel("fitness")
plt.title("Blue: average    Red: max    Green: min")
plt.grid()
plt.show()