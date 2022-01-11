import numpy as np
import matplotlib.pyplot as plt
import random
import math

'''
https://zhuanlan.zhihu.com/p/62238520
'''
# 1.产生数据
SIZE = 200
# 产生数据。np.linspace 返回一个一维数组，SIZE指定数组长度。
# 数组最小值是0，最大值是10。所有元素间隔相等。
X = np.linspace(0, 10, SIZE)
Y = 3 * X + 10

# 让散点图的数据更加随机并且添加一些噪声。
random_x = []
random_y = []
# 添加直线随机噪声
for i in range(SIZE):
    random_x.append(X[i] + random.uniform(-0.5, 0.5))
    random_y.append(Y[i] + random.uniform(-0.5, 0.5))
# 添加随机噪声
print(random_x)
print(random_y)
for i in range(SIZE):
    random_x.append(random.uniform(0,10))  #0-10之间的随机数
    random_y.append(random.uniform(20,40))  #20-40之间的随机数

#最终生成的数据
RANDOM_X = np.array(random_x) # 散点图的横轴。
RANDOM_Y = np.array(random_y) # 散点图的纵轴。



# 使用RANSAC算法估算模型
# 迭代最大次数，每次得到更好的估计会优化iters的数值
iters = 100000
# 数据和模型之间可接受的差值
sigma = 0.25
# 最好模型的参数估计和内点数目
best_a = 0
best_b = 0
pretotal = 0
# 希望的得到正确模型的概率
P = 0.99
for i in range(iters):
    # 随机在数据中红选出两个点去求解模型
    sample_index = random.sample(range(SIZE),2) #随机取两个点，0-SIZE之间
    x_1 = RANDOM_X[sample_index[0]]
    x_2 = RANDOM_X[sample_index[1]]
    y_1 = RANDOM_Y[sample_index[0]]
    y_2 = RANDOM_Y[sample_index[1]]

    # y = ax + b 求解出a，b
    a = (y_2 - y_1) / (x_2 - x_1)
    b = y_1 - a * x_1

    # 算出内点数目
    total_inlier = 0
    for index in range(SIZE):
        y_estimate = a * RANDOM_X[index] + b
        if abs(y_estimate - RANDOM_Y[index]) < sigma:  #abs(x)返回x的绝对值
            total_inlier = total_inlier + 1

    # 判断当前的模型是否比之前估算的模型好
    if total_inlier > pretotal:
        iters = math.log(1 - P) / math.log(1 - pow(total_inlier / SIZE, 2))  #pow(x,y)x的y次方
        pretotal = total_inlier
        best_a = a
        best_b = b

    # 判断是否当前模型已经符合超过一半的点
    if total_inlier > SIZE/2:
        break

# 用我们得到的最佳估计画图
Y = best_a * RANDOM_X + best_b


fig = plt.figure()
# 画图区域分成1行1列。选择第一块区域。
ax1 = fig.add_subplot(1,1, 1)
# 标题
ax1.set_title("RANSAC")
# 画散点图。
ax1.scatter(RANDOM_X, RANDOM_Y)
# 横轴名称。
ax1.set_xlabel("x")
# 纵轴名称。
ax1.set_ylabel("y")

# 直线图
ax1.plot(RANDOM_X, Y,'r+')
text = "best_a = " + str(best_a) + "\nbest_b = " + str(best_b)
plt.text(5,10, text,
         fontdict={'size': 8, 'color': 'r'})
plt.show()