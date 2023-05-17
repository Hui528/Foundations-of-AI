KB = []
variablesIndex = 0  # from 'a' to 'z'


def find(data: list, i: int):
    if not data[i].islower():
        return data[i]
    else:
        if i != ord(data[i]) - ord('a'):
            data[i] = find(data, ord(data[i]) - ord('a'))
        return data[i]


def clauseCopy(clause: list) -> list:
    deepCopy = []
    for element in clause:
        if type(element) is list:
            deepCopy.append(element.copy())
        else:
            deepCopy.append(element)
    return deepCopy


def convertToCNF(sentence: str):
    # convert the sentence to CNF and put it into KB
    # KB: [[A1, A2, ..., An], [B1, B2, ..., Bm], ...], operator between Ai is "|", operator between A and B is "&"
    # Ai: [negation, predicate, parameters] eg. [0, Order, [x, Fish]]
    step_1_res = eliminateImplications(sentence)
    # print(step_1_res)
    if step_1_res[2] != "":
        step_2_res = predicateToCNF(step_1_res[1], True)
        convertedSents = distributionWithOneConcl(step_2_res, step_1_res[2])
    else:  # there is no implication operator in the sentence
        convertedSents = predicateToCNF(step_1_res[1], False)
    # print(step_2_res)
    # print(convertedSents)
    deepCopySents = []
    for i in range(len(convertedSents)):
        deepCopyClauses = []
        # convertedSents[i]: [[True, 'Ate', ['x', 'y']], [False, 'GetCheck', ['x', 'z']]]
        for j in range(len(convertedSents[i])):
            # convertedSents[i][j]: [True, 'Ate', ['x', 'y']]
            deepCopyCl = []
            deepCopyCl.append(convertedSents[i][j][0])
            deepCopyCl.append(convertedSents[i][j][1])
            deepCopyCl.append(convertedSents[i][j][2].copy())
            deepCopyClauses.append(deepCopyCl.copy())
        deepCopySents.append(deepCopyClauses.copy())

    finalSents = standarizedVairables(deepCopySents)
    # finalSents = deepCopySents
    # print(finalSents)
    global KB
    KB.extend(finalSents)


def eliminateImplications(sentence: str) -> list:
    sentence = sentence.strip()
    implication_start = sentence.find('=>')
    if implication_start == -1:
        return ["~", sentence, ""]
    else:
        predicates = sentence[: implication_start]
        predicates = predicates.strip()
        conclution = sentence[implication_start + 2:]
        conclution = conclution.strip()
        return ["~", predicates, conclution]


# convert to [A1, A2, ..., An]
def predicateToCNF(predicates: str, nega: bool):
    res = []  # operator between elements of res is "&"
    if nega:
        for part_with_and_nega in predicates.split("|"):
            element_in_KB = []  # operator between elements of element_in_KB is "|"
            part_with_and_nega = part_with_and_nega.strip()
            for part_with_nega in part_with_and_nega.split("&"):
                part_with_nega = part_with_nega.strip()
                clause = standarizedClause(part_with_nega, nega)
                element_in_KB.append(clause)
            res.append(element_in_KB)
    else:
        # only have "~" and "&"
        if predicates.find('|') == -1:
            for part_with_nega in predicates.split("&"):
                part_with_nega = part_with_nega.strip()
                clause = standarizedClause(part_with_nega, nega)
                res.append([clause])
        # only have "~" and "|"
        elif predicates.find('&') == -1:
            element_in_KB = []
            for part_with_nega in predicates.split("|"):
                part_with_nega = part_with_nega.strip()
                clause = standarizedClause(part_with_nega, nega)
                element_in_KB.append(clause)
            res.append(element_in_KB)
        # have "~", "&", "|"
        else:
            list_of_part_with_and_nega = predicates.split("|")
            # recursively convert (A1 & A2 & ... & An) | (B1 & B2 & ... & Bm) to (A1 | B1) & ... & (An | B1) & (A1 | B2) & ... & (An | B2) & ... & (A1 | Bm) & ... & (An | Bm)
            first_list = list_of_part_with_and_nega[0].split("&")
            for k in range(1, len(list_of_part_with_and_nega)):
                combined = []
                second_list = list_of_part_with_and_nega[k].split("&")
                for first in first_list:
                    for second in second_list:
                        combined.append(first.strip() + " | " + second.strip())
                first_list = combined

            for part in first_list:
                element_in_KB = []
                for atom in part.split("|"):
                    atom = atom.strip()
                    clause = standarizedClause(atom, nega)
                    element_in_KB.append(clause)
                res.append(element_in_KB)
    return res


