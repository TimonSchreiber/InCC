## TODO-List

 - [x] `Loop expr Do expr`
 - [x] `For assign; bool_expr; assign Do expr`
 - [x] `If expr Then expr`
 - [x] `If expr Then expr Else expr`
 - [x] `While expr Do expr`
 - [x] create separate Enviroment class
 - [ ] create separate REPL class
 - [x] `Lock id[(, id)*] In expr` TODO: for now only one id allowed...
 - [x] `Local id assign expr In expr`
 - [ ] change generic expressions in loop/for/while/ite into assign_expr/- bool_expr/...
 - [x] split interpreter.all_expr into files matching lexer/|parser/
 - [x] Lambda: `[id :=] var -> expr`
 - [ ] Lambda: `[id :=] -> expr`
 - [ ] Lambda: `[id :=] v1, v2, ... -> expr`
 - [ ] String, Char Datatypes
 - [ ] List: list(v1,v2,...)
 - [ ] Array: [v1,v2,...] (optional array(v1,v2,...))