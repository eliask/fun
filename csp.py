class CSP(list):
    def __init__(self, constraints):
        self.constraints = constraints

def select_var(csp, assignment):
    assigned_vars = dict(assignment).keys()
    # Choose the most constrained variable:
    for var,dom in sorted(csp, key=lambda(var,dom):len(dom)):
        if not var in assigned_vars:
            return var,dom

def csp_solve(csp, assignment):
    if len(assignment) == len(csp):
        return assignment

    var,dom = select_var(csp, assignment)
    for val in dom:
        if all(C(var,val,assignment) for C in csp.constraints):
            sol = csp_solve( csp, assignment+[(var,val)] )
            if sol: return sol

def all_diff(vars):
    def constraint(_var,_val,assignment):
        if not _var in vars:
            return True
        elim=[]
        for var,val in assignment:
            if not var in vars: continue
            if val in elim: return False
            elim.append(val)
        return not _val in elim

    return constraint

from operator import concat
def sudoku2csp(sudoku):
    rows=[ range(9*i,9*(i+1)) for i in range(9) ]
    cols=[ [9*i+j for i in range(9)] for j in range(9) ]
    blocks=[ [ rows[x+i][y+j] for i in range(3) for j in range(3) ]
             for x in range(0,9,3) for y in range(0,9,3) ]
    constraints = reduce(concat, [map(all_diff, C) for C in rows,cols,blocks])

    csp = CSP(constraints)
    for var,s in enumerate(sudoku):
        dom = range(1,10)
        if s != '.': dom = [int(s)]
        csp.append((var,dom))

    return csp

def print_sudoku(x):
    for i in range(9):
        print ' '.join(map(str, x[9*i : 9*(i+1)]))
    print

def sudoku_solve(x):
    print_sudoku(x)
    res = csp_solve(sudoku2csp(x), [])
    res = [x[1] for x in sorted(res, key=lambda(var,val):var)]
    print_sudoku(res)

sudoku1 = "..2.9..6..4...1..8.7.42...35.....3....1.6.5....3.....61...57.4.6..9...2..2..8.1.."
sudoku9 = "9..1.4..2.8..6..7..........4.......1.7.....3.3.......7..........3..7..8.1..2.9..4"
sudoku_solve(sudoku1)
#sudoku_solve(sudoku9)
