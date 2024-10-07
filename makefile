default:: a.out

clean::
	-rm -f *.out *.o

run:: a.out
	./$<

a.out: a.o
	gcc -no-pie -z noexecstack -o $@ $<

a.o: a.s
	nasm -f elf64 $<
