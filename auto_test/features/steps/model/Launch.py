import pexpect


class Launch:
    def __init__(self, package, file_name, source="/opt/ros/kinetic/setup.sh"):
        self.running = False
        self.package = package
        self.source = source
        self.file_name = file_name
        self.current_shell = None

    def launch_with_file(self, running_flag):
        command = "roslaunch {0} {1}".format(self.package, self.file_name)

        node = pexpect.spawn('/bin/bash')
        self.current_shell = node
        node.expect('$')
        node.sendline('source ' + self.source)
        node.expect('$')
        node.sendline(command)
        node.expect(running_flag, timeout=20)
        self.running = True

    def terminate(self):
        if self.running is True:
            self.current_shell.close()
            self.running = False
            return True
        else:
            return False

