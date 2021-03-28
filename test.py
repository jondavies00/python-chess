a = [i for i in range(8)]
b = [-i for i in range(8)]
moves = list(zip(a,b))
moves.append(list(zip(b,a)))
moves.append(list(zip(a,a)))
moves.append(list(zip(b,b)))
print(moves)