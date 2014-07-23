#! /usr/bin/env python
import threading
import subprocess
import traceback
import shlex


class Command(object):
    """
    Enables to run subprocess commands in a different thread with TIMEOUT option.

    Based on jcollado's solution:
    http://stackoverflow.com/questions/1191374/subprocess-with-timeout/4825933#4825933
    """
    command = None
    process = None
    status = None
    output, error = '', ''

    def __init__(self, command):
        #if isinstance(command, basestring):
        #    command = shlex.split(command)
        print command
        self.command = command

    def run(self, timeout=None, **kwargs):
        """ Run a command then return: (status, output, error). """
        def target(**kwargs):
            try:
                print kwargs
                #self.process = subprocess.Popen(self.command, **kwargs)
                self.process = subprocess.Popen(self.command, shell = True, stdout = subprocess.PIPE)
                self.output, self.error = self.process.communicate()
                self.status = self.process.returncode
            except:
                self.error = traceback.format_exc()
                self.status = -1
        # default stdout and stderr
        if 'stdout' not in kwargs:
            kwargs['stdout'] = subprocess.PIPE
        if 'stderr' not in kwargs:
            kwargs['stderr'] = subprocess.PIPE
        # thread
        thread = threading.Thread(target=target, kwargs=kwargs)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
        return self.status, self.output, self.error

if __name__ == "__main__":
    cmd = Command("echo 'Process started'; sleep 30; echo 'Process finished'")
    status = cmd.run(timeout=2, shell=True)
    print status
