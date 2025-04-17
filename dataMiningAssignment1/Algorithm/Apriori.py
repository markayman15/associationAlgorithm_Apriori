#import data_transformation as dt
import numpy as np
import itertools
#import pandas as pd

#transformed_data, unique_itemsets, num_records = dt.transform_data('D:\dataMiningAssignment1\Algorithm\Groceries data.csv')

global data_matrix

def differ_by_one_str(list1, list2):
    if len(list1) != len(list2):
        return 0
    diff_count = sum(1 for i in list1 if i not in list2)
    return diff_count


def FP_itemsets(transformed_data, unique_itemsets, num_records, support):
    data_matrix = np.array([items for items in transformed_data['item_set']])

    unique_itemsets = unique_itemsets[unique_itemsets >= support]

    FP_result = {}
    candidate_itemsets = []
    for key, value in unique_itemsets.items():
        temp = [key]
        candidate_itemsets.append(temp)
        FP_result[frozenset(temp)] = value

    itemset_size = 2
    temp_results = {}
    candidate_itemsets = sorted(candidate_itemsets)

    while len(candidate_itemsets) != 0:

        for i in range(len(candidate_itemsets) - 1):
            part1 = candidate_itemsets[i]
            new_itemsets = []
            for j in range(i + 1, len(candidate_itemsets)):
                part2 = candidate_itemsets[j]


                if len(part2) > 1 and len(part2) > 1 and differ_by_one_str(part1,part2) != 1:
                    break

                new_itemsets.append(set(part1) | set(part2))

            for item in new_itemsets:
                temp_results[frozenset(list(item))] = sum(1 for rec in data_matrix if item.issubset(rec))

            temp_results = {k: v for k, v in temp_results.items() if v >= support and len(k) == itemset_size}
            FP_result.update(temp_results)

        candidate_itemsets = [list(key) for key in temp_results.keys()]
        temp_results = {}
        itemset_size += 1

    return FP_result

def Apriori(transformed_data, unique_itemsets, support):
    data_matrix = np.array([items for items in transformed_data['item_set']])
    unique_itemsets = unique_itemsets[unique_itemsets >= support]

    result = {}
    candidate_itemsets = []
    for key, value in unique_itemsets.items():
        temp = [key]
        candidate_itemsets.append(temp)
        result[frozenset(temp)] = value

    candidate_itemsets = sorted(candidate_itemsets)
    itemset_size = 2

    while len(candidate_itemsets) != 0:
        Combinations = itertools.combinations(candidate_itemsets,2)
        print(Combinations)
        temp_results = {}
        for comb in Combinations:
            if len(comb[0]) > 1 and comb[0][:-1] != comb[1][:-1]:
                continue

            newSet = set(comb[0]) | set(comb[1])
            temp_results[frozenset(list(newSet))] = sum(1 for item in data_matrix if newSet.issubset(item))

        temp_results = {k: v for k, v in temp_results.items() if v >= support and len(k) == itemset_size}
        result.update(temp_results)

        candidate_itemsets = [sorted(list(key)) for key in temp_results.keys()]
        itemset_size += 1

    return result

#FP_itemsets(transformed_data, unique_itemsets, num_records,0.00000000000000000000000000000000000000000000000001)
def combination(Set, n, k):
    result = []

    def backtracking(Set, curr, comb):
        if len(comb) == k:
            result.append(comb.copy())
            return

        for i in range(curr, n):
            comb.append(Set[i])
            backtracking(Set,i+1, comb)
            comb.pop()

    backtracking(Set,0,[])
    return result

def assosiation_ruls(FP_result, condfidence_level):
    assosiation_result = {}

    for key, value in FP_result.items():
        if len(key) != 1:
            itemSet = list(key)
            size = len(itemSet)
            for i in range(1, size):
                #print(itemSet)
                temp_combinations = combination(itemSet, size, i)
                for comb in temp_combinations:
                    sup = FP_result[frozenset(comb)]

                    if value / sup >= condfidence_level:
                        remaining = [s for s in itemSet if s not in comb]
                        assosiation_result[str(comb) + ' => ' + str(remaining)] = value / sup
    return assosiation_result


