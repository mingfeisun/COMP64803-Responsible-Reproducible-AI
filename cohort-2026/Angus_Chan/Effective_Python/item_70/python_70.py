# Item 70: Profile before Optimising

import numpy as np
import OpenMechanochem as mc
from ase.io import read
from ase import Atoms
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from cProfile import Profile
from pstats import Stats

def fmpes():
    mol = read("hydrogen.xyz")  # returns an ASE Atoms object

    PullPoints = [[0.000,  0.000, -1.000],
                 [0.000,  0.000,  2.000]]

    AppPoints  = [0,1]

    pull = mc.LinearPull(mol)

    for i in np.linspace(0,10,21):
        force = i
        pull.set_params(method='FMPES', pp=PullPoints, ap=AppPoints, pullforce = force)
        pull.set_calculator(EMT())
        dyn = BFGS(pull, trajectory='2FMPES_Hydrogen_{}nN.traj'.format(i))
        dyn.run(fmax=0.05)

profiler = Profile()
profiler.runcall(fmpes)

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats("cumulative")
stats.print_stats()

stats.print_callers()


