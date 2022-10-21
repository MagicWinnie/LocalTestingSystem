"""
This is a little script to run a program through tests.
By @MagicWinnie (Github)

The tester should be launched from a directory where the program and tests folder are located:
directory/         <--- project directory
    autotester.py  <--- tester
    main.py        <--- program we want to run
    tests/         <--- directory with input/ and output/ folders
        input/
            1.*
            2.*
            ...
            N.*
        output/
            1.*
            2.*
            ...
            N.*
Otherwise the script will not work.

The tester:
    * accepts four parameters: python autotester.py --help
    * is located within a single file
    * it can be moved to other projects
    * works only with stdin, stdout, and stderr
    * does not delete or modify files
    * written for python3
"""
import os
from argparse import ArgumentParser
import subprocess
from typing import List, Tuple


def check_exec(exec_path: str) -> None:
    """Sanity checks for file

    Args
        exec_path (str): Executable filename
    """
    assert exec_path in os.listdir('.'), f"File {exec_path} does not exist"


def load_tests(tests_path: str) -> Tuple[List, List]:
    """Sanity checks for tests directory

    Args:
        tests_path (str): Path to tests directory

    Returns:
        Tuple[List, List]: Returns sorted lists of files from input/ and output/, respectively
    """
    
    assert os.path.isdir(tests_path), f"Directory {tests_path} does not exist"
    assert os.path.isdir(os.path.join(tests_path, 'input')), f"Directory {tests_path}/input does not exist"
    assert os.path.isdir(os.path.join(tests_path, 'output')), f"Directory {tests_path}/output does not exist"
    assert len(os.listdir(os.path.join(tests_path, 'input'))) > 0, f"Directory {tests_path}/input is empty"
    assert len(os.listdir(os.path.join(tests_path, 'output'))) > 0, f"Directory {tests_path}/output is empty"
    input_files = os.listdir(os.path.join(tests_path, 'input'))
    output_files = os.listdir(os.path.join(tests_path, 'output'))
    try:
        input_files.sort(key=lambda x: int(os.path.splitext(x)[0]))
        output_files.sort(key=lambda x: int(os.path.splitext(x)[0]))
    except ValueError:
        print(f"Directories {tests_path}/input or {tests_path}/output contain bad files (filename != int)")
    assert len(input_files) == len(output_files), f"Directories {tests_path}/input or {tests_path}/output contain different amount of files"
    return input_files, output_files
    

def run_tests(cmd: str, exec_path: str, tests_path: str, time_limit: int=1) -> None:
    """Run program on tests

    Args:
        cmd (str): Command to run executable
        exec_path (str): Filename of executable
        tests_path (str): Directory to tests folder
        time_limit (int, optional): Timeout in seconds. Defaults to 1.
    """
    check_exec(exec_path)
    input_files, output_files = load_tests(tests_path)
    no_of_good_tests = 0
    for i in range(len(input_files)):
        print('--------------------------------------')
        print(f"TEST #{i + 1}/{len(input_files)}:")

        assert input_files[i] == output_files[i], f"Input test filename {input_files[i]} does not correspond to {output_files[i]}"

        # run program and pass to its stdin the input file
        input_file = open(os.path.join(tests_path, 'input', input_files[i]), 'r')
        command = f'{cmd} {exec_path}'.strip()
        try:
            p = subprocess.check_output(command, stdin=input_file, stderr=subprocess.PIPE, timeout=time_limit)
        except subprocess.CalledProcessError as e:
            print("Runtime Error:")
            print(e.stderr.decode().strip())
            input_file.close()
            continue
        except subprocess.TimeoutExpired:
            print("Timeout Error")
            input_file.close()
            continue
        input_file.close()
        
        # get outputs from program and correct
        program_output = p.decode().strip()
        output_file = open(os.path.join(tests_path, 'output', output_files[i]), 'r')
        correct_output = '\n'.join(map(str.strip, output_file.readlines()))
        output_file.close()

        if program_output == correct_output:
            print("Correct")
            no_of_good_tests += 1
        else:
            print("Wrong answer")
    print('--------------------------------------')
    print(f"Passed {no_of_good_tests}/{len(input_files)} tests")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("cmd", type=str, help="Command to run executable")
    parser.add_argument("exec", type=str, help="Filename of executable (e.g. main.py for Python, main.class for Java, main.exe for C/C++)")
    parser.add_argument("tests", type=str, help="Path to tests (directory with input/ and output/ folders containing tests)")
    parser.add_argument("-tl", "--timelimit", type=int, help="Time limit for a test")
    args = parser.parse_args()

    run_tests(args.cmd, args.exec, args.tests, args.timelimit)
