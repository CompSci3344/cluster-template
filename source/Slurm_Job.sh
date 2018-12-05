#!/bin/bash
#SBATCH -t 1:00:00
#SBATCH -N 12
#SBATCH --ntasks-per-node 4

#echo command to stdout
set -x

# where do I start?
echo $SLURM_SUBMIT_DIR

module load mpi/gcc_openmpi

#may need to be edited for proper dir
cd $SCRATCH
cp ~/examples/mpi/pi_mc.c ./
mpicc -o a.out $SCRATCH/pi_mc.c -lm

echo "With 1 processes"
time mpirun -np 1 ./a.out 100000
  
echo "With 4 processes"
time mpirun -np 4 ./a.out 100000
  
echo "With 9 processes"
time mpirun -np 9 ./a.out 100000
  
echo "With 16 processes"
time mpirun -np 16 ./a.out 100000
  
echo "With 25 processes"
time mpirun -np 25 ./a.out 100000
  
echo "With 36 processes"
time mpirun -np 36 ./a.out 100000
  
echo "With 48 processes"
time mpirun -np 48 ./a.out 100000
