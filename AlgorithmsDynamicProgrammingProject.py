

def process_case(input_file, output_file):
    number_of_weeks = int(input_file.readline())
    job_list = [input_file.readline().split(), input_file.readline().split()]

    input_file.readline()

    output_file.write(str(do_most_work(job_list, number_of_weeks - 1, True)) + '\n')


def do_most_work(job_array, current_week, work_on_last_week):
    low_value = int(job_array[0][current_week])
    high_value = int(job_array[1][current_week])

    if current_week == -1:
        return 0
    else:
        max_previous_no_work = do_most_work(job_array, current_week - 1, False)
        max_previous_work = do_most_work(job_array, current_week - 1, True)
        if work_on_last_week:
            return max(max_previous_work + low_value, max_previous_no_work + high_value)
        else:
            return max_previous_work #because it will always be greater than max_previous_no_work


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
