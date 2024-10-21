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
        sub     rsp,    24       
                 
        ;;; Start des eigentlichen Programms
                                        ;;; loadc 
        push    qword 1  
                                        ;;; loadc 
        push    qword 0  
                                        ;;; store 
        pop     qword rdx 
        neg     rdx      
        add     rdx,    rbx      
        pop     qword rax 
        mov     qword [rdx],rax      
        push    rax      
        pop     rax      
                                        ;;; loadc 
        push    qword 3  
                                        ;;; loadc 
        push    qword 8  
                                        ;;; store 
        pop     qword rdx 
        neg     rdx      
        add     rdx,    rbx      
        pop     qword rax 
        mov     qword [rdx],rax      
        push    rax      
        pop     rax      
                                        ;;; loadc 
        push    qword 1234567890000 
                                        ;;; loadc 
        push    qword 16 
                                        ;;; store 
        pop     qword rdx 
        neg     rdx      
        add     rdx,    rbx      
        pop     qword rax 
        mov     qword [rdx],rax      
        push    rax      
        ;;; Ende des eigentlichen Programms
                 
        pop     rax      
        mov     rsi,    rax      
        mov     rdi,    i64_fmt         ; arguments in rdi, rsi 
        mov     rax,    0               ; no xmm registers used 
        push    rbp                     ; set up stack frame, must be alligned 
        call    printf                  ; Call C function 
        pop     rbp                     ; restore stack 
        add     rsp,    24       
                 
        ;;; Rueckkehr zum aufrufenden Kontext
        pop     rbp                     ; original rbp ist last thing on the stack 
        mov     rax,    0               ; return 0 
        ret      
