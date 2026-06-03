"""Tests for prompt templates — intent-aware guidance for LLM."""

from intelligence_engine.context.intent import QueryIntent
from intelligence_engine.context.prompt_templates import (
    get_prompt_template,
    get_base_rules,
)


def test_base_rules_content():
    """Base rules should contain essential instructions."""
    rules = get_base_rules()
    assert "ONLY" in rules
    assert "hallucinate" in rules
    assert "file paths" in rules or "Cite" in rules


def test_all_intents_have_templates():
    """Every QueryIntent should produce a non-empty template."""
    for intent in QueryIntent:
        template = get_prompt_template(intent)
        assert template, f"Empty template for {intent}"
        assert len(template) > 50, f"Template too short for {intent}"


def test_search_template_focus():
    """SEARCH template should focus on references and locations."""
    template = get_prompt_template(QueryIntent.SEARCH)
    assert "DEFINED" in template or "definition" in template.lower()
    assert "IMPORTED" in template or "import" in template.lower()


def test_explain_template_focus():
    """EXPLAIN template should focus on flow and entrypoints."""
    template = get_prompt_template(QueryIntent.EXPLAIN)
    assert "entrypoint" in template.lower() or "flow" in template.lower()
    assert "dependency" in template.lower() or "chain" in template.lower()


def test_refactor_template_focus():
    """REFACTOR template should mention DTO, Entity, migration."""
    template = get_prompt_template(QueryIntent.REFACTOR)
    assert "DTO" in template
    assert "Entity" in template or "entity" in template
    assert "migration" in template.lower()


def test_debug_template_focus():
    """DEBUG template should focus on writes, call chain, conditions."""
    template = get_prompt_template(QueryIntent.DEBUG)
    assert "WRITTEN" in template or "write" in template.lower()
    assert "CALL CHAIN" in template or "call chain" in template.lower()


def test_impact_template_focus():
    """IMPACT template should mention blast radius and dependents."""
    template = get_prompt_template(QueryIntent.IMPACT)
    assert "dependents" in template.lower() or "depend" in template.lower()
    assert "risk" in template.lower()


def test_test_template_focus():
    """TEST template should mention edge cases and mocking."""
    template = get_prompt_template(QueryIntent.TEST)
    assert "edge case" in template.lower()
    assert "mock" in template.lower()


def test_generate_template_focus():
    """GENERATE template should mention existing patterns."""
    template = get_prompt_template(QueryIntent.GENERATE)
    assert "pattern" in template.lower()
    assert "naming" in template.lower() or "convention" in template.lower()


def test_base_rules_included_in_all_templates():
    """All templates should include the base rules."""
    base = get_base_rules()
    for intent in QueryIntent:
        template = get_prompt_template(intent)
        # Base rules are formatted into the template
        assert "ONLY" in template
        assert "hallucinate" in template
