all: handle_points select_points

handle_points:
	python ./src/dataset_stuff/points_compresser.py ./dataset/data/delivery-instances-1.0/dev/rj
	
select_points:
	python ./src/dataset_stuff/points_selection.py 1000

get_nodes_and_edges:
	src/dataset_stuff/filter -22.515073574700054 -43.75041975692041 -23.07302600621818 -42.748660360854984 dataset/sudeste-latest.osm.pbf ./files/nodes.csv ./files/edges.csv
	
clean:
	rm -R files/*
