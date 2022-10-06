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


#  generate rules and facts and check time
time_start = time()
N = 100000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print("%d rules generated in %f seconds" % (N, time() - time_start))
time_start = time()


def all_rules(rules_list):
    not_rules = []
    or_rules = []
    and_rules = []

    for one_rule in rules_list:
        lus = [{1: list(one_rule['if'].values())[0]}, one_rule['then']]
        if 'not' in one_rule['if'].keys():
            if lus not in not_rules:
                not_rules.append(lus)
            continue
        if 'and' in one_rule['if'].keys():
            if lus not in and_rules:
                and_rules.append(lus)
            continue
        if 'or' in one_rule['if'].keys():
            if lus not in or_rules:
                or_rules.append(lus)
            continue
    return not_rules, and_rules, or_rules


def check_or(or_rules, rang, res, or_mass, max_rang):
    for or_rule in or_rules:

        buf = list(or_rule[0].values())[0]
        if rang in or_rule[0]:
            for i in range(len(buf)):

                if buf[i] in facts:
                    max_rang = 2
                    or_mass.append(
                        {2: or_rule[1]})
                    res[or_rule[1]] = 1
                    break
        else:
            for or_mini in or_mass:

                if rang in or_mini and res[or_rule[1]] != 1:
                    if list(or_mini.values())[0] in buf:
                        max_rang = rang + 1
                        or_mass.append(
                            {max_rang: or_rule[1]})
                        res[or_rule[1]] = 1
    return max_rang


def ab_not_ab(not_rules, and_rules, or_rules):
    """Удаляем факты  a=b, not a=b"""

    for neg in not_rules:
        for pos in or_rules:

            if neg[1] == pos[1] and list(neg[0]).sort == list(pos[0]).sort:
                not_rules.remove(neg)
                or_rules.remove(pos)

        for pos in and_rules:

            if neg[1] == pos[1] and list(neg[0]).sort == list(pos[0]).sort:
                not_rules.remove(neg)
                and_rules.remove(pos)


def check_not(not_rules, res):
    for rule in not_rules:
        flag = 1
        buf = list(rule[0].values())[0]
        for i in range(len(rule[0])):
            if buf[i] in facts or buf[i] in res:
                flag = 0
                break
        if flag == 1:
            res[rule[1]] = 1


def not_a_b_not_b_a(not_rules):
    """Удаляем правило not a=b, not b=a"""
    for one_rule in not_rules:
        buf = list(one_rule[0].values())[0]
        if len(buf) == 1:
            for rule in not_rules:
                if buf[0] == rule[1]:
                    not_rules.remove(one_rule, rule)


def main():

    res = [None] * 10100
    res_facts = []
    or_mass = []
    rang = 1
    max_rang = 1
    not_rules, and_rules, or_rules = all_rules(rules)
    not_a_b_not_b_a(not_rules)

    while rang <= max_rang:
        ab_not_ab(not_rules, and_rules, or_rules)
        for or_rule in or_rules:

            buf = list(or_rule[0].values())[0]
            if rang in or_rule[0]:
                for i in range(len(buf)):

                    if buf[i] in facts:
                        max_rang = 2
                        or_mass.append(
                            {2: or_rule[1]})
                        res[or_rule[1]] = 1
                        break
            else:
                for or_mini in or_mass:

                    if rang in or_mini and res[or_rule[1]] != 1:
                        if list(or_mini.values())[0] in buf:
                            max_rang = rang + 1
                            or_mass.append(
                                {max_rang: or_rule[1]})
                            res[or_rule[1]] = 1
        check_not(not_rules, res)
        rang += 1

    index = 0
    while index < 10100:
        if res[index] == 1:
            res_facts.append(index)
        index += 1

    return res_facts


if __name__ == '__main__':
    time_start = time()
    main()
    print(f"{M} facts validated vs {N} rules in {time() - time_start} seconds")