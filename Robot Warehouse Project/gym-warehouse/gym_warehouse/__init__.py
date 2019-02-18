from gym.envs.registration import register

register(
    id='multirobot-warehouse-v0',
    entry_point='gym_warehouse.envs:MultiRobotWarehouseEnv',
)

register(
    id='singlerobot-warehouse-v0',
    entry_point='gym_warehouse.envs:SingleRobotWarehouseEnv',
)

