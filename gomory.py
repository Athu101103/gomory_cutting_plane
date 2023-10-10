import streamlit as st
import numpy as np
import copy
import sys
import math
from simplex import *

ip_file = "input.txt"
op_file = "output.txt"

def print_cp_results(message, opt_val, opt_vect, num_x, num_cuts):
    if message != "Optimal":
        print(message)
        print(num_cuts)
        return
    print(-round(opt_val, 6))
    x = []
    ind = 1
    for key in opt_vect:
        x.append(int(opt_vect[key]))
        if ind >= num_x:
            break
        ind+=1
    print(*x)
    
    st.write("Message:", message)
    st.write("Number of Gomory Cuts:", num_cuts)
    if message == "Optimal":
        st.write("Optimal Value:", -round(opt_val, 6))
        st.write("Optimal Vector:")
        st.write({key: int(opt_vect[key]) for key in opt_vect})
    else:
        st.write("Infeasible/Unbounded")

def gomory_cutting_plane(c, A, b):
    ini_A, num_row_A, num_col_A, ini_b, ini_c, ini_num_slack, ini_num_artificial, ini_B, ini_vars = initialize(ip_file)
    flag = True
    num_gomory = 0
    ini_c = [-i for i in ini_c]

    while flag:
        message, opt_val, opt_val_vector, basic_variables, x_B, c_j, A_matrix = lp_solve(ini_A, ini_b, ini_c, ini_B, ini_vars, ini_num_artificial, ini_num_slack)

        if message == "Optimal":
            frac_var = None
            for key in opt_val_vector:
                if opt_val_vector[key] != int(opt_val_vector[key]) and key.startswith("x"):
                    frac_var = key
                    break

            if frac_var is None:
                flag = False
            else:
                num_gomory += 1
                ini_num_slack += 1

                vars = ini_vars
                vars.append("Sg" + str(num_gomory))

                basic_variables = ini_B
                basic_variables.append("Sg" + str(num_gomory))

                frac_eq_ind = basic_variables.index(frac_var)

                x_B = ini_b
                x_B.append(math.floor(x_B[frac_eq_ind]))

                c_j.append(0.0)

                num_c = len(A_matrix[0])
                new_constr = [0.0] * num_c

                for i in range(num_c):
                    new_constr[i] = math.floor(A_matrix[frac_eq_ind][i])

                new_constr[-1] = 1.0
                A_matrix.append(new_constr)

        else:
            flag = False

    sys.stdout = open(op_file, 'w')
    print_cp_results(message, opt_val, opt_val_vector, num_col_A, num_gomory)
    sys.stdout.close()

    return {
        "message": message,
        "opt_val": opt_val,
        "opt_val_vector": {key: int(opt_val_vector[key]) for key in opt_val_vector},
        "num_gomory": num_gomory
    }



if __name__ == "__main__":
    st.title("Cutting Plane Method Solver")

    # Input for objective function coefficients
    st.subheader("Objective Function Coefficients")
    c = []
    for i in range(st.number_input("Number of variables", min_value=1, step=1)):
        c.append(st.number_input(f"c{i+1}"))

    # Input for constraint coefficients
    st.subheader("Constraint Coefficients (Enter one row at a time)")
    constraint_counter = 0  # Counter to ensure unique keys for checkboxes
    while st.checkbox("Add constraint", key=f"constraint_checkbox_{constraint_counter}"):
        constraint_row = []
        for i in range(len(c)):
            constraint_row.append(st.number_input(f"A{i+1}"))
        b.append(st.number_input("b"))
        A.append(constraint_row)
        constraint_counter += 1  # Increment the counter for unique keys

    A = np.array(A)
    b = np.array(b)

    # Run the Gomory Cutting Plane Method
    if st.button("Run Cutting Plane Method"):
        gomory_cutting_plane(c, A, b)