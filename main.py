import argparse
import random
from typing import List

from src import GreedySolver, HierarchicalSolver
from utils import ensure_substring_free


def create_dna_test(string: str, length: int, prob: float) -> List[str]:
    strings = []
    for i in range(len(string) - length + 1):
        if random.random() > prob:  # remove with probability prob
            strings.append(string[i:i + length])
    return ensure_substring_free(strings)


def create_slice_test(string: str, repetitions: int, min_len: int, max_len: int) -> List[str]:
    strings = []
    n = len(string)
    for _ in range(repetitions):
        pos = 0
        while n - pos > max_len:
            string_len = random.randint(min_len, max_len)
            strings.append(string[pos:pos + string_len])
            pos += string_len

    return ensure_substring_free(strings)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    dna_from_given = subparsers.add_parser('from_dna')
    dna_from_given.add_argument(
        '--input',
        required=True,
        help='Input DNA string',
    )
    dna_from_given.add_argument(
        '--len',
        required=True,
        type=int,
        help='Size of a single string'
    )
    dna_from_given.add_argument(
        '--prob',
        required=True,
        type=float,
        help='Probability of elimination'
    )

    dna_from_random = subparsers.add_parser('from_random_dna')
    dna_from_random.add_argument(
        '--alphabet',
        required=False,
        help='Alphabet for strings in problem',
        default='AGCT'
    )
    dna_from_random.add_argument(
        '--input-len',
        required=True,
        type=int,
        help='Size of an input string'
    )
    dna_from_random.add_argument(
        '--len',
        required=True,
        type=int,
        help='Size of a single string'
    )
    dna_from_random.add_argument(
        '--prob',
        required=True,
        type=float,
        help='Probability of elimination'
    )

    from_random = subparsers.add_parser('from_random')
    from_random.add_argument(
        '--alphabet',
        required=False,
        help='Alphabet for strings in problem',
        default='AGCT'
    )
    from_random.add_argument(
        '--amount',
        required=True,
        type=int,
        help='Amount of strings in input'
    )
    from_random.add_argument(
        '--len',
        required=True,
        type=int,
        help='Size of a single string'
    )

    slices_from_given = subparsers.add_parser('slice_dna')
    slices_from_given.add_argument(
        '--input',
        required=True,
        help='Input DNA string',
    )
    slices_from_given.add_argument(
        '--repetitions',
        required=True,
        type=int,
        help='Amount of blocks'
    )
    slices_from_given.add_argument(
        '--min-len',
        required=True,
        type=int,
        help='Min size of a single string'
    )
    slices_from_given.add_argument(
        '--max-len',
        required=True,
        type=int,
        help='Max size of a single string'
    )

    slices_from_random = subparsers.add_parser('slice_random')
    slices_from_random.add_argument(
        '--alphabet',
        required=False,
        help='Alphabet for strings in problem',
        default='01'
    )
    slices_from_random.add_argument(
        '--input-len',
        required=True,
        type=int,
        help='Size of an input string'
    )
    slices_from_random.add_argument(
        '--repetitions',
        required=True,
        type=int,
        help='Amount of blocks'
    )
    slices_from_random.add_argument(
        '--min-len',
        required=True,
        type=int,
        help='Min size of a single string'
    )
    slices_from_random.add_argument(
        '--max-len',
        required=True,
        type=int,
        help='Max size of a single string'
    )

    args = parser.parse_args()
    if args.command == 'from_dna':
        strings = create_dna_test(args.input, args.len, args.prob)
    elif args.command == 'from_random_dna':
        strings = create_dna_test(''.join(random.choices(args.alphabet, k=args.input_len)), args.len, args.prob)
    elif args.command == 'from_random':
        strings = ensure_substring_free(
            [''.join(random.choices(args.alphabet, k=args.len)) for _ in range(args.amount)]
        )
    elif args.command == 'slice_dna':
        strings = create_slice_test(args.input, args.repetitions, args.min_len, args.max_len)
    elif args.command == 'slice_random':
        strings = create_slice_test(
            ''.join(random.choices(args.alphabet, k=args.input_len)), args.repetitions, args.min_len, args.max_len
        )
    else:
        raise ValueError(f'Unknown command {args.command}')

    print('Instance:', strings)
    print('GREEDY:', GreedySolver(strings).greedy())
    print('TGREEDY:', GreedySolver(strings).t_greedy())
    print('GHA:', HierarchicalSolver(strings).gha())
    print('CA for trivial:', HierarchicalSolver(strings).trivial_ca())


if __name__ == '__main__':
    main()