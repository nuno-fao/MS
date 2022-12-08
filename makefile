all: handle_points select_points

handle_points:
	python ./src/dataset_stuff/points_compresser.py ./dataset/data/delivery-instances-1.0/dev/rj
	
select_points:
	python ./src/dataset_stuff/points_selection.py 1000
	
clean:
	rm -R files/*
