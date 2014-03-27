
# noinspection PyPep8Naming
def do_most_work(job_array, number_of_weeks, output_file):
    """do_most_work
        input:
            job_array: a 2-D array to hold the high and low earnings for each week
            number_of_weeks: number of weeks to schedule work
            output_file
        output:
            print the largest possible value of total earning for all weeks.
            print the sequence of no work, high stress work, and low stress work schedule
                that gives the optimal total earnings for all weeks

        Time complexity: O(n)
    """

    #Constants created for indexing
    LOW = 0
    HIGH = 1
    NOTHING = 2
    value_table = []    #Dynamic array that holds intermediate values for schedule sequences
    parent_table = []   #Array to hold sequence of steps to achieve optimal solution

    if number_of_weeks == 0: #no weeks to schedule: output 0
        output_file.write(str(0))
        return

    #initialize dynamic programming intermediate value table with 0's
    for i_iterator in range(number_of_weeks+1):
        value_table.append([])
        for j_iterator in range(3):
            value_table[i_iterator].append(0)

    #Fill value table in row major order by week
    for x in range(1, number_of_weeks+1):
        l_val = int(job_array[LOW][x])
        h_val = int(job_array[HIGH][x])
        prev_l = value_table[x - 1][LOW]
        prev_h = value_table[x - 1][HIGH]
        prev_n = value_table[x - 1][NOTHING]

        #For HIGH value choice column. Take previous NOTHING value and add with current week high-stress job  earnings
        value_table[x][HIGH] = prev_n + h_val

        #If we choose to do a low-stress job or no job at all, we must use the best of the previous weeks values
        if prev_h > prev_l:
            #If HIGH value was the best choice of the previous week's possible outcomes, then use HIGH as the parent
            #   and add that high value to this weeks low-stress earnings
            value_table[x][LOW] = prev_h + l_val
            #If we do nothing in this current week we also choose the best outcome of the previous week
            #Note: The NOTHING and LOW options will always use the same value from the previous week as a basis for the
            # current week
            value_table[x][NOTHING] = prev_h
            #since HIGH was used as a basis for the current week values, we add HIGH as a step on the parent array
            parent_table.append(HIGH)
        else:
            #similar reasoning as the if body except with LOW
            value_table[x][LOW] = prev_l + l_val
            value_table[x][NOTHING] = prev_l
            parent_table.append(LOW)

    #get the final low and high values to compare to choose the greatest value
    low_final = value_table[number_of_weeks][LOW]
    high_final = value_table[number_of_weeks][HIGH]

    #Debug info, allows us to see the traceback and parent tables
    #print_tables(value_table)

    #Output the optimal value and use the parent table to print the appropriate path
    if high_final > low_final:
        output_file.write(str(high_final) + '\n')
        parent_table.append(HIGH)
    else:
        output_file.write(str(low_final) + '\n')
        parent_table.append(LOW)
    output_file.write(reconstruct_path(parent_table, number_of_weeks) + '\n')


def reconstruct_path(parent_table, week):
    ''' reconstruct_path: takes the parent table and recursively prints the path for the optimal job scheduling for
        a number of weeks
            Time Complexity: O(n)
    '''
    
    LOW = 0
    HIGH = 1
    NOTHING = 2

    return_string = ""
    prev_week_nothing = False # flag used to ensure that high weeks are always preceeded by none

    # Reconstruct the path in reverse order starting with the last week
    while(week):
        step = parent_table[week]

        if prev_week_nothing: # next week will be high, so this week is none
            return_string += 'N' + ' '
            prev_week_nothing = False

        elif step == LOW:
            return_string += 'L' + ' '

        elif step == HIGH:
            return_string += 'H' + ' '
            prev_week_nothing = True # enables the flag to mark the previous week as none
        week -= 1

    return return_string[::-1].strip() # [::-1] reverses this string since we are reconstructin from the end
    

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
