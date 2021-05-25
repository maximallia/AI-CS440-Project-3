from random import randint
import copy
import sys

'''
    Kyle VanWageninge kjv48
    Daniel Ying dty16
    AI Project 3  Search and Destroy
'''


# place terrain types onto the board
def terrain(board1, size):
    board = board1.copy()

    for i in range(size):
        for k in range(size):
            num = randint(1, 100)
            if num <= 25:
                board[i][k] = 'f'
            elif 25 < num <= 50:
                board[i][k] = 'h'
            elif 50 < num <= 75:
                board[i][k] = 'F'
            elif 75 < num <= 100:
                board[i][k] = 'c'
    return board


# update the belief of all the cells that didn't just get searched
def belief(board, observations, agent, old_board, prev_spot, size):
    # print(board)
    # print(old_board)
    for i in range(size):
        for k in range(size):
            fail = 1
            if [i, k] != agent:
                numerator = board[i][k]
                x = (observations[len(observations) - 1] - board[i][k]) / (1 - board[i][k])
                denominator = numerator + (x * (1 - board[i][k]))
                # print(numerator, denominator)
                board[i][k] = numerator / denominator


# for agent 2s setting the probability of finding the target based on current beliefs
def prediction(board, probs, size, observations, agent):
    pred_board = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for k in range(size):
            if [i, k] != [-1, -1]:
                if board[i][k] == 'f':
                    found = probs[i][k] * .9
                    pred_board[i][k] = found
                if board[i][k] == 'h':
                    found = probs[i][k] * .7
                    pred_board[i][k] = found
                if board[i][k] == 'F':
                    found = probs[i][k] * .3
                    pred_board[i][k] = found
                if board[i][k] == 'c':
                    found = probs[i][k] * .1
                    pred_board[i][k] = found
    return pred_board


# search the current cell that the agent is at
def search(board, probs, agent, target, observations, prev_spot, size):
    success = False

    # if the agent is at the cell with the target use the false negative rate for the type of cell
    # to determine if the serach was successful
    if agent[0] == target[0] and agent[1] == target[1]:
        if board[agent[0]][agent[1]] == 'f':
            x = randint(1, 100)
            if x > 10:
                success = True
        if board[agent[0]][agent[1]] == 'h':
            x = randint(1, 100)
            if x > 30:
                success = True
        if board[agent[0]][agent[1]] == 'F':
            x = randint(1, 100)
            if x > 70:
                success = True
        if board[agent[0]][agent[1]] == 'c':
            x = randint(1, 100)
            if x > 90:
                success = True

    # if the search was a failure or the agent wasn't at the target update the searched cell
    if agent[0] != target[0] and agent[1] != target[1] or not success:
        fail = 0
        # this will update the cell that was just searched using the calculation given in the conditions
        # under question 1
        if board[agent[0]][agent[1]] == 'f':
            fail = ((probs[agent[0]][agent[1]] * .1) + (1 - probs[agent[0]][agent[1]]))
            numerator = probs[agent[0]][agent[1]] * .1
            denominator = numerator + (1 - probs[agent[0]][agent[1]])
            # print(numerator, denominator)
            probs[agent[0]][agent[1]] = numerator / denominator
            # update observations with failure probability
            observations.append(fail)
        elif board[agent[0]][agent[1]] == 'h':
            fail = ((probs[agent[0]][agent[1]] * .3) + (1 - probs[agent[0]][agent[1]]))

            numerator = probs[agent[0]][agent[1]] * .3

            denominator = numerator + (1 - probs[agent[0]][agent[1]])
            # print(numerator, denominator)
            probs[agent[0]][agent[1]] = numerator / denominator
            observations.append(fail)
        elif board[agent[0]][agent[1]] == 'F':
            fail = ((probs[agent[0]][agent[1]] * .7) + (1 - probs[agent[0]][agent[1]]))

            numerator = probs[agent[0]][agent[1]] * .7

            denominator = numerator + (1 - probs[agent[0]][agent[1]])
            # print(numerator, denominator)
            probs[agent[0]][agent[1]] = numerator / denominator
            observations.append(fail)
        elif board[agent[0]][agent[1]] == 'c':
            fail = ((probs[agent[0]][agent[1]] * .9) + (1 - probs[agent[0]][agent[1]]))

            numerator = probs[agent[0]][agent[1]] * .9
            denominator = numerator + (1 - probs[agent[0]][agent[1]])
            # print(numerator, denominator)
            probs[agent[0]][agent[1]] = numerator / denominator
            observations.append(fail)

        prev_spot.append(probs[agent[0]][agent[1]])
        # update the beliefs of the other cells not searched
        belief(probs, observations, agent, board, prev_spot, size)

    if success:
        observations.append('S')


