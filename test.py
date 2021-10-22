# sieve = ['True'] * 101
# for i in range(2,100):
#     if sieve[i]:
#         print(i)
#         for j in range(i*i,100,i):
#             sieve[j] = False
# x = (1,2,3)
# print(x)

# class3_grade = {'lilei':98,'hanmeimei':99}
# # d = dict(class3_grade)
# print(class3_grade)
# class3_grade['hanmeimei']=85
# print(class3_grade)
# class3_grade = [('l',98),('h',85)]
# d = dict(class3_grade)
# print(d)
# student1 = {'name':'lilei','chengji':'98','shiyanban':'true'}
# class1 = {
#     'lilei':{'chengji':'98','shiyanban':'true'},
#     'hanmeimei':{'chengji':'95','shiyanban':'false'},
# }
# print(class1['lilei'])
# print(class1['lilei']['chengji'])
# set1 = {1,2,4,5,8,5}
# set2 = set([1,2,4,1,2,8,5,5])
# print(set1)
# print(set2)
# set3 = {1,2,4,5,8}
# set4 = {1,2,3,5,9}
# Get1 = (set3 | set4)-(set3 & set4)
# Get2 = set3^set4
# print(Get1)
# print(Get2)
# i = 1
# while i<10:
#     i = i + 1
#     if i%2 > 0:
#         continue
#     print(i)
# a = range(1,100)
# for i in a:
#     print(i)



# dog_x = 0
# cat_x = 0
# def dog_move():
#     global dog_x
#     dog_x = dog_x + 10

# def cat_move():
#     global cat_x
#     cat_x = cat_x + 10

# user_input = input()


#                         format                      函数运用！


# if user_input == 'move':
#     print("dog:{0},cat:{1},".format(dog_x,cat_x))
#     dog_move()
#     cat_move()
#     print('dog:{0},cat:{1},'.format(dog_x,cat_x))

# for i in range(1,10):
#     for j in range(1,i+1):
#         print(f'{i}*{j} = {i*j}',end='\t')

#     print(end='\n')
# class Student():
#     def say_hi(self):
#         print('Hello!')

# lilei = Student()
# lilei.say_hi()

# class Student():
#     def __init__(self,user_input_name):
#         self.name = user_input_name

#     def say_hi(self):
#         print('Hello!I\'m {}.'.format(self.name))

# lilei = Student('lilei')
# lilei.say_hi()

# hanmeimei = Student('hanmeimei')
# hanmeimei.say_hi()
str = 'this is string example....wow!!!this is really string'
print (str.replace(' is ',' was '))
