import time
import signal
import argparse
from easydict import EasyDict
import numpy as np
from scipy.spatial.transform import Rotation as R
import yaml
import copy
import torch

class State_struct:
  def __init__(self, pos=np.zeros(3), 
                     vel=np.zeros(3),
                     acc = np.zeros(3),
                     jerk = np.zeros(3), 
                     snap = np.zeros(3),
                     rot=R.from_quat(np.array([0.,0.,0.,1.])), 
                     ang=np.zeros(3)):
    
    self.pos = pos # R^3
    self.vel = vel # R^3
    self.acc = acc
    self.jerk = jerk
    self.snap = snap
    self.rot = rot # Scipy Rotation rot.as_matrix() rot.as_quat()
    self.ang = ang # R^3
    self.t = 0.
  
  def get_vec_state_numpy(self, q_order = 'xyzw'):

    if q_order=='xyzw':
      return np.r_[self.pos, self.vel, self.rot.as_quat(), self.ang]
    else:
      #quaternion -> w,x,y,z
      return np.r_[self.pos, self.vel, np.roll(self.rot.as_quat(), 1), self.ang]
  def get_vec_state_torch(self, q_order = 'xyzw'):
    return torch.tensor(self.get_vec_state_numpy(q_order=q_order))