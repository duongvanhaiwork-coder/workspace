from pathlib import Path
from intelligence_engine.parser.base import ParsedFile
from intelligence_engine.symbols.extractor import SymbolExtractor


def test_python_symbols():
    source = """
class UserService:
    def get_user(self, uid):
        return uid

async def main():
    pass
"""
    parsed = ParsedFile(path="service.py", language="python", source=source)
    symbols = SymbolExtractor().extract(parsed)

    names = [s.name for s in symbols]
    assert "UserService" in names
    assert "get_user" in names
    assert "main" in names


def test_python_syntax_error():
    source = "def broken(:"
    parsed = ParsedFile(path="bad.py", language="python", source=source)
    symbols = SymbolExtractor().extract(parsed)
    assert symbols == []


def test_typescript_regex_fallback():
    source = """export class AuthController {}
function login() {}
const logout = async () => {}
"""
    parsed = ParsedFile(path="auth.ts", language="typescript", source=source, tree=None)
    symbols = SymbolExtractor().extract(parsed)

    names = [s.name for s in symbols]
    assert "AuthController" in names
    assert "login" in names
    assert "logout" in names


def test_csharp_regex():
    source = """public class OrderService {
    public async Task<Order> GetOrder(int id) {
        return null;
    }
}
"""
    parsed = ParsedFile(path="Order.cs", language="csharp", source=source, tree=None)
    symbols = SymbolExtractor().extract(parsed)

    names = [s.name for s in symbols]
    assert "OrderService" in names
    assert "GetOrder" in names


def test_no_duplicates_js():
    source = "export class Foo {}"
    parsed = ParsedFile(path="foo.js", language="javascript", source=source, tree=None)
    symbols = SymbolExtractor().extract(parsed)
    assert len(symbols) == 1
    assert symbols[0].name == "Foo"