# find the cell with the highest wanted probabilities
def find_search(p_board, agent):
    total = 0
    same_p = []
    # find the highest probabilities, if any other cells share that same probability
    # add it to a list to check distance
    for i in range(len(p_board)):
        for k in range(len(p_board)):
            if p_board[i][k] > total:
                total = p_board[i][k]
                same_p = [[i, k]]
                # print('greater than', i, k)
            elif p_board[i][k] == total:
                same_p.append([i, k])

    # if only one cell has the highest probability return its location to the agent
    if len(same_p) == 1:
        return same_p[0]

    distance = []
    # calculate the manhattan distance for every cell with equal probability
    for i in range(len(same_p)):
        d = abs(same_p[i][0] - agent[0]) + abs(same_p[i][1] - agent[1])
        distance.append(d)
    # print(len(distance))
    # print(distance)

    same_d = []
    start = distance[0]
    final = []
    # go through and find the shortest distanced cells, if there are ties add them to another list for random picking
    for k in range(len(distance)):
        if distance[k] < start:
            start = distance[k]
            same_d = [distance[k]]
            final = [same_p[k]]
        elif distance[k] == start:
            same_d.append(distance[k])
            final.append(same_p[k])

    # either return the single shortest distance location or pick a random location from the list
    if same_d == 1:
        return final[0]
    else:
        x = randint(0, len(final) - 1)
        return final[x]


# improved agent
def improved_agent(board, p_board, agent, target, size):
    observations = [1]

    prev_spots = [1 / (size * size)]

    distance = 0
    searches = 1
    if board[target[0]][target[1]] != 'C':
        while observations[len(observations) - 1] != 'S':
            # for i in range(1):
            total = 0
            old_agent = copy.deepcopy(agent)
            # get the current prediction of finding the target in each cell
            prediction_board = prediction(board, p_board, size, observations, agent)
            # send that prediction to be searched for the cell with the highest probability
            agent = find_search(prediction_board, agent)

            # calculate the distance of the old agent and the new agent to get the travel distance
            distance += abs(old_agent[0] - agent[0]) + abs(old_agent[1] - agent[1])

            # here is where we will do multiple searches depending on the cell type, and adding 1 to the search score
            # as we go
            if board[agent[0]][agent[1]] == 'f':
                search(board, p_board, agent, target, observations, prev_spots, size)
                searches += 1
            elif board[agent[0]][agent[1]] == 'h':
                for x in range(3):
                    search(board, p_board, agent, target, observations, prev_spots, size)
                    searches += 1
                    if observations[len(observations) - 1] == 'S':
                        break
            elif board[agent[0]][agent[1]] == 'F':
                for x in range(7):
                    search(board, p_board, agent, target, observations, prev_spots, size)
                    searches += 1
                    if observations[len(observations) - 1] == 'S':
                        break
            elif board[agent[0]][agent[1]] == 'c':
                for x in range(9):
                    search(board, p_board, agent, target, observations, prev_spots, size)
                    searches += 1
                    if observations[len(observations) - 1] == 'S':
                        break
            if observations[len(observations) - 1] == 'S':
                break
            # search(board, p_board, agent, target, observations, prev_spots, size)

            for s in range(size):
                for k in range(size):
                    total += p_board[s][k]
            # searches += 1
            # print(total)

    return distance + searches


# agent 2
def basic_agent_2(board, p_board, agent, target, size):
    observations = [1]

    prev_spots = [1 / (size * size)]

    distance = 0
    searches = 1
    if board[target[0]][target[1]] != 'C':
        while observations[len(observations) - 1] != 'S':
            # for i in range(1):
            total = 0
            old_agent = copy.deepcopy(agent)
            # get the current prediction of finding the target in each cell
            prediction_board = prediction(board, p_board, size, observations, agent)
            # send that prediction to be searched for the cell with the highest probability
            agent = find_search(prediction_board, agent)
            # calculate the distance of the old agent and the new agent to get the travel distance
            distance += abs(old_agent[0] - agent[0]) + abs(old_agent[1] - agent[1])
            # search the cell and update beliefs
            search(board, p_board, agent, target, observations, prev_spots, size)

            for s in range(size):
                for k in range(size):
                    total += p_board[s][k]
            searches += 1
            # print(total)

    return distance + searches


