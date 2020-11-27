import sys, os
import argparse as ap
import subprocess

def base_prefix():
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

def in_virtualenv():
    return base_prefix() != sys.prefix

def parse_args():
    parser = ap.ArgumentParser(description='helper script to install pip requirements')
    parser.add_argument('reqs', nargs='+')
    parser.add_argument('--ignore-check-venv', action='store_const' ,const=False, default=True, dest='check_venv')
    parser.add_argument('--upgrade', action='store_const', const=True, default=False, dest='upgrade')
    return parser.parse_args()

def ask_yes_no(question):
    while True:
        ans = input(question + ' (y/n): ')
        if ans in ['y', 'yes']:
            return True
        elif ans in ['n', 'no']:
            return False
        else:
            print("Expect 'y' or 'n' ('yes' or 'no')")

pip_exec = "pip"
venv_folder_check = ['venv']

if __name__ == "__main__":
    args = parse_args()
    
    if args.check_venv and not in_virtualenv():
        print("You are not in virtual environment.")
        venv_found = False
        for venv_folder in venv_folder_check:
            if os.path.isdir(venv_folder):
                pip_path_suppose = os.path.join('.', venv_folder, 'bin', pip_exec)
                if os.path.isfile(pip_path_suppose) and os.access(pip_path_suppose, os.X_OK):
                    if ask_yes_no(f'Use {pip_path_suppose}?'):
                        pip_exec = pip_path_suppose
                        venv_found = True
                        break
                    else:
                        venv_found = 'declined'
        if not venv_found:
            print("Did not found folders:", venv_folder_check)
            if ask_yes_no("Do you want to create venv?"):
                venv_folder = 'venv'
                print(f"Creating ./{venv_folder}")
                subprocess.check_call([sys.executable, "-m", "venv", venv_folder])
                pip_path_suppose = os.path.join('.', venv_folder, 'bin', pip_exec)
                if os.path.isfile(pip_path_suppose) and os.access(pip_path_suppose, os.X_OK):
                    pip_exec = pip_path_suppose
                else:
                    raise Exception("pip not found at {pip_path_suppose}")
            else:
                sys.exit()
        elif venv_found == 'declined':
            sys.exit()

    print('Using pip:', pip_exec)
    
    for req in args.reqs:
        if args.upgrade:
            subprocess.check_call([pip_exec, "install", "--upgrade", "-r", req])
        else:
            subprocess.check_call([pip_exec, "install", "-r", req])
        
    
