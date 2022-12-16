all_linux: get_nodes_and_edges_linux handle_points select_points distance_points map_draw voronoi

all_ms: get_nodes_and_edges_ms handle_points select_points distance_points map_draw voronoi

all_fast: handle_points select_points distance_points map_draw voronoi

handle_points:
	python ./src/dataset_stuff/points_compresser.py ./dataset/data/delivery-instances-1.0/dev/rj

select_points:
	python ./src/dataset_stuff/points_selection.py 1000

distance_points:
	node ./src/dataset_stuff/points_distance.js

map_draw:
	node ./src/dataset_stuff/map_draw.js

voronoi:
	python src/dataset_stuff/voronoi.py

get_nodes_and_edges_linux:
ifeq ("$(wildcard ./files/nodes.csv)","")
	src/dataset_stuff/filter -22.515073574700054 -43.75041975692041 -23.07302600621818 -42.748660360854984 dataset/sudeste-latest.osm.pbf ./files/nodes.csv ./files/edges.csv
endif

get_nodes_and_edges_ms:
ifeq ("$(wildcard ./files/nodes.csv)","")
	src/dataset_stuff/filter.exe -22.515073574700054 -43.75041975692041 -23.07302600621818 -42.748660360854984 dataset/sudeste-latest.osm.pbf ./files/nodes.csv ./files/edges.csv
endif


clean:
	rm -R files/*
