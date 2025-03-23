# PDF Merger with Dark UI

A modern, user-friendly PDF merger application with drag-and-drop functionality and dark theme interface.

![PDF Merger Screenshot](screenshot.png)

## Features

- 🌙 Modern dark theme interface
- 🖱️ Drag and drop PDF files
- 📂 File upload button
- 🔄 Visual drag-to-reorder functionality
- 📱 Responsive grid layout
- 🎯 Visual feedback during interactions
- 📄 Large, clear PDF previews
- 🔍 Filename display
- 📦 Simple PDF merging

## Requirements

- Python 3.6 or higher
- Required Python packages:
  ```
  tkinterdnd2
  Pillow
  PyPDF2
  ```

## Installation

1. Clone this repository or download the files
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python pdf_merger_tk.py
   ```

2. Add PDF files using either method:
   - Drag and drop PDF files directly into the window
   - Click "Upload PDFs" button to select files

3. Arrange PDFs in desired order:
   - Click and drag PDFs to reorder them
   - Selected PDFs will be highlighted in red
   - Drag a PDF over another to swap their positions

4. Click "Merge PDFs" to combine the files
   - The merged file will be saved as "merged_output.pdf" in the same directory
   - A success message will appear when merging is complete

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Troubleshooting

1. **tkinterdnd2 not found**
   - Make sure you've installed tkinterdnd2: `pip install tkinterdnd2`
   - If issues persist, try: `pip install --upgrade tkinterdnd2`

2. **PDF merging fails**
   - Ensure all PDF files are valid and not corrupted
   - Check if you have write permissions in the directory
   - Make sure no other program is using the output file

3. **Window appears blank**
   - Try resizing the window
   - Ensure your system supports Tkinter
   - Check if your Python installation includes Tk/Tcl

4. **Drag and drop not working**
   - Verify tkinterdnd2 is properly installed
   - Try running the program with administrator privileges
   - Check if your system supports drag and drop operations

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## Acknowledgments

- Built with Python and Tkinter
- Uses PyPDF2 for PDF operations
- Uses tkinterdnd2 for drag and drop functionality
- Uses Pillow for image processing