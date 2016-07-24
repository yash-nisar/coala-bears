from tests.LocalBearTestHelper import verify_local_bear


# Sample code, replace with your own test code.

good_file = """def good_name
  test if something
end
""".splitlines(keepends=True)


bad_file = """def badName
  test if something
end
""".splitlines(keepends=True)


# Add more test methods with settings and/or configuration files.
# Writing Tests documentation available at:
# http://coala.readthedocs.io/en/latest/Users/Tutorials/Testing_Bears.html

TestBearTest = verify_local_bear(
    TestBear,
    valid_files=(good_file,),
    invalid_files=(bad_file),)
