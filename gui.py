import sys
from ortools.linear_solver import pywraplp
import pulp as pl
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QDoubleSpinBox, QTextEdit

def on_button_clicked():
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        return

    # x and y are integer non-negative variables.
    strength = solver.IntVar(8, 99, "strength")
    dexterity = solver.IntVar(8, 99, "dexterity")
    intelligence = solver.IntVar(8, 99, "intelligence")
    faith = solver.IntVar(8, 99, "faith")

    # Scaling factors for each stat
    strength_scaling = spin_box1.value()
    dexterity_scaling = spin_box2.value()
    intelligence_scaling = spin_box3.value()
    faith_scaling = spin_box4.value()

    # Base AR and MR values
    base_AR = 126
    base_MR = 83

    print("Number of variables =", solver.NumVariables())

    solver.Add(strength + dexterity + intelligence + faith >= 40)
    solver.Add(strength + dexterity + intelligence + faith <= 120)

    # All variables must be less than their softcaps.
    solver.Add(strength <= 40)
    solver.Add(dexterity <= 40)
    solver.Add(intelligence <= 30)
    solver.Add(faith <= 30)

    # print("Number of constraints =", solver.NumConstraints())

    # Maximize x + 10 * y.
    solver.Maximize((base_AR * (strength_scaling * strength + dexterity_scaling * dexterity + intelligence_scaling * intelligence  + faith_scaling * faith) + base_MR * (strength_scaling * strength + dexterity_scaling * dexterity + intelligence_scaling * intelligence  + faith_scaling * faith)))

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result_text_edit.setText(f"Strength: {strength.solution_value()}\nDexterity: {dexterity.solution_value()}\nIntelligence: {intelligence.solution_value()}\nFaith: {faith.solution_value()}\n\nHighest possible AR: {solver.Objective().Value()/10}")
        
    else:
        result_text_edit.setText("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Dark Souls AR Calculator")

layout = QVBoxLayout()

# Create spin boxes for numerical input
spin_box1 = QDoubleSpinBox()
spin_box2 = QDoubleSpinBox()
spin_box3 = QDoubleSpinBox()
spin_box4 = QDoubleSpinBox()

# Set default values for the spin boxes
spin_box1.setValue(0.31)   # Default value for spin box 1
spin_box2.setValue(0.3)  # Default value for spin box 2
spin_box3.setValue(0.26)  # Default value for spin box 3
spin_box4.setValue(0.26)  # Default value for spin box 4
# Create labels for each spin box

label1 = QLabel("STR:")
label2 = QLabel("DEX:")
label3 = QLabel("INT:")
label4 = QLabel("FTH:")

# Result label
# Replace QLabel with QTextEdit for the result
result_text_edit = QTextEdit()
result_text_edit.setReadOnly(True)  # Make it read-only
result_text_edit.setPlainText("Enter values and click the button to calculate the weapon's AR.")

# Button to trigger sum calculation
button = QPushButton("Calculate Sum")
button.clicked.connect(on_button_clicked)

# Adding widgets to the layout
layout.addWidget(label1)
layout.addWidget(spin_box1)
layout.addWidget(label2)
layout.addWidget(spin_box2)
layout.addWidget(label3)
layout.addWidget(spin_box3)
layout.addWidget(label4)
layout.addWidget(spin_box4)
layout.addWidget(button)
layout.addWidget(result_text_edit)



window.setLayout(layout)
window.show()

sys.exit(app.exec())
