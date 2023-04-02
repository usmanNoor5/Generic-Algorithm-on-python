from pyamaze import maze, COLOR, agent
from time import sleep
import random

"""This function is used for generating chromosomes. This Choromosome Size will depend on the the size of our Grid (Rows,Colums)
This will run only once when the main() is called """
def baby(row: int, colum: int, pop: int): 
    babies = []
    for _ in range(pop):
        sublist = []
        sublist.append(1)
        for _ in range(1, colum-1):
            sublist.append(random.randint(1, row))
        sublist.append(row)
        babies.append(sublist)
    return babies
"""This function is used for passing through each generation one by one"""
def rows(pop: int, babies: list, Mapm: dict, colum: int, dic: dict):
    Infesible = [];pat = [];turns = [];Di_B = [];Ori_B = []
    for i in range(pop):
        O_B = random.randrange(2)
        D_B = random.randrange(2)
        if tuple(babies[i]) in dic:
            infesible, paths, turn, D_B, O_B, d = dic[tuple(babies[i])]
        else:
            infesible, paths, turn, D_B, O_B, d = path_find(
                O_B, D_B, babies, i, Mapm, colum)
        Infesible.append(infesible)
        pat.append(paths)
        turns.append(turn)
        Di_B.append(D_B)
        Ori_B.append(O_B)
    return Infesible, pat, turns, Di_B, Ori_B
"""Although its name is path_find but it also find the turns and also we can only call the infesible function by this 
path_find fuction you can on the line no. 58"""
def path_find(O_B: int, D_B: int, babies: list, k: int, Mapm: dict, colum: int):
    j = 0;turns = 0;path = 0;d = [(1, 1)]
    for i in range(colum-1):
        if babies[k][i] != babies[k][i+1]:
            turns += 1
    i = 0
    row = max(babies[k])-1
    colums = len(babies[k])-1
    if (O_B == 1 or O_B == 0):
        while (i < row or j < colums):
            if (D_B == 1):
                if i+1 == babies[k][j+1]:j += 1
                elif i+1 != babies[k][j+1]:
                    if babies[k][j]-babies[k][j+1] > 0:i -= 1
                    elif babies[k][j]-babies[k][j+1] < 0:i += 1
            else:
                if i+1 == babies[k][j]:j += 1
                elif i+1 != babies[k][j]:
                    if (babies[k][j-1]-babies[k][j]) > 0:i -= 1
                    elif (babies[k][j-1]-babies[k][j]) < 0:i += 1
            d.append((i+1, j+1))
            path+=1 
    return fitness(d, Mapm, babies, k), path, turns, D_B, O_B, d
"""My naming configuration is a bit odd at the time when i am writing this code. Although its mane is fitness it basically
finds the infesible steps by reading the dictionary of the grid given by payamaze on thr 6th row of the main() program"""
def fitness(d: list, Mapm: dict, babies: list, k: int):
    infesi = 0
    for i in range(len(d)-1):
        row, colum = d[i]
        if row == colum == (len(d)):
            break
        if Mapm[d[i]]['E'] == 0 and d[i+1] == (row, colum+1):
            infesi += 1
        elif Mapm[d[i]]['W'] == 0 and d[i+1] == (row, colum-1):
            infesi += 1
        elif Mapm[d[i]]['N'] == 0 and d[i+1] == (row-1, colum):
            infesi += 1
        elif Mapm[d[i]]['S'] == 0 and d[i+1] == (row+1, colum):
            infesi += 1
    return infesi
"""Now this actually calculate the fitness the max value can 0 to 1600 the formula written in tis function is taken by 
by the pdf of generic algoritm given by Sir Shujat Ali in CP-1"""
def cal_fitness(path: list, Infesible: list, turn: list, pop: int):
    paths = [];infesi = [];Turns = [];fitness = []
    for i in range(pop):
        P = 1 - (((path[i]-max(path))/(max(path)-min(path))))
        I = 1 - (((Infesible[i]-max(Infesible)) /(max(Infesible)-min(Infesible))))
        T = 1 - (((turn[i]-max(turn))/(max(turn)-min(turn))))
        paths.append(P)
        infesi.append(I)
        Turns.append(T)
    for i in range(pop):
        Fitness = (100*4 * infesi[i]*((2*paths[i]+2*Turns[i])/(2+2)))
        fitness.append(Fitness)
    return fitness
"""So from the above all function I guess this function will actually defines the working of this program. The reason 
is that allof the values which we calculate above are sorted in a specific manner to find the solution. I do something
interesting in thsi function by making a dictionary: dic={} so that i have the record of the previous ones generation
if by some chance the chromosome repeat it self it does not have to re-calculate all og these things""" 
def bublesort(dic: dict, babies: list, path: list, Infesible: list, Turns: list, fitness: list, D_B: list, O_B: list, pop: int):
    fitt = [];babb = [];Di_B = [];Ori_B = [];infesi = [];Path = [];turn = []
    
    soort = [(fitness[i], babies[i], Infesible[i], path[i],Turns[i], D_B[i], O_B[i]) for i in range(pop)]
    soort.sort(reverse=True)
    for fit, bab, infe, pth, tur, D_B, O_B in soort:
        fitt.append(fit)
        babb.append(bab)
        infesi.append(infe)
        Path.append(pth)
        turn.append(tur)
        Di_B.append(D_B)
        Ori_B.append(O_B)
    for i in range (pop):
        dic[tuple(babb[i])] = (infesi[i], Path[i],turn[i], Di_B[i], Ori_B[i], fitt[i])
    return fitt, babb, infesi, Di_B, Ori_B, dic
