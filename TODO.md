## Notes:

### Bücher:

* Übersetzerbau - Virtuelle Maschinen

### Git:

https://git.inf.h-brs.de/aaster2m/incc24

### Übersetzungen:
1. `nasm -g -F dwarf -o example.o -f elf64 example.s`
    - `dwarf` -> ein debugging Format
    - `elf64` -> extended library Format in 64 Bit
2. `-gcc -g -gdwarf -ggdb -z noexecstack -o example example.o`
    - `-g -g -gdwarf` -> debugging Optionen
    - `-o example` -> Name der ausführbaren Datei
    - `-z noexecstack` -> der Unterdrückung einer Warnung gilt

## TODO-List

 - [x] `Loop expr Do expr`
 - [x] `For assign; bool_expr; assign Do expr`
 - [x] `If expr Then expr`
 - [x] `If expr Then expr Else expr`
 - [x] `While expr Do expr`
 - [x] create separate Enviroment class
 - [ ] create separate REPL class
 - [x] `Lock id[(, id)*] In expr`
 - [x] `Local id assign expr In expr`
 - [ ] change generic expressions in loop/for/while/ite into assign_expr/- bool_expr/...
 - [x] split interpreter.all_expr into files matching lexer/ and parser/
 - [x] Lambda: `[id :=] var -> expr`
 - [x] Lambda: `[id :=] -> expr`
 - [x] Lambda: `[id :=] v1, v2, ... -> expr`
 - [x] String, Char Datatypes
 - [x] List: `list(v1,v2,...)`
 - [x] List: `head` and `tail` implementation
 - [x] Array: `[v1,v2,...]` (optional `array(v1,v2,...)`)
 - [x] Array access: `id[expr]`
 - [x] Array: `[3+id1, id2]` not working, but `[id1+3, id2]` works
 - [x] Struct: `[id := ] struct {assign [, assign]*} `
 - [x] Struct member access: `id.id`
 - [x] Struct extension: `[id :=] extend struct_id {assign [, assign]*}`
 - [x] Struct: how to access higher lvl members inside struct -> `extend a {x:=1} extend b {x:=2} extend c {y := a.x or .x or ..x}
 - [x] Enviroment: Make the dot notation part of the env and not structs, bcs `s := extend {x := 5} {x := 2 + ..x}`
 - [x] Struct: Anonyme structs => `s := extend struct {...} {...}`
 - [x] Lambda: Add the Lambda \ to the definition
 - [ ] ? Types: add python tpye hints as much as possible for readability. t->ply.lex.LexToken; p->ply.yacc.YaccProduction
 - [ ] ? Lambda: Allow currying for all lambdas: `\x,y -> ...` is equal to `\x -> \y -> ...`
 - [ ] ? Add compound assignments and modulo to this language
 - [ ] Code comes from files instead of python strings
 - [ ] Procedure: `expression : proc (var_list) var_list -> expression`