def standarizedClause(sentence: str, nega: bool) -> list:
    # return clause: [negation, predicate, parameters] eg. [0, Order, [x, Fish]]
    sentence = sentence.strip()
    count_nega = 0
    for i in range(len(sentence)):
        if sentence[i] == "~":
            count_nega += 1
        else:
            break
    sentence = sentence[count_nega:]
    if count_nega % 2 == 1:
        sentence = "~" + sentence

    cl = [True, "", []]
    if (nega and sentence[0] == "~") or (not nega and sentence[0] != "~"):
        cl[0] = False

    paren_start = sentence.find('(')
    paren_end = sentence.find(')')
    if sentence[0] == "~":
        cl[1] = sentence[1: paren_start]
    else:
        cl[1] = sentence[:paren_start]
    params = sentence[paren_start + 1: paren_end]
    for param in params.split(","):
        cl[2].append(param.strip())

    return cl


def distributionWithOneConcl(ready_list: list, concl: str) -> list:
    clause = standarizedClause(concl, False)
    for i in range(len(ready_list)):
        ready_list[i].append(clause)
    return ready_list


def standarizedVairables(sentencesSet: list) -> list:
    global variablesIndex
    charsDict = {}
    for i in range(len(sentencesSet)):
        # sentencesSet[i]: [[True, 'Order', ['x', 'y']], [False, 'Seated', ['x']]]
        for j in range(len(sentencesSet[i])):
            # sentencesSet[i][j]: [True, 'Order', ['x', 'y']]
            for k in range(len(sentencesSet[i][j][2])):
                if sentencesSet[i][j][2][k].islower() and sentencesSet[i][j][2][k] not in charsDict:
                    charsDict[sentencesSet[i][j][2][k]] = chr(
                        variablesIndex + ord('a'))
                    variablesIndex += 1
                    if variablesIndex >= 26:
                        variablesIndex = 0
    for i in range(len(sentencesSet)):
        for j in range(len(sentencesSet[i])):
            for k in range(len(sentencesSet[i][j][2])):
                if sentencesSet[i][j][2][k].islower():
                    sentencesSet[i][j][2][k] = charsDict[sentencesSet[i][j][2][k]]
    return sentencesSet


def isValidKB() -> bool:
    global KB
    for i in range(len(KB)):
        for j in range(i + 1, len(KB)):
            if oppositeSentences(KB[i], KB[j]):
                return False
    return True


def oppositeSentences(sent1: list, sent2: list) -> bool:
    if len(sent1) == len(sent2):
        used = [False] * len(sent2)
        count_oppo_cl = 0
        for i in range(len(sent1)):
            for j in range(len(sent2)):
                if not used[j] and oppositeClauses(sent1[i], sent2[j]):
                    count_oppo_cl += 1
                    used[j] = True
                    break
        if count_oppo_cl == len(sent1):
            return True
    return False


def oppositeClauses(cl1: list, cl2: list) -> bool:
    if cl1[0] != cl2[0] and cl1[1] == cl2[1]:
        for i in range(len(cl1[2])):
            if not cl1[2][i].islower() and not cl2[2][i].islower() and cl1[2][i] != cl2[2][i]:
                return False
        return True
    return False


def resolution(query: str) -> bool:
    # query_nega_clause = predicateToCNF(query, True)
    # global KB
    # KB.extend(query_nega_clause)
    if query[0] == "~":
        nega_query = query[1:]
    else:
        nega_query = "~" + query

    convertToCNF(nega_query)

    # for element in KB:
    #     print(element)

    G = KB
    K = []
    while G:
        A = pickClause(G)
        G.remove(A)
        N = []
        for B in K:
            if resolvable(A, B):
                D, vality = resolve(A, B)
                if vality and not D:  # this is a valid empty set, which means, contradiction
                    return False
                for clauses in D:
                    if not subsumedBy(clauses, [G, K]):
                        N.append(clauses)
        if len(A) == 1:
            K.insert(0, A)
        else:
            K.append(A)
        # if len(K) > 0 and len(A) < len(K[0]):
        #     K.sort(key=len)
        for ele in G:
            if subsumedBy(ele, [N]):
                G.remove(ele)
        for ele in K:
            if subsumedBy(ele, [N]):
                K.remove(ele)
        G.extend(N)
    return True


def pickClause(KB: list) -> list:
    if not KB:
        return []
    shortest = KB[0]
    for element in KB:
        if len(element) < len(shortest):
            shortest = element
    return shortest


def resolvable(A: list, B: list) -> bool:
    for ele1 in A:
        for ele2 in B:
            if ele1[0] != ele2[0] and ele1[1] == ele2[1] and resolvableVariables(ele1, ele2):
                return True
    return False


