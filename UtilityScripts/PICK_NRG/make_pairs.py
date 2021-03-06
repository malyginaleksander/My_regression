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
                elif len(list1) < len(list2):
                    list1.append(random.choice(list1))
                    tup = (list1[i], list2[i])
                continue

            merged_list.append(tup)
            break
    return merged_list


electric_enrollment = ['el_1','el_2','el_3','el_4']
gas_enrollment = ['gas_1', 'gas_2', 'gas_3', 'gas_4', 'gas_5']
merged_list = merge_list(electric_enrollment, gas_enrollment)
for i in merged_list:
    print(i[0], i[1])