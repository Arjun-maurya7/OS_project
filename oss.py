import tkinter as tk
from tkinter import ttk
import psutil
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# Setup main window
root = tk.Tk()
root.title("Real-Time Memory Allocation Tracker")
root.geometry("800x500")

# Create a frame to hold the graph
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Set up figure and axis
fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot([], [], lw=2)
ax.set_title("Memory Usage Over Time")
ax.set_xlabel("Time")
ax.set_ylabel("Used Memory (MB)")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.setp(ax.get_xticklabels(), rotation=45)

# Embed the plot in Tkinter
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Data lists
time_data = []
mem_data = []

# Update function for animation
def update(frame):
    mem = psutil.virtual_memory().used / (1024 ** 2)  # Used memory in MB
    now = datetime.datetime.now()  # datetime object

    time_data.append(now)
    mem_data.append(mem)

    # Keep only latest 20 points
    if len(time_data) > 20:
        time_data.pop(0)
        mem_data.pop(0)

    # Update graph
    line.set_data(mdates.date2num(time_data), mem_data)

    if len(time_data) > 1:
        ax.set_xlim(mdates.date2num(time_data[0]), mdates.date2num(time_data[-1]))
    ax.relim()
    ax.autoscale_view()

    canvas.draw()

# Animation
ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)

# Start the GUI
root.mainloop()