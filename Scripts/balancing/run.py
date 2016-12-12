import sys
from balancing.openRA import executor
from balancing.evoalgosOptimization import optimize


def main():
    if len(sys.argv) < 2:
        cmd = raw_input("Choose what to run. (replay / paramless / optimization)")
    else:
        cmd = sys.argv[1]

    def print_start(cmd):
        print("Starting "+cmd+" execution")

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
