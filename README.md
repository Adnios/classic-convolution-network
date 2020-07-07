## 经典卷积分类网络在 Keras 当中的实现
---

### 目录
1. [所需环境 Environment](#所需环境)
2. [仓库内容 WhatsIn](#仓库内容)
3. [使用方法 Usage](#使用方法)
4. [参考资料 Reference](#Reference)

### 所需环境
1. tensorflow-gpu==1.13.1
2. keras==2.1.5

### 仓库内容：
- VGG16 模型
- MobileNet 模型
    * model summary

        ```
        _________________________________________________________________
        Layer (type)                 Output Shape              Param #
        =================================================================
        input_1 (InputLayer)         (None, 224, 224, 3)       0
        _________________________________________________________________
        conv1 (Conv2D)               (None, 112, 112, 32)      864
        _________________________________________________________________
        conv1_bn (BatchNormalization (None, 112, 112, 32)      128
        _________________________________________________________________
        conv1_relu (Activation)      (None, 112, 112, 32)      0
        _________________________________________________________________
        conv_dw_1 (DepthwiseConv2D)  (None, 112, 112, 32)      288
        _________________________________________________________________
        conv_dw_1_bn (BatchNormaliza (None, 112, 112, 32)      128
        _________________________________________________________________
        conv_dw_1_relu (Activation)  (None, 112, 112, 32)      0
        _________________________________________________________________
        conv_pw_1 (Conv2D)           (None, 112, 112, 64)      2048
        _________________________________________________________________
        conv_pw_1_bn (BatchNormaliza (None, 112, 112, 64)      256
        _________________________________________________________________
        conv_pw_1_relu (Activation)  (None, 112, 112, 64)      0
        _________________________________________________________________
        conv_dw_2 (DepthwiseConv2D)  (None, 56, 56, 64)        576
        _________________________________________________________________
        conv_dw_2_bn (BatchNormaliza (None, 56, 56, 64)        256
        _________________________________________________________________
        conv_dw_2_relu (Activation)  (None, 56, 56, 64)        0
        _________________________________________________________________
        conv_pw_2 (Conv2D)           (None, 56, 56, 128)       8192
        _________________________________________________________________
        conv_pw_2_bn (BatchNormaliza (None, 56, 56, 128)       512
        _________________________________________________________________
        conv_pw_2_relu (Activation)  (None, 56, 56, 128)       0
        _________________________________________________________________
        conv_dw_3 (DepthwiseConv2D)  (None, 56, 56, 128)       1152
        _________________________________________________________________
        conv_dw_3_bn (BatchNormaliza (None, 56, 56, 128)       512
        _________________________________________________________________
        conv_dw_3_relu (Activation)  (None, 56, 56, 128)       0
        _________________________________________________________________
        conv_pw_3 (Conv2D)           (None, 56, 56, 128)       16384
        _________________________________________________________________
        conv_pw_3_bn (BatchNormaliza (None, 56, 56, 128)       512
        _________________________________________________________________
        conv_pw_3_relu (Activation)  (None, 56, 56, 128)       0
        _________________________________________________________________
        conv_dw_4 (DepthwiseConv2D)  (None, 28, 28, 128)       1152
        _________________________________________________________________
        conv_dw_4_bn (BatchNormaliza (None, 28, 28, 128)       512
        _________________________________________________________________
        conv_dw_4_relu (Activation)  (None, 28, 28, 128)       0
        _________________________________________________________________
        conv_pw_4 (Conv2D)           (None, 28, 28, 256)       32768
        _________________________________________________________________
        conv_pw_4_bn (BatchNormaliza (None, 28, 28, 256)       1024
        _________________________________________________________________
        conv_pw_4_relu (Activation)  (None, 28, 28, 256)       0
        _________________________________________________________________
        conv_dw_5 (DepthwiseConv2D)  (None, 28, 28, 256)       2304
        _________________________________________________________________
        conv_dw_5_bn (BatchNormaliza (None, 28, 28, 256)       1024
        _________________________________________________________________
        conv_dw_5_relu (Activation)  (None, 28, 28, 256)       0
        _________________________________________________________________
        conv_pw_5 (Conv2D)           (None, 28, 28, 256)       65536
        _________________________________________________________________
        conv_pw_5_bn (BatchNormaliza (None, 28, 28, 256)       1024
        _________________________________________________________________
        conv_pw_5_relu (Activation)  (None, 28, 28, 256)       0
        _________________________________________________________________
        conv_dw_6 (DepthwiseConv2D)  (None, 14, 14, 256)       2304
        _________________________________________________________________
        conv_dw_6_bn (BatchNormaliza (None, 14, 14, 256)       1024
        _________________________________________________________________
        conv_dw_6_relu (Activation)  (None, 14, 14, 256)       0
        _________________________________________________________________
        conv_pw_6 (Conv2D)           (None, 14, 14, 512)       131072
        _________________________________________________________________
        conv_pw_6_bn (BatchNormaliza (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_pw_6_relu (Activation)  (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_dw_7 (DepthwiseConv2D)  (None, 14, 14, 512)       4608
        _________________________________________________________________
        conv_dw_7_bn (BatchNormaliza (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_dw_7_relu (Activation)  (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_pw_7 (Conv2D)           (None, 14, 14, 512)       262144
        _________________________________________________________________
        conv_pw_7_bn (BatchNormaliza (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_pw_7_relu (Activation)  (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_dw_8 (DepthwiseConv2D)  (None, 14, 14, 512)       4608
        _________________________________________________________________
        conv_dw_8_bn (BatchNormaliza (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_dw_8_relu (Activation)  (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_pw_8 (Conv2D)           (None, 14, 14, 512)       262144
        _________________________________________________________________
        conv_pw_8_bn (BatchNormaliza (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_pw_8_relu (Activation)  (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_dw_9 (DepthwiseConv2D)  (None, 14, 14, 512)       4608
        _________________________________________________________________
        conv_dw_9_bn (BatchNormaliza (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_dw_9_relu (Activation)  (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_pw_9 (Conv2D)           (None, 14, 14, 512)       262144
        _________________________________________________________________
        conv_pw_9_bn (BatchNormaliza (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_pw_9_relu (Activation)  (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_dw_10 (DepthwiseConv2D) (None, 14, 14, 512)       4608
        _________________________________________________________________
        conv_dw_10_bn (BatchNormaliz (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_dw_10_relu (Activation) (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_pw_10 (Conv2D)          (None, 14, 14, 512)       262144
        _________________________________________________________________
        conv_pw_10_bn (BatchNormaliz (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_pw_10_relu (Activation) (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_dw_11 (DepthwiseConv2D) (None, 14, 14, 512)       4608
        _________________________________________________________________
        conv_dw_11_bn (BatchNormaliz (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_dw_11_relu (Activation) (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_pw_11 (Conv2D)          (None, 14, 14, 512)       262144
        _________________________________________________________________
        conv_pw_11_bn (BatchNormaliz (None, 14, 14, 512)       2048
        _________________________________________________________________
        conv_pw_11_relu (Activation) (None, 14, 14, 512)       0
        _________________________________________________________________
        conv_dw_12 (DepthwiseConv2D) (None, 7, 7, 512)         4608
        _________________________________________________________________
        conv_dw_12_bn (BatchNormaliz (None, 7, 7, 512)         2048
        _________________________________________________________________
        conv_dw_12_relu (Activation) (None, 7, 7, 512)         0
        _________________________________________________________________
        conv_pw_12 (Conv2D)          (None, 7, 7, 1024)        524288
        _________________________________________________________________
        conv_pw_12_bn (BatchNormaliz (None, 7, 7, 1024)        4096
        _________________________________________________________________
        conv_pw_12_relu (Activation) (None, 7, 7, 1024)        0
        _________________________________________________________________
        conv_dw_13 (DepthwiseConv2D) (None, 7, 7, 1024)        9216
        _________________________________________________________________
        conv_dw_13_bn (BatchNormaliz (None, 7, 7, 1024)        4096
        _________________________________________________________________
        conv_dw_13_relu (Activation) (None, 7, 7, 1024)        0
        _________________________________________________________________
        conv_pw_13 (Conv2D)          (None, 7, 7, 1024)        1048576
        _________________________________________________________________
        conv_pw_13_bn (BatchNormaliz (None, 7, 7, 1024)        4096
        _________________________________________________________________
        conv_pw_13_relu (Activation) (None, 7, 7, 1024)        0
        _________________________________________________________________
        global_average_pooling2d_1 ( (None, 1024)              0
        _________________________________________________________________
        reshape_1 (Reshape)          (None, 1, 1, 1024)        0
        _________________________________________________________________
        dropout (Dropout)            (None, 1, 1, 1024)        0
        _________________________________________________________________
        conv_preds (Conv2D)          (None, 1, 1, 1000)        1025000
        _________________________________________________________________
        act_softmax (Activation)     (None, 1, 1, 1000)        0
        _________________________________________________________________
        reshape_2 (Reshape)          (None, 1000)              0
        =================================================================
        Total params: 4,253,864
        Trainable params: 4,231,976
        Non-trainable params: 21,888
        _________________________________________________________________
        ```

- MobileNetV2 模型
- MobileNetV3 模型
- Resnet50 模型
- InceptionV3 模型
- Inception ResnetV2 模型
- Xception 模型

### 问题

- efficientNet 网络

### 使用方法

下来过来直接运行即可，会自动下载模型，如果连接失败，可以多试几次。

![原图 Before](./elephant.jpg)

### Reference
- [https://github.com/fchollet/deep-learning-models](https://github.com/fchollet/deep-learning-models)
- [https://github.com/JonathanCMitchell/mobilenet_v2_keras](https://github.com/JonathanCMitchell/mobilenet_v2_keras)
