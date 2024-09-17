#!/usr/bin/env python3
import gurobipy as gp
from gurobipy import GRB
import numpy as np
 
def find_cycle(edges,n):
   remaining = list(range(n))
   cycle = list(range(n))
   cycle_edges=[]
   while len(remaining)!=0:
      curr_cycle = []
      curr_cycle_edges =[]
      neighbors = remaining
      start = neighbors[0]
 
      while len(neighbors)!=0:
         current = neighbors[0]
         curr_cycle.append(current)
         remaining.remove(current)
         neighbors = [j for i, j in edges.select(current, '*')
                      if j in remaining]
         if not neighbors:
            curr_cycle_edges.append([current, start])
         else:
            curr_cycle_edges.append([current,neighbors[0]])
      if len(curr_cycle) < len(cycle):
         cycle = curr_cycle
         cycle_edges = curr_cycle_edges
 
   return cycle,cycle_edges
 
 
def main(input_file, output_file):
   with open(input_file, 'r') as f:
      n, w, h = map(int, f.readline().split())
      mystripes = []
      im = f.read().split()
      im = list(map(int, im))
      mystripes = []
      stripes = np.reshape(im, (n, h, w, 3))
      # print(stripes)
      left_stripes = stripes[:, :, 0, :]
      right_stripes = stripes[:, :, -1, :]
      # for i in range(n):
      #   row = f.readline()
      #  im = tuple(int(j) for j in row.split(" "))
      # myindex = tuple(product(range(h), range(3)))
      # stripe = [[im[l] for l in (3*index*w+3*(w-1)+m for index, m in myindex)],
      #                 [im[l] for l in (3*index*w+m for index, m in myindex)]]
      # mystripes.append(np.array(stripe))
 
   dist = np.abs(right_stripes[:, np.newaxis, :, :] - left_stripes[np.newaxis, :, :, :])
   distan = np.sum(dist, axis=(2, 3))
   for i in range(n):
      for j in range(n):
         if i == j:
            distan[i][j]=999999
   distances = np.pad(distan, [(0, 1), (0, 1)], mode="constant")
   n = len(distances)
   print(distances)
 
   m = gp.Model()
   vars = m.addVars(n,n, vtype=GRB.BINARY)
 
   for i in range(n):
      m.addConstr(gp.quicksum(vars[i,j] for j in range(n)) == 1)
      m.addConstr(gp.quicksum(vars[j,i] for j in range(n)) == 1)
 
   m.setObjective(gp.quicksum(vars[i,j]*distances[i][j] for i in range(n) for j in range(n)))
 
   # Lazy constraints callback
   def subtour_elimination(model, where):
      if where == GRB.Callback.MIPSOL:
         value = m.cbGetSolution(vars)
         edges = []
         for i in range(n):
            for j in range(n):
               if value[i, j] == 1:
                  edges.append((i, j))
         cycle, combos = find_cycle(gp.tuplelist(edges), n)
         if (len(cycle) == n and len(combos) == 0):
            combos = edges
         if (len(cycle) < n):
            m.cbLazy(gp.quicksum(vars[i, j] for i, j in combos) <= len(cycle) - 1)
 
   m.Params.lazyConstraints = 1
   m.optimize(subtour_elimination)
 
   solution = {}
   for i in range(n):
      for j in range(n):
         solution[(i, j)] = int(round(vars[(i, j)].x))
   cycle = []
   curr = None
   i = n - 1
   while curr != n - 1:
      for curr in range(n):
         if solution[(i, curr)] == 1:
            cycle.append(curr)
            i = curr
            break
 
   tsp_solution = cycle[:-1]
   for i in range(len(tsp_solution)):
      tsp_solution[i] += 1
   # Write output file
   with open(output_file, 'w') as f:
      f.write(' '.join(map(str, tsp_solution)))
 
 
if __name__ == '__main__':
   import sys
 
   if len(sys.argv) != 3:
      print("Usage: python image_unshredding.py input_file output_file")
      sys.exit(1)
   main(sys.argv[1], sys.argv[2])
