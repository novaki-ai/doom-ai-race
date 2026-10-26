import sys; sys.path.insert(0, '../tools_m45')
from m5_leg import run
P = [(288, 352, 10, 1), (320, 430), (204, 428), (204, 250), (215, 180), (430, 176), (650, 176), (870, 190), (888, 262, 12)]
run('m5sg_1.lmp', P, int(sys.argv[1]), int(sys.argv[2]), 'm5L2b_best.lmp', ul={310, 312}, mt=700)
