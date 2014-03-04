def process_case(input_file, output_file):
    number_of_weeks = int(input_file.readline())
    low_stress_job_cost_list = input_file.readline().split()
    high_stress_job_cost_list = input_file.readline().split()

    input_file.readline()


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
