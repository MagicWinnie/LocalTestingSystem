# LocalTestingSystem

Two scripts to test your programs on tests:  

## `autotester.py`
This is a little script to run a program through tests.  

The tester should be launched from a directory where the program and tests folder are located:  
```
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
```
Otherwise the script will not work.

The tester:  
* accepts four parameters: `python autotester.py --help`  
* is located within a single file  
* it can be moved to other projects  
* works only with `stdin`, `stdout`, and `stderr`  
* does not delete or modify files  
* written for `python3`  

## `generator.py`
This is a little script to generate correct outputs for tests using an ideal program.  

The generator should be launched from a directory where the program and tests folder are located:  
```
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
```
Otherwise the script will not work.  

The generator:
* accepts three parameters: `python generator.py --help`
* is located within a single file
* it can be moved to other projects
* works only with `stdin`, `stdout`, and `stderr`
* written for `python3`