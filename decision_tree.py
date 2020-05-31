# coding=utf=8
"""
Implementacja algorytmu Quinlana ID3 tworzenia binarnych drzew decyzyjnych.
"""

import math
from operator import itemgetter

DATA_PATH = 'data.csv'
DECISION_NAME = ['Nie pracuj.', 'Może pracuj', 'Pracuj.']
DATA_NAME = {
    'czy_zagraniczna': ['nie', 'tak'],
    'mozliwosci_rozwoju': ['małe', 'średnie', 'duże'],
    'wielkosc_firmy': ['mała', 'średnia', 'duża'],
    'typ_firmy': ['startup', 'korporacja', 'firma państwowa'],
    'wynagrodzenie': ['brak', 'małe', 'średnie', 'duże']
}


def entropy(target):
    """Data entropy."""
    if not target:
        return 0
    result = 0
    for i in range(2):
        p = target.count(i) / len(target)
        if p:
            result -= p * math.log2(p)
    return result


def entropy_after_decision(target, data, var_name, var_names, var_value):
    """Calculate entropy after decision."""
    index = var_names.index(var_name)
    decision_plus = []
    decision_minus = []
    decision_plus_data = []
    decision_minus_data = []
    for i in range(len(data)):
        if data[i][index] == var_value:
            decision_plus.append(target[i])
            decision_plus_data.append(data[i])
        else:
            decision_minus.append(target[i])
            decision_minus_data.append(data[i])
    p_plus = len(decision_plus) / len(target)
    p_minus = 1 - p_plus
    return p_plus * entropy(decision_plus) + p_minus * entropy(decision_minus),\
           (decision_plus, decision_plus_data, decision_minus, decision_minus_data), var_name, var_value


def make_var_max_dict(data, var_names):
    """Make decision var dict."""
    result = {}
    for i in range(len(var_names)):
        mx = 0
        for j in range(len(data)):
            if data[j][i] > mx:
                mx = data[j][i]
        result[var_names[i]] = mx
    return result


class LeafNode:
    """Leaf decision tree node."""
    def __init__(self, decision, text):
        self.decision = decision
        self.text = text

    def __str__(self):
        return self.text + str(self.decision)

    def decide(self, _):
        """Return leaf node decision."""
        return self.decision


class DecisionNode:
    """Decision tree node."""
    def __init__(self, data, target, var_names):
        base = entropy(target)
        decisions = []
        var_max_dict = make_var_max_dict(data, var_names)
        for var_name in var_names:
            for val in range(var_max_dict[var_name]):
                decisions.append(entropy_after_decision(target, data, var_name, var_names, val))
        decisions.sort(key=itemgetter(0))
        self.question_var = decisions[0][2]
        self.question_value = decisions[0][3]
        if not entropy(decisions[0][1][0]):
            if decisions[0][1][0]:
                self.yes_decision = LeafNode(decisions[0][1][0][0], "Yes -> ")
            else:
                self.yes_decision = LeafNode(decisions[0][1][2][0], "Yes -> ")
        else:
            self.yes_decision = DecisionNode(decisions[0][1][1], decisions[0][1][0], var_names)
        if not entropy(decisions[0][1][2]):
            if decisions[0][1][2]:
                self.no_decision = LeafNode(decisions[0][1][2][0], "No -> ")
            else:
                self.no_decision = LeafNode(decisions[0][1][0][0], "No -> ")
        else:
            self.no_decision = DecisionNode(decisions[0][1][3], decisions[0][1][2], var_names)
        self.text = f"Does {self.question_var} equals {self.question_value}?"

    def __str__(self):
        return self.text

    def decide(self, instance):
        """Decide based on value."""
        if instance[self.question_var] == self.question_value:
            return self.yes_decision.decide(instance)
        else:
            return self.no_decision.decide(instance)


def print_tree(root, indent=0):
    """Recursively print decision tree."""
    dash = "|-" * indent
    blank = "| " * indent
    if isinstance(root, LeafNode):
        print(blank + f"Decyzja: {DECISION_NAME[root.decide(None)]}")
    else:
        print(blank + f"Pytanie: Czy {root.question_var} równe jest {DATA_NAME[root.question_var][root.question_value]}?")
        print(blank + "Tak:")
        print_tree(root.yes_decision, indent+1)
        print(blank + "Nie:")
        print_tree(root.no_decision, indent+1)


if __name__ == '__main__':
    in_file = open(DATA_PATH)
    header = in_file.readline().split(',')[:-1]
    x_data = []
    y_data = []
    dict_data = []
    for line in in_file:
        *x_instance, decision = (int(x) for x in line.strip().split(','))
        x_data.append(x_instance)
        y_data.append(decision)
        dict_data.append({key: val for key, val in zip(header, x_instance)})
    print(dict_data)
    decision_tree = DecisionNode(x_data, y_data, header)

    for i in range(len(dict_data)):
        print(dict_data[i])
        print(f"True: {y_data[i]}")
        print(f"Decision: {decision_tree.decide(dict_data[i])}")
        if y_data[i] != decision_tree.decide(dict_data[i]):
            input()
    print_tree(decision_tree)
