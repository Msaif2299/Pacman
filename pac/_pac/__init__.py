from gym.envs.registration import register

register(
    id='pac-v0',
    entry_point='_pac.envs:PacmanPygame'
)