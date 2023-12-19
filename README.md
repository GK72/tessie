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

# Project structure

├── ci                  CI pipeline related files
├── res                 Resources (like example tests)
└── tessie              Python module / Source code
    ├── tess.py         Entrypoint
    └── tools.py        Utility library
