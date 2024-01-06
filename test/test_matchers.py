import tools

def run_test(test_args: dict):
    tools.file_contains_pattern("res/nonexistent.txt", ".*3\.14.*", verbose=True)

    tools.file_contains_pattern("res/test-output.txt", ".*3\.14.*", verbose=True)
    tools.file_contains_line("res/test-output.txt", "Lorem ipsum dolor sit amet", verbose=True)

    tools.file_contains_pattern("res/test-output.txt", ".* bla .*", verbose=True)
    tools.file_contains_line("res/test-output.txt", "Lorem ipsum", verbose=True)

    tools.expect_eq(2, 2)
    tools.expect_eq(2, 4)

    tools.expect_gt(2, 2)
    tools.expect_gt(5, 4)