def resolvableVariables(ele1: list, ele2: list) -> bool:
    for i in range(len(ele1[2])):
        if not ele1[2][i].islower() and not ele2[2][i].islower() and ele1[2][i] != ele2[2][i]:
            return False
    return True


def resolve(A: list, B: list) -> list:
    res = []
    for ele1 in A:
        for ele2 in B:
            if ele1[0] != ele2[0] and ele1[1] == ele2[1] and resolvableVariables(ele1, ele2):
                validity = True
                varsRoot = [c for c in "abcdefghijklmnopqrstuvwxyz"]
                for i in range(len(ele1[2])):
                    # if both ele1 and ele2 only have constants, skip this step and run reproduce
                    if ele1[2][i].islower() or ele2[2][i].islower():
                        varsRoot = substitution(
                            varsRoot, ele1[2][i], ele2[2][i])
                        if not varsRoot:
                            validity = False
                            break
                if validity:
                    updatedClauses = reproduce(varsRoot, A, B, ele1, ele2)
                    if not updatedClauses:
                        return [], True  # we get a empty set from A and B with a valid varsRoot, so now contradiction is found
                    else:
                        res.append(updatedClauses)
    if not res:
        # res is empty, but it's not from a valid varsRoot, so this is not a contradiction
        return [], False
    else:
        return res, True


# at least one of values is a parameter (islower() is true)
def substitution(varsRoot: list, value1: str, value2: str):
    if value1.islower():
        root1 = find(varsRoot, ord(value1) - ord('a'))
    if value2.islower():
        root2 = find(varsRoot, ord(value2) - ord('a'))
    if value1.islower() and value2.islower():
        if not root1.islower() and not root2.islower():
            if root1 != root2:
                return []
        else:
            if root1.islower():
                varsRoot[ord(value1) - ord('a')] = root2
            else:
                varsRoot[ord(value2) - ord('a')] = root1

    else:
        if value1.islower() and not value2.islower():
            if not root1.islower() and root1 != value2:
                return []
            varsRoot[ord(value1) - ord('a')] = value2
        if not value1.islower() and value2.islower():
            if not root2.islower() and root2 != value1:
                return []
            varsRoot[ord(value2) - ord('a')] = value1
    return varsRoot


def reproduce(varsRoot: list, A: list, B: list, ele1: list, ele2: list) -> list:
    updated_ele1 = clauseCopy(ele1)
    for k in range(len(updated_ele1[2])):
        if updated_ele1[2][k].islower():
            updated_ele1[2][k] = varsRoot[ord(updated_ele1[2][k]) - ord('a')]

    updated_ele2 = clauseCopy(ele2)
    for k in range(len(updated_ele2[2])):
        if updated_ele2[2][k].islower():
            updated_ele2[2][k] = varsRoot[ord(updated_ele2[2][k]) - ord('a')]

    res = []
    for i in range(len(A)):
        updatedAClause = clauseCopy(A[i])
        for k in range(len(updatedAClause[2])):
            if updatedAClause[2][k].islower():
                updatedAClause[2][k] = varsRoot[ord(
                    updatedAClause[2][k]) - ord('a')]
        if updatedAClause != updated_ele1 and updatedAClause != updated_ele2:
            res.append(updatedAClause.copy())

    for j in range(len(B)):
        updatedBClause = clauseCopy(B[j])
        for k in range(len(updatedBClause[2])):
            if updatedBClause[2][k].islower():
                updatedBClause[2][k] = varsRoot[ord(
                    updatedBClause[2][k]) - ord('a')]
        if updatedBClause != updated_ele1 and updatedBClause != updated_ele2:
            res.append(updatedBClause.copy())
    return res


def subsumedBy(clause: list, clausesList: list) -> bool:
    for clausesSet in clausesList:
        for clauses in clausesSet:
            flag = True
            for cl in clauses:
                if cl not in clause:
                    flag = False
                    break
            if flag:
                return True
    return False


def main():
    # file = open("hw3_10_examples/test_case_10/input.txt", "r")
    file = open("input.txt", "r")
# first line
    line = file.readline()
    line = line.strip()
    query = line
# second line
    line = file.readline()
    line = line.strip()
    k = int(line)
# fellowing lines
    sentences = []
    for _ in range(k):
        line = file.readline()
        line = line.strip()
        sentences.append(line)
    # print(query)
    # print(sentences)
    for sentence in sentences:
        convertToCNF(sentence)

    f = open("output.txt", "w")
    if not isValidKB():
        f.write("FALSE")
        print("FALSE")

    else:
        if resolution(query):
            f.write("FALSE")
            print("FALSE")
        else:
            f.write("TRUE")
            print("TRUE")
    f.close()


if __name__ == "__main__":
    main()
