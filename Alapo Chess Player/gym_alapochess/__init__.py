from gym.envs.registration import register

register(
	id='Alapochess-v1',
	entry_point='gym_alapochess.envs:AlapoEnv'
)