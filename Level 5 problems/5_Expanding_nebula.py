# main function used to call a test case

def main():
    print(solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]))

def bitconversion(ls):
    return sum(v<<i for i, v in enumerate((ls)))

def initialise_frontiers(target):
    # Initialise the possible prior states
    prev_states = {}
    prev_states2 = {}
    current_state = []
    # Start with one - base case
    if target[0] == True:
        prev_states[0] = [[[True, False], [False, False]], [[False, True],[False, False]]]
        prev_states[2] = [[[False, False], [True, False]]]
        prev_states[1] = [[[False, False], [False, True]]]
    else:
        prev_states[0] = [[[False, False], [False, False]], [[True, True], [False, False]]]
        prev_states[1] = [[[True, False], [False, True]], [[False, True], [False, True]], [[True, True], [False, True]]]
        prev_states[2] = [[[True, False], [True, False]], [[False, True], [True, False]], [[True, True], [True, False]]]
        prev_states[3] = [[[False, False], [True, True]], [[True, False], [True, True]], [[False, True], [True, True]], [[True, True], [True, True]]]

    iterations = [[True, True], [True, False], [False, True], [False, False]]
    for n in range(1, len(target)):
        for states in prev_states:
            a = prev_states[states][0][-1][0]
            b = prev_states[states][0][-1][1]
            for i in iterations:
                c = i[0]
                d = i[1]
                hash = bitconversion(i)
                if target[n] == True:
                    if a + b + c + d == 1:
                        for state in prev_states[states]:
                            copy = state.copy()
                            copy.append(i)
                            if hash in prev_states2:
                                prev_states2[hash].append(copy)
                            else:
                                prev_states2[hash] = [copy]
                elif target[n] == False:
                    if a + b + c + d != 1:
                        for state in prev_states[states]:
                            copy = state.copy()
                            copy.append(i)
                            if hash in prev_states2:
                                prev_states2[hash].append(copy)
                            else:
                                prev_states2[hash] = [copy]
        prev_states = prev_states2
        prev_states2 = {}

    frontiers = []
    frontiertest=[]
    for states in prev_states:
        for i in prev_states[states]:
            frontier = []
            for j in i:
                frontier.append(j[0])
            frontiertest.append(frontier)

    for states in prev_states:
        for i in prev_states[states]:
            frontier = []
            for j in i:
                frontier.append(j[1])
            frontiers.append(frontier)
    return(frontiers)


def new_frontier(length, target, frontier_state):
    new_frontiers = []
    a = frontier_state & 1
    b = frontier_state >> 1 & 1
    for i in range(4):
        c = i & 1
        d = i >> 1 & 1
        if target & 1 == 1:
            if a + b + c + d == 1:
                new_frontiers.append(i)
        else:
            if a + b + c + d != 1:
                new_frontiers.append(i)

    for i in range(1, length):
        prev_frontier = new_frontiers
        new_frontiers = []
        a = frontier_state >> i & 1  
        b = frontier_state >> (i+1) & 1
        for frontier in prev_frontier:
            c = frontier >> i & 1
            if target >> i & 1 == 1:
                if a + b + c == 1:
                    new_frontiers.append(frontier)
                elif a + b + c == 0:
                    frontier = frontier + (1 << (i+1))
                    new_frontiers.append(frontier)
            else:
                if a + b + c == 0:
                    new_frontiers.append(frontier)
                elif a + b + c == 1:
                    frontier = frontier + (1 << (i+1))
                    new_frontiers.append(frontier)
                else:
                    new_frontiers.append(frontier)
                    frontier = frontier + (1 << (i+1))
                    new_frontiers.append(frontier)
    return(new_frontiers)

def solution(g):
    def getcolumn(i):
        column = []
        for n in range(len(g)):
            column.append(g[n][i])
        return column
    
    firstcolumn = getcolumn(0)
    length = len(firstcolumn)

    current_frontier = initialise_frontiers(firstcolumn)
    next_frontier = []
    # Start moving the frontiers towards the right, generating/eliminating all the possible paths, using the existing possible frontiers
    for i in range(len(current_frontier)):
        current_frontier[i] = bitconversion(current_frontier[i])
    
    current_count = {}
    for frontier in current_frontier:
        if frontier in current_count:
            current_count[frontier] += 1
        else:
            current_count[frontier] = 1 

    current_frontier = set(current_frontier)

    for i in range(1, len(g[0])):
        next_frontier = set()
        next_count = {}
        for frontier in current_frontier:
            column = bitconversion(getcolumn(i))
            multiplier = current_count[frontier]
            local_next = new_frontier(length, column, frontier)
            for f in local_next:
                if f in next_frontier:
                    next_count[f] += 1 * multiplier
                else:
                    next_count[f] = 1 * multiplier
                    next_frontier.add(f)
        current_frontier = next_frontier
        next_frontier = set()
        current_count = next_count
    
    
    return(sum(current_count.values()))

            
        
main()
