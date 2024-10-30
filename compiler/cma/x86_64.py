import re
from .enviroment import global_variables, total_size

"""
    reference: https://www.felixcloutier.com/x86/
"""

def to_x86_64(cma_code: str, env: dict) -> str:
    with open("./cma.cma","w") as cma:
        cma.write(cma_code)

    code = ''
    for line in cma_code.splitlines():
        match re.split('[,\s]+', line):
            case ['pop'] :
                code += f''';;; pop
                    pop   rax
                '''
            case ['loadc', q] :
                code += f''';;; loadc
                    mov   rax, {str(q)}
                    push  rax
                '''
            case ['load'] :
                code += f''';;; load
                    pop   rdx
                    neg   rdx
                    add   rdx, rbx
                    push  qword [rdx]
                '''
            case ['loadrc', j] :
                code += f''';;; loadrc
                    mov   rax, rbp
                    add   rax, qword {j}
                    push  rax
                '''
            case ['store'] :
                code += f''';;; store
                    pop   qword rdx
                    neg   rdx
                    add   rdx, rbx
                    pop   qword rax
                    mov   qword [rdx], rax
                    push  rax
                '''
            case ['jumpz', l] :
                code += f''';;; jumpz
                    pop   rax
                    test  rax,rax
                    je {l}
                '''
            case ['jump', l] :
                code += f''';;; jump
                    jmp   {l}
                '''
            case ['dup'] :
                code += f''';;; dup
                    pop   rax
                    push  rax
                    push  rax
                '''
            case ['swap'] :
                code += f''';;; swap
                    pop   rcx
                    pop   rax
                    push  rcx
                    push  rax
                '''
            case ['slide', q, m] :
                code += f''';;; slide
                    pop   rax
                    add   rsp, qword {q}
                    push  rax
                '''
            case ['alloc', s] :
                code += f''';;; alloc
                    sub   rsp, qword {s}
                '''
            case ['enter'] :
                code += f''';;; enter
                    mov   rbp, rbx
                    sub   rbp, rsp
                '''
            case ['mark'] :
                code += f''';;; mark
                    push  rbp
                '''
            case ['call'] :
                code += f''';;; call
                    pop   rax
                    call  rax
                '''
            case ['ret'] :
                code += f''';;; ret
                    mov   rsp, rbx      ; restore stack pointer to prev frame
                    sub   rsp, rbp      ; rsp <- rbx - rbp (=N)
                    mov   rax, rbx      ; restore frame pointer
                    sub   rax, rbp      ;
                    mov   rbp, [rax+8]  ; rbp <- [rbx - rbp + 8]
                    ret
                '''
            case ['dec'] :  # also 'inc' available
                code += f''';;; dec
                    pop   rax
                    dec   rax
                    push  rax
                '''
            case ['add'] :
                code += f''';;; add
                    pop   rcx
                    pop   rax
                    add   rax, rcx
                    push  rax
                '''
            case ['sub'] :
                code += f''';;; sub
                    pop   rcx
                    pop   rax
                    sub   rax, rcx
                    push  rax
                '''
            case ['mul'] :
                code += f''';;; mul
                    pop   rcx
                    pop   rax
                    mul   rcx
                    push  rax
                '''
            case ['div'] :
                ## cqo copies the sign (bit 63) of the value in the RAX register into every bit position of the RDX register
                code += f''';;; div
                    pop   rcx
                    pop   rax
                    cqo
                    idiv  rcx
                    push  rax
                '''
            case ['le'] :
                code += f''';;; le
                    pop   rcx
                    pop   rax
                    cmp   rax, rcx
                    setl  al
                    movzx rax, al
                    push  rax
                '''
            case ['gr'] :
                code += f''';;; gr
                    pop   rcx
                    pop   rax
                    cmp   rax, rcx
                    setg  al
                    movzx rax, al
                    push  rax
                '''
            case ['leq'] :
                code += f''';;; leq
                    pop   rcx
                    pop   rax
                    cmp   rax, rcx
                    setle al
                    movzx rax, al
                    push  rax
                '''
            case ['geq'] :
                code += f''';;; geq
                    pop   rcx
                    pop   rax
                    cmp   rax, rcx
                    setge al
                    movzx rax, al
                    push  rax
                '''
            case ['eq'] :
                code += f''';;; eq
                    pop   rcx
                    pop   rax
                    cmp   rax, rcx
                    sete  al
                    movzx rax, al
                    push  rax
                '''
            case ['neq'] :
                code += f''';;; neq
                    pop   rcx
                    pop   rax
                    cmp   rax, rcx
                    setne al
                    movzx rax, al
                    push  rax
                '''
            case ['uminus'] :
                code += f''';;; uminus
                    pop   rax
                    neg   rax
                    push  rax
                '''
            case [label] if label.endswith(':') :
                code += label + '\n'
            case [*unknown] :
                code += f'Error: unknown CMa statement {unknown}'

    return code #format_code(code)

