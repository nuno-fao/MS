all_linux: get_nodes_and_edges_linux handle_points select_points distance_points map_draw voronoi

all_ms: get_nodes_and_edges_ms handle_points select_points distance_points map_draw voronoi

all_fast: handle_points select_points distance_points map_draw voronoi

handle_points:
	python3 ./src/dataset/points_compresser.py ./dataset/data/delivery-instances-1.0/dev/rj

select_points:
	python3 ./src/dataset/points_selection.py 500

distance_points:
	node ./src/dataset/points_distance.js

map_draw:
	node ./src/dataset/map_draw.js

voronoi:
	python3 src/dataset/voronoi.py

get_nodes_and_edges_linux:
ifeq ("$(wildcard ./files/nodes.csv)","")
	if [ ! -f ./dataset/sudeste-latest.osm.pbf ]; then \
		wget -P ./dataset http://download.geofabrik.de/south-america/brazil/sudeste-latest.osm.pbf; \
	fi 
	src/dataset/filter -22.515073574700054 -43.75041975692041 -23.07302600621818 -42.748660360854984 dataset/sudeste-latest.osm.pbf ./files/nodes.csv ./files/edges.csv
endif

get_nodes_and_edges_ms:
ifeq ("$(wildcard ./files/nodes.csv)","")
	src/dataset/filter.exe -22.515073574700054 -43.75041975692041 -23.07302600621818 -42.748660360854984 dataset/sudeste-latest.osm.pbf ./files/nodes.csv ./files/edges.csv
endif

clean:
	rm -R files/*
