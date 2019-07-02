#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy
import cv2
from std_msgs.msg import String, Header
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import os
import numpy as np
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from sd_maskrcnn.config import MaskConfig
from mrcnn import model as modellib
from autolab_core import YamlConfig

class image_converter:

  def __init__(self, config, graph):
    self.config = config
    self.graph = graph

    self.mask_pub = rospy.Publisher("mask_topic",Image, queue_size=10)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("image_topic",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "rgb8")
    except CvBridgeError as e:
      print(e)
    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)
    np_image = np.asarray(cv_image)

    global model
    with self.graph.as_default():
      result = model.detect([np_image], verbose=0)[0]
      masks = result['masks'].astype(np.uint8)
      print(masks.shape)
   # masks = [masks[:,:,i:i+1] for i in range(masks.shape[2])]

    try:
      self.mask_pub.publish(self.bridge.cv2_to_imgmsg(masks))
    except CvBridgeError as e:
      print(e)



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

  global model
  model_dir, _ = os.path.split(config['model']['path'])
  model = modellib.MaskRCNN(mode=config['model']['mode'], config=inference_config, model_dir=model_dir)

  # Load trained weights
  print("Loading weights from ", config['model']['path'])
  model.load_weights('/home/sean_hastings/sd-maskrcnn/' + config['model']['path'], by_name=True)
	
  graph = tf.get_default_graph()

  result = model.detect([image], verbose=0)[0]
  masks = result['masks']
  print(masks.shape)

  return graph


def main(args):
  config = YamlConfig('/home/sean_hastings/sd-maskrcnn/cfg/benchmark.yaml')

  tf_config = tf.ConfigProto()
  tf_config.gpu_options.allow_growth = True
  with tf.Session(config=tf_config) as sess:
    set_session(sess)
    graph = camtest(config)

    ic = image_converter(config, graph)
    rospy.init_node('image_converter2', anonymous=True)
    try:
      rospy.spin()
    except KeyboardInterrupt:
      print("Shutting down")
    finally:
      cv2.destroyAllWindows()

if __name__ == '__main__':
  main(sys.argv)
