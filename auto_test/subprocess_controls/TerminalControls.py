import subprocess


class TerminalControls:

    @staticmethod
    def get_sourced_shell(source):
        return subprocess.Popen('source ' + source, shell=True,
                                universal_newlines=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")

    @staticmethod
    def perform_command(shell, command):
        return subprocess.Popen(command, shell=True, universal_newlines=True, stdin=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
