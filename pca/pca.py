#!/usr/bin/env python
# coding=utf-8
from PIL import Image
import numpy as np
from pylab import *

dims = [1, 3, 5, 10, 15, 20, 25, 30, 35]


def pca_compress_matrix(matrix, dim):
  U,Sigma,VT = np.linalg.svd(matrix)
  # todo remove magic number
  S = np.zeros([1032, 1032])
  for i in range(dim):
    S[i][i] = Sigma[i]
  return np.int_(np.dot(np.dot(U,S),VT))


def pca_compress_img(img, dim):
  channelr, channelg, channelb = pca_compress_matrix(img[:,:,0], dim), pca_compress_matrix(img[:,:,1], dim), pca_compress_matrix(img[:,:,2], dim)
  return np.dstack([channelr, channelg, channelb])

im = np.array(Image.open("../data/image/avatar.jpeg"))

figure()
for i, dim in enumerate(dims):
  subplot(3,3,i+1)
  new_img = pca_compress_img(im, dim)
  imshow(new_img)
  title("pca dim: {}".format(dim))

show()

