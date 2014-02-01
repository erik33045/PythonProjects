def pythagorean_trips(x, y, z):
    a = 0
    b = 0
    c = 0

    if x != "_":
        a = int(x)
        for i in range(0, 10000):
            if (i + 1) * (i + 1) == i * i + a * a:
                b = i
                c = i + 1
                break
        print str(abs(b)) + ", " + str(abs(c))
    elif y != "_":
        b = int(y)
        for i in range(0, 10000):
            if (b + 1) * (b + 1) == (b * b + i * i):
                a = i
                c = b + 1
                break
        print str(abs(a)) + ", " + str(abs(c))
    elif z != "_":
        c = int(z)
        for i in range(0, 10000):
            if (c * c) == (i * i + (c - 1) * (c - 1)):
                b = c - 1
                a = i
                break
        print str(abs(a)) + ", " + str(abs(b))


if '__main__' == __name__:
    print pythagorean_trips("_", "12", "_")
