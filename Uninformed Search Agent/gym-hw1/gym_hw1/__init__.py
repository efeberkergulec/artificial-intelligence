from gym.envs.registration import register

register(
    id='escape-v0',
    entry_point='gym_hw1.envs:EscapeEnv',
)

register(
    id='zork1-v0',
    entry_point='gym_hw1.envs:Zork1Env',
)

register(
    id='zork2-v0',
    entry_point='gym_hw1.envs:Zork2Env',
)
