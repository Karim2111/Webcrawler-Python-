import math

def euclidean_dist(a,b):
    a = a[0]
    b = b[0]
    if len(a) != len(b):
        return None
    return math.sqrt(sum([((a[i]-b[i])**2) for i in range(len(a))]))

def mult_matrix(a, b):
    if len(a[0]) != len(b): #cols a must equal rows b
        return None
	
    new_matrix = []
    for i in range(len(a)): #rows of a
        new_matrix_row = []
        for j in range(len(b[0])): #columns of b
            total = 0
            for k in range(len(b)): #columns a/rows of b
                total += a[i][k] * b[k][j]
            new_matrix_row.append(total)
        new_matrix.append(new_matrix_row)
        new_matrix_row = []
    return new_matrix