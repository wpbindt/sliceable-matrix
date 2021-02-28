run-tests :
	python3 -m unittest tests.tests
run-mypy :
	mypy sliceable_matrix tests
run-mutmut :
	mutmut run
