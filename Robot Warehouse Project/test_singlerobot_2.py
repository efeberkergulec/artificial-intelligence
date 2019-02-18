import singlerobot
from gym.envs.registration import register
import gym.envs

del gym.envs.registry.env_specs['singlerobot-warehouse-v0']

register(
    id='singlerobot-warehouse-v0',
    entry_point='gym_warehouse.envs:SingleRobotWarehouseEnv',
    kwargs={'desc': [
        "........",
        ".***....",
        "..a*....",
        "...*.A..",
        ]
    }
)

singlerobot.run_agent()

