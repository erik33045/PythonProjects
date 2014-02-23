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

    def print_final_output(self):
        #position, name, points, games played, scored goals, suffered goals, goal difference, % of earned points
        return str(self.position) + ". " + self.name + " " + str(self.points) + " " + str(self.games_played) + " " + \
               str(self.scored_goals) + " " + \
               str(self.suffered_goals) + " " + str(self.goal_difference()) + " " + \
               str(self.calculate_percentage_of_earned_points())

    def goal_difference(self):
        return self.scored_goals - self.suffered_goals

    def calculate_percentage_of_earned_points(self):
        percentage = 0
        if self.games_played != 0:
            percentage = float(self.points) / float(self.games_played * 3)
        else:
            percentage = 1
        answer = percentage * 100
        return "%.2f" % answer

    name = ""
    games_played = 0
    scored_goals = 0
    suffered_goals = 0
    order_added = 1
    position = 0
    points = 0


def process_game(game, team_list):
    first_team = [team for team in team_list if team.name == game[0]][0]
    first_team.process_game(int(game[1]), int(game[3]))
    second_team = [team for team in team_list if team.name == game[4]][0]
    second_team.process_game(int(game[3]), int(game[1]))


def add_team_to_list(team_name, team_list, order):
    team_list.append(TeamStats(team_name, order))


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


def team_sort_comparison(x, y):
    points = y.points - x.points
    if points == 0:
        goal_difference = y.goal_difference() - x.goal_difference()
        if goal_difference == 0:
            scored_goals = y.scored_goals - x.scored_goals
            if scored_goals == 0:
                return x.order_added - y.order_added
            else:
                return scored_goals
        else:
            return goal_difference
    else:
        return points


def process_dataset(input_file, output_file, is_first_dataset):
    #Get number of teams and games
    teams_and_games = input_file.readline().split()
    number_of_teams, number_of_games = int(teams_and_games[0]), int(teams_and_games[1])

    #Add Teams
    team_list = []
    [team_list.append(TeamStats(input_file.readline().strip(), x+1)) for x in range(number_of_teams)]

    #Process Game Stats
    [process_game(input_file.readline().split(), team_list) for x in range(number_of_games)]

    #sort the list based on the comparison function
    team_list.sort(cmp=team_sort_comparison)

    #Now that the list has been sorted, fill in the final positions
    determine_position_of_teams(team_list)

    #This is so we don't write a null as the first line in the output file
    if not is_first_dataset:
        output_file.write('\n')

    #Write the amount of proceeding teams
    output_file.write(str(len(team_list)) + '\n')

    #Write each team to the output file
    [output_file.write(str(team.print_final_output()) + '\n') for team in team_list]

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

    #Close the files
    input_file.close()
    output_file.close()

if __name__ == '__main__':
    algorithm_sorting_project()