import os
import sys
import subprocess


def install_req(venv_bin, fullpath):
    print("Install requirements.txt")
    with subprocess.Popen(
        [
            os.path.join(venv_bin, 'pip'),
            'install',
            '-r',
            os.path.join(fullpath, 'requirements.txt')
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True
    ) as p:
        for line in p.stdout:
            print(line, end='')

        if p.returncode != 0:
            print(
                'error in pip install requirements.txt, look at pip_error.log')
            with open('pip_error.log', 'w') as fd:
                fd.write(p.stderr.read())
            sys.exit(2)


def init_venv(python_path):

    bin_path = 'Scripts' if sys.platform == 'win32' else 'bin'

    fullpath = os.getcwd()
    _, project_name = os.path.split(fullpath)
    home_dir = os.environ['USERPROFILE'] if sys.platform == 'win32' else os.environ['HOME']
    venv_path = os.path.join(
        home_dir, '.virtualenvs', project_name)
    print("venv_path ", venv_path)

    output, error = subprocess.Popen(
        [python_path, "-m", "venv", venv_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()

    if error:
        with open('virtualenv_error.log', 'w') as fd:
            fd.write(error.decode('utf-8'))
            print("An error occurred with virtualenv")
            sys.exit(2)

    venv_bin = os.path.join(venv_path, bin_path)
    print(os.path.join(venv_bin, "activate"))
    if sys.platform == "win32":
        output, error = subprocess.Popen(
            ["cmd", "/c", "mklink", "activate_venv.bat",
                os.path.join(venv_bin, "activate.bat")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()
    else:
        output, error = subprocess.Popen(
            ["ln", "-s", os.path.join(venv_bin, "activate"), "activate_venv"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()
    if error:
        print('Couldn\'t create symbolic link')

    install_req(venv_bin, fullpath)


if __name__ == "__main__":
    if (int(sys.version.split('.')[0]) < 3):
        print("Please start this script with python 3 or above")
    print("Start process")
    python_path = sys.executable
    init_venv(python_path)
