clean::
	-rm -f cma.out cma.o cma.s cma.cma mama.out mama.o mama.s mama.mama

c :: cma.out

m :: mama.out

runc:: cma.out
	./$<

runm:: mama.out
	./$<

cma.out: cma.o
	gcc -no-pie -z noexecstack -o $@ $<

cma.o: cma.s
	nasm -f elf64 $<

cma.s: cma.py compiler/cma/*
	python3 ./$<

mama.out: mama.o
	gcc -no-pie -z noexecstack -o $@ $<

mama.o: mama.s
	nasm -f elf64 $<

mama.s: mama.py compiler/mama/*
	python3 ./$<
