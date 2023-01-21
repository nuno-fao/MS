all: get_nodes_and_edges handle_points select_points map_draw distance_matrix api kmeans

handle_points:
	python3 ./src/dataset/points_compresser.py ./dataset/data/delivery-instances-1.0/dev/rj

select_points:
	python3 ./src/dataset/points_selection.py 500

map_draw:
	node ./src/dataset/map_draw.js
	
distance_matrix:
ifeq ("$(wildcard ./files/step3.json)","")
	src/dataset/distance-matrix file ./files/nodes.csv ./files/edges.csv ./files/nodes.csv ./files/step3.json
endif

api:
	src/dataset/distance-matrix api ./files/nodes.csv ./files/edges.csv ./files/nodes.csv &
	sleep 10
	
kmeans:
	python3 src/kmean.py

	

get_nodes_and_edges:
ifeq ("$(wildcard ./files/nodes.csv)","")
	if [ ! -f ./dataset/sudeste-latest.osm.pbf ]; then \
		wget -P ./dataset http://download.geofabrik.de/south-america/brazil/sudeste-latest.osm.pbf; \
	fi 
	src/dataset/filter -22.515073574700054 -43.75041975692041 -23.07302600621818 -42.748660360854984 dataset/sudeste-latest.osm.pbf ./files/nodes.csv ./files/edges.csv
endif

