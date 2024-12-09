from compiler.enviroment import global_variables, total_size

'''
    reference: https://www.felixcloutier.com/x86/
'''

def to_x86_64(cma_code: list[str]) -> str:
    # write to cma.cma file to view the cma code
    with open("./cma.cma","w") as cma:
        for e in cma_code:
            cma.write(f'{str(e)}\n')

    code = ''
    for e in cma_code:
        match e:
            case ('pop') :
                code += f''';;; pop
                    pop   rax
                '''
            case ('loadc', q) :
                code += f''';;; loadc
                    mov   rax, {str(q)}
                    push  rax
                '''
            case ('load') :
                code += f''';;; load
                    pop   rdx
                    neg   rdx
                    add   rdx, rbx
                    push  qword [rdx]
                '''
            case ('loadrc', j) :
                code += f''';;; loadrc
                    mov   rax, rbp
                    add   rax, qword {j}
                    push  rax
                '''
            case ('store') :
                code += f''';;; store
                    pop   qword rdx
                    neg   rdx
                    add   rdx, rbx
                    pop   qword rax
                    mov   qword [rdx], rax
                    push  rax
                '''
            case ('jumpz', l) :
                code += f''';;; jumpz
                    pop   rax
                    test  rax,rax
                    je {l}
                '''
            case ('jump', l) :
                code += f''';;; jump
                    jmp   {l}
                '''
            case ('dup') :
                code += f''';;; dup
                    pop   rax
                    push  rax
                    push  rax
                '''
            case ('swap') :
                code += f''';;; swap
                    pop   rcx
                    pop   rax
                    push  rcx
                    push  rax
                '''
            case ('slide', q, m) :
                code += f''';;; slide
                    pop   rax
                    add   rsp, qword {q}
                    push  rax
                '''
            case ('alloc', s) :
                code += f''';;; alloc
                    sub   rsp, qword {s}
                '''
            case ('enter') :
                code += f''';;; enter
                    mov   rbp, rbx
                    sub   rbp, rsp
                '''
            case ('mark') :
                code += f''';;; mark
                    push  rbp
                '''
            case ('call') :
                code += f''';;; call
                    pop   rax
                    call  rax
                '''
            case ('ret') :
                code += f''';;; ret
                    mov   rsp, rbx      ; restore stack pointer to prev frame
                    sub   rsp, rbp      ; rsp <- rbx - rbp (=N)
                    mov   rax, rbx      ; restore frame pointer
                    sub   rax, rbp      ;
                    mov   rbp, [rax+8]  ; rbp <- [rbx - rbp + 8]
                    ret
                '''
            case ('neg' | 'dec' | 'inc' as op) :
                code += f''';;; dec
                    pop   rax
                    {op}  rax
                    push  rax
                '''
            case ('add' | 'sub' as op) :
                code += f''';;; add
                    pop   rcx
                    pop   rax
                    {op}  rax, rcx
                    push  rax
                '''
            case ('mul' | 'div' as op) :
                ## cqo copies the sign (bit 63) of the value in the RAX register into every bit position of the RDX register
                code += f''';;; div
                    pop   rcx
                    pop   rax
                    cqo
                    i{op}  rcx
                    push  rax
                '''
            case ('le' | 'gr' | 'leq' | 'geq' | 'eq' | 'neq' as op) :
                code += f''';;; le
                    pop   rcx
                    pop   rax
                    cmp   rax, rcx
                    set{op[:-1]}  al
                    movzx rax, al
                    push  rax
                '''
            case ('label', name):
                code += f'{name}:\n'
            case (unknown) :
                code += f'Error: unknown CMa statement {unknown}\n'
    return code

def x86_program(x86_code: str, env: dict) -> str:
    # TODO:
    size = total_size(global_variables(env))
    program  = x86_prefix()
    program += x86_start(size)
    program += '\n;;; Start des eigentlichen Programms\n'
    program += x86_code
    program += ';;; Ende des eigentlichen Programms\n'
    program += x86_final(size)
    return program

def x86_prefix() -> str:
    return '''
        extern  printf
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

# def format_line(line: str) -> str:
#     tab_width = 8
#     l = ''
#     if ':' in line:
#         x = re.split(':', line, 1)
#         l += f'{x[0] + ": ":<{tab_width}}'
#         line = x[1]
#     else:
#         l += tab_width * ' '

#     if line.strip().startswith(';;;'):
#         return l + line.strip() + '\n'

#     comment = None
#     if ';' in line :
#         x = re.split(";", line.strip(), 1)
#         comment = x[1]
#         line = x[0]

#     x = re.split("[\s]+", line.strip(), 1)
#     l += f'{x[0]:<{tab_width}}'

#     if len(x) > 1:
#         line = x[1]
#         x = re.split(",", line.strip())
#         for y in x[:-1]:
#             l += f'{y.strip() + ",":<{tab_width}}'
#         l += f'{x[-1].strip():<{tab_width}}'
#     if comment:
#         l = f'{l:<40}' + ';' + comment

#     return l + '\n'

# def format_code(c: str) -> str:
#     return ''.join([format_line(l) for l in c.splitlines()])
