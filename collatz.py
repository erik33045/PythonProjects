import matplotlib.pyplot as plt


def main():
    number = int(input('Enter Number: '))
    number_list = []
    while number != 1:
        print(int(number))
        number_list.append(int(number))
        if number % 2 == 0:
            number = number / 2
        else:
            number = (number * 3) + 1

    number_list.append(1)
    print('1')

    plt.plot(number_list)
    # plt.yscale("log")
    plt.ylabel("value")
    plt.xlabel("iteration")

    i = 0
    for num in number_list:
        plt.annotate(num,
                     xy=(i, num), xycoords='data',
                     xytext=(0, +30), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->"))
        i += 1
    plt.show()


if __name__ == "__main__":
    main()
