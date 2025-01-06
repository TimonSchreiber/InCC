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
