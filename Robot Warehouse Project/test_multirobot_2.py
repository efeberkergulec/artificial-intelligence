import multirobot
from gym.envs.registration import register
import gym.envs

del gym.envs.registry.env_specs['multirobot-warehouse-v0']

register(
    id='multirobot-warehouse-v0',
    entry_point='gym_warehouse.envs:MultiRobotWarehouseEnv',
    kwargs={'desc': [
        "B.A",
        "*.*",
        "a.b"
        ]
    }
)

multirobot.run_agent()

