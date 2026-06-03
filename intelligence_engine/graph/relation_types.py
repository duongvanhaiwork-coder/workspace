"""Graph edge relation types per architecture spec (section 4.4)."""

IMPORTS = "imports"
EXPORTS = "exports"
DEFINES = "defines"
CALLS = "calls"
READS = "reads"
WRITES = "writes"
EXTENDS = "extends"
IMPLEMENTS = "implements"
USES_MODEL = "uses_model"
USES_DTO = "uses_dto"
ROUTE_TO_HANDLER = "route_to_handler"

# Legacy alias
REFERENCES = "references"
ROUTE = "route"

# Priority for retrieval ranking (section 9.4)
RELATION_PRIORITY = {
    DEFINES: 1,
    REFERENCES: 2,
    CALLS: 3,
    READS: 3,
    WRITES: 3,
    USES_DTO: 4,
    USES_MODEL: 4,
    IMPORTS: 5,
    EXPORTS: 5,
    EXTENDS: 4,
    IMPLEMENTS: 4,
    ROUTE_TO_HANDLER: 2,
}
