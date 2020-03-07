import os
import signal
from subprocess import Popen, PIPE

from subprocess_controls.TerminalControls import TerminalControls


class Topic:
    def __init__(self, name, source="/opt/ros/kinetic/setup.sh"):
        self.name = name
        self.source = source
        self.running = False
        self.current_shell = None

    def rostopic_pub(self, message_type, velocity_command, orientation_command, confirmation_flag):
        if self.running is False:
            self.current_shell = TerminalControls.get_sourced_shell(self.source)
        self.current_shell.sendline(
            'rostopic pub {0} {1} \'{2}\' \'{3}\''.format(self.name, message_type, velocity_command,
                                                          orientation_command))
        self.current_shell.expect(confirmation_flag, timeout=20)
        self.running = True

    def echo(self, n_lines):
        output = []
        shell_setup_script = "/opt/ros/kinetic/setup.sh"
        command = "rostopic echo /odometry/base_raw/pose"
        cmd = ". %s; %s" % (shell_setup_script, command)
        self.current_shell = Popen(cmd, stdout=PIPE, shell=True, preexec_fn=os.setsid)
        self.running = True

        i = 0
        for line in iter(self.current_shell.stdout.readline, ''):
            output.append(line[0:].decode('utf-8').strip())
            if i == n_lines:
                break
            i += 1
        self.current_shell.terminate()
        return output

    def terminate(self):
        if self.running is True:
            os.killpg(os.getpgid(self.current_shell.pid), signal.SIGKILL)  # Send the signal to all the process groups
            self.running = False
            return True
        else:
            return False
