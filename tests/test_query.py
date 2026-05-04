from appbasics import QCgen

data = {
    'a': 1,
    'b': 1.23,
    'c': 'Hello'
}

def test_simpleQuery():
    a1 = QCgen.condition('a', '=', 1)
    assert a1.passed(data) == True
    