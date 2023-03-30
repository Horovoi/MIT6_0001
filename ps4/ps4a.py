# Problem Set 4A: Permutations of a string
# Name: Mykyta Horovoi
# Collaborators: None

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 0:
        return ['']
    elif len(sequence) == 1:
        return [sequence]
    else:
        permutations = []
        for i in range(len(sequence)):
            first_char = sequence[i]
            rest_of_sequence = sequence[:i] + sequence[i+1:]
            rest_of_permutations = get_permutations(rest_of_sequence)
            for permutation in rest_of_permutations:
                permutations.append(first_char + permutation)
        return permutations


if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    # Test case 1
    test_case_1 = 'qwe'
    print('Input:', test_case_1)
    print('Expected Output:', ['qwe', 'qew', 'wqe', 'weq', 'eqw', 'ewq'])
    if set(get_permutations(test_case_1)) == set(['qwe', 'qew', 'wqe', 'weq', 'eqw', 'ewq']):
        print('Test case 1 PASSED!')
    else:
        print('Test case 1 failed')

    # Test case 2
    test_case_2 = 'xyz'
    print('Input:', test_case_2)
    print('Expected Output:', ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx'])
    if set(get_permutations(test_case_2)) == set(['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']):
        print('Test case 2 PASSED!')
    else:
        print('Test case 2 failed')

    # Test case 3
    test_case_3 = 'hui'
    print('Input:', test_case_3)
    print('Expected Output:', ['hui', 'hiu', 'ihu', 'iuh', 'uhi', 'uih'])
    if set(get_permutations(test_case_3)) == set(['hui', 'hiu', 'ihu', 'iuh', 'uhi', 'uih']):
        print('Test case 3 PASSED!')
    else:
        print('Test case 3 failed')