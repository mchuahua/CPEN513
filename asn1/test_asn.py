# Imports
from asn1 import *

#####################
# Initialization tests
#####################

def test_putname():
    '''
    This function contains 1 test:
    - Tests that the putname function has the correct number of files found
    '''
    folder = 'benchmarks'
    suffix = '.infile'
    # Make sure that putname is correctly finding the associated folder and files
    assert np.size(putname(folder, suffix)) == 11

def test_dataloader():
    '''
    This function contains 2 tests:
    - Tests that the dataloader function has the correct number of benchmark files found
    - Tests that there is a name associated to each benchmark
    '''
    benchmarks, names = dataloader()
    
    # Make sure there are 11 benchmarks
    assert np.size(names) == 11

    # Make sure there is a name associated to each benchmark
    for name in names:
        try:
            benchmarks[name]
        except KeyError:
            print(f'{name} does not exist in benchmarks dict!')
            assert False

def test_initbenchmark():
    '''
    This function contains 6 tests:
    - Tests that the initialize benchmark function returns a benchmark with a grid
    - Tests that each grid is valid and is of a correct size according to what is defined in the loaded benchmark file
    - Tests that each grid contains at least one obstacle
    - Tests that each grid contains at least one source
    - Tests that each grid contains at least one sink
    - Tests that each grid contains at least one open space for routing
    '''
    benchmarks, names = dataloader()

    for benchmark in benchmarks:
        initialize_benchmark(benchmarks[benchmark])

        # Make sure each benchmark has a grid
        try:
            benchmarks[benchmark]['grid']
        except KeyError:
            print(f'{benchmark} grid does not exist in benchmarks dict!')
            assert False

        # Make sure each benchmark's grid is of size benchmarks[benchmark][size]
        assert np.size(benchmarks[benchmark]['grid']) == np.multiply(benchmarks[benchmark]['size'][0],benchmarks[benchmark]['size'][1])

        # Make sure each benchmark's grid has at least one obstacle, one source, one sink, and one open space for routing
        for value in COLOURS:
            try:
                a = benchmarks[benchmark]['grid'].ravel()
                COLOURS[value] in a
            except ValueError:
                # Expected that there shouldn't be any working value inside grid
                if value == 'working':
                    continue
                # Otherwise if we can't find it, raise an error
                raise ValueError("{!r} is not in list".format(value))
                assert False

def test_workspace():
    '''
    This function contains 1 test:
    - Tests that the initialize workspace function has a workspace filled with empty dicts (aka initialized properly)
    '''
    benchmarks, names = dataloader()
    
    for benchmark in benchmarks:    
        init_workspace(benchmarks[benchmark])    
        
        # Make sure each benchmark has a workspace filled with empty dicts
        for row in benchmarks[benchmark]['workspace']:
            for val in row:
                assert val == dict()

#####################
# A* tests
#####################
def test_manhattan():
    '''
    This function contains 1 test:
    - Tests that the manhattan distance is computed properly
    '''
    for i in range(10):
        for j in range (10):
            for k in range (10):
                for l in range (10):
                    assert manhattan(i,j,k,l) == (abs(i-j) + abs(k-l))

def test_cost():
    '''
    This function contains 1 test:
    - Tests that the cost is computed properly
    '''
    for i in range(10):
        for j in range (10):
            for k in range (10):
                for l in range (10):
                    for a in range (10):
                        for b in range (10):
                            assert cost(i,j,k,l,a,b) == (abs(i-j) + abs(l-a)) + (abs(j-k) + abs(a-b))

def test_calcclosest():
    '''
    This function contains 1 test:
    - Tests that the calc closest function is computed properly
    '''
    temp = []
    # construct grid
    for i in range(10):
        temp2 = []
        for j in range(10):
            temp2.append(j)
        temp.append(temp2)

    # Check calc closest is working properly
    for i in range(1,10):
        min, x, y = calc_closest(1, temp, i, i)
        assert min == i-1 
        assert x == 1
        assert y == i



