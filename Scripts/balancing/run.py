import sys
from openRA import executor
from evoalgosOptimization import optimize
import logging
from utility import log_util
from utility import thread_util


def get_arg(name):
    for arg in sys.argv:
        if arg.count('=') != 1:
            continue
        argname, value = arg.split('=')
        if argname == name:
            return value

commands = {
"paramless" : executor.run_paramless,
"replay" : executor.run_replay,
"write-params" : executor.replay_params,
"optimization": optimize.run_optimization
}


def handle_cmd(cmd):
    log = get_arg('-log')
    if log:
        log_util.add_handler(logging.FileHandler(filename=log))

    if cmd in commands.keys():
        print("Starting "+cmd+" execution")
        try:
            commands[cmd]()
            thread_util.show_messagebox("Evoalgos Balancing Optimization", "Execution finished.")
        except:
            thread_util.show_messagebox("Evoalgos Balancing Optimization", "Execution finished with erros.")
            raise
    else:
        print ('Unknown command ' + cmd)

def main():
    cmd = get_arg("-cmd")
    if not cmd:
        cmd = raw_input("Choose what to run. ({0})".format(" / ".join(commands.keys())))
    handle_cmd(cmd)

if __name__ == "__main__":
    main()

