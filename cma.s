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
        mov     rax,    3       
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
        ;;; jump
        jmp     endproc_1
                proc_1:         
        ;;; enter
        mov     rbp,    rbx     
        sub     rbp,    rsp     
        ;;; alloc
        sub     rsp,    qword 8 
        ;;; loadc
        mov     rax,    0       
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; loadrc
        mov     rax,    rbp     
        add     rax,    qword -16
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; add
        pop     rcx     
        pop     rax     
        add     rax,    rcx     
        push    rax     
        ;;; loadrc
        mov     rax,    rbp     
        add     rax,    qword 8 
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
        ;;; jump
        jmp     endproc_2
                proc_2:         
        ;;; enter
        mov     rbp,    rbx     
        sub     rbp,    rsp     
        ;;; alloc
        sub     rsp,    qword 8 
        ;;; loadrc
        mov     rax,    rbp     
        add     rax,    qword -16
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; loadc
        mov     rax,    0       
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; add
        pop     rcx     
        pop     rax     
        add     rax,    rcx     
        push    rax     
        ;;; loadrc
        mov     rax,    rbp     
        add     rax,    qword -24
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; sub
        pop     rcx     
        pop     rax     
        sub     rax,    rcx     
        push    rax     
        ;;; loadrc
        mov     rax,    rbp     
        add     rax,    qword 8 
        push    rax     
        ;;; store
        pop     qword rdx
        neg     rdx     
        add     rdx,    rbx     
        pop     qword rax
        mov     qword [rdx],rax     
        push    rax     
        ;;; loadrc
        mov     rax,    rbp     
        add     rax,    qword -16
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
        ;;; ret
        mov     rsp,    rbx             ; restore stack pointer to prev frame
        sub     rsp,    rbp             ; rsp <- rbx - rbp (=N)
        mov     rax,    rbx             ; restore frame pointer
        sub     rax,    rbp     
        mov     rbp,    [rax+8]         ; rbp <- [rbx - rbp + 8]
        ret     
                endproc_2:         
        ;;; loadc
        mov     rax,    proc_2  
        push    rax     
        ;;; loadc
        mov     rax,    16      
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
        mov     rax,    7       
        push    rax     
        ;;; loadrc
        mov     rax,    rbp     
        add     rax,    qword 8 
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; mark
        push    rbp     
        ;;; loadc
        mov     rax,    16      
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; call
        pop     rax     
        call    rax     
        ;;; pop
        pop     rax     
        ;;; slide
        pop     rax     
        add     rsp,    qword 8 
        push    rax     
        ;;; loadrc
        mov     rax,    rbp     
        add     rax,    qword -16
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
        ;;; ret
        mov     rsp,    rbx             ; restore stack pointer to prev frame
        sub     rsp,    rbp             ; rsp <- rbx - rbp (=N)
        mov     rax,    rbx             ; restore frame pointer
        sub     rax,    rbp     
        mov     rbp,    [rax+8]         ; rbp <- [rbx - rbp + 8]
        ret     
                endproc_1:         
        ;;; loadc
        mov     rax,    proc_1  
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
        ;;; pop
        pop     rax     
        ;;; loadc
        mov     rax,    3       
        push    rax     
        ;;; mark
        push    rbp     
        ;;; loadc
        mov     rax,    8       
        push    rax     
        ;;; load
        pop     rdx     
        neg     rdx     
        add     rdx,    rbx     
        push    qword [rdx]
        ;;; call
        pop     rax     
        call    rax     
        ;;; pop
        pop     rax     
        ;;; slide
        pop     rax     
        add     rsp,    qword 0 
        push    rax     
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
