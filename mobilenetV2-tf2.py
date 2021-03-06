import math

import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.layers import (Activation, Add, BatchNormalization,
                                     Conv2D, Dense, DepthwiseConv2D, Dropout,
                                     GlobalAveragePooling2D,
                                     GlobalMaxPooling2D, Input, MaxPooling2D,
                                     ZeroPadding2D)
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import get_file

BASE_WEIGHT_PATH = ('https://github.com/JonathanCMitchell/mobilenet_v2_keras/'
                    'releases/download/v1.1/')

tf.keras.Model
# relu6！
def relu6(x):
    return K.relu(x, max_value=6)

# 用于计算padding的大小，用于ZeroPadding2D(3*3卷积后，长和宽变为1/2)
# 代码的语法看懂了，为啥这样写还不是很懂
def correct_pad(inputs, kernel_size):
    """
    Returns a tuple for zero-padding for 2D convolution with downsampling.
    # Arguments
        input_size: An integer or tuple/list of 2 integers.
        kernel_size: An integer or tuple/list of 2 integers.
    # Returns
        A tuple.
    """
    img_dim = 1
    input_size = K.int_shape(inputs)[img_dim:(img_dim + 2)] # (224, 224)
    # print(K.int_shape(inputs)) # (None, 224, 224, 3)
    # 判断kernel_size是不是int类型
    if isinstance(kernel_size, int):
        kernel_size = (kernel_size, kernel_size) # (3,3)

    if input_size[0] is None:
        adjust = (1, 1)
    else:
        adjust = (1 - input_size[0] % 2, 1 - input_size[1] % 2)

    correct = (kernel_size[0] // 2, kernel_size[1] // 2)
    # print(correct[0], adjust[0]) # 1,1

    return ((correct[0] - adjust[0], correct[0]),
            (correct[1] - adjust[1], correct[1]))

# 使其结果可以被8整除，因为使用到了膨胀系数α
# 代码的语法看懂了，为啥这样写还不是很懂
def _make_divisible(v, divisor, min_value=None):
    if min_value is None:
        min_value = divisor
    new_v = max(min_value, int(v + divisor / 2) // divisor * divisor) # 32, 8
    if new_v < 0.9 * v:
        new_v += divisor
    return new_v


# alpha=1.0表示忽略这个参数，alpha表示对MobileNet的扩张
def MobileNetV2(input_shape=[224,224,3],
                alpha=1.0,
                include_top=True,
                classes=1000):

    rows = input_shape[0]

    img_input = Input(shape=input_shape)

    # stem部分
    # 224,224,3 -> 112,112,32
    first_block_filters = _make_divisible(32 * alpha, 8)
    # ZeroPadding2D目的使经过Conv2D后正好变为1/2
    # print(correct_pad(img_input, 3)) # ((0, 1), (0, 1)) 上下，左右

    # 225,225,3, if no padding, 224-->111
    x = ZeroPadding2D(padding=correct_pad(img_input, 3),
                             name='Conv1_pad')(img_input)
    # 112,112,32
    x = Conv2D(first_block_filters,
                      kernel_size=3,
                      strides=(2, 2),
                      padding='valid',
                      use_bias=False,
                      name='Conv1')(x)
    x = BatchNormalization(epsilon=1e-3,
                                  momentum=0.999,
                                  name='bn_Conv1')(x)
    x = Activation(relu6, name='Conv1_relu')(x)

    # 112,112,32 -> 112,112,16
    # 残差结构块
    x = _inverted_res_block(x, filters=16, alpha=alpha, stride=1,
                            expansion=1, block_id=0)

    # 112,112,16 -> 56,56,24
    # 1. 112,112,16 -> 112,112,96(16*6)
    # 2. 112,112,96 -> 113,113,96
    # 3. 113,113,96 -> 56,56,96
    # 4. 56,56,96 -> 56,56,24
    x = _inverted_res_block(x, filters=24, alpha=alpha, stride=2,
                            expansion=6, block_id=1)
    # 56,56,24 -> 56,56,24
    # especially, block_2_add
    x = _inverted_res_block(x, filters=24, alpha=alpha, stride=1,
                            expansion=6, block_id=2)

    # 56,56,24 -> 28,28,32
    x = _inverted_res_block(x, filters=32, alpha=alpha, stride=2,
                            expansion=6, block_id=3)
    x = _inverted_res_block(x, filters=32, alpha=alpha, stride=1,
                            expansion=6, block_id=4)
    x = _inverted_res_block(x, filters=32, alpha=alpha, stride=1,
                            expansion=6, block_id=5)

    # 28,28,32 -> 14,14,64
    x = _inverted_res_block(x, filters=64, alpha=alpha, stride=2,
                            expansion=6, block_id=6)
    x = _inverted_res_block(x, filters=64, alpha=alpha, stride=1,
                            expansion=6, block_id=7)
    x = _inverted_res_block(x, filters=64, alpha=alpha, stride=1,
                            expansion=6, block_id=8)
    x = _inverted_res_block(x, filters=64, alpha=alpha, stride=1,
                            expansion=6, block_id=9)

    # 14,14,64 -> 14,14,96
    x = _inverted_res_block(x, filters=96, alpha=alpha, stride=1,
                            expansion=6, block_id=10)
    x = _inverted_res_block(x, filters=96, alpha=alpha, stride=1,
                            expansion=6, block_id=11)
    x = _inverted_res_block(x, filters=96, alpha=alpha, stride=1,
                            expansion=6, block_id=12)
    # 14,14,96 -> 7,7,160
    x = _inverted_res_block(x, filters=160, alpha=alpha, stride=2,
                            expansion=6, block_id=13)
    x = _inverted_res_block(x, filters=160, alpha=alpha, stride=1,
                            expansion=6, block_id=14)
    x = _inverted_res_block(x, filters=160, alpha=alpha, stride=1,
                            expansion=6, block_id=15)

    # 7,7,160 -> 7,7,320
    x = _inverted_res_block(x, filters=320, alpha=alpha, stride=1,
                            expansion=6, block_id=16)

    if alpha > 1.0:
        last_block_filters = _make_divisible(1280 * alpha, 8)
    else:
        last_block_filters = 1280

    # 7,7,320 -> 7,7,1280
    x = Conv2D(last_block_filters,
                      kernel_size=1,
                      use_bias=False,
                      name='Conv_1')(x)
    x = BatchNormalization(epsilon=1e-3,
                                  momentum=0.999,
                                  name='Conv_1_bn')(x)
    x = Activation(relu6, name='out_relu')(x)

    # 7,7,1280 -> 1,1,1280，平均池化
    x = GlobalAveragePooling2D()(x)
    # 全连接层
    x = Dense(classes, activation='softmax',
                        use_bias=True, name='Logits')(x)

    inputs = img_input

    model = Model(inputs, x, name='mobilenetv2_%0.2f_%s' % (alpha, rows))

    return model


def _inverted_res_block(inputs, expansion, stride, alpha, filters, block_id):
    in_channels = K.int_shape(inputs)[-1]
    pointwise_conv_filters = int(filters * alpha)
    pointwise_filters = _make_divisible(pointwise_conv_filters, 8)
    x = inputs
    prefix = 'block_{}_'.format(block_id)

    # part1 数据扩张，1*1卷积升维，block_id = 0 不执行
    if block_id:
        # Expand
        x = Conv2D(expansion * in_channels,
                          kernel_size=1,
                          padding='same',
                          use_bias=False,
                          activation=None,
                          name=prefix + 'expand')(x)
        x = BatchNormalization(epsilon=1e-3,
                                      momentum=0.999,
                                      name=prefix + 'expand_BN')(x)
        x = Activation(relu6, name=prefix + 'expand_relu')(x)
    else:
        prefix = 'expanded_conv_'

    if stride == 2:
        x = ZeroPadding2D(padding=correct_pad(x, 3),
                                 name=prefix + 'pad')(x)

    # part2 可分离卷积，3*3卷积
    x = DepthwiseConv2D(kernel_size=3,
                               strides=stride,
                               activation=None,
                               use_bias=False,
                               padding='same' if stride == 1 else 'valid',
                               name=prefix + 'depthwise')(x)
    x = BatchNormalization(epsilon=1e-3,
                                  momentum=0.999,
                                  name=prefix + 'depthwise_BN')(x)

    x = Activation(relu6, name=prefix + 'depthwise_relu')(x)

    # part3压缩特征，而且不使用relu函数，保证特征不被破坏
    x = Conv2D(pointwise_filters,
                      kernel_size=1,
                      padding='same',
                      use_bias=False,
                      activation=None,
                      name=prefix + 'project')(x)

    x = BatchNormalization(epsilon=1e-3,
                                  momentum=0.999,
                                  name=prefix + 'project_BN')(x)

    # 残差相加
    if in_channels == pointwise_filters and stride == 1:
        return Add(name=prefix + 'add')([inputs, x])
    return x

def preprocess_input(x):
    x /= 255.
    x -= 0.5
    x *= 2.
    return x

if __name__ == '__main__':
    model = MobileNetV2(input_shape=(224, 224, 3))
    model.summary()

    model_name = ('mobilenet_v2_weights_tf_dim_ordering_tf_kernels_' + "1.0" + '_' + '224' + '.h5')
    weight_path = BASE_WEIGHT_PATH + model_name
    weights_path = get_file(model_name, weight_path, cache_subdir='models')
    model.load_weights(weights_path)

    img_path = 'elephant.jpg'
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    print('Input image shape:', x.shape)

    preds = model.predict(x)
    print(np.argmax(preds))
    print('Predicted:', decode_predictions(preds, 1))
