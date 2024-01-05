#!/usr/bin/env python3

import concurrent.futures
import inspect
import os
import time


class EnvironmentMeta(type):
    """An Environment metaclass that will be used for suite class creation.
    """

    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'init') and
                callable(subclass.init))

class SuiteMeta(type):
    """A Suite metaclass that will be used for suite class creation.
    """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'init') and
                callable(subclass.init))

class ISuite(metaclass=SuiteMeta):
    pass

class IEnvironment(metaclass=EnvironmentMeta):
    """This interface is used for concrete classes to inherit from.
    There is no need to define the EnvironmentMeta methods as they
    are implicitly made available via .__subclasscheck__().
    """

    _suites: []

    def __init__(self, config: dict = dict()):
        self._suites = []

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def add_suite(self, *args):
        for elem in args:
            self._suites.append(elem)

    def run(self):
        # print("Config:")
        # for elem in self.config:
        #     print(f"{elem}: {self.config[elem]}")

        print("Suites:")
        n_proc = os.cpu_count()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=n_proc/2)

        for elem in self._suites:
            pool.submit(elem.run())

        pool.shutdown(wait=True)

class ISuite(metaclass=SuiteMeta):
    """This interface is used for concrete classes to inherit from.
    There is no need to define the SuiteMeta methods as they
    are implicitly made available via .__subclasscheck__().
    """
    _par_test_cases: []
    _seq_test_cases: []

    def __init__(self, config: dict = dict()):
        test_methods = filter(lambda x: x.startswith("test_") and callable(getattr(self, x)), dir(self))
        test_methods = [getattr(self, elem) for elem in test_methods]
        self._config = config
        self._par_test_cases = [elem for elem in test_methods if inspect.signature(elem).parameters['parallel'].default]
        self._seq_test_cases = [elem for elem in test_methods if not inspect.signature(elem).parameters['parallel'].default]

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def run(self):
        print("Config:")
        for elem in self.config:
            print(f"{elem}: {self.config[elem]}")

        print("Sequential test cases:")
        for elem in self._seq_test_cases:
            elem()

        print("Parallel test cases:")
        n_proc = os.cpu_count()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=n_proc/2)

        for elem in self._par_test_cases:
            pool.submit(elem)

        # pool.shutdown(wait=True)

class DockerEnvironment(IEnvironment):
    def init(self, config: dict):
        self.config = config

class FilterSuite(ISuite):
    def init(self, config: dict):
        self.config = config

    def test_case_1(self, parallel=False):
        print(inspect.currentframe().f_code.co_name)

    def test_case_2(self, parallel=False):
        print(inspect.currentframe().f_code.co_name)

    def test_case_3(self, parallel=True):
        print(inspect.currentframe().f_code.co_name)

    def test_case_4(self, parallel=True):
        for i in range(1, 4):
            time.sleep(1)
        print(inspect.currentframe().f_code.co_name)

    def test_case_5(self, parallel=True):
        print(inspect.currentframe().f_code.co_name)

class EventSendingSuite(ISuite):
    def init(self, config: dict):
        self.config = config

    def test_case_1(self, parallel=False):
        print(inspect.currentframe().f_code.co_name)

    def test_case_2(self, parallel=False):
        print(inspect.currentframe().f_code.co_name)

    def test_case_3(self, parallel=True):
        print(inspect.currentframe().f_code.co_name)

    def test_case_4(self, parallel=True):
        for i in range(1, 4):
            time.sleep(1)
        print(inspect.currentframe().f_code.co_name)

    def test_case_5(self, parallel=True):
        print(inspect.currentframe().f_code.co_name)


def main():
    print(f"{FilterSuite.__name__} {'is' if issubclass(FilterSuite, ISuite) else 'isn`t'} the subclass of {ISuite.__name__}.")

    f_suite = FilterSuite()
    f_suite.init({"cica": "kutya"})

    print(f"{EventSendingSuite.__name__} {'is' if issubclass(EventSendingSuite, ISuite) else 'isn`t'} the subclass of {ISuite.__name__}.")

    es_suite = EventSendingSuite()
    es_suite.init({"tyúk": "kakas"})

    print(f"{DockerEnvironment.__name__} {'is' if issubclass(DockerEnvironment, IEnvironment) else 'isn`t'} the subclass of {IEnvironment.__name__}.")

    d_env = DockerEnvironment()
    d_env.init({"kutya": "cica"})
    d_env.add_suite(f_suite, es_suite)
    d_env.run()

if __name__ == "__main__":
    main()


# CONFIG

#  containers:
  #  kafka:
    #  env:
    #  image:
    #  network: test-network
  #  parser:
    #  env:
      #  EEA_LOGLEVEL: 7
    #  image:
    #  network: test-network
  #  schema-registry:
    #  env:
    #  image:
    #  network: test-network

#  networks:
  #  test-network:
    #  containers:
      #  - kafka
      #  - parser
      #  - schema-registry
