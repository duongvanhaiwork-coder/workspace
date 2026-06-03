from intelligence_engine.scanner.scanner import Scanner

def test_skip_node_modules():
    s = Scanner(exclude=["node_modules"])
    assert s.extensions
