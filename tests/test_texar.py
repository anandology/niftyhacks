from niftyhacks.texar import parse

archive1 = """
== numbers.txt
1
2
3
== sum.txt
6
"""

def test_parse():
    files = parse(archive1)
    assert sorted(files.keys()) == ["numbers.txt", "sum.txt"]
    assert files == {
        "numbers.txt": "1\n2\n3\n",
        "sum.txt": "6\n"
    }
