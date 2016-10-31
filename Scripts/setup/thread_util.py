import threading
import subprocess


class TimerClass(threading.Thread):
    def __init__(self, proc, timeout):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = timeout # Seconds for forced kill
        self.proc = proc

    def run(self):
        while self.count > 0 and not self.event.is_set():
            self.event.wait(1)
            self.count -= 1
        if not self.event.is_set():
            print "Killing due to timeout"
            self.proc.kill()

    def stop(self):
        self.event.set()


def execute_with_timout(timeout, executable, **kwargs):
    arguments = [executable]
    for k, v in kwargs.iteritems():
        arguments.append("--{0}={1}".format(k,str(v)))
    proc = subprocess.Popen(arguments)
    tmr = TimerClass(proc, timeout)
    tmr.start()
    proc.wait()
    tmr.stop()
    return proc.returncode
