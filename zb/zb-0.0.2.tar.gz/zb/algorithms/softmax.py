# -*- coding: utf-8 -*-

from sklearn import model_selection
from sklearn import metrics
import tensorflow as tf
import numpy as np
from tensorflow.contrib.learn.python.learn.estimators.estimator import SKCompat
learn = tf.contrib.learn


# 加载测试数据
def load_datas():

    from sklearn import datasets
    iris = datasets.load_iris()
    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=0)

    x_train, x_test = map(np.float32, [x_train, x_test])

    return x_train, x_test, y_train, y_test


def softmax_in_tf(features, target, classes=3):
    target = tf.one_hot(target, classes, 1, 0)

    # 计算预测值及损失函数。
    logits = tf.contrib.layers.fully_connected(features, 3, tf.nn.softmax)
    loss = tf.losses.softmax_cross_entropy(target, logits)

    # 创建优化步骤。
    train_op = tf.contrib.layers.optimize_loss(
        loss,
        tf.contrib.framework.get_global_step(),
        optimizer='Adam',
        learning_rate=0.01)
    return tf.arg_max(logits, 1), loss, train_op


def main(x_train, y_train, x_test, y_test, model_dir):

    classifier = SKCompat(learn.Estimator(model_fn=softmax_in_tf, model_dir=model_dir))
    classifier.fit(x_train, y_train, steps=800)

    y_predicted = [i for i in classifier.predict(x_test)]
    score = metrics.accuracy_score(y_test, y_predicted)
    print('Accuracy: %.2f%%' % (score * 100))


if __name__ == "__main__":
    x_train, x_test, y_train, y_test = load_datas()
    main(x_train, y_train, x_test, y_test, model_dir='Models/softmax')
