import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class SignalProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Exercise 1")
        
        self.file1 = None
        self.file2 = None
        self.data1 = None
        self.data2 = None
        self.result = None
        
        self.init_gui()
        
    def init_gui(self):
        tk.Button(self.root, text="Load Signal 1", command=self.load_file1).pack()
        tk.Button(self.root, text="Load Signal 2", command=self.load_file2).pack()
        
        tk.Button(self.root, text="Calculate Correlation", command=self.init_correlation).pack()
        tk.Button(self.root, text="Calculate Autocorrelation (Signal 1)", command=self.init_autocorrelation).pack()
 
        tk.Button(self.root, text="Save Result", command=self.save_result).pack()
        
        tk.Button(self.root, text="Display Oscillogram", command=self.display_oscillogram).pack()
        
        
    def load_file1(self):
        self.file1 = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file1:
            self.data1 = pd.read_csv(self.file1)
            
    def load_file2(self):
        self.file2 = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file2:
            self.data2 = pd.read_csv(self.file2)
            
    def update_channels(self):
        if self.data1 is not None:
            channels = self.data1.columns.tolist()
            self.channel_var.set(channels[0])
            menu = self.channel_dropdown['menu']
            menu.delete(0, 'end')
            for channel in channels:
                menu.add_command(label=channel, command=tk._setit(self.channel_var, channel))
    
    def init_correlation(self):
        if self.data1 is not None and self.data2 is not None:
            signal1 = self.data1.values.flatten()
            signal2 = self.data2.values.flatten()
            correlation = self.calculate_correlation(signal1, signal2)
            self.show_result(correlation, "Correlation")
    
    def init_autocorrelation(self):
        if self.data1 is not None:
            signal = self.data1.values.flatten()
            autocorrelation = self.calculate_correlation(signal, signal)
            self.show_result(autocorrelation, "Autocorrelation")
    
    def calculate_correlation(self, signal1, signal2):
        shortened_signal_length = min(len(signal1), len(signal2))
        signal1 = signal1[:shortened_signal_length]
        signal2 = signal2[:shortened_signal_length]
        mean_signal1 = sum(signal1) / shortened_signal_length
        mean_signal2 = sum(signal2) / shortened_signal_length
        variance_signal1 = sum((x - mean_signal1) ** 2 for x in signal1) / shortened_signal_length
        variance_signal2 = sum((x - mean_signal2) ** 2 for x in signal2) / shortened_signal_length
        correlation = []
        for k in range(shortened_signal_length):
            sum_value = 0
            for n in range(shortened_signal_length - k):
                sum_value += (signal1[n] - mean_signal1) * (signal2[n + k] - mean_signal2)
            correlation.append(sum_value / (shortened_signal_length * (variance_signal1 * variance_signal2) ** 0.5))
        return correlation
    
    def show_result(self, result, title):
        plt.figure()
        plt.plot(result)
        plt.title(title)
        plt.show()
        self.result = result
    
    def display_oscillogram(self):
        if self.data1 is not None:
            channel = self.channel_var.get()
            if channel in self.data1.columns:
                signal = self.data1[channel].values
                plt.figure()
                plt.plot(signal)
                plt.title("Oscillogram")
                plt.show()
            else:
                messagebox.showerror("Error", f"Column '{channel}' not found in the file.")
    
    def save_result(self):
        if self.result is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                pd.DataFrame(self.result).to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Result saved successfully")
        else:
            messagebox.showwarning("No result", "No result to save")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessor(root)
    root.mainloop()