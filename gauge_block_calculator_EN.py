'''
Author: Anton CN
YouTube: https://www.youtube.com/@boessi
This program has the following advantages:
-It is guaranteed to find the exact combination of end gauges if one exists.
-It uses recursion with backtracking to check all possible combinations.
-It takes floating point inaccuracies into account by using a very small tolerance value (1e-9).
-It outputs the combination found, the number of end gauges used, and the total sum.

To run the program, make sure you have Python and Tkinter installed.

The backtracking in this program works like this:
1.) The find_end_gauges function implements the backtracking algorithm. It tries to find a combination of end gauges
that exactly gives the target length.
2.) The algorithm starts with an empty combination and gradually adds end gauges.
3.) In each step, a end gauge is added to the current combination and checked:
-If the sum of the end gauges is equal to the target length, a solution has been found.
-If the sum is greater than the target length, this path is not useful.
-If the sum is smaller, the search continues recursively.
If a path does not lead to a solution, the algorithm "backtracks" by returning to the previous state and trying another option.

The process repeats until either a solution is found or all possibilities are exhausted.

Using a set (used_end_measurements) ensures that each end measure is used only once.

This approach makes it possible to search the solution space efficiently by terminating non-useful paths early.
'''

import tkinter as tk
from tkinter import ttk, messagebox, font, scrolledtext

# Function to find gauge blocks using recursion and backtracking
def find_gauge_blocks(target, available_blocks, current_combination=None, used_blocks=None):
    if current_combination is None:
        current_combination = []
    if used_blocks is None:
        used_blocks = set()

    current_sum = sum(current_combination)

    if abs(current_sum - target) < 0.005:
        return current_combination

    if current_sum > target:
        return None

    for i, block in enumerate(available_blocks):
        if block not in used_blocks:
            new_combination = current_combination + [block]
            new_used = used_blocks.copy()
            new_used.add(block)
            result = find_gauge_blocks(target, available_blocks, new_combination, new_used)
            if result:
                return result

    return None

# GUI Application class
class GaugeBlockCalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Anton CNC: Gauge Block Calculator")
        master.geometry("440x750")

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=16)
        master.option_add("*Font", default_font)

        self.blocks_ideal = [
            50, 30, 20, 10, 9, 8, 7, 6, 5, 4, 3, 2,
            1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2,
            1.1, 1.09, 1.08, 1.07, 1.06, 1.05,
            1.04, 1.03, 1.02, 1.01, 1.005, 1
        ]

        self.blocks_real = [
            50.00028, 30.00025, 19.99979, 10.00012, 9.00005, 7.99960, 6.99985, 5.99988,
            5.00002, 4.00040, 3.00002, 2.00014, 1.90028, 1.79992, 1.70032, 1.60038,
            1.50033, 1.40016, 1.29970, 1.20005, 1.10000, 1.09045, 1.07969, 1.07010,
            1.06015, 1.04972, 1.04004, 1.03040, 1.01967, 1.01005, 1.00472, 0.99990
        ]

        self.label = ttk.Label(master, text="Desired Length (mm):")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(master)
        self.entry.pack()
        self.entry.bind("<Return>", lambda event: self.calculate())

        self.mode_selection = tk.StringVar(value="ideal")
        self.radio_frame = ttk.Frame(master)
        self.radio_frame.pack()

        self.ideal_radio = ttk.Radiobutton(self.radio_frame, text="Ideal", variable=self.mode_selection, value="ideal")
        self.real_radio = ttk.Radiobutton(self.radio_frame, text="Real", variable=self.mode_selection, value="real")
        self.ideal_radio.pack(side=tk.LEFT, padx=10)
        self.real_radio.pack(side=tk.LEFT, padx=10)

        self.calculate_button = ttk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(master, height=20, width=50)
        self.result_text.pack(pady=10, padx=10)
        self.result_text.configure(padx=20, pady=10)

    def calculate(self):
        self.result_text.delete(1.0, tk.END)

        try:
            input_value = self.entry.get().replace(',', '.')
            target = float(input_value)
            if target <= 0:
                messagebox.showerror("Error", "Length must be greater than 0.")
                return

            if self.mode_selection.get() == "ideal":
                available_blocks = self.blocks_ideal
            else:
                available_blocks = self.blocks_real

            result = find_gauge_blocks(target, available_blocks)

            if result:
                self.result_text.insert(tk.END, f"Exact length of {target} mm:\n\n")
                for block in result:
                    if block < 10:
                        self.result_text.insert(tk.END, f" {block:.5f} mm\n")
                    else:
                        self.result_text.insert(tk.END, f"{block:.5f} mm\n")
                self.result_text.insert(tk.END, f"\nNumber of gauge blocks: {len(result)}\n")

                if self.mode_selection.get() == "real":
                    real_sum = sum(result)
                    deviation = real_sum - target
                    self.result_text.insert(tk.END, f"Sum (real): {real_sum:.5f} mm\n")
                    self.result_text.insert(tk.END, f"Deviation: {deviation:.5f} mm\n")
                else:
                    self.result_text.insert(tk.END, f"Sum: {sum(result):.5f} mm\n")
            else:
                self.result_text.insert(tk.END, f"No exact combination for {target} mm found.")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

# Run the application
root = tk.Tk()
app = GaugeBlockCalculatorApp(root)
root.mainloop()
