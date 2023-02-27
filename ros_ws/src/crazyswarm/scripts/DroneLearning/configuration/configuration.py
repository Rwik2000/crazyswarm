import numpy as np

from enum import Enum
from typing import TypeVar, Generic, Optional, Any, Tuple, List, Union
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass
class ConfigValue(Generic[T]):
    """
    Represents any configurable parameter that can be randomized.

    :param default: The value of the parameter without randomization
    :param randomize: Whether this parameter should be randomly sampled
    :param min: The minimium value of this parameter, only needed when randomization
        true
    :param max: The maximum value of this parameter

    Note: when `T` is an `np.ndarray`, randomization and min/max ranges should
    apply per-element (although the actual behavior will depend on the sampling func)
    """
    default: T
    randomize: bool = False
    min: Optional[T] = None
    max: Optional[T] = None

    def __post_init__(self):
        if self.randomize and (self.min is None or self.max is None):
            raise ValueError(f'Must specify a min and a max when randomizing a param.') 


class Sampler:
    def __init__(self, sampling_func=None, name='custom_sampler'):
        if sampling_func is None:
            self.sampling_func = self.default_sample
            self.name = 'uniform'
        else:
            self.sampling_func = sampling_func
            self.name = name

    def sample_param(self, param: ConfigValue, **kwargs):
        if param.randomize:
            return self.sampling_func(param, **kwargs)
        else:
            return param.default

    def default_sample(self, param: ConfigValue, **kwargs):
        return np.random.uniform(param.min, param.max)


@dataclass
class DroneConfiguration:
    mass: ConfigValue[float] = ConfigValue[float](default=1.0, randomize=False)
    # assumes all axes are same
    I: ConfigValue[float] = ConfigValue[float](default=1.0, randomize=False)
    g: ConfigValue[float] = ConfigValue[float](default=9.8, randomize=False)

    sampler: Sampler = Sampler()

@dataclass
class WindConfiguration:
    is_wind: bool = False

    pos: ConfigValue[np.ndarray] = ConfigValue[np.ndarray](default=np.array([0.0, 0.0, 0.0]), randomize=False)
    dir: ConfigValue[np.ndarray] = ConfigValue[np.ndarray](default=np.array([0.0, 0.0, 0.0]), randomize=False)
    vmax: ConfigValue[float] = ConfigValue[float](default=0, randomize=False)

    sampler: Sampler = Sampler()

@dataclass
class InitializationConfiguration:
    pos: ConfigValue[np.ndarray] = ConfigValue[np.ndarray](
        default=np.array([0.0, 0.0, 0.0]), 
        randomize=True,
        min=np.array([-0.5, -0.5, -0.5]),
        max=np.array([0.5, 0.5, 0.5])
    )
    vel: ConfigValue[np.ndarray] = ConfigValue[np.ndarray](
        default=np.array([0.0, 0.0, 0.0]), 
        randomize=False
    )
    # Represented as Euler ZYX in degrees
    rot: ConfigValue[np.ndarray] = ConfigValue[np.ndarray](
        default=np.array([0.0, 0.0, 0.0]),
        randomize=False
    )
    ang: ConfigValue[np.ndarray] = ConfigValue[np.ndarray](
        default=np.array([0.0, 0.0, 0.0]),
        randomize=False
    )

    sampler: Sampler = Sampler()

@dataclass
class SimConfiguration:
    linear_var: ConfigValue[float] = ConfigValue[float](default=0.0, randomize=False)
    angular_var: ConfigValue[float] = ConfigValue[float](default=0.0, randomize=False)

    obs_noise: ConfigValue[float] = ConfigValue[float](default=0.0, randomize=False)
    # latency currently only supports being measured as multiples of dt
    latency: ConfigValue[int] = ConfigValue[int](default=0, randomize=False)
    k: ConfigValue[float] = ConfigValue[float](default=1, randomize=False)

    sampler: Sampler = Sampler()


class EnvCondition(Enum):
    WIND = 'wind'
    MASS = 'mass'
    I = 'moment_of_inertia'
    LATENCY = 'latency'

    def get_attribute(self, env) -> Tuple[Any, int, Union[Tuple[float], float], Union[Tuple[float], float]]:
        """
        Given the particular env condition, get the corresponding attribute of the
        BaseQuadsimEnv that corresponds to that condition, the dimensionality 
        of the encoding of that condition, and the min/max of each param. The min/max
        can be given as a single number, in which case it applies to all values in 
        the encoding, or a tuple equal to the dimensionality that gives the min/max
        for each value.
        """
        return {
            EnvCondition.WIND: (env.wind_vector, 3, -2.0, 2.0),
            EnvCondition.MASS: (env.model.mass, 1, 0.0, np.inf),
            # Assume diagonal
            EnvCondition.I: (np.diagonal(env.model.I), 3, 0.0, np.inf),
            EnvCondition.LATENCY: (env.latency, 1, 0.0, np.inf)
        }[EnvCondition(self._value_)]

@dataclass
class AdaptationConfiguration:
    # Which parameters to include as part of the environmental conditions
    # Best to specify in order as defined in EnvCondition, to keep order consistent
    # across different models
    include: List[EnvCondition] = field(default_factory=list)

    # time horizon of history to pass to adaptation network
    time_horizon: int = 50
    

@dataclass
class AllConfig:
    drone_config: DroneConfiguration
    wind_config: WindConfiguration
    init_config: InitializationConfiguration
    sim_config: SimConfiguration
    adapt_config: AdaptationConfiguration = None
