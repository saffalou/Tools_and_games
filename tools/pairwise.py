import csv
import argparse
import os
from itertools import combinations, product
from random import choice


def generate_pairs(parameters):
    pairs = []
    for i in range(len(parameters)):
        for j in range(i + 1, len(parameters)):
            param1_name, param1_values = parameters[i]
            param2_name, param2_values = parameters[j]
            for value1 in param1_values:
                for value2 in param2_values:
                    pairs.append({param1_name: value1, param2_name: value2})
    return pairs


def read_parameters_from_csv(filename):
    parameters = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        values_by_column = {header: [] for header in headers}
        for row in reader:
            for idx, value in enumerate(row):
                values_by_column[headers[idx]].append(value)
    for header in headers:
        parameters.append((header, values_by_column[header]))
    return parameters


def write_to_csv(filename, test_cases):
    fieldnames = test_cases[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(test_cases)
    print(f"Test cases successfully written to {filename}")


def calculate_pairwise_test_cases(parameters):
    pairs = generate_pairs(parameters)
    uncovered_pairs = set(frozenset(pair.items()) for pair in pairs)
    test_cases = []

    while uncovered_pairs:
        test_case = {}
        covered_in_this_case = set()

        # Iterate through each parameter to select values
        for param, values in parameters:
            value_coverage = {value: 0 for value in values}

            for pair_set in uncovered_pairs:
                pair_dict = dict(pair_set)
                for value in values:
                    if param in pair_dict and pair_dict[param] == value:
                        value_coverage[value] += 1

            # Select value that covers the most uncovered pairs
            selected_value = max(value_coverage, key=value_coverage.get)
            test_case[param] = selected_value

        # Identify pairs covered by this test case
        for pair in pairs:
            pair_set = frozenset(pair.items())
            if pair_set in uncovered_pairs and all(test_case.get(k) == v for k, v in pair.items()):
                covered_in_this_case.add(pair_set)

        # Add test case only if it covers new pairs
        if covered_in_this_case:
            test_cases.append(test_case)
            uncovered_pairs -= covered_in_this_case
        else:
            # Final pass to target specific remaining pairs
            for pair_set in uncovered_pairs.copy():
                pair_dict = dict(pair_set)
                new_test_case = {param: choice(values)
                                 for param, values in parameters}
                new_test_case.update(pair_dict)
                test_cases.append(new_test_case)
                uncovered_pairs -= {pair_set}
                break

        print(f"Generated test case: {test_case}")
        print(f"Remaining uncovered pairs: {len(uncovered_pairs)}")

    # Consolidation pass to further reduce test cases
    print("Consolidating test cases to minimize redundancy...")
    consolidated_cases = []
    seen_pairs = set()

    for case in test_cases:
        new_pairs = set(frozenset(pair.items()) for pair in generate_pairs(
            [(k, [v]) for k, v in case.items()]))
        if not seen_pairs.intersection(new_pairs):
            consolidated_cases.append(case)
            seen_pairs.update(new_pairs)

    return consolidated_cases


def main():
    input_file = r'C:/projects/parameters.csv'
    output_file = r'C:/projects/pairwise_test_cases.csv'
    parser = argparse.ArgumentParser(description="Pairwise Testing Tool")
    parser.add_argument('--input', type=str,
                        help='Input CSV file path', default=input_file)
    parser.add_argument('--output', type=str,
                        help='Output CSV file path', default=output_file)
    args = parser.parse_args()

    parameters = read_parameters_from_csv(args.input)

    total_combinations = 1
    for param in parameters:
        total_combinations *= len(param[1])

    pairwise_test_cases = calculate_pairwise_test_cases(parameters)
    pairwise_test_cases_count = len(pairwise_test_cases)

    print(f"Total combinations without pairwise: {total_combinations}")
    print(f"Total test cases using pairwise: {pairwise_test_cases_count}")

    output_dir = os.path.dirname(output_file)
    output_filename = os.path.basename(output_file)
    pairwise_output_file = os.path.join(
        output_dir, 'pairwise_' + output_filename)
    write_to_csv(pairwise_output_file, pairwise_test_cases)


if __name__ == "__main__":
    main()
