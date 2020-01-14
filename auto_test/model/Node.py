import re
import time

import pexpect


class Node:
    def __init__(self, name, package, required_source):
        self.name = name + ".py"
        self.package = package
        self.running = False
        self.current_shell = None
        self.required_source = required_source

    def start_node(self, running_flag="\r", args=None):
        if args is not None:
            optional_args = " ".join(args)
            command = "rosrun {0} {1} {2}".format(self.package, self.name, optional_args)

        else:
            command = "rosrun {0} {1}".format(self.package, self.name)

        node = pexpect.spawn('/bin/bash')
        self.current_shell = node
        node.expect('$')
        node.sendline('source ' + self.required_source)
        node.expect('$')
        node.sendline(command)
        node.expect(running_flag, timeout=20)
        self.running = True

    def start_node_get_immediate_response(self, args=None):
        if args is not None:
            optional_args = " ".join(args)
            command = "rosrun {0} {1} {2}".format(self.package, self.name, optional_args)

        else:
            command = "rosrun {0} {1}".format(self.package, self.name)

        node = pexpect.spawn('/bin/bash')
        self.current_shell = node
        node.expect('$')
        node.sendline('source ' + self.required_source)
        node.expect('$')
        node.sendline(command)
        self.running = True

        stdout_buffer = b""
        while 1:
            try:
                stdout_buffer += node.read_nonblocking(size=999, timeout=1)
            except pexpect.exceptions.TIMEOUT:
                return stdout_buffer.decode('iso-8859-1')

    def send_message_to_node(self, command):
        self.current_shell.sendline(command)
        self.current_shell.expect('\n')
        return self.current_shell.after

    def send_message_to_node_get_response(self, command, response_regex, timeout):
        self.current_shell.sendline(command)
        self.current_shell.expect(response_regex, timeout=timeout)
        return self.current_shell.read()

    def read_node_buffer_for_value(self, expected_regex, timeout):
        output = []
        t_end = time.time() + timeout * 60
        while time.time() < t_end:
            for line in self.current_shell.read():
                output.append(line)
                if re.match(re.compile(expected_regex), line):
                    break
        return output
