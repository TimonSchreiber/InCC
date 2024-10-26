        extern  printf  
        SECTION .data                   ; Data section, initialized variables
i64_fmt: db      "%lld", 10,     0       ; printf format for printing an int64
                
        SECTION .text   
        global  main    
main:           
        push    rbp                     ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault
        mov     rax,    rsp             ; rsp zeigt auf den geretteten rbp
        sub     rax,    qword 8         ; neuer rbp sollte ein wort darüber liegen
        mov     rbp,    rax             ; set frame pointer to current (empty) stack pointer
        sub     rsp,    8               ; move rsp to accomodate global variables
                
;;; Start des eigentlichen Programms
;;; loadc
        mov     rax,    1       
        push    rax     
;;; uminus
        pop     rax     
        neg     rax     
        push    rax     
;;; loadc
        mov     rax,    0       
        push    rax     
;;; store
        pop     qword rdx
        neg     rdx     
        add     rdx,    rbx     
        pop     qword rax
        mov     qword [rdx],rax     
        push    rax     
        pop     rax     
;;; loadc
        mov     rax,    0       
        push    rax     
while_1:         
;;; loadc
        mov     rax,    0       
        push    rax     
;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
;;; loadc
        mov     rax,    2       
        push    rax     
;;; le
        pop     rcx     
        pop     rax     
        cmp     rax,    rcx     
        setl    al      
        movzx   rax,    al      
        push    rax     
;;; jumpz
        pop     rax     
        test    rax,    rax     
        je      endwhile_1
        pop     rax     
do_1:           
;;; loadc
        mov     rax,    0       
        push    rax     
;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
;;; loadc
        mov     rax,    1       
        push    rax     
;;; add
        pop     rcx     
        pop     rax     
        add     rax,    rcx     
        push    rax     
;;; loadc
        mov     rax,    0       
        push    rax     
;;; store
        pop     qword rdx
        neg     rdx     
        add     rdx,    rbx     
        pop     qword rax
        mov     qword [rdx],rax     
        push    rax     
;;; jump
        jmp     while_1 
endwhile_1:         
;;; Ende des eigentlichen Programms
                
        pop     rax     
        mov     rsi,    rax     
        mov     rdi,    i64_fmt         ; arguments in rdi, rsi
        mov     rax,    0               ; no xmm registers used
        push    rbp                     ; set up stack frame, must be alligned
        call    printf                  ; Call C function
        pop     rbp                     ; restore stack
        add     rsp,    8               ; clean up variables
                
;;; Rueckkehr zum aufrufenden Kontext
        pop     rbp                     ; original rbp ist last thing on the stack
        mov     rax,    0               ; return 0
        ret     
