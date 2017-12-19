from keras.datasets import imdb

# 读取网络电影数据库，25000个训练样本，25000个测试样本
# num_words=10000指的是保留在训练集中最频繁出现的前10000个词
# 标签中0代表消极、1代表积极
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

# 查看训练样本
print(train_data[0])
print(train_labels[0])

# 每个单词的下标都低于10000
print(max([max(sequence) for sequence in train_data]))
print(min([min(sequence) for sequence in train_data]))

# 解码整数序列为句子
# word_index是单词->下标的字典
word_index = imdb.get_word_index()
# 反转word_index字典
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
# 我们解码评论，下标从3开始，因为0->'padding',1->'start of sequence',2->'unknown'(其实是从4开始，因为训练集中的下标是从1开始的，1、2、3是无效的)
decode_review = ' '.join(reverse_word_index.get(i - 3, '?') for i in train_data[0])
print(decode_review)

# 把整数序列编码成二元矩阵
import numpy as np


def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


# 向量化的训练数据
x_train = vectorize_sequences(train_data)
# 向量化的测试数据
x_test = vectorize_sequences(test_data)

# 查看一个向量化后的样本
print(x_train[0])

'''
l = []
for i in train_data[0]:
    if i not in l:
        l.append(i)
print(len(l))
'''

# 向量化标签
y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')

print(train_labels.shape)
print(y_train.shape)

# 模型定义
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics

model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

small_model = models.Sequential()
small_model.add(layers.Dense(4, activation='relu', input_shape=(10000,)))
small_model.add(layers.Dense(4, activation='relu'))
small_model.add(layers.Dense(1, activation='sigmoid'))

big_model = models.Sequential()
big_model.add(layers.Dense(512, activation='relu', input_shape=(10000,)))
big_model.add(layers.Dense(512, activation='relu'))
big_model.add(layers.Dense(1, activation='sigmoid'))

# 模型编译
# model.compile(optimizer='rmsprop',
#               loss='binary_crossentropy',
#               metrics=['accuracy'])
# 另一种方式
model.compile(optimizer=optimizers.RMSprop(lr=0.001),
              loss=losses.binary_crossentropy,
              metrics=[metrics.binary_accuracy])
small_model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                    loss=losses.binary_crossentropy,
                    metrics=[metrics.binary_accuracy])
big_model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                  loss=losses.binary_crossentropy,
                  metrics=[metrics.binary_accuracy])

# 设置验证集
x_val = x_train[:10000]
partial_x_train = x_train[10000:]

y_val = y_train[:10000]
partial_y_train = y_train[10000:]

# 训练模型
history = model.fit(partial_x_train, partial_y_train, epochs=20, batch_size=512, validation_data=(x_val, y_val))
small_history = small_model.fit(partial_x_train, partial_y_train, epochs=20, batch_size=512,
                                validation_data=(x_val, y_val))
big_history = big_model.fit(partial_x_train, partial_y_train, epochs=20, batch_size=512, validation_data=(x_val, y_val))

# 画出训练集和验证集的目标函数值
import matplotlib.pyplot as plt

loss = history.history['val_loss']
small_loss = small_history.history['val_loss']
big_loss = big_history.history['val_loss']

epochs = range(1, len(loss) + 1)

plt.plot(epochs, loss, 'ro', label='Original model')
plt.plot(epochs, small_loss, 'bo', label='Smaller model')
# plt.plot(epochs, big_loss, 'bo', label='Bigger model')
plt.title('Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Validation loss')
plt.legend()

plt.show()
