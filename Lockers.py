def Clock_Game():
    inputString = raw_input("Enter 12 integers 1-6:")
    clock = int(inputString.split(" "))
    print str(clock)


if '__main__' == __name__:
    Clock_Game()
