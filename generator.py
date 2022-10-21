"""
This is a little script to generate correct outputs for tests using an ideal program.
By @MagicWinnie (Github, Telegram)

The generator should be launched from a directory where the program and tests folder are located:
directory/         <--- project directory
    generator.py   <--- generator
    main.py        <--- program we want to run
    tests/         <--- directory with input/ and output/ folders
        input/
            1.*
            2.*
            ...
            N.*
        output/
            1.*    <--- these files will be generated
            2.*    <--- these files will be generated
            ...
            N.*    <--- these files will be generated
Otherwise the script will not work.

The generator:
    * accepts three parameters: python generator.py --help
    * is located within a single file
    * it can be moved to other projects
    * works only with stdin, stdout, and stderr
    * written for python3
"""
import os
from argparse import ArgumentParser
import subprocess
from typing import List


def check_exec(exec_path: str) -> None:
    """Sanity checks for file

    Args
        exec_path (str): Executable filename
    """
    assert exec_path in os.listdir('.'), f"File {exec_path} does not exist"


def load_tests(tests_path: str) -> List:
    """Sanity checks for tests directory and create output if does not exist

    Args:
        tests_path (str): Path to tests directory

    Returns:
        List: Returns sorted list of files from input/
    """
    
    assert os.path.isdir(tests_path), f"Directory {tests_path} does not exist"
    assert os.path.isdir(os.path.join(tests_path, 'input')), f"Directory {tests_path}/input does not exist"
    assert len(os.listdir(os.path.join(tests_path, 'input'))) > 0, f"Directory {tests_path}/input is empty"
    if not os.path.isdir(os.path.join(tests_path, 'output')):
        os.mkdir(os.path.join(tests_path, 'output'))
    input_files = os.listdir(os.path.join(tests_path, 'input'))
    try:
        input_files.sort(key=lambda x: int(os.path.splitext(x)[0]))
    except ValueError:
        print(f"Directory {tests_path}/input contains bad files (filename != int)")
    return input_files
    

def run_tests(cmd: str, exec_path: str, tests_path: str) -> None:
    """Run program on tests

    Args:
        cmd (str): Command to run executable
        exec_path (str): Filename of executable
        tests_path (str): Directory to tests folder
    """
    check_exec(exec_path)
    input_files = load_tests(tests_path)
    for i in range(len(input_files)):
        print('--------------------------------------')
        print(f"TEST #{i + 1}/{len(input_files)}:")

        # run program and pass to its stdin the input file
        input_file = open(os.path.join(tests_path, 'input', input_files[i]), 'r')
        command = f'{cmd} {exec_path}'.strip()
        try:
            p = subprocess.check_output(command, stdin=input_file, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print("Runtime Error:")
            print(e.stderr.decode().strip())
            input_file.close()
            continue
        input_file.close()
        
        # get outputs from program and correct
        program_output = p.decode().strip()
        output_file = open(os.path.join(tests_path, 'output', input_files[i]), 'w')
        output_file.write(program_output)
        output_file.close()
        print("Generated")
    print('--------------------------------------')
    print("Done")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("cmd", type=str, help="Command to run executable")
    parser.add_argument("exec", type=str, help="Filename of executable (e.g. main.py for Python, main.class for Java, main.exe for C/C++)")
    parser.add_argument("tests", type=str, help="Path to tests (directory with input/ and output/ folders containing tests)")
    args = parser.parse_args()

    run_tests(args.cmd, args.exec, args.tests)
