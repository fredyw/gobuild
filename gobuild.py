#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Fredy Wijaya
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = 'Fredy Wijaya'

import argparse, shutil, sys, subprocess, os, zipfile

# put your source packages here
source_packages = [
]

# put your third party packages here
third_party_packages = [
]

all_packages = third_party_packages + source_packages

# put your test packages here
test_packages = [
]

# any target compilation, leave it empty
cross_compilations = [
]

# the name of the executable
executables = []
# the release directory
release_dir = ''
# the release archive file
release_file = ''

files_to_remove = [
    'bin',
    'pkg',
    release_dir,
    release_file,
]

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=80))
    parser.add_argument('--clean', action='store_true', dest='clean',
                        help='clean the project')
    parser.add_argument('--package', action='store_true', dest='package',
                        help='create a package')
    parser.add_argument('--test', action='store_true', dest='test',
                       help='run the tests')
    parser.add_argument('--test-package', type=str, dest='test_package',
                       help='run a specific test package')
    parser.add_argument('--test-case', type=str, dest='test_case',
                       help='run a specific test case')
    parser.add_argument('--cross-compile', action='store_true', dest='cross_compile',
                        help='cross-compile the build')
    parser.add_argument('--no-govet', action='store_true', dest='no_govet',
                        help='run go vet')
    parser.add_argument('--no-golint', action='store_true', dest='no_golint',
                        help='run go lint')

    args = parser.parse_args()
    if args.test_package is not None:
        if not args.test:
            error_and_exit('--test option is required for --test-package option')
    if args.test_case is not None:
        if not args.test:
            error_and_exit('--test option is required for --test-case option')
        if args.test_package is None:
            error_and_exit('--test-package option is required for --test-case option')
    return args

def error(msg):
    print 'Error:', msg

def error_and_exit(msg):
    error(msg)
    sys.exit(1)

def build_packages(args):
    for package in all_packages:
        # only do gofmt, golint, and govet on source packages
        env_vars = os.environ.copy()
        if 'GOPATH' in env_vars:
            env_vars['GOPATH'] = os.getcwd() + os.pathsep + env_vars['GOPATH']
        else:
            env_vars['GOPATH'] = os.getcwd()
        if package in source_packages:
            gofmt(package, env_vars)
            if not args.no_golint:
                golint(package, env_vars)
            if not args.no_govet:
                govet(package, env_vars)
        cmd = ['go', 'install', package]
        cmd_str = ' '.join(cmd)
        if args.cross_compile:
            for cross_compilation in cross_compilations:
                env_vars['GOOS'] = cross_compilation[0]
                env_vars['GOARCH'] = cross_compilation[1]
                if subprocess.call(cmd, env=env_vars) != 0:
                    error_and_exit('Got a non-zero exit code while executing ' + cmd_str)
        else:
            if subprocess.call(cmd, env=env_vars) != 0:
                error_and_exit('Got a non-zero exit code while executing ' + cmd_str)

def run_tests(args):
    if args.test_package is not None:
        if args.test_case is not None:
            # run all tests in a particular test package
            cmd = ['go', 'test', args.test_package, '-run', args.test_case, '-v']
            cmd_str = ' '.join(cmd)
            env_vars = os.environ.copy()
            env_vars['GOPATH'] = os.getcwd()
            if subprocess.call(cmd, env=env_vars) != 0:
                error_and_exit('Got a non-zero exit code while executing ' + cmd_str)
        else:
            # run a specific test case in a particular test package
            cmd = ['go', 'test', args.test_package, '-v']
            cmd_str = ' '.join(cmd)
            env_vars = os.environ.copy()
            env_vars['GOPATH'] = os.getcwd()
            if subprocess.call(cmd, env=env_vars) != 0:
                error_and_exit('Got a non-zero exit code while executing ' + cmd_str)
    else:
        # run all tests in all test packages
        for test_package in test_packages:
            cmd = ['go', 'test', test_package, '-v']
            cmd_str = ' '.join(cmd)
            env_vars = os.environ.copy()
            env_vars['GOPATH'] = os.getcwd()
            if subprocess.call(cmd, env=env_vars) != 0:
                error_and_exit('Got a non-zero exit code while executing ' + cmd_str)

def clean():
    for f in files_to_remove:
        if os.path.exists(f):
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)

def create_package():
    if not os.path.isdir(release_dir):
        os.makedirs(release_dir)
    execs = []
    for root, dirs, files in os.walk('bin'):
        for f in files:
            for executable in executables:
                if f.startswith(executable):
                    execs.append(os.path.join(root, f))
    for exc in execs:
        shutil.copy2(exc, release_dir)
    with zipfile.ZipFile(release_file, 'w') as zf:
        for root, dirs, files in os.walk(release_dir):
            for f in files:
                zf.write(os.path.join(root, f))

def gofmt(pkg, env_vars):
    cmd = ['go', 'fmt', pkg]
    cmd_str = ' '.join(cmd)
    if subprocess.call(cmd, env=env_vars) != 0:
        error_and_exit('Got a non-zero exit code while executing ' + cmd_str)

def govet(pkg, env_vars):
    cmd = ['go', 'vet', pkg]
    cmd_str = ' '.join(cmd)
    if subprocess.call(cmd, env=env_vars) != 0:
        error_and_exit('Got a non-zero exit code while executing ' + cmd_str)

def golint(pkg, env_vars):
    cmd = ['golint', pkg]
    cmd_str = ' '.join(cmd)
    if subprocess.call(cmd, env=env_vars) != 0:
        error_and_exit('Got a non-zero exit code while executing ' + cmd_str)

def main(args):
    if args.clean:
        clean()
    else:
        build_packages(args)
        if args.test:
            run_tests(args)
        if args.package:
            create_package()

if __name__ == '__main__':
    args = parse_args()
    main(args)
