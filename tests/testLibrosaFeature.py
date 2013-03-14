#!/usr/bin/env python
# CREATED:2013-03-08 15:25:18 by Brian McFee <brm2132@columbia.edu>
#  unit tests for librosa.feature (feature.py)
#
# Run me as follows:
#   cd tests/
#   nosetests -v
#
# This test suite verifies that librosa core routines match (numerically) the output
# of various DPWE matlab implementations on a broad range of input parameters.
#
# All test data is generated by the Matlab script "makeTestData.m".
# Each test loads in a .mat file which contains the input and desired output for a given
# function.  The test then runs the librosa implementation and verifies the results
# against the desired output, typically via numpy.allclose().
#
# CAVEATS:
#
#   Currently, not all tests are exhaustive in parameter space.  This is typically due
#   restricted functionality of the librosa implementations.  Similarly, there is no
#   fuzz-testing here, so behavior on invalid inputs is not yet well-defined.
#

import librosa
import os, glob
import numpy, scipy.io

from nose.tools import nottest

#-- utilities --#
def files(pattern):
    test_files = glob.glob(pattern)
    test_files.sort()
    return test_files

def load(infile):
    DATA = scipy.io.loadmat(infile, chars_as_strings=True)
    return DATA
#--           --#

#-- Tests     --#
def test_hz_to_mel():
    def __test_to_mel(infile):
        DATA    = load(infile)
        z       = librosa.feature.hz_to_mel(DATA['f'], DATA['htk'])

        assert numpy.allclose(z, DATA['result'])
    
    for infile in files('data/feature-hz_to_mel-*.mat'):
        yield (__test_to_mel, infile)

    pass

def test_mel_to_hz():

    def __test_to_hz(infile):
        DATA    = load(infile)
        z       = librosa.feature.mel_to_hz(DATA['f'], DATA['htk'])

        assert numpy.allclose(z, DATA['result'])
    
    for infile in files('data/feature-mel_to_hz-*.mat'):
        yield (__test_to_hz, infile)

    pass

def test_hz_to_octs():
    def __test_to_octs(infile):
        DATA    = load(infile)
        z       = librosa.feature.hz_to_octs(DATA['f'])

        assert numpy.allclose(z, DATA['result'])

    for infile in files('data/feature-hz_to_octs-*.mat'):
        yield (__test_to_octs, infile)

    pass

def test_melfb():

    def __test(infile):
        DATA    = load(infile)

        wts = librosa.feature.melfb( DATA['sr'][0], 
                                    DATA['nfft'][0], 
                                    nfilts  =   DATA['nfilts'][0],
                                    width   =   DATA['width'][0],
                                    fmin    =   DATA['fmin'][0],
                                    fmax    =   DATA['fmax'][0],
                                    use_htk =   DATA['htk'][0])
                                
        assert wts.shape == DATA['wts'].shape

        assert numpy.allclose(wts, DATA['wts'])

    for infile in files('data/feature-melfb-*.mat'):
        yield (__test, infile)
    pass
