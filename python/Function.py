from random import randint as rnd

# list1 = []
# for i in range(5):
#     list1.append(rnd(0,3))
# print(list1)

def generate_random_list(M,N):
    return [rnd(0,M) for i in range(N)]

list1 = generate_random_list(M = 10, N = 10)
list2 = generate_random_list(M = 3, N = 20)
list3 = generate_random_list(M = 10, N = 100)

print("list_1 : ",list1)
print("list_2 : ",list2)
print("list_3 : ",list3)

