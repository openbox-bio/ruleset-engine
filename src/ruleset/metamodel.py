import os
from textx import language, metamodel_from_file

@language('ruleset', '*.ruleset')
def ruleset_lang():
    """
    RuleSet data validation DSL
    """
    grammar_path = os.path.join(os.path.dirname(__file__), 'RuleSet.tx')
    return metamodel_from_file(grammar_path)