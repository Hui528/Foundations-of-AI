import collections


class solution:
    def BFS(grid: list, stamina: int, start, end: tuple) -> list:
        def BFS_isValid(grid: list, stamina: int, cur, next: tuple, parent: dict) -> bool:
            if 0 <= next[0] < len(grid[0]) and 0 <= next[1] < len(grid) and next not in parent:
                if grid[next[1]][next[0]] >= 0:
                    if stamina + abs(grid[cur[1]][cur[0]]) >= abs(grid[next[1]][next[0]]):
                        return True
                else:  # the next cell is a tree
                    if abs(grid[cur[1]][cur[0]]) >= abs(grid[next[1]][next[0]]):
                        return True
            return False

        def BFS_findPath(parent: dict, end: tuple):
            path = [end]
            posi = end  # find path from the destination to the start cell
            while parent[posi]:
                path.append(parent[posi])
                posi = parent[posi]
            path.reverse()
            return path

        queue = collections.deque()  # all nodes in queue are guaranteed to be valid
        queue.append(start)
        parent = {start: None}  # record visited cells and their parents
        steps = [[-1, 0], [1, 0], [0, -1], [0, 1],
                 [-1, -1], [-1, 1], [1, -1], [1, 1]]
        while queue:
            cur = queue.popleft()
            for step in steps:
                next = (step[0] + cur[0], step[1] + cur[1])
                if BFS_isValid(grid, stamina, cur, next, parent):
                    parent[next] = cur
                    if next == end:
                        return BFS_findPath(parent, end)
                    queue.append(next)
        return "FAIL"

    def UCS(grid: list, stamina: int, start, end: list) -> list:

        def findChildInList(l, child):
            for i in range(len(l)):
                if l[i][0] == child:
                    return i
            return -1

        def isValid(grid: list, stamina: int, cur, next: tuple):
            if 0 <= next[0] < len(grid[0]) and 0 <= next[1] < len(grid):
                if grid[next[1]][next[0]] >= 0:
                    if stamina + abs(grid[cur[1]][cur[0]]) >= abs(grid[next[1]][next[0]]):
                        return True
                else:  # the next cell is a tree
                    if abs(grid[cur[1]][cur[0]]) >= abs(grid[next[1]][next[0]]):
                        return True
            return False

        def findPath(parent: dict, end: tuple):
            path = [end]
            posi = end  # find path from the destination to the start cell
            while parent[posi]:
                path.append(parent[posi])
                posi = parent[posi]
            path.reverse()
            return path

        steps = [[-1, 0], [1, 0], [0, -1], [0, 1],
                 [-1, -1], [-1, 1], [1, -1], [1, 1]]
        open = []  # element: [position, cost]
        open.append([start, 0])
        closed = []  # element: [position, cost]
        parent = {start: None}

        while open:
            cur = open.pop()  # sort open in decreasing order
            curPos = cur[0]
            if curPos == end:
                return findPath(parent, curPos)
            for step in steps:
                diagonal = True if abs(step[0]) + abs(step[1]) == 2 else False
                child = (step[0] + curPos[0], step[1] + curPos[1])
                if isValid(grid, stamina, curPos, child):
                    childCost = cur[1] + 14 if diagonal else cur[1] + 10
                    childInOpenIndex = findChildInList(open, child)
                    childInClosedIndex = findChildInList(closed, child)
                    if childInOpenIndex == -1 and childInClosedIndex == -1:
                        open.append([child, childCost])
                        parent[child] = curPos
                    elif childInOpenIndex != -1:
                        if childCost < open[childInOpenIndex][1]:
                            open[childInOpenIndex][1] = childCost
                            parent[child] = curPos
                    elif childInClosedIndex != -1:
                        if childCost < closed[childInClosedIndex][1]:
                            del closed[childInClosedIndex]
                            open.append([child, childCost])
                            parent[child] = curPos
            closed.append(cur)
            open.sort(key=lambda x: x[1], reverse=True)
        return "FAIL"

    def A_Star(grid: list, stamina: int, start, end: tuple) -> list:

        def heuristic(start, end: tuple):
            diff_x = abs(start[0] - end[0])
            diff_y = abs(start[1] - end[1])
            return 14 * min(diff_x, diff_y) + 10 * abs(diff_y - diff_x)

        def findPairInList(l: list, prePos: tuple, curPos: tuple, nextPos: tuple):
            for i in range(len(l) - 2):
                if l[i] == prePos and l[i + 1] == curPos and l[i + 2] == nextPos:
                    return True
            return False

        def isValid(grid: list, stamina: int, prev, cur, next: tuple):
            if 0 <= next[0] < len(grid[0]) and 0 <= next[1] < len(grid):
                if grid[next[1]][next[0]] >= 0:
                    if max(abs(grid[prev[1]][prev[0]]) - abs(grid[cur[1]][cur[0]]), 0) + stamina + abs(grid[cur[1]][cur[0]]) >= abs(grid[next[1]][next[0]]):
                        return True
                else:  # the next cell is a tree
                    if abs(grid[cur[1]][cur[0]]) >= abs(grid[next[1]][next[0]]):
                        return True
            return False

        steps = [[-1, 0], [1, 0], [0, -1], [0, 1],
                 [-1, -1], [-1, 1], [1, -1], [1, 1]]
        # parent = {start: None}  # the parent with smallest gScore
        # # fScore = dict()
        # # fScore[start] = heuristic(start, end)
        # element: [[path], gScore, fScore]
        path = [start]
        open = [[path, 0, heuristic(start, end)]]
        while open:
            cur = open.pop()  # sort open in decreasing order
            print(cur)
            path = cur[0]
            curPos = path[-1]
            prePos = path[-2] if len(path) > 1 else curPos
            if curPos == end:
                # print(parent)
                # return findPath(parent, curPos)
                return path
            for step in steps:
                diagonal = True if abs(step[0]) + abs(step[1]) == 2 else False
                child = (step[0] + curPos[0], step[1] + curPos[1])
                if child != prePos and not findPairInList(path, prePos, curPos, child) and isValid(grid, stamina, prePos, curPos, child):
                    M = max(abs(grid[prePos[1]][prePos[0]]) -
                            abs(grid[curPos[1]][curPos[0]]), 0)
                    child_gScore = cur[1]
                    child_gScore += max(
                        0, abs(grid[child[1]][child[0]]) - abs(grid[curPos[1]][curPos[0]]) - M)
                    child_gScore += 14 if diagonal else 10
                    # childInOpenIndex = findChildInList(open, child)
                    # if childInOpenIndex == -1 or child_gScore < open[childInOpenIndex][2]:
                    #     parent[child] = curPos
                    # always append the new pair (child, curPos) into open list, since some pairs with bigger cost may have bigger M, and then these pairs have some new next step choices
                    open.append([path + [child], child_gScore,
                                child_gScore + heuristic(child, end)])
            open.sort(key=lambda x: x[2], reverse=True)  # in descending order
        return "FAIL"


