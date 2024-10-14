import re

def to_x86_64(cma_code, env) :
    code = ""

    for line in cma_code.splitlines() :
        match re.split("[,\s]+",line) :
            case ['pop'] :
                code +=  'pop   rax\n'
            case ['loadc', q] :
                code += f'push  qword {str(q)}\n'
            case ['add'] :
                code += 'pop  rcx\n'
                code += 'pop  rax\n'
                code += 'add  rax, rcx\n'
                code += 'push rax\n'
            case ['sub'] :
                code += 'pop  rcx\n'
                code += 'pop  rax\n'
                code += 'sub  rax, rcx\n'
                code += 'push rax\n'
            case ['mul'] :
                code += 'pop  rcx\n'
                code += 'pop  rax\n'
                code += 'mul  rcx\n'
                code += 'push rax\n'
            case ['div'] :
                code += 'pop  rcx\n'
                code += 'pop  rax\n'
                code += 'div  rcx\n'
                code += 'push rax\n'
            case [*unknown] :
                code += f'Error: unknown CMa statement {unknown}'

    return format_code(code)

def x86_program(x86_code, env) :
    program  = x86_prefix(env)
    program += x86_start(env)
    program += "\n;;; Start des eigentlichen Programms\n"
    program += x86_code
    program += ";;; Ende des eigentlichen Programms\n\n"
    program += x86_final(env)
    return format_code(program)

def x86_prefix(env):
    program  = "extern  printf\n"
    program += "SECTION .data               ; Data section, initialized variables\n"
    program += 'i64_fmt:  db  "%lld", 10, 0 ; printf format for printing an int64\n'
    return program

def x86_start(env):
    program  = "\n"
    program += "SECTION  .text\nglobal main\n"
    program += "main:\n"
    program += "  push  rbp                 ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault\n"
    program += "  mov   rax,rsp             ; rsp zeigt auf den geretteten rbp  \n"
    program += "  sub   rax,qword 8         ; neuer rbp sollte ein wort darüber liegen\n"
    program += "  mov   rbp,rax             ; set frame pointer to current (empty) stack pointer\n"
    return program

def x86_final(env):
    program  = "  pop   rax\n"
    program += "  mov   rsi, rax\n"
    program += "  mov   rdi,i64_fmt         ; arguments in rdi, rsi\n"
    program += "  mov   rax,0               ; no xmm registers used\n"
    program += "  push  rbp                 ; set up stack frame, must be alligned\n"
    program += "  call  printf              ; Call C function\n"
    program += "  pop   rbp                 ; restore stack\n"
    program += "\n;;; Rueckkehr zum aufrufenden Kontext\n"
    program += "  pop   rbp                 ; original rbp ist last thing on the stack\n"
    program += "  mov   rax,0               ; return 0\n"
    program += "  ret\n"
    return program

def format_line(line) :
    tab_width=8
    l = ""
    if ':' in line :
        x = re.split(":",line,1)
        l +=f'{x[0]+": ":<{tab_width}}'
        line = x[1]
    else :
        l += tab_width*' '

    if line.startswith(";;;") :
        return l+line+'\n'

    comment = None
    if ";" in line :
        x = re.split(";",line.strip(),1)
        comment = x[1]
        line = x[0]

    x=re.split("[\s]+", line.strip(),1)
    l+=f'{x[0]:<{tab_width}}'

    if len(x)>1 :
        line = x[1]
        x=re.split(",", line.strip())
        for y in x[:-1]:
            l += f'{y.strip()+",":<{tab_width}}'
        l += f'{x[-1].strip():<{tab_width}}'
    if comment :
        l=f'{l:<40}'+";"+comment

    return l+'\n'

def format_code(c) :
    return "".join([format_line(l) for l in c.splitlines()])
