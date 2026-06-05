"""Symbol-aware code chunker.

Chunks code by structural units (function, method, class, interface, enum)
rather than fixed-size windows. Each chunk gets rich metadata for retrieval.

Chunk types:
- function: standalone function or arrow function
- method: class method (includes constructor)
- class: class-level overview (signature + constructor + method list)
- interface: interface definition
- file: fallback for files without parsed symbols (windowed)
"""

import hashlib
from intelligence_engine.parser.base import ParsedFile
from intelligence_engine.symbols.models import Symbol, ImportRef
from intelligence_engine.symbols.calls import CallRef
from .models import CodeChunk

# Max content size per chunk (chars) — prevents huge class bodies from bloating index
MAX_CHUNK_CONTENT = 3000


class Chunker:
    """Produces CodeChunks from parsed files, using symbol boundaries."""

    def chunk(
        self,
        parsed: ParsedFile,
        symbols: list[Symbol] | None = None,
        imports: list[ImportRef] | None = None,
        calls: list[CallRef] | None = None,
    ) -> list[CodeChunk]:
        """Create chunks from a parsed file.

        Args:
            parsed: Parsed source file
            symbols: Extracted symbols (functions, methods, classes)
            imports: Import references for this file
            calls: Call references for this file

        Returns:
            List of CodeChunks with metadata
        """
        lines = parsed.source.splitlines()

        if not symbols:
            return self._by_window(parsed, lines)

        # Separate symbols by kind
        classes = [s for s in symbols if s.kind in ("class", "interface", "enum")]
        functions = [s for s in symbols if s.kind in ("function", "method")]

        # Build imports metadata for this file
        file_imports = [imp.module for imp in (imports or []) if imp.file_path == parsed.path]

        # Build calls lookup: caller_qualified_name -> [callee_names]
        calls_by_caller: dict[str, list[str]] = {}
        for call in (calls or []):
            if call.caller_file_path == parsed.path:
                calls_by_caller.setdefault(call.caller_qualified_name, []).append(call.callee_name)

        chunks: list[CodeChunk] = []

        # 1. Class-level overview chunks (signature + method signatures)
        for cls in classes:
            content = self._build_class_overview(cls, functions, lines)
            method_names = [
                s.name for s in functions
                if s.qualified_name and s.qualified_name.startswith(f"{cls.name}.")
            ]
            metadata = {
                "imports": file_imports,
                "methods": method_names,
                "type": cls.kind,
            }
            chunks.append(self._make(
                parsed, content, cls.line_start, cls.line_end,
                cls.qualified_name or cls.name, cls.kind, metadata,
            ))

        # 2. Function/method-level chunks (the main retrieval unit)
        for fn in functions:
            content = "\n".join(lines[max(fn.line_start - 1, 0):fn.line_end])
            # Truncate very long functions
            if len(content) > MAX_CHUNK_CONTENT:
                content = content[:MAX_CHUNK_CONTENT] + "\n// ... (truncated)"

            fn_calls = calls_by_caller.get(fn.qualified_name or fn.name, [])
            # Deduplicate calls
            unique_calls = list(dict.fromkeys(fn_calls))

            metadata = {
                "imports": file_imports,
                "calls": unique_calls[:20],  # cap to avoid huge metadata
                "type": fn.kind,
            }

            # Add parent class info if method
            if fn.qualified_name and "." in fn.qualified_name:
                metadata["class"] = fn.qualified_name.split(".")[0]

            chunks.append(self._make(
                parsed, content, fn.line_start, fn.line_end,
                fn.qualified_name or fn.name, fn.kind, metadata,
            ))

        # 3. File-level chunk for small files without symbols (e.g. config, constants)
        if not chunks:
            return self._by_window(parsed, lines)

        return chunks

    def _build_class_overview(
        self, cls: Symbol, all_functions: list[Symbol], lines: list[str]
    ) -> str:
        """Build a class overview: declaration + method signatures (not full bodies)."""
        # Get class declaration line(s) — first few lines
        cls_start = max(cls.line_start - 1, 0)
        # Find opening brace or first method
        header_end = min(cls_start + 5, cls.line_end, len(lines))
        header = "\n".join(lines[cls_start:header_end])

        # Collect method signatures
        methods = [
            s for s in all_functions
            if s.qualified_name and s.qualified_name.startswith(f"{cls.name}.")
        ]
        sigs = []
        for m in methods:
            sig = m.signature or m.name
            if not sig.strip():
                # Fallback: first line of method
                if m.line_start - 1 < len(lines):
                    sig = lines[m.line_start - 1].strip()
            sigs.append(f"  {sig}")

        overview = header
        if sigs:
            overview += "\n\n  // Methods:\n" + "\n".join(sigs[:30])

        # Cap size
        if len(overview) > MAX_CHUNK_CONTENT:
            overview = overview[:MAX_CHUNK_CONTENT]

        return overview

    def _by_window(self, parsed: ParsedFile, lines: list[str], size: int = 120) -> list[CodeChunk]:
        """Fallback: fixed-size window chunks for files without symbols."""
        chunks = []
        for start in range(0, len(lines), size):
            end = min(start + size, len(lines))
            content = "\n".join(lines[start:end])
            chunks.append(self._make(
                parsed, content, start + 1, end, None, "file", {},
            ))
        return chunks

    def _make(
        self, parsed: ParsedFile, content: str, start: int, end: int,
        symbol: str | None, kind: str = "", metadata: dict | None = None,
    ) -> CodeChunk:
        """Create a CodeChunk with deterministic ID."""
        raw = f"{parsed.path}:{start}:{end}:{symbol or ''}:{content[:64]}"
        cid = hashlib.sha1(raw.encode()).hexdigest()
        return CodeChunk(
            chunk_id=cid,
            file_path=parsed.path,
            language=parsed.language,
            content=content,
            line_start=start,
            line_end=end,
            symbol=symbol,
            kind=kind,
            summary="",
            metadata=metadata or {},
        )
