counter = '''
{ counter := s ->
    local acc := s in n ->
        acc := acc + n
; c := counter(0)
; a1 := c(1)
; a2 := c(1)
; a3 := c(1)
; a4 := c(2)
; a5 := c(3)
}'''
