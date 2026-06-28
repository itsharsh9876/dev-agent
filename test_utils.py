import pytest

def test_add_normal_cases():
    assert add(2.5, 3) == 5.5
    assert add(-1.0, 1.0) == 0.0
    assert add(10.0, 0.0) == 10.0

def test_add_edge_cases():
    with pytest.raises(TypeError):
        add("hello", 3)
    with pytest.raises(TypeError):
        add(2.5, "world")
    with pytest.raises(TypeError):
        add(None, 1.0)

def test_subtract_normal_cases():
    assert subtract(2.5, 3) == -0.5
    assert subtract(-1.0, 1.0) == -2.0
    assert subtract(10.0, 0.0) == 10.0

def test_subtract_edge_cases():
    with pytest.raises(TypeError):
        subtract("hello", 3)
    with pytest.raises(TypeError):
        subtract(2.5, "world")
    with pytest.raises(TypeError):
        subtract(None, 1.0)

def test_add_and_subtract_error_cases():
    with pytest.raises(TypeError):
        add("hello", "world")
    with pytest.raises(TypeError):
        subtract("hello", 3)
```