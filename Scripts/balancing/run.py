import sys
from balancing.openRA import executor
from balancing.evoalgosOptimization import optimize


def main():
    if len(sys.argv) < 2:
        cmd = raw_input("Choose what to run. (replay / paramless / optimization)")
    else:
        cmd = sys.argv[1]
    if cmd == "paramless":
        print("Starting "+cmd+" execution")
        executor.run_paramless()
    elif cmd == "replay":
        print("Starting "+cmd+" execution")
        executor.run_replay()
    elif cmd == "optimization":
        print("Starting "+cmd+" execution")
        optimize.run_optimization()
    else:
        print ('Unknown command ' + cmd)

if __name__ == "__main__":
    main()
