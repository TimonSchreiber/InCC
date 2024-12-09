from compiler.enviroment import global_vars, total_size

'''
    reference: https://www.felixcloutier.com/x86/
'''

def malloc(n: int) -> str:
    return f'''
        mov   rdi, {8*n}
        call  malloc
        mov   rdx, rax
    '''

def to_x86_64(mama_code: list[str]) -> str:
    # write to mama.mama file to view the mama code
    with open("./mama.mama","w") as mama:
        for e in mama_code:
            mama.write(f'{str(e)}\n')

    code = ''
    for e in mama_code:
        match e:
            # case ('pop') :
            #     code += f''';;; pop
            #         pop   rax
            #     '''
            case ('loadc', q) :
                code += f''';;; loadc {q}
                    mov   rax, {str(q)}
                    push  rax
                '''
            # case ('load') :
            #     code += f''';;; load
            #         pop   rdx
            #         neg   rdx
            #         add   rdx, rbx
            #         push  qword [rdx]
            #     '''
            # case ('loadrc', j) :
            #     code += f''';;; loadrc
            #         mov   rax, rbp
            #         add   rax, qword {j}
            #         push  rax
            #     '''
            # case ('store') :
            #     code += f''';;; store
            #         pop   qword rdx
            #         neg   rdx
            #         add   rdx, rbx
            #         pop   qword rax
            #         mov   qword [rdx], rax
            #         push  rax
            #     '''
            case ('jumpz', l) :
                code += f''';;; jumpz {l}
                    pop   rax
                    test  rax, rax
                    je    {l}
                '''
            case ('jump', l) :
                code += f''';;; jump {l}
                    jmp   {l}
                '''
            # case ('dup') :
            #     code += f''';;; dup
            #         pop   rax
            #         push  rax
            #         push  rax
            #     '''
            # case ('swap') :
            #     code += f''';;; swap
            #         pop   rcx
            #         pop   rax
            #         push  rcx
            #         push  rax
            #     '''
            case ('slide', k) :
                code += f''';;; slide {k}
                    pop   rax
                    add   rsp, {8*k}
                    push  rax
                '''
            case ('alloc', n) :
                code += f';;; alloc {n}'
                code += f'''
                    {malloc(4)}
                    mov   qword [rdx], "F"
                    mov   qword [rdx + {8 * 1}], 0
                    mov   qword [rdx + {8 * 2}], 0
                    mov   qword [rdx + {8 * 3}], 0
                    push  rdx
                ''' * n
            # case ('enter') :
            #     code += f''';;; enter
            #         mov   rbp, rbx
            #         sub   rbp, rsp
            #     '''
            # case ('call') :
            #     code += f''';;; call
            #         pop   rax
            #         call  rax
            #     '''
            # case ('ret') :
            #     code += f''';;; ret
            #         mov   rsp, rbx      ; restore stack pointer to prev frame
            #         sub   rsp, rbp      ; rsp <- rbx - rbp (=N)
            #         mov   rax, rbx      ; restore frame pointer
            #         sub   rax, rbp      ;
            #         mov   rbp, [rax+8]  ; rbp <- [rbx - rbp + 8]
            #         ret
            #     '''
            case ('neg' as op) :
                code += f''';;; {op}
                    pop   rax
                    {op}  rax
                    push  rax
                '''
            case ('add' | 'sub' as op) :
                code += f''';;; {op}
                    pop   rcx
                    pop   rax
                    {op}  rax, rcx
                    push  rax
                '''
            case ('mul' | 'div' as op) :
                ## cqo copies the sign (bit 63) of the value in the RAX register into every bit position of the RDX register
                code += f''';;; {op}
                    pop   rcx
                    pop   rax
                    cqo
                    i{op} rcx
                    push  rax
                '''
            case ('le' | 'gr' | 'leq' | 'geq' | 'eq' | 'neq' as op) :
                code += f''';;; {op}
                    pop   rcx
                    pop   rax
                    cmp   rax, rcx
                    set{op[:-1]}  al
                    movzx rax, al
                    push  rax
                '''
            case ('mkbasic'):
                code += f''';;; mkbasic
                    {malloc(2)}
                    mov   qword [rdx], 'B'
                    pop   rax
                    mov   [rdx + 8], rax
                    push rdx
                '''
            case ('getbasic') :
                code += f''';;; getbasic
                    pop   rdx
                    mov   rax, [rdx + 8]
                    push  rax
                '''
            case ('pushloc', i) : # TODO:                                                                           push qword [rsp + 8*i]
                code += f''';;; pushloc {i}
                    mov   rdx, rsp
                    add   rdx, {8*i}
                    mov   rax, [rdx]
                    push  rax
                '''
            case ('pushglob', i) : # TODO:
                # code += f''';;; pushglob {i}
                #     mov   rdx, rbx
                #     mov   rax, [rdx]
                #     add   rdx, {8*(2*i-1)}
                #     mov   rax, [rdx]
                #     push  rax
                # '''
                code += f''';;; pushglob {i}
                    push qword [rbx + {8 * (2+i)}]
                '''
            case ('rewrite', j) :
                code += f''';;; rewrite {j}
                    mov   rcx, [rsp + {8*j}]
                    pop   rdx
                    mov   qword rax, [rcx + 0]
                    mov   qword [rdx + 0], rax
                    mov   qword rax, [rcx + 8]
                    mov   qword [rdx + 8], rax
                    mov   qword rax, [rcx + 16]
                    mov   qword [rdx + 16], rax
                    mov   qword rax, [rcx + 24]
                    mov   qword [rdx + 24], rax
                '''
            case ('mkvec', g) :# TODO:
                code += f''';;; mkvec {g}
                    {malloc(g+2)}
                    mov   qword [rdx], 'V'
                    mov   qword [rdx + 8], {g}
                '''
                for i in range(g, -1, -1):
                    code += f'''
                        pop   rax
                        mov   qword [rdx+{16+(g-i-1)*8}], rax
                    '''
                code += '''
                    push   rdx
                '''
            case ('mkfunval', addr) : # TODO:
                # code += f''';;; mkfunval {addr}
                #     mov   rdi, {8*2}  ; V-Objekt allokieren
                #     call  malloc
                #     mov   rdx, rax
                #     pop   rax
                #     mov   qword [rdx], qword 'V'  ; 1.
                #     mov   qword [rdx+8], qword 0 ; 2. Feld schreiber
                #     push  rdx
                #     mov   rdi, {8*4}  ; F-Objekt allokieren
                #     call  malloc
                #     mov   rdx, rax
                #     pop   rax
                #     pop   rcx ; und Adresse in rcx legen
                #     mov   qword [rcx], qword 'F'  ; 1. Feld
                #     mov   rax,  {addr}  ; 2. Feld
                #     mov   qword [rcx+8], rax  ; schreiber
                #     pop   rdx
                #     mov   qword [rcx+{2*8}], rdx  ; 3. von F -Objekt auf Adresse von v-Objekt
                #     pop   rax ; Objektadresse auf dem Stack
                #     mov   qword [rcx+{3*8}], rax  ; an die 4. Stelle des f-Objekts schreiben
                #     push  rcx  ; F-Objekt auf den Stack legen
                # '''
                code += f''';;; mkfunval {addr}
                    {malloc(4)}
                    mov   qword [rdx], "F"
                    mov   qword [rdx+8], {addr}
                    mov   qword [rdx+16], 0
                    pop   qword [rdx+24]
                    push  rdx
                '''
            case ('mark', A):
                # lea => load effective address
                code += f''';;; mark {A}
                    push   rbx            ; s[sp+1] <- gp
                    push   rbp            ; s[sp+2] <- fp
                    lea    rax, [rel {A}] ; -> rip + (l - A) mit 'l' nächste Zeile
                    push   rax            ; s[sp+3] <- A
                    mov    rbp, rsp       ; fp <- sp (sp<-sp_old+3)
                '''
            case ('apply'):
                code += f''';;; apply
                    pop   rcx                ; funktionsobjekt-pointer nach rcx
                    mov   rbx, [rcx + {8*3}] ; gp neu setzen
                    mov   rax, [rcx + {8*1}] ; Adresse der Funktion nach rax laden
                    jmp   rax                ; und den PC auf diesen Wert setzen
                '''
            case ('popenv'):
                code +=f''';;; popenv
                    mov   rbx, [rbp + {8*2}]    ; gp <- s[fp-2]
                    pop   rax                   ; s[fp-2] <- s[sp]
                    mov   [rbp + {8*2}], rax    ; ...
                    mov   rcx, rbp              ; sp <- fp-2
                    add   rcx, {8*2}            ; ...
                    mov   rsp, rcx              ; ...
                    mov   rax, [rbp]            ; rax <-s[fp] ...
                    mov   rbp, [rbp + {8*1}]    ; fp <- s[fp-1]
                    jmp   rax                   ; pc <- rax=s[fp]
                '''
            case ('label', name):
                code += f'{name}:\n'
            case (unknown) :
                code += f'Error: unknown mama statement {unknown}\n'

    return code

def x86_program(x86_code: str, env: dict) -> str:
    size = total_size(global_vars(env))
    program  = x86_prefix()
    program += x86_start(size)
    program += '\n;;; Start des eigentlichen Programms\n'
    program += x86_code
    program += ';;; Ende des eigentlichen Programms\n\n'
    program += x86_final(size)
    return program

def x86_prefix(func : str) -> str:
    # TODO: add a parameter for external functions
    return f'''
        extern  {(", ".join(*func))}
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
