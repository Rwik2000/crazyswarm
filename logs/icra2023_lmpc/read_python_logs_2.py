import numpy as np
import argparse
import matplotlib.pyplot as plt
from plt_utils import load_cf_data

def first_nonzero(arr, axis, invalid_val=-1):
    mask = arr!=0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)

def plot_npz(filename):

    data_dict = load_cf_data(filenames, args)

    # plt.figure(5)
    # plt.plot(data_dict[filename[0]]['ref_positions'][:, 0], data_dict[filename[0]]['ref_positions'][:, 1])
    # for key in data_dict.keys():
    #     plt.plot(data_dict[key]['pose_positions'][:,0], data_dict[key]['pose_positions'][:, 1], label=key)
    # plt.legend()
    # ax = plt.gca()
    # ax.set_aspect('equal', 'box')

    # print(pose_orientations.shape, pose_orientations.shape, cf_positions.shape, ts.shape, thrust_cmds.shape)
    
    fig = plt.figure(0)

# using padding
    plt.subplots_adjust(hspace=0.5)
    plt.rcParams['axes.grid'] = True
    ax1 = plt.subplot(4, 1, 1)
    ax1.title.set_text('X direction')
    ax1.set_ylabel('meters')

    ct = 0
    for key in data_dict.keys():
        plt.plot(data_dict[key]['ts'], data_dict[key]['pose_positions'][:, 0], label='/cf/pose position')
        # plt.plot(data_dict[key]['ts'], data_dict[key]['cf_positions'][:, 0], label='cf.position()')
        if ct == 0:
            plt.plot(data_dict[key]['ts'], data_dict[key]['ref_positions'][:, 0])
            ct = 1
            
    ax2 = plt.subplot(4, 1, 2, sharex=ax1)
    ax2.title.set_text('Y direction')
    ax2.set_ylabel('meters')

    ct = 0
    for key in data_dict.keys():
        plt.plot(data_dict[key]['ts'], data_dict[key]['pose_positions'][:, 1], label='/cf/pose position')
        # plt.plot(data_dict[key]['ts'], data_dict[key]['cf_positions'][:, 1], label='cf.position()')
        if ct == 0:
            plt.plot(data_dict[key]['ts'], data_dict[key]['ref_positions'][:, 1])
            ct += 1

    ax3 = plt.subplot(4, 1, 3, sharex=ax1)
    ax3.title.set_text('Z direction')
    ax3.set_ylabel('meters')

    ct = 0
    for key in data_dict.keys():
        plt.plot(data_dict[key]['ts'], data_dict[key]['pose_positions'][:, 2], label='/cf/pose position')
        # plt.plot(data_dict[key]['ts'], data_dict[key]['cf_positions'][:, 2], label=key+'_cf.position()')
        if ct == 0:
            plt.plot(data_dict[key]['ts'], data_dict[key]['ref_positions'][:, 2],label=key+'_ref position')
            ct += 1
    ax4 = plt.subplot(4, 1, 4, sharex=ax1)
    ax4.title.set_text('Yaw')
    ax4.set_ylabel('Degrees ')

    ct = 0 
    for key in data_dict.keys():
        if 'mppi' in key:
            leg = 'MPPI'
        else:
            leg = 'DMPO'
        plt.plot(data_dict[key]['ts'], data_dict[key]['pose_orientations'][:, 0], label=leg)
        if ct == 0:
            plt.plot(data_dict[key]['ts'], data_dict[key]['ref_orientation'][:, 0],label='reference')
            ct += 1
    
    plt.xlabel('Time (s)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), fancybox=True, shadow=True, ncol=4)
    plt.show()

    plt.savefig('high_res_plot.pdf', dpi=300, format='pdf')

    # plt.suptitle('PPO curriculum')
    
    # pos_rmse = np.sqrt(np.mean(data_dict[key]['cf_positions'] - data_dict[key]['ref_positions'], axis=0) ** 2)
    # print("position RMSE : ", pos_rmse)
    # print("total position RMSE", np.linalg.norm(pos_rmse))
    # error = data_dict[key]['ref_positions'] - data_dict[key]['cf_positions']

    # plt.figure(1)
    # ax1 = plt.subplot(3, 1, 1)
    # for key in data_dict.keys():
    #     # plt.plot(data_dict[key]['ts'], data_dict[key]['pose_positions'][:, 0], label='/cf/pose position')
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['pose_orientations'][:, 0], label='cf.position()')
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['ref_orientation'][:, 0])
    # plt.subplot(3, 1, 2, sharex=ax1)
    # for key in data_dict.keys():
    #     # plt.plot(data_dict[key]['ts'], data_dict[key]['pose_positions'][:, 1], label='/cf/pose position')
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['pose_orientations'][:, 1], label='cf.position()')
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['ref_orientation'][:, 1])
    # plt.subplot(3, 1, 3, sharex=ax1)
    # for key in data_dict.keys():
    #     # plt.plot(data_dict[key]['ts'], data_dict[key]['pose_positions'][:, 2], label='/cf/pose position')
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['pose_orientations'][:, 2], label=key+'_cf.position()')
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['ref_orientation'][:, 2],label=key+'_ref position')
    # plt.legend()
    # plt.suptitle('PPO curriculum attitude')


    # plt.figure(2)
    # ax1 = plt.subplot(3, 1, 1)
    # for key in data_dict.keys():
    #     zero_error = np.zeros_like(data_dict[key]['ts'])
    #     # plt.plot(data_dict[key]['ts'], data_dict[key]['pose_positions'][:, 0], label='/cf/pose position')
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['ref_positions'][:, 0] - data_dict[key]['pose_positions'][:, 0], label='cf.position()')
    #     plt.plot(data_dict[key]['ts'], zero_error)
    # plt.subplot(3, 1, 2, sharex=ax1)
    # for key in data_dict.keys():
    #     zero_error = np.zeros_like(data_dict[key]['ts'])
    #     # plt.plot(data_dict[key]['ts'], data_dict[key]['pose_positionss'][:, 1], label='/cf/pose position')
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['ref_positions'][:, 1] - data_dict[key]['pose_positions'][:, 1], label='cf.position()')
    #     plt.plot(data_dict[key]['ts'], zero_error)
    # plt.subplot(3, 1, 3, sharex=ax1)
    # for key in data_dict.keys():
    #     zero_error = np.zeros_like(data_dict[key]['ts'])
    #     # plt.plot(data_dict[key]['ts'], data_dict[key]['pose_positionss'][:, 2], label='/cf/pose position')
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['ref_positions'][:, 2] - data_dict[key]['pose_positions'][:, 2], label=key+'_cf.position()')
    #     plt.plot(data_dict[key]['ts'], zero_error, label=key+'zero error')
    # plt.legend()
    # plt.suptitle('position error')
    # # plt.figure(1)
    # # ax2 = plt.subplot(3, 1, 1)
    # # plt.plot(ts, ang_vel_cmds[:, 0])
    # # plt.plot(ts, mocap_orientation[:,2])
    # # plt.plot(ts, pose_orientations[:, 2], color='red')
    # # plt.subplot(3, 1, 2, sharex=ax2)
    # # plt.plot(ts, ang_vel_cmds[:, 1])
    # # plt.plot(ts, mocap_orientation[:,1])
    # # plt.plot(ts, pose_orientations[:, 1], color='red')
    # # plt.subplot(3, 1, 3, sharex=ax2)
    # # plt.plot(ts, ang_vel_cmds[:, 2], label='Ang Vel Cmd (deg/s)')
    # # plt.plot(ts, mocap_orientation[:,0], label='mocap data')
    # # plt.plot(ts, pose_orientations[:, 0], color='red', label='Euler Angle (deg)')
    # # plt.suptitle('cf/pose orientation (python) & ang vel cmds')
    # # plt.legend()

    # # plt.figure(2)
    # # ax3 = plt.subplot(3, 1, 1)
    # # plt.plot(ts, cf_positions[:, 0])
    # # plt.subplot(3, 1, 2, sharex=ax3)
    # # plt.plot(ts, cf_positions[:, 1])
    # # plt.subplot(3, 1, 3, sharex=ax3)
    # # plt.plot(ts, cf_positions[:, 2])
    # # plt.suptitle('cf.position() (python)')

    # plt.figure(3)
    # for key in data_dict.keys():
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['thrust_cmds'], label=key)
    # plt.legend()
    # plt.title('Cmd z acc (python)')

    # # try:
    # plt.figure(4)
    # for key in data_dict.keys():
    #     # print(data_dict[key]['adaptation_terms'])
    #     plt.plot(data_dict[key]['ts'], data_dict[key]['adaptation_terms'])
    # plt.title('adaptation term')
    # except:
    #     pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="+")
    parser.add_argument("--runtime", type=float, default=2.0)
    parser.add_argument("--hovertime",type=float,default=4)
    parser.add_argument("-bh", "--baseheight", type=float, default=1.0)
    parser.add_argument("-tt", "--takeofftime",type=float,default=5.0)

    args = parser.parse_args()
    filenames = args.filename
    # print(filename)
    # exit()

    plot_npz(filenames)
    
