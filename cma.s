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
                
        ;;; Start des eigentlichen Programms
        push    qword 13
        push    qword 2 
        pop     rcx     
        pop     rax     
        sub     rax,    rcx     
        push    rax     
        push    qword 47
        push    qword 100
        pop     rcx     
        pop     rax     
        mul     rcx     
        push    rax     
        pop     rcx     
        pop     rax     
        add     rax,    rcx     
        push    rax     
        ;;; Ende des eigentlichen Programms
                
        pop     rax     
        mov     rsi,    rax     
        mov     rdi,    i64_fmt         ; arguments in rdi, rsi
        mov     rax,    0               ; no xmm registers used
        push    rbp                     ; set up stack frame, must be alligned
        call    printf                  ; Call C function
        pop     rbp                     ; restore stack
                
        ;;; Rueckkehr zum aufrufenden Kontext
        pop     rbp                     ; original rbp ist last thing on the stack
        mov     rax,    0               ; return 0
        ret     