'''This function will run when one generation executed successfully and the program can't find a particular answer
in this we do cross over from the mid of generation means if their are 1000 generation we will do our crossover from
500. And the main thing we also chose the cross_over point the mid value of the len(colums) means if their are 10 
colums then the cross_over point will be 5. Also this function is the only means to call the mutation funtion
see line no. 129'''
def crossover(babies: list, pop: int, colum: int, row: int, infesible: list):
    if pop % 2 == 0:
        cross_over = int((pop/2)-1)
    else:
        cross_over = int(((pop-1)/2)-1)
    pt = random.randrange(colum)
    for i in range(0, cross_over+1, 2):
        for j in range(int(colum/2)):
            babies[cross_over+i][j] = babies[i][j]
            babies[cross_over+i+1][j] = babies[i+1][j]
        for k in range(pt, colum):
            babies[cross_over+i][k] = babies[i+1][k]
            babies[cross_over+i+1][k] = babies[i][k]
    mutation(babies, pop, row, colum, infesible)
    
    return babies
'''Mutation i guess the function name describes its whole purpoes after doing some cross over we directly go to mutation
Bez their might be a chance when a particular choromosome or in my case a baby afer changing its value gives us the answer
we required. In this program I also do some crispy things that might give error some times but most of the times it lead
to the answer the thing is according to our grid i change the of infesible in if cond. so that it gives us more batter 
way to approach our destination'''
def mutation(babies: list, pop: int, row: int, colum: int, infesible: list):
    for i in range(0, pop):
        index = random.randrange(colum)
        if infesible[i] <= 6: continue
        if index == 0 or index == colum-1: continue
        value = random.randrange(1, row)
        babies[i][index] = value
    return babies
'''This is the simplest of all function we only check either the fitness at index 0 is 1600 (means maximum)
or the Infesible steps is 0 from 0 to 3rd index we check upto third the reason is there might be a possiblity when
fitness is not maximum and the infesible is  0. You might wounder what is the purpoes of returing 4 its not paricularly
that we have to return 4 we can return any no. other than 0 to 3 as you can see on the line 172
'''
def sol_found(fin_fitness: list, Infesible: list, itra: int, pop: int):
    if (fin_fitness[0] == 1600 and Infesible[0] == 0):
        return 0
    elif (itra >= pop/5):
        for i in range(0, 4):
            if Infesible[i] == 0:return i
    return 4
'''This is our main() function in this we call all the function is a pattren so it makes the solution. We declare 
all the varibles assing the values and some different things as you can see'''
'''###----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------###'''
def main():
    pop = 500;global size;Start = 1;row = 20;colum = 15;is_solve = 4;itra = 1;i = 0
    dic = {}
    m = maze(row, colum)
    b = m.CreateMaze(row, colum, loopPercent=100,pattern='v')
    a = agent(m, Start, Start, shape='square', footprints=True)
    Mapm = m.maze_map
# -----------------------------------------------------------#
    babies = baby(row, colum, pop)
    Infesible, path, turns, D_B, O_B = rows(pop, babies, Mapm, colum, dic)
    fitness = cal_fitness(path, Infesible, turns, pop)
    fitness, babies, Infesible, D_B, O_B, dic = bublesort(dic, babies, path, Infesible, turns, fitness, D_B, O_B, pop)
    
    while (itra <= 650 and is_solve == 4):
        babies = crossover(babies, pop, colum, row, Infesible)
        Infesible, path, turns, D_B, O_B = rows(pop, babies, Mapm, colum, dic)
        fitness = cal_fitness(path, Infesible, turns, pop)
        fitness, babies, Infesible, D_B, O_B, dic = bublesort(dic, babies, path, Infesible, turns, fitness, D_B, O_B, pop)
        # with open ("path.csv" ,"a") as f:
        #     f.writelines(f'{path[1]}\n')
        is_solve = sol_found(fitness, Infesible, itra, pop)
        if i/50 == 1:
            dic = {}
            i = 0
        itra += 1
        i += 1
        print(itra)
    if is_solve != 4:
        
        infesi, path, turn, D_B, O_B, d = path_find(O_B[is_solve], D_B[is_solve], babies, is_solve, Mapm, colum)
        m.tracePath({a: d})
        print("\n")
        print(f"The Solution is found at Itration: {itra}")
        print(f"Path length:{path}\t\tTurns:{turn}\t\tInfesible moves:{infesi}\tO_B:{O_B}\tD_B:{D_B}\t\tFitness:{fitness[is_solve]}")
        print(f"Baby is: {babies[is_solve]}")
        sleep(10)
        m.run()
    else:
        print (f'Could not find answer in {itra} generations\n')

if __name__ =='__main__':
   
     main()
