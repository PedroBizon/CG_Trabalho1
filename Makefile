all: 
	run

setup:
	export MUJOCO_GL=glx
	export PYOPENGL_PLATFORM=glx
	
run:
	python3 main.py

test:
	python3 teste.py