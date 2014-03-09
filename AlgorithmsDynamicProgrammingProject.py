class Cell:
    def __init__(self):
        pass

    val = 0
    parent = 0


def do_most_work_recursive(job_array, current_week, work_on_last_week):
    low_value = int(job_array[0][current_week])
    high_value = int(job_array[1][current_week])

    if current_week == -1:
        return 0
    else:
        max_previous_no_work = do_most_work_recursive(job_array, current_week - 1, False)
        max_previous_work = do_most_work_recursive(job_array, current_week - 1, True)
        if work_on_last_week:
            return max(max_previous_work + low_value, max_previous_no_work + high_value)
        else:
            return max_previous_work


def print_tables(value_table):
    for i in range(len(value_table)):
        print ''
        for j in range(len(value_table[i])):
            print str(value_table[i][j].val) + ' ',
    print ''
    for i in range(len(value_table)):
        print ''
        for j in range(len(value_table[i])):
            print str(value_table[i][j].parent) + ' ',
    print ' \n'


# noinspection PyPep8Naming
def do_most_work(job_array, number_of_weeks, output_file):
    LOW = 0
    HIGH = 1
    NOTHING = 2
    value_table = []

    for i_iterator in range(number_of_weeks+1):
        value_table.append([])
        for j_iterator in range(3):
            value_table[i_iterator].append(Cell())

    if number_of_weeks == 0:
        return 0

    for y in range(LOW, NOTHING+1):
        value_table[0][y].val = 0
        value_table[0][y].parent = NOTHING
        value_table[1][y].parent = NOTHING

    for y in range(1, number_of_weeks+1):
        value_table[y][HIGH].parent = NOTHING

    for x in range(1, number_of_weeks+1):
        l_val = int(job_array[LOW][x])
        h_val = int(job_array[HIGH][x])
        prev_l = value_table[x - 1][LOW].val
        prev_h = value_table[x - 1][HIGH].val
        prev_n = value_table[x - 1][NOTHING].val

        value_table[x][HIGH].val = prev_n + h_val

        if prev_h > prev_l:
            value_table[x][LOW].val = prev_h + l_val
            value_table[x][LOW].parent = HIGH

            value_table[x][NOTHING].val = prev_h
            value_table[x][NOTHING].parent = HIGH

        else:
            value_table[x][LOW].val = prev_l + l_val
            value_table[x][LOW].parent = LOW
            value_table[x][NOTHING].val = prev_l
            value_table[x][NOTHING].parent = LOW

    low_final = value_table[number_of_weeks][LOW].val
    high_final = value_table[number_of_weeks][HIGH].val

    #Debug info, allows us to see the traceback and parent tables
    #print_tables(value_table)

    if high_final > low_final:
        output_file.write(str(high_final) + '\n')
        output_file.write(reconstruct_path(value_table, HIGH, number_of_weeks) + '\n')
    else:
        output_file.write(str(low_final) + '\n')
        output_file.write(reconstruct_path(value_table, LOW, number_of_weeks) + '\n')


# noinspection PyPep8Naming
def reconstruct_path(value_table, step, week):
    LOW = 0
    HIGH = 1
    NOTHING = 2

    return_string = ""

    if step == LOW:
        if week != 1:
            return_string += reconstruct_path(value_table, value_table[week][LOW].parent, week - 1)
        return_string += 'L' + ' '
    elif step == HIGH:
        if week != 1:
            return_string += reconstruct_path(value_table, value_table[week][HIGH].parent, week - 1)
        return_string += 'H' + ' '
    elif step == NOTHING:
        if week != 1:
            return_string += reconstruct_path(value_table, value_table[week][NOTHING].parent, week - 1)
        return_string += 'N' + ' '
    return return_string


def process_case(input_file, output_file):
    number_of_weeks = int(input_file.readline())
    job_list = [[0], [0]]

    low_value_list = input_file.readline().split()
    high_value_list = input_file.readline().split()

    [job_list[0].append(int(value)) for value in low_value_list]
    [job_list[1].append(int(value)) for value in high_value_list]

    input_file.readline()

    do_most_work(job_list, number_of_weeks, output_file)
    output_file.write('\n')


def dynamic_programming():
    #Open the files
    input_file = open("input.txt", 'r')
    output_file = open("Hendrickson.txt", 'wb')

    #Read the number of expected datasets and place the file header in the correct place
    number_of_cases = int(input_file.readline())
    input_file.readline()

    #For each case, process it seperately
    [process_case(input_file, output_file) for x in range(number_of_cases)]

    #Close the files
    input_file.close()
    output_file.close()

if __name__ == '__main__':
    dynamic_programming()