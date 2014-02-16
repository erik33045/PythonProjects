class TeamStats:
    def __init__(self, name, order_added):
        self.name = name
        self.order_added = order_added

    def process_game(self, scored, suffered):
        self.games_played += 1
        self.scored_goals += scored
        self.suffered_goals += suffered

        if scored == suffered:
            self.points += 1
        elif scored > suffered:
            self.points += 3

    def print_final_output(self, total_earned_points):
        #position, name, points, games played, scored goals, suffered goals, goal difference, % of earned points
        return str(self.position) + ". " + self.name + " " + str(self.points) + " " + str(self.games_played) + " " + \
               str(self.scored_goals) + " " + \
               str(self.suffered_goals) + " " + str(self.goal_difference()) + " " + \
               str(self.calculate_percentage_of_earned_points(total_earned_points))

    def goal_difference(self):
        return self.scored_goals - self.suffered_goals

    def calculate_percentage_of_earned_points(self, total_points):
        return "%.2f" % (float(self.points / total_points) * 100)

    name = ""
    games_played = 0
    scored_goals = 0
    suffered_goals = 0
    order_added = 1
    position = 0
    points = 0


def process_game(game, team_dictionary):
    first_team = team_dictionary[game[0]]
    first_team.process_game(int(game[1]), int(game[3]))
    second_team = team_dictionary[game[4]]
    second_team.process_game(int(game[3]), int(game[1]))


def add_team_to_dictionary(team_name, dictionary, order):
    dictionary[team_name] = TeamStats(team_name, order)


def determine_position_of_teams(team_list):
    position = 1
    for i in range(1, len(team_list) + 1):
        team = team_list[i - 1]

        if i != 1:
            previous_team = team_list[i - 2]
            if team.points != previous_team.points \
                or team.scored_goals != previous_team.scored_goals \
                or team.goal_difference() != previous_team.goal_difference():
                position = i

        team.position = position


def process_dataset(input_file, output_file, is_first_dataset):
    #Get number of teams and games
    teams_and_games = input_file.readline().split()
    number_of_teams, number_of_games = int(teams_and_games[0]), int(teams_and_games[1])

    #Add Teams
    team_dictionary = {}
    [add_team_to_dictionary(input_file.readline().strip(), team_dictionary, x + 1) for x in range(number_of_teams)]

    #Process Game Stats
    [process_game(input_file.readline().split(), team_dictionary) for x in range(number_of_games)]

    #Turn the dictionary into a list and then sort on the function provided by the class
    team_list = [value for key, value in team_dictionary.items()]
    team_list.sort(key=lambda i: (-i.points, -i.goal_difference(), -i.scored_goals, i.order_added,))

    #Now that the list has been sorted, fill in the final positions
    determine_position_of_teams(team_list)

    #Get the total amount of points earned so the percentage can be calculated for each team
    total_earned_points = sum([team.points for team in team_list])

    #This is so we don't write a null as the first line in the output file
    if not is_first_dataset:
        output_file.write('\n')

    #Write the amount of proceeding teams
    output_file.write(str(len(team_list)) + '\n')

    #Write each team to the output file
    [output_file.write(str(team.print_final_output(total_earned_points)) + '\n') for team in team_list]

    #Move the file header in place to read the next team
    input_file.readline()


def algorithm_sorting_project():
    #Open the files
    input_file = open("input.txt", 'r')
    output_file = open("Hendrickson.txt", 'wb')

    #Read the number of expected datasets and place the file header in the correct place
    number_of_datasets = int(input_file.readline())
    input_file.readline()

    is_first_dataset = True
    for dataset in range(number_of_datasets):
        process_dataset(input_file, output_file, is_first_dataset)
        is_first_dataset = False

    #Close the file
    output_file.close()