def x86_program(x86_code: str, env: dict) -> str:
    program  = x86_prefix(env)
    program += x86_start(env)
    program += '\n;;; Start des eigentlichen Programms\n'
    program += x86_code
    program += ';;; Ende des eigentlichen Programms\n\n'
    program += x86_final(env)
    return format_code(program)

def x86_prefix(env: dict) -> str:
    program  = 'extern  printf\n'
    program += 'SECTION .data               ; Data section, initialized variables\n'
    program += 'i64_fmt:  db  "%lld", 10, 0 ; printf format for printing an int64\n'
    return program

def x86_start(env: dict) -> str:
    size = total_size(global_variables(env))
    program  = '\n'
    program += 'SECTION  .text\nglobal main\n'
    program += 'main:\n'
    program += '  push  rbp                 ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault\n'
    program += '  mov   rax,rsp             ; rsp zeigt auf den geretteten rbp\n'
    program += '  sub   rax,qword 8         ; neuer rbp sollte ein wort darüber liegen\n'
    program += '  mov   rbp,rax             ; set frame pointer to current (empty) stack pointer\n'
    program +=f'  sub   rsp, {size}         ; reserve space for {size} bytes of global variables\n'
    return program

def x86_final(env: dict) -> str:
    size = total_size(global_variables(env))
    program  = '  pop   rax\n'
    program += '  mov   rsi, rax\n'
    program += '  mov   rdi, i64_fmt        ; arguments in rdi, rsi\n'
    program += '  mov   rax, 0              ; no xmm registers used\n'
    program += '  push  rbp                 ; set up stack frame, must be alligned\n'
    program += '  call  printf              ; Call C function\n'
    program += '  pop   rbp                 ; restore stack\n'
    program +=f'  add   rsp, {size}         ; free space for {size} bytes of global variables\n'
    program += '\n;;; Rueckkehr zum aufrufenden Kontext\n'
    program += '  pop   rbp                 ; original rbp ist last thing on the stack\n'
    program += '  mov   rax, 0              ; return 0\n'
    program += '  ret\n'
    return program

def format_line(line: str) -> str:
    tab_width = 8
    l = ''
    if ':' in line:
        x = re.split(':', line, 1)
        l += f'{x[0] + ": ":<{tab_width}}'
        line = x[1]
    else:
        l += tab_width * ' '

    if line.strip().startswith(';;;'):
        return l + line.strip() + '\n'

    comment = None
    if ';' in line :
        x = re.split(";", line.strip(), 1)
        comment = x[1]
        line = x[0]

    x = re.split("[\s]+", line.strip(), 1)
    l += f'{x[0]:<{tab_width}}'

    if len(x) > 1:
        line = x[1]
        x = re.split(",", line.strip())
        for y in x[:-1]:
            l += f'{y.strip() + ",":<{tab_width}}'
        l += f'{x[-1].strip():<{tab_width}}'
    if comment:
        l = f'{l:<40}' + ';' + comment

    return l + '\n'

def format_code(c: str) -> str:
    return ''.join([format_line(l) for l in c.splitlines()])
