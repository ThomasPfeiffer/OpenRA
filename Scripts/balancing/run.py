import sys
from balancing.openRA import executor

def main():
    if len(sys.argv) < 2:
        cmd = raw_input("Choose what to run. (replay / paramless / optimization)")
    else:
        cmd = sys.argv[1]
    if cmd == "paramless":
        executor.main()



if __name__ == "__main__":
    main()
