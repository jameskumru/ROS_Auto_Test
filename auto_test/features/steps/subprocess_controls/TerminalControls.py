import os
import re
import subprocess
import time

import pexpect


class TerminalControls:

    @staticmethod
    def get_sourced_shell(source):
        shell = pexpect.spawnu('/bin/bash')
        shell.expect('$')
        shell.sendline('source ' + source)
        shell.expect('$')
        return shell

    @staticmethod
    def perform_command(shell, command):
        return subprocess.Popen(command, shell=True, universal_newlines=True, stdin=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash", preexec_fn=os.setsid)

    @staticmethod
    def read_node_buffer_for_value(shell, expected_regex, timeout):
        output = []
        t_end = time.time() + timeout * 60
        while time.time() < t_end:
            for line in shell.read():
                output.append(line)
                if re.match(re.compile(expected_regex), line):
                    break
        return output
