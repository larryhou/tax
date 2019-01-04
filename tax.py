#!/usr/bin/env python3
#encoding: utf-8

from __future__ import print_function

TAX_FREE_AMOUNT = 5000

def find_tax_tier(amount, table): # type: (float, list[tuple])->tuple
    min_idx, max_idx = 0, len(table) - 1
    while min_idx <= max_idx:
        mid_idx = (min_idx + max_idx) // 2
        tier = table[mid_idx]
        if tier[0] > amount:
            max_idx = mid_idx - 1
        elif tier[1] <= amount:
            min_idx = mid_idx + 1
        else:
            return tier
    raise RuntimeError()

def caculate_new_tax(amount, bonus, table): # type: (float, float, list[tuple])->list[tuple[int,float,float]]
    if amount > TAX_FREE_AMOUNT:
        tax_amount = amount - TAX_FREE_AMOUNT
    else:
        tax_amount = 0
    result = []
    total_tax, total_amount = 0, 0
    for n in range(12):
        total_amount += tax_amount
        if n + 1 == 2:
            total_amount += bonus
        tier = find_tax_tier(total_amount, table)
        assert tier
        month_tax = tier[2] * total_amount - tier[3] - total_tax
        # print(tier, month_tax, total_tax, total_amount)
        total_tax += month_tax
        result.append((n+1, month_tax, total_tax))
    # print(result)
    return result

def caculate_old_tax(amount, bonus, table, bonus_table): # type: (float, float, list[tuple], list[tuple])->list[tuple[int,float,float]]
    if bonus > 0:
        bonus_tier = find_tax_tier(bonus, bonus_table)
        bonus_tax = bonus_tier[2] * bonus - bonus_tier[3]
    else:
        bonus_tax = 0
    if amount > TAX_FREE_AMOUNT:
        tax_amount = amount - TAX_FREE_AMOUNT
        tier = find_tax_tier(tax_amount, table)
    else:
        tax_amount = 0
        tier = (0,)*4
    result = []
    total_tax = 0
    for n in range(12):
        tax = tax_amount * tier[2] - tier[3]
        if n + 1 == 2:
            tax += bonus_tax
        total_tax += tax
        result.append((n + 1, tax, total_tax))
    # print(result)
    return result

def main():
    import argparse, sys
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--amount', '-a', required=True, type=int, help='计税额度=月薪-社保-公积金')
    arguments.add_argument('--bonus', '-b', type=int, default=0, help='年终奖金')
    options = arguments.parse_args(sys.argv[1:])
    amount = options.amount # type: float
    old_table = [
        (0, 3000, 0.03, 0),
        (3000, 12000, 0.1, 210),
        (12000, 25000, 0.20, 1410),
        (25000, 35000, 0.25, 2660),
        (35000, 55000, 0.30, 4410),
        (55000, 80000, 0.35, 7160),
        (80000, 1e+9, 0.45, 15160)
    ]
    new_table = [
        (0, 36000, 0.03, 0),
        (36000, 144000, 0.1, 2520),
        (144000, 300000, 0.20, 16920),
        (300000, 420000, 0.25, 31920),
        (420000, 660000, 0.30, 52920),
        (660000, 960000, 0.35, 85920),
        (960000, 1e+15, 0.45, 181920)
    ]
    bonus_table=[
        (18000, 54000, 0.03, 105),
        (54000, 108000, 0.10, 555),
        (108000, 420000, 0.20, 1005),
        (420000, 660000, 0.25, 2755),
        (660000, 960000, 0.35, 5505),
        (960000, 1e+15, 0.45, 13505)
    ]
    new_sum = caculate_new_tax(amount, table=new_table, bonus=options.bonus)
    old_sum = caculate_old_tax(amount, table=old_table, bonus=options.bonus, bonus_table=bonus_table)
    print('|月份|旧月税|新月税|旧累积税|新累积税|')
    print('|-:|-:|-:|-:|-:|')
    for n in range(12):
        record = '| {:2d} | {:>10,} | {:>10,} | {:>12,} | {:>12,} |'.format(n+1, round(old_sum[n][1]), round(new_sum[n][1]), round(old_sum[n][2]), round(new_sum[n][2]))
        print(record)

if __name__ == '__main__':
    main()