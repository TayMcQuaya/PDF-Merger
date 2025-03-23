from tkinterdnd2 import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PyPDF2 import PdfMerger
import sys
from pathlib import Path
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont

class CustomButton(tk.Button):
    def __init__(self, master, is_accent=False, **kwargs):
        self.is_accent = is_accent
        # Define colors
        self.normal_bg = '#ff4444' if is_accent else '#333333'
        self.hover_bg = '#ff6666' if is_accent else '#444444'
        self.normal_fg = 'white'
        
        super().__init__(
            master,
            bg=self.normal_bg,
            fg=self.normal_fg,
            font=('Segoe UI', 10),
            borderwidth=0,
            padx=20,
            pady=8,
            cursor='hand2',
            **kwargs
        )
        
        # Bind hover events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self['bg'] = self.hover_bg
        
    def on_leave(self, e):
        self['bg'] = self.normal_bg

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("1000x700")  # Larger window
        
        # Configure dark theme
        self.configure_dark_theme()
        
        # Create and configure main frame
        main_frame = ttk.Frame(root, padding="20", style='Dark.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create header frame
        header_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)  # Make middle column expand
        
        # Upload button (using custom button)
        self.upload_btn = CustomButton(
            header_frame,
            text="Upload PDFs",
            command=self.upload_files,
            is_accent=False
        )
        self.upload_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Instructions label
        self.instructions = ttk.Label(header_frame, 
            text="Drag & drop PDFs or use upload button. Click to select, drag to rearrange.",
            font=('Segoe UI', 10), style='Dark.TLabel')
        self.instructions.grid(row=0, column=1, pady=10)
        
        # Merge button (using custom button)
        self.merge_btn = CustomButton(
            header_frame,
            text="Merge PDFs",
            command=self.merge_pdfs,
            is_accent=True
        )
        self.merge_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Create canvas with scrollbar for PDF icons
        self.canvas_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        self.canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='#1e1e1e', highlightthickness=0)
        self.scrollbar_y = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        
        self.content_frame = ttk.Frame(self.canvas, style='Dark.TFrame')
        
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set,
                            xscrollcommand=self.scrollbar_x.set)
        
        # Bind mouse wheel
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Create window in canvas for content
        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Create PDF icon
        self.pdf_icon = self.create_pdf_icon()
        
        # Enable drag and drop for files
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_files)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Store PDF frames and drag data
        self.pdf_frames = []
        self.drag_data = {"widget": None, "x": 0, "y": 0}
        self.selected_frame = None
        
    def configure_dark_theme(self):
        style = ttk.Style()
        
        # Configure dark theme colors
        dark_bg = '#1e1e1e'
        darker_bg = '#252525'
        accent_color = '#ff4444'  # Red accent color
        hover_color = '#ff6666'
        text_color = '#ffffff'
        
        style.configure('Dark.TFrame', background=dark_bg)
        style.configure('Dark.TLabel', 
                       background=dark_bg, 
                       foreground=text_color)
        
        # Normal frame style
        style.configure('PDF.TFrame', 
                       background=darker_bg,
                       relief='solid',
                       borderwidth=1)
        
        # Selected frame style
        style.configure('Selected.TFrame',
                       background=accent_color,
                       relief='solid',
                       borderwidth=2)
        
        # Hover frame style
        style.configure('Hover.TFrame',
                       background='#404040',
                       relief='solid',
                       borderwidth=2)
        
        # Button styles
        button_style = {
            'background': dark_bg,
            'foreground': text_color,
            'borderwidth': 1,
            'relief': 'solid',
            'font': ('Segoe UI', 10),
            'padding': 10
        }
        
        style.configure('Action.TButton', **button_style)
        style.configure('Accent.TButton', **button_style)
        
        # Button hover styles
        style.map('Action.TButton',
                 background=[('active', darker_bg)],
                 foreground=[('active', accent_color)])
        style.map('Accent.TButton',
                 background=[('active', accent_color)],
                 foreground=[('active', text_color)])
        
        # Configure dark theme for the root window
        self.root.configure(bg=dark_bg)
        
    def create_pdf_icon(self):
        # Create a larger, more sophisticated PDF icon
        icon_size = (100, 120)  # Taller to accommodate the "PDF" text better
        icon = Image.new('RGBA', icon_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon)
        
        # Draw PDF icon (red rectangle with white "PDF" text)
        margin = 4
        # Main rectangle
        draw.rectangle([margin, margin, icon_size[0]-margin, icon_size[1]-margin],
                      fill='#ff4444', outline='#ff6666', width=2)
        
        # Folded corner effect
        corner_size = 20
        draw.polygon([(icon_size[0]-margin-corner_size, margin),
                     (icon_size[0]-margin, margin),
                     (icon_size[0]-margin, margin+corner_size)],
                    fill='#ff6666')
        
        # Add "PDF" text
        draw.text((icon_size[0]//4, icon_size[1]//3), "PDF",
                 fill='white', font=None, size=32)
        
        return ImageTk.PhotoImage(icon)
    
    def create_pdf_frame(self, filename, full_path):
        # Create a frame for each PDF with icon and label
        frame = ttk.Frame(self.content_frame, style='PDF.TFrame')
        
        # Store the full path and initial position
        frame.full_path = full_path
        frame.dragging = False
        frame.original_position = None
        
        # Add icon label
        icon_label = ttk.Label(frame, image=self.pdf_icon, style='Dark.TLabel')
        icon_label.pack(pady=10, padx=10)
        
        # Add filename label
        name = os.path.basename(filename)
        if len(name) > 25:
            name = name[:22] + "..."
        name_label = ttk.Label(frame, text=name, wraplength=120,
                             style='Dark.TLabel', font=('Segoe UI', 9))
        name_label.pack(pady=(0, 10), padx=10)
        
        # Bind events to the frame
        frame.bind('<Button-1>', lambda e: self.on_drag_start(e, frame))
        frame.bind('<B1-Motion>', lambda e: self.on_drag_motion(e, frame))
        frame.bind('<ButtonRelease-1>', lambda e: self.on_drag_release(e, frame))
        
        # Make labels part of dragging too
        for widget in (icon_label, name_label):
            widget.bind('<Button-1>', lambda e, f=frame: self.on_drag_start(e, f))
            widget.bind('<B1-Motion>', lambda e, f=frame: self.on_drag_motion(e, f))
            widget.bind('<ButtonRelease-1>', lambda e, f=frame: self.on_drag_release(e, f))
        
        return frame
    
    def upload_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")]
        )
        for file in files:
            if file.lower().endswith('.pdf'):
                new_frame = self.create_pdf_frame(file, file)
                self.pdf_frames.append(new_frame)
        self.arrange_frames()
    
    def on_drag_start(self, event, frame):
        # Select the frame
        if self.selected_frame and self.selected_frame != frame:
            self.selected_frame.configure(style='PDF.TFrame')
        self.selected_frame = frame
        frame.configure(style='Selected.TFrame')
        
        # Initialize drag
        frame.dragging = True
        frame.original_position = (frame.winfo_x(), frame.winfo_y())
        frame.start_x = event.x_root
        frame.start_y = event.y_root
        
        # Lift the frame to the top
        frame.lift()
    
    def on_drag_motion(self, event, frame):
        if not frame.dragging:
            return
            
        # Calculate new position
        dx = event.x_root - frame.start_x
        dy = event.y_root - frame.start_y
        new_x = frame.original_position[0] + dx
        new_y = frame.original_position[1] + dy
        
        # Move the frame
        frame.place(x=new_x, y=new_y)
        
        # Find potential swap target
        self.find_swap_target(frame, event.x_root, event.y_root)
    
    def find_swap_target(self, drag_frame, x_root, y_root):
        for target in self.pdf_frames:
            if target != drag_frame:
                # Get target's position relative to content frame
                target_x = target.winfo_x()
                target_y = target.winfo_y()
                target_width = target.winfo_width()
                target_height = target.winfo_height()
                
                # Convert root coordinates to widget coordinates
                rel_x = x_root - self.content_frame.winfo_rootx()
                rel_y = y_root - self.content_frame.winfo_rooty()
                
                # Check if mouse is over target
                if (target_x < rel_x < target_x + target_width and
                    target_y < rel_y < target_y + target_height):
                    # Visual feedback for potential drop target
                    for frame in self.pdf_frames:
                        if frame != self.selected_frame:
                            frame.configure(style='PDF.TFrame')
                    target.configure(style='Hover.TFrame')
                    return target
        return None
    
    def on_drag_release(self, event, frame):
        if not frame.dragging:
            return
            
        frame.dragging = False
        
        # Find the target frame under the cursor
        target = self.find_swap_target(frame, event.x_root, event.y_root)
        
        if target:
            # Swap positions in the list
            idx1 = self.pdf_frames.index(frame)
            idx2 = self.pdf_frames.index(target)
            self.pdf_frames[idx1], self.pdf_frames[idx2] = self.pdf_frames[idx2], self.pdf_frames[idx1]
        
        # Reset all frames to normal style
        for pdf_frame in self.pdf_frames:
            if pdf_frame != self.selected_frame:
                pdf_frame.configure(style='PDF.TFrame')
        
        # Rearrange all frames
        self.arrange_frames()
    
    def arrange_frames(self):
        # Calculate the number of columns based on window width
        canvas_width = self.canvas.winfo_width()
        item_width = 150  # Wider items for better spacing
        max_columns = max(1, canvas_width // item_width)
        
        current_row = 0
        current_col = 0
        
        for frame in self.pdf_frames:
            # Remove any place geometry manager settings
            frame.place_forget()
            # Use grid for normal layout
            frame.grid(row=current_row, column=current_col, padx=15, pady=15)
            current_col += 1
            if current_col >= max_columns:
                current_col = 0
                current_row += 1
        
        # Configure column weights to center items
        for i in range(max_columns):
            self.content_frame.columnconfigure(i, weight=1)
        
        self.content_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        # Recalculate layout when window is resized
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.arrange_frames()
        
    def drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith('.pdf'):
                # Create and add new PDF frame
                new_frame = self.create_pdf_frame(file, file)
                self.pdf_frames.append(new_frame)
        
        self.arrange_frames()
    
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def merge_pdfs(self):
        if len(self.pdf_frames) < 2:
            messagebox.showwarning("Warning", "Please add at least 2 PDF files to merge.")
            return
        
        merger = PdfMerger()
        try:
            # Merge PDFs in the order they appear in the grid
            for frame in self.pdf_frames:
                merger.append(frame.full_path)
            
            # Save the merged PDF
            output_path = "merged_output.pdf"
            with open(output_path, "wb") as output_file:
                merger.write(output_file)
            
            messagebox.showinfo("Success", f"PDFs successfully merged!\nSaved as: {output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error merging PDFs: {str(e)}")
        finally:
            merger.close()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFMergerApp(root)
    root.mainloop() 