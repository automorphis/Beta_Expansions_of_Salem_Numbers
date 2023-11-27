import os
import sys
from pathlib import Path

from beta_numbers.beta_orbits import calc_orbits, calc_orbits_setup
from cornifer import parallelize, load_shorthand
from cornifer._utilities.multiprocessing import slurm_timecode_to_timedelta
from dagtimers import Timers

def f(
    num_procs, proc_index, perron_polys_reg, perron_nums_reg, poly_orbit_reg, coef_orbit_reg, periodic_reg, status_reg,
    max_blk_len, max_orbit_len, max_dps, timers
):

    return calc_orbits(
        perron_polys_reg,
        perron_nums_reg,
        poly_orbit_reg,
        coef_orbit_reg,
        periodic_reg,
        status_reg,
        max_blk_len,
        max_orbit_len,
        max_dps,
        num_procs,
        proc_index,
        timers
    )

if __name__ == '__main__':

    num_procs = int(sys.argv[1])
    perron_polys_dir = Path(sys.argv[2])
    beta_numbers_dir = Path(sys.argv[3])
    do_setup = sys.argv[4] == 'True'
    max_blk_len = int(sys.argv[5])
    max_orbit_len = int(sys.argv[6])
    max_dps = int(sys.argv[7])
    timeout = int(slurm_timecode_to_timedelta(sys.argv[8]).total_seconds() * 0.90)
    update_period = int(sys.argv[9])
    update_timeout = int(sys.argv[10])
    sec_per_block_upper_bound = int(sys.argv[11])
    tmp_filename = Path(os.environ['TMPDIR'])
    perron_polys_reg = load_shorthand('perron_polys_reg', perron_polys_dir)
    perron_nums_reg = load_shorthand('perron_nums_reg', perron_polys_dir)
    timers = Timers()

    if do_setup:
        poly_orbit_reg, coef_orbit_reg, periodic_reg, status_reg = calc_orbits_setup(perron_polys_reg, perron_nums_reg, beta_numbers_dir, max_blk_len, timers)

    else:

        poly_orbit_reg = load_shorthand('poly_orbit_reg', beta_numbers_dir)
        coef_orbit_reg = load_shorthand('coef_orbit_reg', beta_numbers_dir)
        periodic_reg = load_shorthand('periodic_reg', beta_numbers_dir)
        status_reg = load_shorthand('status_reg', beta_numbers_dir)

    parallelize(
        num_procs, f, (
            perron_polys_reg, perron_nums_reg, poly_orbit_reg, coef_orbit_reg, periodic_reg, status_reg,
            max_blk_len, max_orbit_len, max_dps, timers
        ), timeout, tmp_filename, update_period, update_timeout, sec_per_block_upper_bound
    )