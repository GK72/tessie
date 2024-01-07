import tools

def run_test(test_args: dict):
    tools.file_match(".*3\.14.*", "test/nonexistent.txt", verbose=True)

    tools.file_match(".*3\.14.*", "test/input.txt", verbose=True)
    tools.file_contains_line("Lorem ipsum dolor sit amet", "test/input.txt", verbose=True)

    tools.file_match(".* bla .*", "test/input.txt", verbose=True)
    tools.file_contains_line("Lorem ipsum", "test/input.txt", verbose=True)

    tools.expect_eq(2, 2)
    tools.expect_eq(2, 4)

    tools.expect_gt(2, 2)
    tools.expect_gt(5, 4)
