import random


def merge_list(list1, list2):
    merged_list = []
    for i in range(max((len(list1), (len(list2))))):
        while True:
            try:
                tup = (list1[i], list2[i])
            except IndexError:
                if len(list1) > len(list2):
                    list2.append('')
                    tup = (list1[i], list2[i])
                if len(list1) < len(list2):
                    list1.append(random.choice(list1))
                    print(list1)
                    tup = (list1[i], list2[i])
                continue

            merged_list.append(tup)
            break
    print(list1)

    return merged_list

#
# electric_enrollment = [1,2,]
# gas_enrollment = ['a', 'b', 'c']
# merged_list = merge_list(electric_enrollment, gas_enrollment)
# for i in merged_list:
#     print(i[0], i[1])
