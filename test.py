



import subprocess, threading

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True , stdout = subprocess.PIPE)
            self.output, self.error = self.process.communicate()
            print self.output

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process'
            self.process.terminate()
            thread.join()
        print self.process.returncode

if __name__ == '__main__':
    #command = Command("echo 'Process started'; sleep 20; echo 'Process finished'")
    command = Command("echo 'Process started'; sleep 20; echo 'Process finished'")
    command.run(timeout=3)
    command.run(timeout=1)
