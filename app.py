import streamlit as st
import numpy as np
from gomory import gomory_cutting_plane

st.title("Cutting Plane Method Solver")

# Input for objective function coefficients
st.subheader("Objective Function Coefficients")
c = []
num_variables = st.number_input("Number of variables", min_value=1, step=1)
for i in range(num_variables):
    c.append(st.number_input(f"Coefficient for c{i + 1}"))

# Input for constraint coefficients
st.subheader("Constraint Coefficients (Enter one row at a time)")
constraints = []
for i in range(num_variables):
    constraint_row = []
    st.write(f"Constraint {i + 1}")
    for j in range(num_variables):
        val = st.number_input(f"Coefficient for A{i + 1}{j + 1}", key=f"constraint_{i}_var_{j}")
        constraint_row.append(val)
    constraint_row.append(st.number_input(f"Right-hand side value for constraint {i + 1}", key=f"constraint_{i}_rhs"))
    constraints.append(constraint_row)

A = np.array(constraints)
b = np.array([constraint[-1] for constraint in constraints])

# Run the Gomory Cutting Plane Method
if st.button("Run Cutting Plane Method"):
    results = gomory_cutting_plane(c, A, b)

    # Display results in Streamlit
    st.write("Message:", results["message"])
    st.write("Number of Gomory Cuts:", results["num_gomory"])
    if results["message"] == "Optimal":
        st.write("Optimal Value:", -round(results["opt_val"], 6))
        st.write("Optimal Vector:", results["opt_val_vector"])
    else:
        st.write("Infeasible/Unbounded")