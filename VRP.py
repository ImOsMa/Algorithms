from scipy.spatial import distance
import itertools
import pandas as pd
#from tsp_vis import visualize_vrp


class Market:
    def __init__(self, id, demand, start_time, end_time, work_time):
        self.id = id
        self.demand = demand
        self.start_time = start_time
        self.end_time = end_time
        self.work_time = work_time
        self.is_visited = False


class Tabu:
    def __init__(self, len_path, path, alive_tabu):
        self.len_path = len_path
        self.path = path
        self.alive_tabu = alive_tabu


class VRP:
    def __init__(self):
        self.market_num = 0
        self.vehicles_num = 0
        self.vehicles_cap = 0
        self.coords = list()
        self.time_window = list()
        self.demand = list()
        self.demand_time = list()
        self.distance_matrix = list()
        self.market_list = list()
        self.tabu_list = list()
        self.best_solution = list()

    def read_file(self, file_name):
        f = open(file_name)
        main_data = f.readline().split(' ')
        self.market_num = int(main_data[0])

        self.vehicles_num = int(main_data[1])
        self.vehicles_cap = int(main_data[2])
        for line in f:
            data = line.split(' ')
            while '' in data:
                data.remove('')
            data[-1].replace('\n', '')
            coord_x = int(data[1])
            coord_y = int(data[2])
            object = Market(int(data[0]), int(data[3]),
                            int(data[4]), int(data[5]),
                            int(data[6]))
            self.market_list.append(object)
            self.coords.append((coord_x, coord_y))
            self.demand.append(int(data[3]))
            self.time_window.append((int(data[4]), int(data[5])))
            self.demand_time.append(int(data[6]))

    def create_distance_matrix(self):
        for coord in self.coords:
            distances = list()
            dst = 0
            for other_coord in self.coords:
                dst = distance.euclidean(coord, other_coord)
                distances.append(dst)
            self.distance_matrix.append(distances)

    def not_visited_markets(self):
        not_visited = list()
        for i in self.market_list:
            if not i.is_visited and i.id:
                not_visited.append(i)
        return sorted(not_visited, key=lambda value: value.end_time)

    def init_is_keep_up(self, path):
        # [0 65 5 0]
        time = 0
        cap = self.vehicles_cap
        for start, target in zip(path, path[1:]):
            service_time = max([self.market_list[target.id].start_time, time +
                                self.distance_matrix[start.id][target.id]])
            if service_time > self.market_list[target.id].end_time:
                return False
            time = service_time + self.market_list[target.id].work_time
            cap -= self.market_list[target.id].demand
        if time >= self.market_list[0].end_time or cap < 0:
            return False
        return True

    def generate_first_path(self):
        solution = []
        while len(self.not_visited_markets()) > 0:
            markets = self.not_visited_markets()
            marsh = list()
            for market in markets:
                if self.init_is_keep_up([self.market_list[0]] + marsh + [market, self.market_list[0]]):
                    market.is_visited = True
                    marsh.append(market)
            solution.append([self.market_list[0]] + marsh + [self.market_list[0]])
        self.best_solution = list(solution)

    def last_best(self, init_sol): # пока не найдется лучший из худших
        new_sol = list(init_sol)
        iter = 0
        second_best = list()
        for i in range(len(init_sol)):
            is_stucked = False
            while not is_stucked:
                way = new_sol[i]
                is_stucked = True
                for t, v in itertools.combinations(range(self.market_num), 2):
                    new_way = self.two_opt(way[1:-1], t, v)
                    new_way = [self.market_list[0]] + new_way + [self.market_list[0]]
                    buf_sol = list(new_sol)
                    buf_sol[i] = new_way
                    if self.init_is_keep_up(new_way):
                        if self.fitness(new_way[1:-1]) > self.fitness(way[1:-1]) and not \
                                self.check_element_in_tabu_list(buf_sol):
                            if iter == 0:
                                second_best = list(new_way)
                                new_sol[i] = second_best
                                is_stucked = False
                            if self.fitness(second_best[1:-1]) < self.fitness(new_way[1:-1]):
                                second_best = list(new_way)
                                new_sol[i] = second_best
                                is_stucked = False
                            iter += 1
        return new_sol

    def two_opt(self, init_sol, i, j):
        if i == 0:
            return init_sol[j:i:-1] + [init_sol[i]] + init_sol[j + 1:]
        return init_sol[:i] + init_sol[j:i - 1:-1] + init_sol[j + 1:]

    def crossVal(self, a, b, i, j):
        lst = list()
        lst.append(a[:i] + b[j:])
        lst.append(b[:j] + a[i:])
        return lst

    def insertionVal(self, a, b, i, j):
        if len(a) == 0:
            return a, b
        i -= len(a) * int(i / len(a))
        lst = list()
        lst.append(a[:i] + a[i + 1:])
        lst.append(b[:j] + [a[i]] + b[j:])
        return lst

    def swapVal(self, a, b, i, j):
        if i >= len(a) or j >= len(b):
            return a, b
        a, b = a.copy(), b.copy()
        a[i], b[j] = b[j], a[i]
        return a, b

    def fitness(self, init_sol):
        time = 0
        for start, target in zip(init_sol, init_sol[1:]):
            service_time = max([self.market_list[target.id].start_time, time +
                                self.distance_matrix[start.id][target.id]])
            time = service_time + self.market_list[target.id].work_time
        return time

    def all_fitness(self, all_sol):
        dst = 0
        for element in all_sol:
            dst += self.fitness(element[1:-1])
        return dst

    def check_element_in_tabu_list(self, init_sol):
        for element in self.tabu_list:
            if init_sol == element.path or \
                    self.all_fitness(init_sol) == self.all_fitness(element.path):
                return True
        return False

    def mix(self, init_sol):
        current_sol = list(init_sol)
        is_stucked = False
        while not is_stucked:
            is_stucked = True
            for i, j in itertools.combinations(range(len(current_sol)), 2):
                for k, l in itertools.product(range(len(current_sol[i])), range(len(current_sol[j]))):
                    for func in [self.crossVal, self.insertionVal, self.swapVal]:
                        c1, c2 = func(current_sol[i][1:-1], current_sol[j][1:-1], k, l)
                        r1, r2 = [self.market_list[0]] + c1 + [self.market_list[0]], \
                                 [self.market_list[0]] + c2 + [self.market_list[0]]
                        if self.init_is_keep_up(c1) and self.init_is_keep_up(c2):
                            buf_sol = list(current_sol)
                            buf_sol[i] = r1
                            buf_sol[j] = r2
                            if self.fitness(r1[1:-1]) + self.fitness(r2[1:-1]) < \
                               self.fitness(current_sol[i][1:-1]) + self.fitness(current_sol[j][1:-1]) and not \
                               self.check_element_in_tabu_list(buf_sol):
                                current_sol[i] = r1
                                current_sol[j] = r2
                                is_stucked = False
            current_sol = list(filter(lambda x: len(x) - 2 != 0, current_sol))
        return current_sol

    def improve(self, init_sol, mode='two_opt'):
        new_sol = list(init_sol)
        if mode == 'two_opt':
            for i in range(len(init_sol)):
                is_stucked = False
                while not is_stucked:
                    way = new_sol[i]
                    is_stucked = True
                    for t, v in itertools.combinations(range(self.market_num), 2):
                        new_way = self.two_opt(way[1:-1], t, v)
                        new_way = [self.market_list[0]] + new_way + [self.market_list[0]]
                        buf_sol = list(new_sol)
                        buf_sol[i] = new_way
                        if self.init_is_keep_up(new_way) and not self.check_element_in_tabu_list(buf_sol):
                            if self.fitness(new_way[1:-1]) < self.fitness(way[1:-1]):
                                new_sol[i] = new_way
                                is_stucked = False
            return new_sol

    def tabu_search(self, iterations):
        new_sol = list(self.best_solution)
        for _ in range(iterations):
            print(1)
            if len(self.tabu_list) != 0:
                delete_list = list()
                for element in self.tabu_list:
                    element.alive_tabu -= 1
                    if element.alive_tabu <= 0:
                        delete_list.append(element)
                    if element.path == new_sol:
                        print("Before last best:", self.all_fitness(new_sol))
                        new_sol = self.last_best(new_sol)
                        print("After last best: ", self.all_fitness(new_sol))
                for i in delete_list:
                    self.tabu_list.remove(i)
            new_sol = self.improve(new_sol)
            print("After improve: ", self.all_fitness(new_sol))
            new_sol = self.mix(new_sol)
            print("After mix: ", self.all_fitness(new_sol))
            if self.all_fitness(new_sol) < self.all_fitness(self.best_solution):
                self.best_solution = new_sol
            print()
            tabu_element = Tabu(self.all_fitness(new_sol), new_sol, 10)
            self.tabu_list.append(tabu_element)
        return self.best_solution


t = VRP()
t.read_file('data.txt')
t.create_distance_matrix()
t.generate_first_path()
decision = list()
solution = t.tabu_search(10)
for k in solution:
    second_decision = list()
    for j in k:
        second_decision.append(j.id)
        print(j.id, end=' ')
    decision.append(second_decision)
    print()
print("TOTAL LENGTH: ", t.all_fitness(solution))
data_id = list()
data_x = list()
data_y = list()
for i in range(len(t.market_list)):
    data_id.append(i)
    data_x.append(t.coords[i][0])
    data_y.append(t.coords[i][1])

data_frame = pd.DataFrame(list(zip(data_id, data_x, data_y)), columns = ["Id", "X", "Y"])

vertexes = {data_frame["Id"][i]: [data_frame["X"][i], data_frame["Y"][i]] for i in range(len(data_frame["Id"]))}

init_decision = decision
#visualize_vrp(vertexes, init_decision, node_size=20, edge_size=0.8, font_size=4, dpi=1000)


