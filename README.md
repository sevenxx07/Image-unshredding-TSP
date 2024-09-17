# Problem solution
Interestingly, quite reliable image reconstructions can be obtained by transforming this problem
to Shortest Hamiltonian Path Problem (SHPP), where each stripe will represent one node in a
graph. The idea is to order the stripes in such a way that adjacent stripes are “similar”. For this,
we need to define a distance function between two stripes.
Let w denote the width, i.e., the number of pixel columns in each stripe and let h denote the
height, i.e., the number of rows in each stripe.
The distance function is a sum of the absolute difference between the RGB color components
of the adjacent pixel columns of the stripes, i.e.,<br />
![obrazek](https://github.com/user-attachments/assets/99a79a5b-5e1d-4861-9997-bc210ec07ee8)<br />
Therefore, the image unshredding problem can be solved by computing the distances between
every pair of stripes and solving the corresponding SHPP. The solution of the SHPP then represents
the order of the stripes.
Moreover, we can further transform SHPP to TSP by adding a “dummy” node that has a
zero distance to all other nodes (the nodes that will be connected to the dummy node in the
TSP solution are the left and right edges of the reconstructed image.). The motivation for this
transformation is that there exists really good solvers for TSP, whereas for SHPP this is not the
case.
