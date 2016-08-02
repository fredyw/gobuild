# gobuild
A small Python script to build a Go program.

`gobuild` requires the project to use the [standard Go workspace](https://golang.org/doc/code.html).

`gobuild` runs `gofmt`, `golint`, and `govet`.

### Software Requirements
1. Python 2.7+
2. Go Lint (`go get -u github.com/golang/lint/golint`) - optional

### Usage:
    usage: gobuild.py [-h] [--clean] [--package] [--test]
                      [--test-package TEST_PACKAGE] [--test-case TEST_CASE]
                      [--cross-compile] [--no-govet] [--no-golint]

    optional arguments:
      -h, --help                   show this help message and exit
      --clean                      clean the project
      --package                    create a package
      --test                       run the tests
      --test-package TEST_PACKAGE  run a specific test package
      --test-case TEST_CASE        run a specific test case
      --cross-compile              cross-compile the build
      --no-govet                   run go vet
      --no-golint                  run go lint