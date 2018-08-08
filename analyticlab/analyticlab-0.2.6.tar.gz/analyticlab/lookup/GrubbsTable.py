﻿# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 22:19:47 2018

@author: xingrongtech
"""
from analyticlab.system.exceptions import tooMuchDataForTestException, tooLessDataForTestException

table = {}
table[0.90] = (1.148, 1.425, 1.602, 1.729, 1.828, 1.909, 1.977, 2.036, 
     2.088, 2.134, 2.175, 2.213, 2.247, 2.279, 2.309, 2.335, 2.361, 2.385, 
     2.408, 2.429, 2.448, 2.467, 2.486, 2.502, 2.519, 2.534, 2.549, 2.563, 
     2.577, 2.591, 2.604, 2.616, 2.628, 2.639, 2.650, 2.661, 2.671, 2.682, 
     2.692, 2.700, 2.710, 2.719, 2.727, 2.736, 2.744, 2.753, 2.760, 2.768, 
     2.775, 2.783, 2.790, 2.798, 2.804, 2.811, 2.818, 2.824, 2.831, 2.837, 
     2.842, 2.849, 2.854, 2.860, 2.866, 2.871, 2.877, 2.883, 2.888, 2.893, 
     2.897, 2.903, 2.908, 2.912, 2.917, 2.922, 2.927, 2.931, 2.935, 2.940, 
     2.945, 2.949, 2.953, 2.957, 2.961, 2.966, 2.970, 2.973, 2.977, 2.981, 
     2.984, 2.989, 2.993, 2.996, 3.000, 3.003, 3.006, 3.011, 3.014, 3.017)
table[0.95] = (1.153, 1.463, 1.672, 1.822, 1.938, 2.032, 2.110, 2.176, 
     2.234, 2.285, 2.331, 2.371, 2.409, 2.443, 2.475, 2.504, 2.532, 2.557, 
     2.580, 2.603, 2.624, 2.644, 2.663, 2.681, 2.698, 2.714, 2.730, 2.745, 
     2.759, 2.773, 2.786, 2.799, 2.811, 2.823, 2.835, 2.846, 2.857, 2.866, 
     2.877, 2.887, 2.896, 2.905, 2.914, 2.923, 2.931, 2.940, 2.948, 2.956, 
     2.964, 2.971, 2.978, 2.986, 2.992, 3.000, 3.006, 3.013, 3.019, 3.025, 
     3.032, 3.037, 3.044, 3.049, 3.055, 3.061, 3.066, 3.071, 3.076, 3.082, 
     3.087, 3.092, 3.098, 3.102, 3.107, 3.111, 3.117, 3.121, 3.125, 3.130, 
     3.134, 3.139, 3.143, 3.147, 3.151, 3.155, 3.160, 3.163, 3.167, 3.171, 
     3.174, 3.179, 3.182, 3.186, 3.189, 3.193, 3.196, 3.201, 3.204, 3.207)
table[0.975] = (1.155, 1.481, 1.715, 1.887, 2.020, 2.126, 2.215, 2.290, 
     2.355, 2.412, 2.462, 2.507, 2.549, 2.585, 2.620, 2.651, 2.681, 2.709, 
     2.733, 2.758, 2.781, 2.802, 2.822, 2.841, 2.859, 2.876, 2.893, 2.908, 
     2.924, 2.938, 2.952, 2.965, 2.979, 2.991, 3.003, 3.014, 3.025, 3.036, 
     3.046, 3.057, 3.067, 3.075, 3.085, 3.094, 3.103, 3.111, 3.120, 3.128, 
     3.136, 3.143, 3.151, 3.158, 3.166, 3.172, 3.180, 3.186, 3.193, 3.199, 
     3.205, 3.212, 3.218, 3.224, 3.230, 3.235, 3.241, 3.246, 3.252, 3.257, 
     3.262, 3.267, 3.272, 3.278, 3.282, 3.287, 3.291, 3.297, 3.301, 3.305, 
     3.309, 3.315, 3.319, 3.323, 3.327, 3.331, 3.335, 3.339, 3.343, 3.347, 
     3.350, 3.355, 3.358, 3.362, 3.365, 3.369, 3.372, 3.377, 3.380, 3.383)
table[0.99] = (1.155, 1.492, 1.749, 1.944, 2.097, 2.221, 2.323, 2.410, 
     2.485, 2.550, 2.607, 2.659, 2.705, 2.747, 2.785, 2.821, 2.854, 2.884, 
     2.912, 2.939, 2.963, 2.987, 3.009, 3.029, 3.049, 3.068, 3.085, 3.103, 
     3.119, 3.135, 3.150, 3.164, 3.178, 3.191, 3.204, 3.216, 3.228, 3.240, 
     3.251, 3.261, 3.271, 3.282, 3.292, 3.302, 3.310, 3.319, 3.329, 3.336, 
     3.345, 3.353, 3.361, 3.368, 3.376, 3.383, 3.391, 3.397, 3.405, 3.411, 
     3.418, 3.424, 3.430, 3.437, 3.442, 3.449, 3.454, 3.460, 3.466, 3.471, 
     3.476, 3.482, 3.487, 3.492, 3.496, 3.502, 3.507, 3.511, 3.516, 3.521, 
     3.525, 3.529, 3.534, 3.539, 3.543, 3.547, 3.551, 3.555, 3.559, 3.563, 
     3.567, 3.570, 3.575, 3.579, 3.582, 3.586, 3.589, 3.593, 3.597, 3.600)
table[0.995] = (1.155, 1.496, 1.764, 1.973, 2.139, 2.274, 2.387, 2.482, 
     2.564, 2.636, 2.699, 2.755, 2.806, 2.852, 2.894, 2.932, 2.968, 3.001, 
     3.031, 3.060, 3.087, 3.112, 3.135, 3.157, 3.178, 3.199, 3.218, 3.236, 
     3.253, 3.270, 3.286, 3.301, 3.316, 3.330, 3.343, 3.356, 3.369, 3.381, 
     3.393, 3.404, 3.415, 3.425, 3.435, 3.445, 3.455, 3.464, 3.474, 3.483, 
     3.491, 3.500, 3.507, 3.516, 3.524, 3.531, 3.539, 3.546, 3.553, 3.560, 
     3.566, 3.573, 3.579, 3.586, 3.592, 3.598, 3.605, 3.610, 3.617, 3.622, 
     3.627, 3.633, 3.638, 3.643, 3.648, 3.654, 3.658, 3.663, 3.669, 3.673, 
     3.677, 3.682, 3.687, 3.691, 3.695, 3.699, 3.704, 3.708, 3.712, 3.716, 
     3.720, 3.725, 3.728, 3.732, 3.736, 3.739, 3.744, 3.747, 3.750, 3.754)

def G(confLevel, n):
    if n > 100:
        raise tooMuchDataForTestException('Grubbs检验不支持超过100组数据')
    elif n < 3:
        raise tooLessDataForTestException('Grubbs检验')
    return table[confLevel][n-3]