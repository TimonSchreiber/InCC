                
        extern  printf, malloc  
        SECTION .data                   ; Data section, initialized variables
        i64_fmt: db      "%lld", 10,     0       ; printf format for printing an int64
                
        SECTION .text   
        global  main    
        main:         
        push    rbp                     ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault
        mov     rax,    rsp             ; rsp zeigt auf den geretteten rbp
        sub     rax,    qword 8         ; neuer rbp sollte ein wort darüber liegen
        mov     rbp,    rax             ; set frame pointer to current (empty) stack pointer
        sub     rsp,    8               ; reserve space for 8 bytes of global variables
                
        ;;; Start des eigentlichen Programms
        ;;; pushglob 0
        push    qword [rbx + 16]
        ;;; getbasic
        pop     rdx     
        mov     rax,    [rdx + 8]
        push    rax     
        ;;; loadc 21
        mov     rax,    21      
        push    rax     
        ;;; store
        pop     qword rdx
        neg     rdx     
        add     rdx,    rbx     
        pop     qword rax
        mov     qword [rdx],rax     
        push    rax     
        ;;; getbasic
        pop     rdx     
        mov     rax,    [rdx + 8]
        push    rax     
        ;;; Ende des eigentlichen Programms
                
                
        pop     rax     
        mov     rsi,    rax     
        mov     rdi,    i64_fmt         ; arguments in rdi, rsi
        mov     rax,    0               ; no xmm registers used
        push    rbp                     ; set up stack frame, must be alligned
        call    printf                  ; Call C function
        pop     rbp                     ; restore stack
        add     rsp,    8               ; free space for 8 bytes of global variables
                
        ;;; Rueckkehr zum aufrufenden Kontext
        pop     rbp                     ; original rbp ist last thing on the stack
        mov     rax,    0               ; return 0
        ret     
                
