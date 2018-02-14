import pyconfig
from pytest import fixture

# We are using the pyconfig package to provide global settings across the whole
# application. It's implemented as a singleton and thus if you mutate it in one
# function, the changes propagate to others. That's needed at runtime, but in the
# context of testing it's super bad! It means that the pyconfig singleton can
# leak state from one test to another.
#
# To stop that happening, we will declare a universal, automatically invoked
# setup fixture that applies to every single test and reset the config to
# the baseline state.
@fixture(scope='module', autouse=True)
def reload_pyconfig():
    pyconfig.reload(clear=True)
