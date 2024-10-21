default:: cma.out

clean::
	-rm -f cma.out cma.o cma.s

run:: cma.out
	./$<

cma.out: cma.o
	gcc -no-pie -z noexecstack -o $@ $<

cma.o: cma.s
	nasm -f elf64 $<

cma.s: cma.py compiler/cma/x86_64.py
	python3 ./$<