# agent 1
def basic_agent_1(board, p_board, agent, target, size):
    observations = []

    prev_spots = [1 / (size * size)]
    # search the spot the agent was placed at
    search(board, p_board, agent, target, observations, prev_spots, size)

    distance = 0
    searches = 1
    if board[target[0]][target[1]] != 'C':
        while observations[len(observations) - 1] != 'S':
            # for i in range(1):
            total = 0
            old_agent = copy.deepcopy(agent)
            # using only the current board of belief that the target is located in each cell
            # find the highest probability and give it to the agent
            agent = find_search(p_board, agent)
            # find the distance of where the agent was and where it is now and add it to the total distance
            distance += abs(old_agent[0] - agent[0]) + abs(old_agent[1] - agent[1])
            # search the given cell and update beliefs
            search(board, p_board, agent, target, observations, prev_spots, size)
            # this just checks that the probability of all the cells is equal to about 1
            for s in range(size):
                for k in range(size):
                    total += p_board[s][k]
            searches += 1
            # print(total)

    return distance + searches


def main():
    # for testing on 10 different boards
    for s in range(10):
        hill = 0
        cave = 0
        forest = 0
        flat = 0

        hill2 = 0
        cave2 = 0
        forest2 = 0
        flat2 = 0

        hill3 = 0
        cave3 = 0
        forest3 = 0
        flat3 = 0

        totalc = 0
        totalf = 0
        totalF = 0
        totalh = 0
        size = int(sys.argv[1])
        board = [[0 for _ in range(size)] for _ in range(size)]

        p_board = [[0 for _ in range(size)] for _ in range(size)]
        board = terrain(board, size)
        for i in range(size):
            for k in range(size):
                p_board[i][k] = (1 / (size * size))

        # will run each board 50 times with new agent and target locations
        for y in range(50):
            print(y)
            t_x = randint(0, size - 1)
            t_y = randint(0, size - 1)
            target = [t_x, t_y]

            start_x = randint(0, size - 1)
            start_y = randint(0, size - 1)
            agent = [start_x, start_y]

            for i in range(size):
                for k in range(size):
                    p_board[i][k] = (1 / (size * size))

            # will run each agent using the starting agent and target location

            board_agent1 = copy.deepcopy(p_board)
            board_agent2 = copy.deepcopy(p_board)
            agent2 = copy.deepcopy(agent)
            agent1 = copy.deepcopy(agent)
            board_agent3 = copy.deepcopy(p_board)
            agent3 = copy.deepcopy(agent)

            score1 = basic_agent_1(board, board_agent1, agent1, target, size)

            score2 = basic_agent_2(board, board_agent2, agent2, target, size)

            score3 = improved_agent(board, board_agent3, agent3, target, size)

            # how we update each score for each cell type the target was in
            if board[target[0]][target[1]] == 'f':
                flat += score1
                flat2 += score2
                flat3 += score3
                totalf += 1
            if board[target[0]][target[1]] == 'h':
                hill += score1
                hill2 += score2
                hill3 += score3
                totalh += 1
            if board[target[0]][target[1]] == 'F':
                forest += score1
                forest2 += score2
                forest3 += score3
                totalF += 1
            if board[target[0]][target[1]] == 'c':
                cave += score1
                cave2 += score2
                cave3 += score3
                totalc += 1

            print(score1, score2, score3)

        # calculate the average of each cell type the target was in for comparisons
        flat_average = [flat / totalf, flat2 / totalf, flat3 / totalf]
        hill_average = [hill / totalh, hill2 / totalh, hill3 / totalh]
        forest_average = [forest / totalF, forest2 / totalF, forest3 / totalF]
        cave_average = [cave / totalc, cave2 / totalc, cave3 / totalc]
        average = [flat_average, hill_average, forest_average, cave_average]
        print(average)

    print('agent1: ', score1)
    print('agent2: ', score2)


main()
