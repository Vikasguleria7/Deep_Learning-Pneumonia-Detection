# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:53:06 2022

@author: vikas
"""

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt 

# re-size all the images to this 
Image_Size = [224,224]

train_path = 'train'
valid_path = 'test'

# add preprocessing layer to the front of VGG
vgg = VGG16(input_shape=Image_Size + [3], weights='imagenet', include_top=False)

#don't train existing weights
for layer in vgg.layers:
    layer.trainable = False
    
# useful for getting number of classes
folders = glob('C:/Users/vikas/chest_xray/test/*')

# our layers - can add more if needed
x = Flatten()(vgg.output)

prediction = Dense(len(folders), activation= 'softmax')(x)

#create a model object

model = Model(inputs=vgg.input, outputs=prediction)

#view the structure of the model 
model.summary()

#tell the model what cost and optimization method to use
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
    )

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True
    )
test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory('C:/Users/vikas/chest_xray/train',
                                                 target_size = (224,224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical'
    )

test_set = train_datagen.flow_from_directory('C:/Users/vikas/chest_xray/test',
                                                 target_size = (224,224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical'
    )

# fit the model
r = model.fit_generator(
    training_set,
    validation_data=test_set,
    epochs=5,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
    )

# loss
plt.plot(r.history['loss'], label='train_loss')
plt.plot(r.history['val_loss'], label='val_loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# accuracies
plt.plot(r.history['acc'], label='train_acc')
plt.plot(r.history['val_acc'],label = 'val_acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')


import tensorflow as tf

from keras.model import load_model

model.save('model_vgg16.h5')

