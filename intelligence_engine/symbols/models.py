from dataclasses import dataclass


@dataclass
class Symbol:
    name: str
    kind: str  # class | method | function | property | import | route | interface | enum
    file_path: str
    start_line: int
    end_line: int
    signature: str = ""
    qualified_name: str = ""  # e.g. OrderService.createOrder
    symbol_id: str = ""  # e.g. business-lounge-api:OrderService.createOrder


@dataclass
class ImportRef:
    module: str
    file_path: str
    line: int
