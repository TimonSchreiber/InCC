from compiler.enviroment import global_vars, total_size

def x86_program(x86_code: str, env: dict, *func: tuple[str]) -> str:
    size = total_size(global_vars(env))
    program  = x86_prefix(*func)
    program += x86_start(size)
    program += '\n;;; Start des eigentlichen Programms\n'
    program += x86_code
    program += ';;; Ende des eigentlichen Programms\n\n'
    program += x86_final(size)
    return program

def x86_prefix(*func: tuple[str]) -> str:
    return f'''
        extern  {(", ".join(func))}
        SECTION .data               ; Data section, initialized variables
        i64_fmt:  db  "%lld", 10, 0 ; printf format for printing an int64
    '''

def x86_start(size: int) -> str:
    return f'''
        SECTION  .text
        global main
        main:
          push  rbp                 ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault
          mov   rax,rsp             ; rsp zeigt auf den geretteten rbp
          sub   rax,qword 8         ; neuer rbp sollte ein wort darüber liegen
          mov   rbp,rax             ; set frame pointer to current (empty) stack pointer
          sub   rsp, {size}         ; reserve space for {size} bytes of global variables
    '''

def x86_final(size: int) -> str:
    return f'''
        pop   rax
        mov   rsi, rax
        mov   rdi, i64_fmt        ; arguments in rdi, rsi
        mov   rax, 0              ; no xmm registers used
        push  rbp                 ; set up stack frame, must be alligned
        call  printf              ; Call C function
        pop   rbp                 ; restore stack
        add   rsp, {size}         ; free space for {size} bytes of global variables

        ;;; Rueckkehr zum aufrufenden Kontext
        pop   rbp                 ; original rbp ist last thing on the stack
        mov   rax, 0              ; return 0
        ret
    '''
