# Tess(ie) The Tester

A framework for functional testing.

Try it out with the following command:

```sh
tessie/tess.py res/base.py --port 8080
```

# Contributing

Checkers can be run via `ci/check.sh`. It will assume a Python virtual
environment in `~/.venv/def` and activate it. If it cannot find the virtual
environment, it will run it in the native environment.

# Testing the tester

* regression-test.sh        Script for running the test
* input.txt                 Input for regression test
* reference.txt             Expectation
* test_regression.py        The test itself

Updating the reference file:

```sh
./tessie/tess.py test/test_regression.py > test/reference.txt
```

# Project structure

```
├── ci                  CI pipeline related files
├── res                 Resources (like example tests)
├── tessie              Python module / Source code
│   ├── internal.py     Implementation details
│   ├── tess.py         Entrypoint
│   └── tools.py        Utility library
└── test                Regression tests
```
