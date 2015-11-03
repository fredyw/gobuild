# gobuild
A small Python script to build a Go program.

`gobuild` requires the project to use the [standard Go workspace](https://golang.org/doc/code.html).

`gobuild` runs `gofmt`, `golint`, and `govet`.

### Software Requirements
1. Python 2.7+
2. Go Lint (`go get -u github.com/golang/lint/golint`)

### Usage:
    usage: gobuild.py [-h] [--clean] [--package] [--test]
                      [--test-package TEST_PACKAGE] [--test-case TEST_CASE]
    
    optional arguments:
      -h, --help                   show this help message and exit
      --clean                      cleans the project
      --package                    creates a package
      --test                       runs the tests
      --test-package TEST_PACKAGE  runs a specific test package
      --test-case TEST_CASE        runs a specific test case
