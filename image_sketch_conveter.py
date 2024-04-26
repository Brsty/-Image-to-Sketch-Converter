import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

DEFAULT_LINE_THICKNESS = 1
DEFAULT_CONTRAST = 1.0
DEFAULT_BRIGHTNESS = 0

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        try:
            img = cv2.imread(file_path)
            if img is None:
                raise ValueError("Unable to read the selected file.")
            sketch = convert_to_sketch(img)
            if sketch is None:
                raise ValueError("Sketch conversion failed.")
            show_preview(sketch)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def convert_to_sketch(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inverted = 255 - gray
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        inverted_blurred = 255 - blurred
        sketch = cv2.divide(gray, inverted_blurred, scale=256)
        return sketch
    except Exception as e:
        messagebox.showerror("Error", "Sketch conversion failed: " + str(e))
        return None

def show_preview(sketch):
    preview_window = tk.Toplevel()
    preview_window.title("Sketch Preview")
    
    parameter_frame = tk.Frame(preview_window)
    parameter_frame.pack(pady=10)
    
    line_thickness_label = tk.Label(parameter_frame, text="Line Thickness")
    line_thickness_label.grid(row=0, column=0, padx=5)
    line_thickness_slider = tk.Scale(parameter_frame, from_=1, to=10, orient="horizontal", length=200)
    line_thickness_slider.set(DEFAULT_LINE_THICKNESS)
    line_thickness_slider.grid(row=0, column=1, padx=5)
    
    contrast_label = tk.Label(parameter_frame, text="Contrast")
    contrast_label.grid(row=1, column=0, padx=5)
    contrast_slider = tk.Scale(parameter_frame, from_=0, to=2, resolution=0.1, orient="horizontal", length=200)
    contrast_slider.set(DEFAULT_CONTRAST)
    contrast_slider.grid(row=1, column=1, padx=5)
    
    brightness_label = tk.Label(parameter_frame, text="Brightness")
    brightness_label.grid(row=2, column=0, padx=5)
    brightness_slider = tk.Scale(parameter_frame, from_=-100, to=100, orient="horizontal", length=200)
    brightness_slider.set(DEFAULT_BRIGHTNESS)
    brightness_slider.grid(row=2, column=1, padx=5)
    
    preview_canvas = tk.Canvas(preview_window, width=sketch.shape[1], height=sketch.shape[0])
    preview_canvas.pack()
    
    sketch_photo = cv2.cvtColor(sketch, cv2.COLOR_BGR2RGB)
    sketch_photo = Image.fromarray(sketch_photo)
    sketch_photo = ImageTk.PhotoImage(sketch_photo)
    
    preview_canvas.create_image(0, 0, anchor=tk.NW, image=sketch_photo)
    preview_canvas.image = sketch_photo
    
    def update_preview():
        line_thickness = line_thickness_slider.get()
        contrast = contrast_slider.get()
        brightness = brightness_slider.get()
        updated_sketch = adjust_sketch(sketch, line_thickness, contrast, brightness)
        updated_sketch_photo = cv2.cvtColor(updated_sketch, cv2.COLOR_BGR2RGB)
        updated_sketch_photo = Image.fromarray(updated_sketch_photo)
        updated_sketch_photo = ImageTk.PhotoImage(updated_sketch_photo)
        preview_canvas.create_image(0, 0, anchor=tk.NW, image=updated_sketch_photo)
        preview_canvas.image = updated_sketch_photo
    
    line_thickness_slider.bind("<ButtonRelease-1>", lambda event: update_preview())
    contrast_slider.bind("<ButtonRelease-1>", lambda event: update_preview())
    brightness_slider.bind("<ButtonRelease-1>", lambda event: update_preview())
    
    save_button = tk.Button(root, text="Save", command=lambda: save_sketch(sketch))
    save_button.pack(pady=10)


def adjust_sketch(sketch, line_thickness, contrast, brightness):
    return sketch

def save_sketch(sketch):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        try:
            cv2.imwrite(file_path, sketch)
            messagebox.showinfo("Success", "Sketch saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", "Failed to save the sketch: " + str(e))

root = tk.Tk()
root.title('Image to Sketch Converter')

upload_button = tk.Button(root, text='Upload Image', command=upload_image)
upload_button.pack(pady=10)

root.mainloop()
