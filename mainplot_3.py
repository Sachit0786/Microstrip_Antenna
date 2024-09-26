import tkinter as tk
import math
from fractions import Fraction
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


def calculate():
    global L
    global h
    global Lf
    global W
    global y0
    global DL
    global Wm
    try:
        er = float(entry1.get())
        h = float(entry2.get())
        f0 = float(entry3.get())
        rin = float(entry4.get())
        Wm = float(entry5.get())        

        c = 299792458
        W = c/(2*f0*1e9*(math.sqrt((er+1)/2)))
        ef = (er+1)/2+((er-1)/2)*(pow(1+12*(h/1000)/W,-0.5))
        Lf = c/(2*f0*1e9*(math.sqrt(ef)))
        DL = 0.412*h/1000*((ef+0.3)*(W/(h/1000)+0.264))/((ef-0.258)*(W/(h/1000)+0.8))
        L = Lf-2*DL
        L *= 1000
        DL *= 1000
        Lf *= 1000
        W *= 1000
        k0 = 2 * math.pi * f0 / c * 1e9
        G1 = Wm / (120 * math.pi**2) * (1 - 1 / (24 * (k0 * h/1000)**2))
        G12 = 1e-4
        Rin = 1 / (2 * (G1 + G12))
        y0 = (math.acos(math.sqrt(rin/Rin))*L/(math.pi))
        
        print(f"er: {er}, h: {h}, f0: {f0}, rin: {rin}, Wm: {Wm}")
        
        result_text.set(f"Width(mm): {W:.5f}\nLength(mm): {L:.5f}\nEffective length of patch(mm): {Lf:.5f}\nInput Impedance : {Rin:.5f}\nLength of feed line(mm): {DL:.5f}\nInset feed point is {y0:.5f}mm from edge of patch")

    except ValueError as e:
        print(f"Error: {e}")
        result_text.set("INVALID INPUT\nPlease enter valid numbers.")

def reset():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)
    entry4.delete(0, tk.END)
    entry5.delete(0, tk.END)
    result_text.set("Results will be displayed here")

