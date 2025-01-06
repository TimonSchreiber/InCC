clean::
	-rm -f cma.out cma.o cma.s cma.cma mama.out mama.o mama.s mama.mama ima24.out ima24.o ima24.s ima24.ima24

c :: cma.out

i :: ima24.out

m :: mama.out

runc:: cma.out
	./$<

runi:: ima24.out
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

ima24.out: ima24.o
	gcc -no-pie -z noexecstack -o $@ $<

ima24.o: ima24.s
	nasm -f elf64 $<

ima24.s: ima24.py compiler/ima24/*
	python3 ./$<
