import json
import os
import select
import shlex
import subprocess
import sys
import click


def main_call_cmd():
    """Sample to call a command and get back it's output to work with"""
    code, output, error = run_cmd('hockeyapp apps list', live=False)
    print('Code')
    print(code)

    print('Output')
    print(output)

    print('Error')
    print(error)

    print('Before data')
    data = json.loads('{}'.format(output), 'utf-8')
    print(data)
    print('After data')


def run_cmd(cmd, live=True, readsize=2, working_dir=None, env=None):
    """Live outputs the script call and captures the output"""
    if live:
        click.secho(cmd, fg='white', bold=True)

    if env is None:
        env = os.environ

    cmdargs = shlex.split(cmd)
    p = subprocess.Popen(cmdargs, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

    stdout = ''
    stderr = ''
    rpipes = [p.stdout, p.stderr]
    while True:
        rfd, wfd, efd = select.select(rpipes, [], rpipes, 1)

        if p.stdout in rfd:
            dat = os.read(p.stdout.fileno(), readsize)
            if live:
                sys.stdout.write(dat)
            stdout += dat
            if dat == '':
                rpipes.remove(p.stdout)
        if p.stderr in rfd:
            dat = os.read(p.stderr.fileno(), readsize)
            stderr += dat
            if live:
                sys.stdout.write(dat)
            if dat == '':
                rpipes.remove(p.stderr)
        # only break out if we've emptied the pipes, or there is nothing to
        # read from and the process has finished.
        if (not rpipes or not rfd) and p.poll() is not None:
            break
        # Calling wait while there are still pipes to read can cause a lock
        elif not rpipes and p.poll() is None:
            p.wait()

    return p.returncode, stdout, stderr


if __name__ == '__main__':
    main_call_cmd()