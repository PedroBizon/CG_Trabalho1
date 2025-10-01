all: 
	run

run:
	export MUJOCO_GL=glx
	export PYOPENGL_PLATFORM=glx
	python3 main.py

test:
	export MUJOCO_GL=glx
	export PYOPENGL_PLATFORM=glx
	python3 teste.py