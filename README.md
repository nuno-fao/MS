# MS 2022/2023

| Nome          | Email             |
| ------------- | ----------------- |
| Nuno Oliveira | up201806525@up.pt |
| Luís Pinto    | up201806206@up.pt |
| Maria Baía    | ---               |

To run the simulation pypy3 is recommended, python3 may also work but runs considerably slower.

Copy folders inside [folder](https://we.tl/t-7Mi8cGfUqk) to the root of the project with the folowing tree:

	root-
		files/
		dataset/
		src/
		
		
Navigate to src/sim/ and run ```python3 simple_run.py``` or ```pypy3 simple_run.py```.

The files related to the simulation are inside src/sim/.

To change the policies change file src/sim/agents/station.py:
```python3
percentage_cut = 0.5 # percentage of battery to cut
distance_cut = 50 # distance in km to cut
time_cut = 20 # time in minutes to cut

number_of_cars_to_cut = 4 # length of the queue to apply the cut

shall_cut = True # if the cut policy sould be applied
shall_order = True # if the non fifo ordering should be applied
```
The following should also be changed to change the applied policy:
```python3
        self.cut_car = self.cut_on_distance # can be = self.cut_on_distance or self.cut_on_percentage or self.cut_on_time
```
		
		
To run the setup parts of the system delete the contents of dataset/ and files/ and then run ```make```. 
This is not recommendend as the full make may take over 2 hours and consume over 13GiB of memory.

If ```make``` is run without deleting the files, the expensive steps will be ignored.
The setup part of the system only works on Linux 64bit System (tested in Ubuntu 22.04) as parts of the setup (Distance matrix and API) depend on a compiled version of the algorithm made in Go, as python proved to be too slow for the task.

The repository with the dijkstra code can be found [here](https://github.com/rocas777/RouteFInder
