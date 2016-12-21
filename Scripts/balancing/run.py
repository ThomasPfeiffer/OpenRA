import sys
from openRA import executor
from evoalgosOptimization import optimize
import logging
from utility import log_util


def main():
    cmd = get_arg("-cmd")
    if not cmd:
        cmd = raw_input("Choose what to run. (replay / paramless / optimization)")
    handle_cmd(cmd)


def get_arg(name):
    for arg in sys.argv:
        if arg.count('=') != 1:
            continue
        argname, value = arg.split('=')
        if argname == name:
            return value


def handle_cmd(cmd):
    def print_start(cmd):
        print("Starting "+cmd+" execution")

    log = get_arg('-log')
    if log:
        log_util.add_handler(logging.FileHandler(filename=log))
    if cmd == "paramless":
        print_start(cmd)
        executor.run_paramless()
    elif cmd == "replay":
        print_start(cmd)
        executor.run_replay()
    elif cmd == "write-params":
        print_start(cmd)
        executor.replay_params()
    elif cmd == "optimization":
        print_start(cmd)
        optimize.run_optimization()
    else:
        print ('Unknown command ' + cmd)

if __name__ == "__main__":
    main()
