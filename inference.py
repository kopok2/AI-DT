from abc import ABC, abstractmethod
from typing import Set, Callable, Optional, List


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


def first_goal_in_output(goal: List[str], output: Set[str]) -> Optional[str]:
    for g in goal:
        if g in output:
            return g
    return None


class InferenceType:
    FORWARD_CHAINING = 0
    BACKWARD_CHAINING = 1
    MIXED_CHAINING = 2


class BaseChaining(ABC):
    rule_base: [Rule]
    knowledge_base: Set[str]
    goals: List[str]

    def __init__(self, rule_base, knowledge_base, goals):
        self.knowledge_base = set(knowledge_base)
        self.rule_base = [rule for rule in rule_base]
        self.goals = goals

    @abstractmethod
    def run(self):
        NotImplementedError()

    def output_result(self):
        return first_goal_in_output(self.goals, self.knowledge_base)


class ForwardChaining(BaseChaining):
    def __init__(self, rule_base, knowledge_base, goals):
        super().__init__(rule_base, knowledge_base, goals)

    def run(self):
        self.forward_run()

    def forward_run(self):
        while rule := pop_first_match(self.rule_base, lambda r: r.passes_knowledge_check(self.knowledge_base)):
            self.knowledge_base.add(rule.result)


class BackwardChaining(BaseChaining):
    def __init__(self, rule_base, knowledge_base, goals):
        super().__init__(rule_base, knowledge_base, goals)

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
    def __init__(self, rule_base, knowledge_base, goals):
        super().__init__(rule_base, knowledge_base, goals)

    def run(self):

        for rule in self.rule_base:
            if resolved := self.resolve_backwards(rule):
                self.knowledge_base.add(resolved)
            else:
                break

        self.forward_run()


def inference_factory(inference_type, rule_base, knowledge_base, goals: List[str]):
    if inference_type == InferenceType.FORWARD_CHAINING:
        return ForwardChaining(rule_base, knowledge_base, goals)

    if inference_type == InferenceType.BACKWARD_CHAINING:
        return BackwardChaining(rule_base, knowledge_base, goals)

    if inference_type == InferenceType.MIXED_CHAINING:
        return MixedChaining(rule_base, knowledge_base, goals)

    raise ValueError("Invalid inference type")


if __name__ == '__main__':

    with open('salary.csv', 'r') as f:
        for line in f.readlines()[1:]:
            goals = ["brak", "małe", "średnie", "duże"]
            city = ["nie duże miasto", "duże miasto"]
            position = ["tester", "frontend", 'backend']
            experience = ["junior", "mid", "senior"]

            values = [int(i) for i in line.split(",")]
            knowledge = [city[values[0]], position[values[1]], experience[values[2]]]

            rules = [
                Rule(first="junior", second="frontend", result="brak"),
                Rule(first="junior", second="tester", result="brak"),
                Rule(first="junior", second="backend", result="stażysta na backendzie"),
                Rule(first="duże miasto", second="stażysta na backendzie", result="małe"),
                Rule(first="nie duże miasto", second="stażysta na backendzie", result="brak"),
                Rule(first="mid", second="tester", result="mid tester"),
                Rule(first="nie duże miasto", second="mid tester", result="małe"),
                Rule(first="duże miasto", second="mid tester", result="średnie"),
                Rule(first="mid", second="frontend", result="średnie"),
                Rule(first="mid", second="backend", result="średnie"),
                Rule(first="duże miasto", second="senior", result="duże"),
                Rule(first="nie duże miasto", second="senior", result="średnie"),
            ]

            forward_chaining = inference_factory(InferenceType.FORWARD_CHAINING, rules, knowledge, goals)
            forward_chaining.run()

            backwards_chaining = inference_factory(InferenceType.BACKWARD_CHAINING, rules, knowledge, goals)
            backwards_chaining.run()

            mixed_chaining = inference_factory(InferenceType.MIXED_CHAINING, rules, knowledge, goals)
            mixed_chaining.run()
            print(backwards_chaining.output_result())

    with open('progress.csv', 'r') as f:
        for line in f.readlines()[1:]:
            goals = ["małe", "średnie", "duże"]
            old_tech = ["stare technologie", "nie stare technologie"]
            project_type = ["legacy", "nowy projekt", "do napisania"]
            change_team = ["nie zmiana drużyny", "tylko w wyjątkowych", "często zmiana drużyny"]

            values = [int(i) for i in line.split(",")]
            knowledge = [old_tech[values[0]], project_type[values[1]], change_team[values[2]]]

            rules = [
                Rule(first="stare technologie", second="legacy", result="małe"),
                Rule(first="nie stare technologie", second="legacy", result="małe"),
                Rule(first="stare technologie", second="do napisania", result="średnie"),
                Rule(first="stare technologie", second="nowy projekt", result="małe"),
                Rule(first="nie stare technologie", second="nowy projekt", result="szansa dużego rozwoju"),
                Rule(first="nie stare technologie", second="do napisania", result="szansa dużego rozwoju"),
                Rule(first="szansa dużego rozwoju", second="tylko w wyjątkowych", result="duże"),
                Rule(first="szansa dużego rozwoju", second="często zmiana drużyny", result="duże"),
                Rule(first="szansa dużego rozwoju", second="nie zmiana drużyny", result="średnie"),
            ]

            forward_chaining = inference_factory(InferenceType.FORWARD_CHAINING, rules, knowledge, goals)
            forward_chaining.run()

            backwards_chaining = inference_factory(InferenceType.BACKWARD_CHAINING, rules, knowledge, goals)
            backwards_chaining.run()

            mixed_chaining = inference_factory(InferenceType.MIXED_CHAINING, rules, knowledge, goals)
            mixed_chaining.run()
            print(backwards_chaining.output_result())
