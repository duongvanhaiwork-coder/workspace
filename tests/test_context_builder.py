from intelligence_engine.context.context_builder import ContextBuilder

def test_context_builder():
    text = ContextBuilder().build([{"file_path":"a.py","start_line":1,"end_line":1,"content":"x=1"}])
    assert "a.py" in text
