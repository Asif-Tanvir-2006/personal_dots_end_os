#!/usr/bin/env python3

import subprocess
import wlroots

# Initialize the Wayland display
wl_display = wlroots.Display()
wl_display.init()

# Create a list to store information about open windows
open_windows = []

# Define a function to handle new windows
@wlroots.global_registry.new_surface
def new_surface(surface):
    if surface.surface_type == wlroots.SurfaceType.WLR_SURFACE_TOPLEVEL:
        open_windows.append(surface)

# Start the Wayland event loop
wl_display.run()

# Generate a list of window names and PIDs
window_list = [
    f"{window.title} ({window.pid})"
    for window in open_windows
    if window.title and window.pid
]

# Pass the list of windows to Rofi for user selection
chosen_window = subprocess.run(
    ["rofi", "-dmenu", "-i", "-p", "Switch to Window:"],
    input="\n".join(window_list).encode("utf-8"),
    text=True,
    capture_output=True,
)

# Extract the PID of the chosen window
chosen_pid = chosen_window.stdout.strip().split(" ")[-1]

# Use wlr-roots to focus on the chosen window
for window in open_windows:
    if window.pid == chosen_pid:
        window.activate()

# Clean up and exit
wl_display.terminate()

