import pexpect


class Roscore(object):
    def __init__(self):
        self.running = False
        self.current_process = None

    def start_roscore(self):
        if self.running:
            return self
        else:
            child = pexpect.spawn('/bin/bash')
            self.current_process = child
            child.expect('$')
            child.sendline("source /opt/ros/kinetic/setup.sh")
            child.expect('$')
            child.sendline("roscore")
            child.expect('started core service', timeout=20)
            self.running = True
            return child

    def terminate(self):
        if self.running is True:
            self.current_process.close()
            self.running = False
            return True
        else:
            return False
