from abc import ABC, abstractmethod
from typing import Set, Callable, Optional


class Rule:
    def __init__(self, first, second, result):
        self.first = first
        self.second = second
        self.result = result

    def passes_knowledge_check(self, knowledge_base):
        return self.first in knowledge_base and self.second in knowledge_base


def pop_first_match(elements: [Rule], func: Callable) -> Optional[Rule]:
    for i in range(len(elements)):
        if func(elements[i]):
            return elements.pop(i)


def find_first_match(elements: [Rule], func: Callable) -> Optional[Rule]:
    for i in range(len(elements)):
        if func(elements[i]):
            return elements[i]


class InferenceType:
    FORWARD_CHAINING = 0
    BACKWARD_CHAINING = 1
    MIXED_CHAINING = 2


class BaseChaining(ABC):
    rule_base: [Rule]
    knowledge_base: Set[str]

    def __init__(self, rule_base, knowledge_base):
        self.knowledge_base = set(knowledge_base)
        self.rule_base = rule_base

    @abstractmethod
    def run(self):
        NotImplementedError()

    def output_results(self):
        return self.knowledge_base


class ForwardChaining(BaseChaining):
    def __init__(self, rule_base, knowledge_base):
        super().__init__(rule_base, knowledge_base)

    def run(self):
        while rule := pop_first_match(self.rule_base, lambda r: r.passes_knowledge_check(self.knowledge_base)):
            self.knowledge_base.add(rule.result)


class BackwardChaining(BaseChaining):
    def __init__(self, rule_base, knowledge_base):
        self.regression_stack = []
        super().__init__(rule_base, knowledge_base)

    def run(self):
        self.regression_stack = [rule for rule in self.rule_base if not rule.passes_knowledge_check(self.knowledge_base)]

        for rule in self.regression_stack:
            rule = find_first_match(self.rule_base, lambda r: r.result == rule.result)
            if not rule.passes_knowledge_check(self.knowledge_base):
                self.regression_stack.append(rule)


class MixedChaining(BaseChaining):
    def __init__(self, rule_base, knowledge_base):
        super().__init__(rule_base, knowledge_base)

    def run(self):
        while rule := pop_first_match(self.rule_base, lambda r: r.passes_knowledge_check(self.knowledge_base)):
            self.knowledge_base.add(rule.result)


def inference_factory(inference_type, rule_base, knowledge_base):
    if inference_type == InferenceType.FORWARD_CHAINING:
        return ForwardChaining(rule_base, knowledge_base)

    if inference_type == InferenceType.BACKWARD_CHAINING:
        return BackwardChaining(rule_base, knowledge_base)

    if inference_type == InferenceType.MIXED_CHAINING:
        return MixedChaining(rule_base, knowledge_base)

    raise ValueError("Invalid inference type")


if __name__ == '__main__':
    rules = [
        Rule(first="wiecej niż 50 pracowników", second="długie projekty", result="duża firma"),
        Rule(first="duża firma", second="brak klauzuli poufności", result="korporacja"),
        Rule(first="mniej niz 50 pracowników", second="krótkie projekty", result="mała firma"),
        Rule(first="mała firma", second="brak klauzuli poufności", result="startup"),
        Rule(first="duża firma", second="calkowita klauzula poufności", result="firma państwowa")
    ]
    knowledge = ["wiecej niż 50 pracowników", "długie projekty", "brak klauzuli poufności"]

    forward_chaining = inference_factory(InferenceType.FORWARD_CHAINING, rules, knowledge)
    forward_chaining.run()


