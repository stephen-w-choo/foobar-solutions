def main():
    print(solution([2,5], [1,2], [1,4], 11))

def solution(dimensions, your_position, trainer_position, distance):

    # Function to reduce a vector to its simplest form
    # Uses the Eucliean greatest common denominator algorithm
    def reduce_vector(x, y):
        if x == 0 and y == 0:
            return
        
        def euclid_algo(a, b):
            while b != 0:
                (a, b) = (b, a % b)
            return abs(a)

        divisor = euclid_algo(x, y)
        while divisor != 1:
            x = x // divisor
            y = y // divisor
            divisor = euclid_algo(x, y)
        
        return(x, y)

    # Function to create a bidirectional iterator - goes [0, 1, -1, 2, -2...]
    def iterate2ways(n):
        if n > 0:
            n = n * -1
        else:
            n = n * -1                
            n += 1 
        return n

    # Function to generate a set of all vectors that will hit a specific point
    # Function will take into account possible collisions with the trainer and yourself
    def get_vectors(gunner_position):
        distancelimit = distance ** 2
        i = 0
        ipass = True
        self_vectors = set()
        target_vectors = set()
        # Summary: create a loop within a loop to generate mirror image (x,y) positions
        # Loop starts from the (0, 0) iteration and moves outwards
        # Subtract the mirror image positions from the self position to generate the vector
        # Simplify the vector
        # Store all previous vectors so far in a self_vector set and target_vector set, check for collisions
        # Loops are designed to terminate if distance limit is exceeded 
        # This can potentially result in early termination eg at i = 1 even if i = -1 would be below the distance limit
        # Pass boolean initialised to give it 2 chances
        while True:
            j = 0
            jpass = True
            if i % 2 == 1:
                vector_x = (i + 1) * dimensions[0] - gunner_position[0] - your_position[0]
                selfvector_x = (i + 1) * dimensions[0] - 2 * your_position[0] 
            else:
                vector_x = i * dimensions[0] + gunner_position[0] - your_position[0]
                selfvector_x = i * dimensions[0]
            if vector_x **2 + (gunner_position[1] - your_position[1]) ** 2 > distancelimit:
                if ipass == True:
                    i = iterate2ways(i)
                    ipass = False
                    continue
                if ipass == False:
                    break
            while True:
                if j % 2 == 1:
                    vector_y = (j + 1) * dimensions[1] - gunner_position[1] - your_position[1]
                    selfvector_y = (j + 1) * dimensions[1] - 2 * your_position[1]
                else:
                    vector_y = j * dimensions[1] + gunner_position[1] - your_position[1]
                    selfvector_y = j * dimensions[1]
                if vector_y ** 2 + vector_x ** 2 > distancelimit:
                    if jpass == True:
                        j = iterate2ways(j)
                        jpass = False
                        continue
                    if jpass == False:
                        break
                self_vector = reduce_vector(selfvector_x, selfvector_y)
                target_vector = reduce_vector(vector_x, vector_y)
                if self_vector not in target_vectors:
                    self_vectors.add(self_vector)
                if target_vector not in self_vectors:
                    target_vectors.add(target_vector)
                j = iterate2ways(j)
            i = iterate2ways(i)      
        return len(target_vectors)
    
    return get_vectors(trainer_position)

main()
