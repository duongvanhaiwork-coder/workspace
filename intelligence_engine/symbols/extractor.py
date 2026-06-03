import ast
import re
from intelligence_engine.parser.base import ParsedFile
from .models import Symbol

JS_FUNC_RE = re.compile(
    r"(?:export\s+)?(?:async\s+)?function\s+(?P<name>[A-Za-z_$][\w$]*)"
    r"|(?:const|let|var)\s+(?P<var>[A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\(?[^=]*?\)?\s*=>"
)
CLASS_RE = re.compile(r"(?:export\s+)?class\s+(?P<name>[A-Za-z_$][\w$]*)")
CS_RE = re.compile(
    r"\b(?:class|interface|record)\s+(?P<name>[A-Za-z_][\w]*)"
    r"|\b(?:public|private|protected|internal).*?\s+(?P<method>[A-Za-z_][\w]*)\s*\("
)


class SymbolExtractor:
    def extract(self, parsed: ParsedFile) -> list[Symbol]:
        if parsed.language == "python":
            return self._python(parsed)
        if parsed.tree is not None:
            return self._tree_sitter(parsed)
        return self._regex(parsed)

    def _python(self, parsed: ParsedFile) -> list[Symbol]:
        out: list[Symbol] = []
        try:
            tree = ast.parse(parsed.source)
        except SyntaxError:
            return out
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                out.append(Symbol(
                    node.name, "class", parsed.path,
                    node.lineno, getattr(node, "end_lineno", node.lineno), node.name,
                    qualified_name=node.name,
                ))
                # Methods inside this class
                for item in ast.walk(node):
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item is not node:
                        qname = f"{node.name}.{item.name}"
                        out.append(Symbol(
                            item.name, "method", parsed.path,
                            item.lineno, getattr(item, "end_lineno", item.lineno),
                            item.name, qualified_name=qname,
                        ))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Only top-level functions (not nested in class — those are handled above)
                # Check parent isn't a class by seeing if it's at module level
                pass

        # Separate pass for top-level functions only
        if hasattr(tree, 'body'):
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    out.append(Symbol(
                        node.name, "function", parsed.path,
                        node.lineno, getattr(node, "end_lineno", node.lineno),
                        node.name, qualified_name=node.name,
                    ))

        return sorted(out, key=lambda s: (s.line_start, s.name))

    def _tree_sitter(self, parsed: ParsedFile) -> list[Symbol]:
        """Extract symbols using tree-sitter AST."""
        out: list[Symbol] = []
        source_bytes = parsed.source.encode("utf-8")
        root = parsed.tree.root_node()
        self._walk_ts_node(root, parsed.source, source_bytes, parsed, out, parent_class=None)
        return sorted(out, key=lambda s: (s.line_start, s.name))

    def _walk_ts_node(
        self, node, source: str, source_bytes: bytes,
        parsed: ParsedFile, out: list[Symbol],
        parent_class: str | None = None,
    ) -> None:
        node_kind = node.kind()

        # Class / interface declarations
        if node_kind in ("class_declaration", "interface_declaration"):
            name_node = node.child_by_field_name("name")
            if name_node:
                name = self._node_text(name_node, source_bytes)
                kind = "class" if node_kind == "class_declaration" else "interface"
                out.append(Symbol(
                    name, kind, parsed.path,
                    node.start_position().row + 1,
                    node.end_position().row + 1,
                    name,
                    qualified_name=name,
                ))
                # Recurse children with parent_class set
                for i in range(node.child_count()):
                    self._walk_ts_node(
                        node.child(i), source, source_bytes, parsed, out,
                        parent_class=name,
                    )
            return  # Already recursed children

        # Method definitions (inside class body)
        if node_kind == "method_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                name = self._node_text(name_node, source_bytes)
                qualified = f"{parent_class}.{name}" if parent_class else name
                out.append(Symbol(
                    name, "method", parsed.path,
                    node.start_position().row + 1,
                    node.end_position().row + 1,
                    self._node_first_line(node, source_bytes),
                    qualified_name=qualified,
                ))
            # Don't recurse into method body for symbol extraction
            return

        # Function declarations (top-level or exported)
        if node_kind == "function_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                name = self._node_text(name_node, source_bytes)
                out.append(Symbol(
                    name, "function", parsed.path,
                    node.start_position().row + 1,
                    node.end_position().row + 1,
                    self._node_first_line(node, source_bytes),
                    qualified_name=name,
                ))
            return

        # Variable declarations with arrow functions: const foo = () => ...
        if node_kind == "lexical_declaration":
            for i in range(node.child_count()):
                child = node.child(i)
                if child.kind() == "variable_declarator":
                    name_node = child.child_by_field_name("name")
                    value_node = child.child_by_field_name("value")
                    if name_node and value_node and value_node.kind() == "arrow_function":
                        name = self._node_text(name_node, source_bytes)
                        qualified = f"{parent_class}.{name}" if parent_class else name
                        out.append(Symbol(
                            name, "function", parsed.path,
                            node.start_position().row + 1,
                            node.end_position().row + 1,
                            self._node_first_line(node, source_bytes),
                            qualified_name=qualified,
                        ))
            return  # Don't recurse into children again

        # Recurse for other node types
        for i in range(node.child_count()):
            self._walk_ts_node(
                node.child(i), source, source_bytes, parsed, out,
                parent_class=parent_class,
            )

    @staticmethod
    def _node_text(node, source_bytes: bytes) -> str:
        """Get the source text of a node using byte offsets correctly."""
        br = node.byte_range()
        return source_bytes[br.start:br.end].decode("utf-8", errors="replace")

    @staticmethod
    def _node_first_line(node, source_bytes: bytes) -> str:
        """Get first line of node as signature using byte offsets correctly."""
        br = node.byte_range()
        text = source_bytes[br.start:br.end].decode("utf-8", errors="replace")
        first_line = text.split("\n", 1)[0]
        return first_line[:200]

    def _regex(self, parsed: ParsedFile) -> list[Symbol]:
        out: list[Symbol] = []
        is_csharp = parsed.language == "csharp"
        for i, line in enumerate(parsed.source.splitlines(), start=1):
            if is_csharp:
                for m in CS_RE.finditer(line):
                    name = m.group("name") or m.group("method")
                    kind = "class" if m.group("name") else "method"
                    out.append(Symbol(name, kind, parsed.path, i, i, line.strip()))
            else:
                for m in CLASS_RE.finditer(line):
                    out.append(Symbol(m.group("name"), "class", parsed.path, i, i, line.strip()))
                for m in JS_FUNC_RE.finditer(line):
                    name = m.group("name") or m.group("var")
                    out.append(Symbol(name, "function", parsed.path, i, i, line.strip()))
        return out
