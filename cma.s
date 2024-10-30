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
        sub     rsp,    16              ; reserve space for 16 bytes of global variables
                
        ;;; Start des eigentlichen Programms
        ;;; loadc
        mov     rax,    2       
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
        ;;; pop
        pop     rax     
        ;;; loadc
        mov     rax,    1       
        push    rax     
        ;;; loadc
        mov     rax,    8       
        push    rax     
        ;;; store
        pop     qword rdx
        neg     rdx     
        add     rdx,    rbx     
        pop     qword rax
        mov     qword [rdx],rax     
        push    rax     
        ;;; loadc
        mov     rax,    0       
        push    rax     
                for_1:         
        ;;; loadc
        mov     rax,    8       
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; loadc
        mov     rax,    2       
        push    rax     
        ;;; gr
        pop     rcx     
        pop     rax     
        cmp     rax,    rcx     
        setg    al      
        movzx   rax,    al      
        push    rax     
        ;;; jumpz
        pop     rax     
        test    rax,    rax     
        je      endfor_1
        ;;; pop
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
        mov     rax,    2       
        push    rax     
        ;;; mul
        pop     rcx     
        pop     rax     
        mul     rcx     
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
        ;;; loadc
        mov     rax,    8       
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; loadc
        mov     rax,    1       
        push    rax     
        ;;; sub
        pop     rcx     
        pop     rax     
        sub     rax,    rcx     
        push    rax     
        ;;; loadc
        mov     rax,    8       
        push    rax     
        ;;; store
        pop     qword rdx
        neg     rdx     
        add     rdx,    rbx     
        pop     qword rax
        mov     qword [rdx],rax     
        push    rax     
        ;;; jump
        jmp     for_1   
                endfor_1:         
        ;;; Ende des eigentlichen Programms
                
        pop     rax     
        mov     rsi,    rax     
        mov     rdi,    i64_fmt         ; arguments in rdi, rsi
        mov     rax,    0               ; no xmm registers used
        push    rbp                     ; set up stack frame, must be alligned
        call    printf                  ; Call C function
        pop     rbp                     ; restore stack
        add     rsp,    16              ; free space for 16 bytes of global variables
                
        ;;; Rueckkehr zum aufrufenden Kontext
        pop     rbp                     ; original rbp ist last thing on the stack
        mov     rax,    0               ; return 0
        ret     
