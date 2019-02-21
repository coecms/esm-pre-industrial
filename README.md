## Introduction

This is a branch for testing bit reproducibility.

Created "truth" data from Scott running for 2 days from CSIRO scripts:

```
TRUTHDIR='/short/w35/saw562/scratch/access-esm/access-esm1.5-cmip6/ksh/exp/PI-01/Running.dir'
grep 'Final Absolute Norm' ${TRUTHDIR}/ATM_RUNDIR/um_out/PI-01.fort6.pe0 > test/final_absolute_norm.cmip6.PI-01
grep '\[chksum\]' ${TRUTHDIR}/OCN_RUNDIR/stdout.rank.1.192 > test/mom_chksums.cmip6.PI-01 
```

## Running test

Ensure `payu` is in `$PATH` and `pytest` is available
```
pytest test
```
For example, to run from a user `pip install`
```
PATH=$PATH:~/.local/bin pytest test
```