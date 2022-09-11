from random import choice, shuffle, randint
from time import time
import collections

def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):
        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': code_max + j
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_stairway_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(i + j)
        rule = {
            'if': {
                log_oper: items
            },
            'then': i + j + 1
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_ring_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = generate_stairway_rules(code_max, n_max, n_generate - 1, log_oper_choice)
    log_oper = choice(log_oper_choice)  # not means and-not (neither)
    if n_max < 2:
        n_max = 2
    n_items = randint(2, n_max)
    items = []
    for i in range(0, n_items):
        items.append(code_max - i)
    rule = {
        'if': {
            log_oper: items
        },
        'then': 0
    }
    rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_random_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': randint(1, code_max)
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_seq_facts(M):
    facts = list(range(0, M))
    shuffle(facts)
    return facts


def generate_rand_facts(code_max, M):
    facts = []
    for i in range(0, M):
        facts.append(randint(0, code_max))
    return facts


def correct_rules(rules):
    conflict_list = []
    for fir in range(len(rules)):
        for sec in range(fir+1, len(rules)):
            if 'and' in rules[fir]['if'] and 'and' in rules[sec]['if']:
                if collections.Counter(rules[fir]['if']['and']) == collections.Counter(rules[sec]['if']['and']):
                    conflict_list.append(fir)
            elif 'or' in rules[fir]['if'] and 'or' in rules[sec]['if']:
                if collections.Counter(rules[fir]['if']['or']) == collections.Counter(rules[sec]['if']['or']):
                    conflict_list.append(fir)
            elif 'not' in rules[fir]['if'] and 'not' in rules[sec]['if']:
                if collections.Counter(rules[fir]['if']['not']) == collections.Counter(rules[sec]['if']['not']):
                    conflict_list.append(fir)
    return conflict_list

#  samples:
print(generate_simple_rules(100, 4, 10))
print(generate_random_rules(100, 4, 10))
print(generate_stairway_rules(100, 4, 10, ["or"]))
print(generate_ring_rules(100, 4, 10, ["or"]))

#  generate rules and facts and check time
time_start = time()
N = 10000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print("%d rules generated in %f seconds" % (N, time() - time_start))
time_start = time()
conflict = correct_rules(rules)
conflict.sort(reverse=True)
print(conflict)
result_facts = []
print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))
for i in conflict:
    rules.pop(i)
for one_rule in rules:
    if 'and' in one_rule['if']:
        if all(one_rule['if']['and']) in facts:
            result_facts.append(one_rule['then'])
    elif 'or' in one_rule['if']:
        if any(one_rule['if']['or']) in facts:
            result_facts.append(one_rule['then'])
    elif 'not' in one_rule['if']:
        if all(one_rule['if']['not']) not in facts:
            result_facts.append(one_rule['then'])
#  YOUR CODE HERE

#  check facts vs rules


# YOUR CODE HERE


print(facts)
print(result_facts)
