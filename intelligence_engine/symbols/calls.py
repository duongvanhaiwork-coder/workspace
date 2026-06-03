"""Call extraction — extract function/method calls from source using tree-sitter.

Produces CallRef entries that the GraphBuilder can use to create CALLS edges.
"""

from dataclasses import dataclass
from intelligence_engine.parser.base import ParsedFile
from .models import Symbol


@dataclass
class CallRef:
    """A call from one symbol to another."""

    caller_qualified_name: str
    caller_file_path: str
    caller_line_start: int
    callee_name: str  # bare name or member expression (e.g. "this.configService.get")
    call_line: int


class CallExtractor:
    """Extract call references from parsed files using tree-sitter."""

    def extract(self, parsed: ParsedFile, symbols: list[Symbol]) -> list[CallRef]:
        """Extract calls within each symbol's body.

        Args:
            parsed: The parsed file (must have tree for tree-sitter path).
            symbols: Symbols already extracted from this file.

        Returns:
            List of CallRef representing calls made within each symbol.
        """
        if parsed.tree is None:
            return []

        source_bytes = parsed.source.encode("utf-8")
        root = parsed.tree.root_node()

        # Build line ranges for each symbol so we can attribute calls to callers
        # Sort by line_start descending so inner (more specific) ranges match first
        sym_ranges = sorted(
            [(s.line_start, s.line_end, s) for s in symbols if s.kind in ("method", "function")],
            key=lambda x: (-x[0], x[1]),
        )

        # Collect all call_expression nodes
        call_nodes: list[tuple[int, str]] = []  # (line, callee_name)
        self._find_calls(root, source_bytes, call_nodes)

        # Attribute each call to its enclosing symbol
        refs: list[CallRef] = []
        for call_line, callee_name in call_nodes:
            caller = self._find_enclosing_symbol(call_line, sym_ranges)
            if caller is None:
                continue
            refs.append(CallRef(
                caller_qualified_name=caller.qualified_name or caller.name,
                caller_file_path=parsed.path,
                caller_line_start=caller.line_start,
                callee_name=callee_name,
                call_line=call_line,
            ))

        return refs

    def _find_calls(self, node, source_bytes: bytes, out: list[tuple[int, str]]) -> None:
        """Recursively find call_expression nodes and extract callee names."""
        node_kind = node.kind()

        if node_kind == "call_expression":
            func_node = node.child_by_field_name("function")
            if func_node:
                callee = self._extract_callee_name(func_node, source_bytes)
                if callee:
                    line = node.start_position().row + 1
                    out.append((line, callee))

        # Also handle new_expression (constructor calls)
        elif node_kind == "new_expression":
            constructor_node = node.child_by_field_name("constructor")
            if constructor_node:
                callee = self._node_text(constructor_node, source_bytes)
                if callee:
                    line = node.start_position().row + 1
                    out.append((line, callee))

        for i in range(node.child_count()):
            self._find_calls(node.child(i), source_bytes, out)

    def _extract_callee_name(self, node, source_bytes: bytes) -> str:
        """Extract a useful callee name from a call expression's function node.

        Handles:
        - identifier: `doSomething` → "doSomething"
        - member_expression: `this.service.method` → "service.method"
        - member_expression: `obj.method` → "obj.method"
        """
        node_kind = node.kind()

        if node_kind == "identifier":
            return self._node_text(node, source_bytes)

        if node_kind == "member_expression":
            return self._extract_member_chain(node, source_bytes)

        # Fallback: try to get text directly
        text = self._node_text(node, source_bytes)
        if text and len(text) < 100:
            return text
        return ""

    def _extract_member_chain(self, node, source_bytes: bytes) -> str:
        """Extract member chain, stripping `this.` prefix.

        `this.configService.get` → "configService.get"
        `super.method` → "method"
        `obj.prop.method` → "obj.prop.method"
        """
        parts: list[str] = []
        current = node

        while current and current.kind() == "member_expression":
            prop = current.child_by_field_name("property")
            if prop:
                parts.append(self._node_text(prop, source_bytes))
            current = current.child_by_field_name("object")

        # Add the root object
        if current:
            root_text = self._node_text(current, source_bytes)
            if root_text not in ("this", "super"):
                parts.append(root_text)

        parts.reverse()
        return ".".join(parts)

    @staticmethod
    def _node_text(node, source_bytes: bytes) -> str:
        br = node.byte_range()
        return source_bytes[br.start:br.end].decode("utf-8", errors="replace")

    @staticmethod
    def _find_enclosing_symbol(
        line: int, sym_ranges: list[tuple[int, int, Symbol]],
    ) -> Symbol | None:
        """Find the most specific (innermost) symbol enclosing a given line."""
        for start, end, sym in sym_ranges:
            if start <= line <= end:
                return sym
        return None
