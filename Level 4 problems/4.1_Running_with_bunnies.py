def solution(times, times_limit):

    # Start by running Floyd-Warshall to identify the shortest paths and eliminate backtracking, as well identify any negative cycles
    
    station_map = times
    nodes_no = len(station_map)

    for k in range(nodes_no):
        for i in range(nodes_no):
            for j in range(nodes_no):
                if k != i:
                    station_map[i][j]= min(station_map[i][j], station_map[i][k] + station_map[k][j])

    # Check for negative cycles - if negative cycle is present, return a list of all the bunnies
    for i in range(nodes_no):
        if station_map[i][i] < 0:
            return list(range(0, nodes_no-2))

    # If no negative cycle is present - we now have a modified travelling salesman problem (since there's no backtracking anymore), combined with a knapsack problem
    # In the worst case scenario, (ie if we need to go all the way, it is exactly like the traveling salesman)

    # Initialise a list to represent the area that will next be searched
    total_search = []
    current_search = {"1":[]}
    next_search = {}

    # Iteration 1 - gets the first path
    for i in range(1, nodes_no - 1):
        search = [i]
        distance = station_map[0][i]
        current_search["1"].append((search, distance))
    total_search.append(current_search)


    # Iteration 2 - gets the second path
    for entry in current_search:
        for path in current_search[entry]:
            for next_node in range(1, (nodes_no-1)):
                current_node = path[0][-1]
                newpath = list(path[0])
                newpath.append(next_node)
                if next_node not in path[0]:
                    distance = path[1] + station_map[current_node][next_node]
                    pathhash = "".join(map(str, sorted(newpath)))
                    if pathhash in next_search:
                        next_search[pathhash].append((newpath,distance))
                    else:
                        next_search.update({"".join(map(str, sorted(newpath))):[(newpath, distance)]})

    total_search.insert(0, next_search)
    current_search = next_search
    next_search = {}

    # Iteration 3 - dynamic programming starts
    # For the remaining iterations up to the last bunny
    for i in range(2, nodes_no - 2):
        # For each dictionary entry
        for entry in current_search:
            for next_node in range(1, (nodes_no-1)):
                if next_node not in current_search[entry][0][0]:
                    lowestdistance=999999                
                    # Loop through the list within each dictionary entry to find the lowest distance
                    for path in current_search[entry]:
                        current_node = path[0][-1]
                        distance = path[1] + station_map[current_node][next_node]
                        if distance < lowestdistance:
                            lowestdistance = distance
                            newpath = list(path[0])
                            newpath.append(next_node)
                    pathhash = "".join(map(str, sorted(newpath)))
                    if pathhash in next_search:
                        next_search[pathhash].append((newpath, lowestdistance))
                    else:
                        next_search.update({"".join(map(str, sorted(newpath))):[(newpath, lowestdistance)]})
        total_search.insert(0, next_search)
        current_search = next_search
        next_search = {}
    # Finally, search through the total_search list - starting from max number of bunnies down

    for iteration in total_search:
        for entry in sorted(iteration.keys()):
            for path in iteration[entry]:
                if station_map[path[0][-1]][nodes_no-1]+path[1] <= times_limit:
                    return sorted(map(lambda x: x-1, path[0]))
    
    return([])

def main():
# test code
    print(solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3))

main()
