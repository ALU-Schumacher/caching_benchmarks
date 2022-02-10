#by Benjamin Rottler

import subprocess

def bash_command(cmd):
    """Execute a bash command, returns the stdout and stderr output.

    Arguments:
        cmd (str): The command to execute.
    Returns:
    (str, str): Stdout and stderr output of the command.
    """

    output, error = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    return output.decode("ascii"), error.decode("ascii")