def main():
    file = open("input.txt", "r")

    # first line
    line = file.readline()
    algo = line.strip()
    # second line
    line = file.readline()
    elements = line.strip().split()
    grid = [[0] * int(elements[0]) for _ in range(int(elements[1]))]
    # third line
    line = file.readline()
    elements = line.strip().split()
    start = (int(elements[0]), int(elements[1]))
    # forth line
    line = file.readline()
    stamina = int(line.strip())
    # fifth line
    line = file.readline()
    numOfLodges = int(line.strip())
    # next numOfLodges lines
    lodges = []
    for _ in range(numOfLodges):
        line = file.readline()
        elements = line.strip().split()
        lodges.append((int(elements[0]), int(elements[1])))
    # next H lines
    for i in range(len(grid)):
        line = file.readline()
        elements = line.strip().split()
        for j in range(len(grid[0])):
            grid[i][j] = int(elements[j])

    f = open("output.txt", "w")

    if algo == "BFS":
        for lodge in lodges:
            res = solution.BFS(grid, stamina, start, lodge)
            if res == "FAIL":
                f.write(res)
            else:
                for pos in res:
                    f.write(str(pos[0]) + "," + str(pos[1]))
                    if pos != res[-1]:
                        f.write(" ")
            f.write("\n")

    if algo == "UCS":
        for lodge in lodges:
            res = solution.UCS(grid, stamina, start, lodge)
            if res == "FAIL":
                f.write(res)
            else:
                for pos in res:
                    f.write(str(pos[0]) + "," + str(pos[1]))
                    if pos != res[-1]:
                        f.write(" ")
            f.write("\n")

    if algo == "A*":
        for lodge in lodges:
            res = solution.A_Star(grid, stamina, start, lodge)
            if res == "FAIL":
                f.write(res)
            else:
                for pos in res:
                    f.write(str(pos[0]) + "," + str(pos[1]))
                    if pos != res[-1]:
                        f.write(" ")
            f.write("\n")

    f.close()


if __name__ == "__main__":
    main()
