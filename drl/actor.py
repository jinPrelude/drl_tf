from __future__ import print_function

import logging
import random
import argparse

import grpc
import seed_rl_pb2
import seed_rl_pb2_grpc

import gym
import numpy as np

def reset_env(stub, env, actor_id):
    obs, _ = env.reset()
    print(f"id: {actor_id}\tobs: {obs}")
    obs = str(obs)
    response = stub.Reset(seed_rl_pb2.ResetRequest(actor_id=actor_id, obs=obs))
    print(f"response: {response}")
    action = response.action - 1
    return action

def actor_loop(stub, env, actor_id):
    print("actor loop!!")
    while True:
        obs, _ = env.reset()
        obs = str(obs)
        done = False
        request_type, reward = "reset", 0
        while True:
            print(f"request type: {request_type}")
            response = stub.DiscreteGymStep(seed_rl_pb2.CallRequest(actor_id=actor_id, obs=obs, reward=reward, done=str(done), request_type=request_type))
            if done:
                break
            request_type = "step"
            action = response.action - 1
            obs, reward, done, _, _ = env.step(action)
            obs = str(obs)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=int)
    args = parser.parse_args()

    channel = grpc.insecure_channel('localhost:50051')
    stub = seed_rl_pb2_grpc.SeedRLStub(channel)

    env = gym.make("CartPole-v1")

    # action = reset_env(stub, env, args.id)
    actor_loop(stub, env, args.id)
    print("passed!")


if __name__ == '__main__':
    logging.basicConfig()
    run()