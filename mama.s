                
        extern  printf  
        extern  malloc  
        SECTION .data                   ; Data section, initialized variables
        i64_fmt: db      "%lld", 10,     0       ; printf format for printing an int64
                
        SECTION .text   
        global  main    
        main:         
        push    rbp                     ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault
        mov     rax,    rsp             ; rsp zeigt auf den geretteten rbp
        sub     rax,    qword 8         ; neuer rbp sollte ein wort darüber liegen
        mov     rbp,    rax             ; set frame pointer to current (empty) stack pointer
        sub     rsp,    0               ; reserve space for 0 bytes of global variables
                
        ;;; Start des eigentlichen Programms
        ;;; mkvec 0
                
        mov     rdi,    16      
        call    malloc  
        mov     rdx,    rax     
                
        mov     qword [rdx],'V'     
        mov     qword [rdx + 8],0       
                
        pop     rax     
        mov     qword [rdx+8],rax     
                
        push    rdx     
        ;;; mkfunval lambda_1
                
        mov     rdi,    32      
        call    malloc  
        mov     rdx,    rax     
                
        mov     qword [rdx],"F"     
        mov     qword [rdx+8],lambda_1
        mov     qword [rdx+16],0       
        pop     qword [rdx+24]
        push    rdx     
        ;;; jump endlambda_1
        jmp     endlambda_1
                lambda_1:         
        ;;; pushloc 0
        mov     rdx,    rsp     
        add     rdx,    0       
        mov     rax,    [rdx]   
        push    rax     
        ;;; popenv
        mov     rbx,    [rbp + 16]      ; gp <- s[fp-2]
        pop     rax                     ; s[fp-2] <- s[sp]
        mov     [rbp + 16],rax          ; ...
        mov     rcx,    rbp             ; sp <- fp-2
        add     rcx,    16              ; ...
        mov     rsp,    rcx             ; ...
        mov     rax,    [rbp]           ; rax <-s[fp] ...
        mov     rbp,    [rbp + 8]       ; fp <- s[fp-1]
        jmp     rax                     ; pc <- rax=s[fp]
                endlambda_1:         
        ;;; loadc 5
        mov     rax,    5       
        push    rax     
        ;;; mkbasic
                
        mov     rdi,    16      
        call    malloc  
        mov     rdx,    rax     
                
        mov     qword [rdx],'B'     
        pop     rax     
        mov     [rdx + 8],rax     
        push    rdx     
        ;;; slide 1
        pop     rax     
        add     rsp,    8       
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
        add     rsp,    0               ; free space for 0 bytes of global variables
                
        ;;; Rueckkehr zum aufrufenden Kontext
        pop     rbp                     ; original rbp ist last thing on the stack
        mov     rax,    0               ; return 0
        ret     
                