def show_figure():
    # Given dimensions in millimeters (customize these values)
    length = Lf
    width = Wm
    height_lower = 0.5
    height_upper = h
    pad_length = L
    pad_width = W
    ant_height = h/8
    box_length = W/5
    box_shift = width / 2

    # Create a figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define the lower box vertices
    vertices_lower = [
        [0, 0, 0],
        [0, width, 0],
        [length, width, 0],
        [length, 0, 0],
        [0, 0, height_lower],
        [0, width, height_lower],
        [length, width, height_lower],
        [length, 0, height_lower]
    ]

    # Define the lower box faces
    faces_lower = [
        [vertices_lower[0], vertices_lower[1], vertices_lower[5], vertices_lower[4]],
        [vertices_lower[1], vertices_lower[2], vertices_lower[6], vertices_lower[5]],
        [vertices_lower[2], vertices_lower[3], vertices_lower[7], vertices_lower[6]],
        [vertices_lower[3], vertices_lower[0], vertices_lower[4], vertices_lower[7]],
        [vertices_lower[0], vertices_lower[3], vertices_lower[2], vertices_lower[1]],
        [vertices_lower[4], vertices_lower[5], vertices_lower[6], vertices_lower[7]]
    ]

    # Create a Poly3DCollection for the lower box with alpha set to 1.0 and face color red
    cuboid_lower = Poly3DCollection(faces_lower, edgecolor='black', alpha=1.0, facecolors='red', label='Ground')

    # Add the lower box to the 3D axis
    ax.add_collection3d(cuboid_lower)

    # Define the upper box vertices (positioned above the lower box)
    vertices_upper = [
        [0, 0, height_lower],
        [0, width, height_lower],
        [length, width, height_lower],
        [length, 0, height_lower],
        [0, 0, height_lower + height_upper],
        [0, width, height_lower + height_upper],
        [length, width, height_lower + height_upper],
        [length, 0, height_lower + height_upper]
    ]

    # Define the upper box faces
    faces_upper = [
        [vertices_upper[0], vertices_upper[1], vertices_upper[5], vertices_upper[4]],
        [vertices_upper[1], vertices_upper[2], vertices_upper[6], vertices_upper[5]],
        [vertices_upper[2], vertices_upper[3], vertices_upper[7], vertices_upper[6]],
        [vertices_upper[3], vertices_upper[0], vertices_upper[4], vertices_upper[7]],
        [vertices_upper[0], vertices_upper[3], vertices_upper[2], vertices_upper[1]],
        [vertices_upper[4], vertices_upper[5], vertices_upper[6], vertices_upper[7]]
    ]

    # Create a Poly3DCollection for the upper box with alpha set to 1.0 and face color yellow
    cuboid_upper = Poly3DCollection(faces_upper, edgecolor='black', alpha=1.0, facecolors='yellow', label='Substrate')

    # Add the upper box to the 3D axis
    ax.add_collection3d(cuboid_upper)

    # Define the additional box vertices (centered on top)
    vertices_ant = [
        [(length - pad_length) / 2, (width - pad_width) / 2, height_lower + height_upper],
        [(length - pad_length) / 2, (width + pad_width) / 2, height_lower + height_upper],
        [(length + pad_length) / 2, (width + pad_width) / 2, height_lower + height_upper],
        [(length + pad_length) / 2, (width - pad_width) / 2, height_lower + height_upper],
        [(length - pad_length) / 2, (width - pad_width) / 2, height_lower + height_upper + ant_height],
        [(length - pad_length) / 2, (width + pad_width) / 2, height_lower + height_upper + ant_height],
        [(length + pad_length) / 2, (width + pad_width) / 2, height_lower + height_upper + ant_height],
        [(length + pad_length) / 2, (width - pad_width) / 2, height_lower + height_upper + ant_height]
    ]

    # Define the additional box faces
    faces_ant = [
        [vertices_ant[0], vertices_ant[1], vertices_ant[5], vertices_ant[4]],
        [vertices_ant[1], vertices_ant[2], vertices_ant[6], vertices_ant[5]],
        [vertices_ant[2], vertices_ant[3], vertices_ant[7], vertices_ant[6]],
        [vertices_ant[3], vertices_ant[0], vertices_ant[4], vertices_ant[7]],
        [vertices_ant[0], vertices_ant[3], vertices_ant[2], vertices_ant[1]],
        [vertices_ant[4], vertices_ant[5], vertices_ant[6], vertices_ant[7]]
    ]

    # Create a Poly3DCollection for the additional box with alpha set to 1.0 and face color blue
    cuboid_ant = Poly3DCollection(faces_ant, edgecolor='black', alpha=0.5, facecolors='blue', label='Antenna Patch')

    # Add the additional box to the 3D axis
    ax.add_collection3d(cuboid_ant)

    # Define the box vertices (centered on top, shifted along X-axis) with str_height
    str_height = ant_height

    vertices_box = [
        [length-DL-y0 , box_shift - box_length / 2, height_lower + height_upper],
        [length-DL-y0 , box_shift + box_length / 2, height_lower + height_upper],
        [length, box_shift + box_length / 2, height_lower + height_upper],
        [length, box_shift - box_length / 2, height_lower + height_upper],
        [length-DL-y0 , box_shift - box_length / 2, height_lower + height_upper + str_height],
        [length-DL-y0 , box_shift + box_length / 2, height_lower + height_upper + str_height],
        [length, box_shift + box_length / 2, height_lower + height_upper + str_height],
        [length, box_shift - box_length / 2, height_lower + height_upper + str_height]
    ]


    # Define the box faces
    faces_box = [
        [vertices_box[0], vertices_box[1], vertices_box[2], vertices_box[3]],
        [vertices_box[4], vertices_box[5], vertices_box[6], vertices_box[7]],
        [vertices_box[0], vertices_box[1], vertices_box[5], vertices_box[4]],
        [vertices_box[1], vertices_box[2], vertices_box[6], vertices_box[5]],
        [vertices_box[2], vertices_box[3], vertices_box[7], vertices_box[6]],
        [vertices_box[3], vertices_box[0], vertices_box[4], vertices_box[7]]
    ]

    # Create a Poly3DCollection for the box with alpha set to 1.0 and face color blue
    box = Poly3DCollection(faces_box, edgecolor='black', alpha=1.0, facecolors='pink', label='Transmission line')

    # Add the box to the 3D axis
    ax.add_collection3d(box)

    # Set increased axis limits
    ax.set_xlim([0, length + 10])  # Increase X limit by 10
    ax.set_ylim([0, width + 10])   # Increase Y limit by 10
    ax.set_zlim([0, height_lower + height_upper + ant_height + 5])  # Increase Z limit by 5

    # Set axis labels and title
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('Three 3D Cuboids with 3D Box')

    # Add legend
    ax.legend()

    # Show the plot
    plt.show()



# GUI setup
root = tk.Tk()
root.title("Microstrip Antenna line Feed Desinger")

# Input fields
label1 = tk.Label(root, text="Dielectric Constant:")
label1.grid(row=0, column=0, padx=10, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=5)

label2 = tk.Label(root, text="Dielectric Height(mm):")
label2.grid(row=1, column=0, padx=10, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=10, pady=5)

label3 = tk.Label(root, text="Frequency(GHz):")
label3.grid(row=2, column=0, padx=10, pady=5)
entry3 = tk.Entry(root)
entry3.grid(row=2, column=1, padx=10, pady=5)

label4 = tk.Label(root, text="Required Input Impedance(ohms):")
label4.grid(row=3, column=0, padx=10, pady=5)
entry4 = tk.Entry(root)
entry4.grid(row=3, column=1, padx=10, pady=5)

label5 = tk.Label(root, text="Width(mm) : ")
label5.grid(row=4, column=0, padx=10, pady=5)
entry5 = tk.Entry(root)
entry5.grid(row=4, column=1, padx=10, pady=5)


# Calculate button
calculate_button = tk.Button(root, text="Compute", command=calculate)
calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

# Reset button
reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.grid(row=6, column=0, columnspan=2, pady=10)

# Result text
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text)
result_label.grid(row=7, column=0, columnspan=2, pady=10)

# Figure Command
figure_button = tk.Button(root, text="Generate Model", command=show_figure)
figure_button.grid(row=8, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()

