import re
from .enviroment import global_variables, total_size

def to_x86_64(cma_code: str, env: dict) -> str:
    code = ''

    for line in cma_code.splitlines():
        match re.split('[,\s]+', line):
            case ['pop'] :
                code += 'pop   rax\n'
            case ['loadc', q] :
                code += ';;; loadc\n'
                code +=f'mov   rax, {str(q)}\n'
                code += 'push  rax\n'
            case ['load'] :
                code += ';;; load\n'
                code +=f'mov   rax, {str(q)}\n'
                code += 'push  rax\n'
                code += 'neg   rdx\n'
                code += 'add   rdx, rbx\n'
                code += 'push  qword [rdx]\n'
            case ['store'] :
                code += ';;; store\n'
                code += 'pop   qword rdx\n'
                code += 'neg   rdx\n'
                code += 'add   rdx, rbx\n'
                code += 'pop   qword rax\n'
                code += 'mov   qword [rdx], rax\n'
                code += 'push  rax\n'
            case ['add'] :
                code += ';;; add\n'
                code += 'pop   rcx\n'
                code += 'pop   rax\n'
                code += 'add   rax, rcx\n'
                code += 'push  rax\n'
            case ['sub'] :
                code += ';;; sub\n'
                code += 'pop   rcx\n'
                code += 'pop   rax\n'
                code += 'sub   rax, rcx\n'
                code += 'push  rax\n'
            case ['mul'] :
                code += ';;; mul\n'
                code += 'pop   rcx\n'
                code += 'pop   rax\n'
                code += 'mul   rcx\n'
                code += 'push  rax\n'
            case ['div'] :
                code += ';;; div\n'
                code += 'pop   rcx\n'
                code += 'pop   rax\n'
                code += 'cqo\n'     ## copies the sign (bit 63) of the value in the RAX register into every bit position of the RDX register
                code += 'idiv  rcx\n'
                code += 'push  rax\n'
            case ['uminus'] :
                code += ';;; uminus\n'
                code += 'pop   rax\n'
                code += 'neg   rax\n'
                code += 'push  rax\n'
            case [*unknown] :
                code += f'Error: unknown CMa statement {unknown}'
            # TODO: 'alloc n', 'loadrc j', 'enter', 'ret', 'mark', 'call ?', 'slide q m',

            # TODO: classes?? 'proc formals locals? ?body?'

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
    program  = '\n'
    program += 'SECTION  .text\nglobal main\n'
    program += 'main:\n'
    program += '  push  rbp                 ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault\n'
    program += '  mov   rax,rsp             ; rsp zeigt auf den geretteten rbp\n'
    program += '  sub   rax,qword 8         ; neuer rbp sollte ein wort darüber liegen\n'
    program += '  mov   rbp,rax             ; set frame pointer to current (empty) stack pointer\n'
    size = total_size(global_variables(env))
    program +=f'  sub   rsp, {size}         ; move rsp to accomodate global variables\n'
    return program

def x86_final(env: dict) -> str:
    program  = '  pop   rax\n'
    program += '  mov   rsi, rax\n'
    program += '  mov   rdi, i64_fmt        ; arguments in rdi, rsi\n'
    program += '  mov   rax, 0              ; no xmm registers used\n'
    program += '  push  rbp                 ; set up stack frame, must be alligned\n'
    program += '  call  printf              ; Call C function\n'
    program += '  pop   rbp                 ; restore stack\n'
    size = total_size(global_variables(env))
    program +=f'  add   rsp, {size}         ; clean up variables\n'
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

    if line.startswith(';;;'):
        # return l + line + '\n'
        return line + '\n'

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
