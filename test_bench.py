import os

from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO

from SelfDriveEnv import Car, Track
from training_utils import TensorboardCallback, constant_schedule, linear_schedule, run_experiment, testing, with_changes
from config import cfg

# Create custom reward function

@Car.reward_function
def reward_func(car):
    reward = 0
    if car.crashed:
        reward = car.config["reward"]["crash_reward"]
    elif car.has_finished:
        print('finished!')
        reward += 100
    else:
        curr = car.current_tile()
        if curr not in car.traveled:
            reward = car.config["reward"]["new_tile_reward"] * (len(car.traveled) + 1)
        elif car.speed <= car.config["reward"]["min_speed"]:
            reward = car.config["reward"]["same_tile_penalty"]
        else:
            reward = car.config["reward"]["same_tile_reward"]
    return reward

# Specify folders to save models/logs in

model_dir = "learning-rate-tests"
log_dir = "test-bench-logs"

os.makedirs(model_dir, exist_ok=True)

# Define tests

run_experiment(

    testing("constant learning rate with .01",            
        with_changes(
                {
                    "training": {
                        "learning_rate": constant_schedule(.01),
                        "log_dir": log_dir,
                    }
                }
            ),
        save_as="constant-01",
        in_dir=model_dir),
    
    testing("constant learning rate with .007",            
        with_changes(
                {
                    "training": {
                        "learning_rate": constant_schedule(.007),
                        "log_dir": log_dir,
                    }
                }
            ),
        save_as="constant-007",
        in_dir=model_dir),
    
    testing("constant learning rate with .005",            
        with_changes(
                {
                    "training": {
                        "learning_rate": constant_schedule(.005),
                        "log_dir": log_dir,
                    }
                }
            ),
        save_as="constant-005",
        in_dir=model_dir),
    
    testing("constant learning rate with .003",            
        with_changes(
                {
                    "training": {
                        "learning_rate": constant_schedule(.003),
                        "log_dir": log_dir,
                    }
                }
            ),
        save_as="constant-003",
        in_dir=model_dir),
    
    timesteps=50000, 
    render=True,
    trials=5,
    run_after_training=False,
)