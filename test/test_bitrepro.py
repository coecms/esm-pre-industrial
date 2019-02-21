def test_atmosphere():
    """
    Test absolute norms are the same as truth
    """
    with open('test/final_absolute_norm.cmip6.PI-01','r') as truth,\
        open('work/atmosphere/atm.fort6.pe0','r') as test:
        lines = [line for line in test if 'Final Absolute Norm' in line]
        assert(len(lines) == 96)
        for l_truth, l_test in zip(truth.readlines(), lines):
            assert(l_truth == l_test)

def test_ocean():
    """
    Test checksums for the first day are the same
    """
    with open('test/mom_chksums.cmip6.PI-01','r') as truth,\
         open('work/ocean/stdout.rank.1.192','r') as test:
        lines = [line for line in test if '[chksum]' in line]
        assert(len(lines) == 1515)
        for i, (l_truth, l_test) in enumerate(zip(truth.readlines(), lines)):
            assert(l_truth == l_test)
