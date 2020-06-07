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
        self.rule_base = [rule for rule in rule_base]

    @abstractmethod
    def run(self):
        NotImplementedError()

    def output_results(self):
        return self.knowledge_base


class ForwardChaining(BaseChaining):
    def __init__(self, rule_base, knowledge_base):
        super().__init__(rule_base, knowledge_base)

    def run(self):
        self.forward_run()

    def forward_run(self):
        while rule := pop_first_match(self.rule_base, lambda r: r.passes_knowledge_check(self.knowledge_base)):
            self.knowledge_base.add(rule.result)


class BackwardChaining(BaseChaining):
    def __init__(self, rule_base, knowledge_base):
        super().__init__(rule_base, knowledge_base)

    def run(self):
        for rule in self.rule_base:
            if resolved := self.resolve_backwards(rule):
                self.knowledge_base.add(resolved)

    def resolve_backwards(self, rule):
        if not rule:
            return None

        first = True if rule.first in self.knowledge_base else self.resolve_backwards(
            find_first_match(self.rule_base, lambda r: r.result == rule.first))
        second = True if rule.second in self.knowledge_base else self.resolve_backwards(
            find_first_match(self.rule_base, lambda r: r.result == rule.second))

        if first and second:
            return rule.result

        return None


class MixedChaining(BackwardChaining, ForwardChaining):
    def __init__(self, rule_base, knowledge_base):
        super().__init__(rule_base, knowledge_base)

    def run(self):

        for rule in self.rule_base:
            if resolved := self.resolve_backwards(rule):
                self.knowledge_base.add(resolved)
            else:
                break

        self.forward_run()


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
        Rule(first="duża firma", second="brak klauzuli poufności", result="korporacja"),
        Rule(first="wiecej niż 50 pracowników", second="długie projekty", result="duża firma"),
        Rule(first="mniej niz 50 pracowników", second="krótkie projekty", result="mała firma"),
        Rule(first="mała firma", second="brak klauzuli poufności", result="startup"),
        Rule(first="duża firma", second="calkowita klauzula poufności", result="firma państwowa")
    ]
    knowledge = ["wiecej niż 50 pracowników", "długie projekty", "brak klauzuli poufności"]

    forward_chaining = inference_factory(InferenceType.FORWARD_CHAINING, rules, knowledge)
    forward_chaining.run()

    backwards_chaining = inference_factory(InferenceType.BACKWARD_CHAINING, rules, knowledge)
    backwards_chaining.run()

    print(backwards_chaining.output_results())

    mixed_chaining = inference_factory(InferenceType.MIXED_CHAINING, rules, knowledge)
    mixed_chaining.run()

    assert forward_chaining.output_results() == backwards_chaining.output_results()
    assert forward_chaining.output_results() == mixed_chaining.output_results()
