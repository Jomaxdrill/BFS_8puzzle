eight puzzle solver using BFS
AUTHOR: Jonathan Leonard Crespo Eslava
Project1 for UMD  Planning for Autonomous Robots-Spring 2024

DEPENDENCIES and PACKAGES
python 3.11.7
numpy 1.26.3
pygame 2.5.2 (for use the Animate.py)

LIBRARIES
numpy 1.17.4
deque

INSTRUCTIONS

-Using linux terminal locate the folder with the python file 'proj1_jonathan_crespo.py'

-Run the command 'python3 proj1_jonathan_crespo.py'

-Follow the instructions provided. You will be asked to input each row of the initial and goal state separated by commas.

-When the program finalizes three txt output files will be generated which the summary of the computation.

-Use Animate.py file (run 'python3 Animate.py') provided to animate the solution of the problem. Check it's in the same folder as generated files

EXAMPLES

To generate solvable test cases the following application is very useful https://deniz.co/8-puzzle-solver/

CONSIDERATIONS

Instances like 807146235 -> 147258360 are not solvable. It was verified by running the code with the following case. The result was the program never ended. Source: https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/

Hardest solution seems about 31 moves to solve and computation time can vary a lot depending of your system specs. Source: http://w01fe.com/blog/2009/01/the-hardest-eight-puzzle-instances-take-31-moves-to-solve/


