import os
import numpy as np
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from sd_maskrcnn.config import MaskConfig
from mrcnn import model as modellib
from autolab_core import YamlConfig
import cv2
from matplotlib import pyplot as plt
from math import sqrt


def camtest(config):
	#image = data.camera()
	image = cv2.resize(cv2.imread('/home/sean_hastings/sd-maskrcnn/datasets/wisdom/wisdom-real/high-res/depth_ims/image_000000.png'), dsize=(512, 512))
	print(image.shape)

	image_shape = config['model']['settings']['image_shape']
	config['model']['settings']['image_min_dim'] = min(image_shape)
	config['model']['settings']['image_max_dim'] = max(image_shape)
	config['model']['settings']['gpu_count'] = 1
	config['model']['settings']['images_per_gpu'] = 1
	inference_config = MaskConfig(config['model']['settings'])

	model_dir, _ = os.path.split(config['model']['path'])
	model = modellib.MaskRCNN(mode=config['model']['mode'], config=inference_config, model_dir=model_dir)

	# Load trained weights
	print("Loading weights from ", config['model']['path'])
	model.load_weights('/home/sean_hastings/sd-maskrcnn/' + config['model']['path'], by_name=True)
	
	result = model.detect([image], verbose=0)[0]
	masks = result['masks']

	plt.subplot(int(sqrt(masks.shape[2]))+1, int(sqrt(masks.shape[2]))+1, 1)
	plt.imshow(image)
	
	for i in range(masks.shape[2]):
		plt.subplot(int(sqrt(masks.shape[2]))+1, int(sqrt(masks.shape[2]))+1, i+2)
		plt.imshow(masks[:,:,i])

	plt.show()


if __name__ == '__main__':
	config = YamlConfig('/home/sean_hastings/sd-maskrcnn/cfg/benchmark.yaml')
	
	tf_config = tf.ConfigProto()
	tf_config.gpu_options.allow_growth = True
	with tf.Session(config=tf_config) as sess:
		set_session(sess)
		camtest(config)

