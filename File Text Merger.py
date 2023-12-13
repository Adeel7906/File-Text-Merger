import os
import tkinter as tk
from tkinter import filedialog, messagebox


class FileTextMerger:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Text Merger (SQA ENGG ADEEL)")

        # Create a list to store file paths and corresponding widgets
        self.file_paths_entries = []

        # Variable to track whether a file path has been added
        self.file_path_added = False

        # Create and place labels and entry widgets using grid
        tk.Label(self.root, text="File Paths:").grid(row=0, column=0, pady=5, padx=5, sticky=tk.E)
        self.file_paths_frame = tk.Frame(self.root)
        self.file_paths_frame.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        self.create_file_path_entry()

        # Initially, disable the "-" button
        self.minus_button = tk.Button(self.root, text="       -", command=self.remove_file_path_entry, state=tk.DISABLED,
                                      bg="#D3D3D3")
        self.minus_button.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

        # Create and place combined "+" and "-" button
        self.plus_minus_button = tk.Button(self.root, text="+", command=self.toggle_file_path_entry, bg="#90EE90")
        self.plus_minus_button.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

        tk.Label(self.root, text="Output File Path:").grid(row=1, column=0, pady=5, padx=5, sticky=tk.E)
        self.output_entry = tk.Entry(self.root, width=50)
        self.output_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        tk.Button(self.root, text="Browse", command=self.browse_output_file).grid(row=1, column=2, pady=5, padx=5,
                                                                                  sticky=tk.W)

        # Create and place merge button
        tk.Button(self.root, text="SUBMIT", command=self.merge_files,bg="#90EE90").grid(row=3, column=1, pady=10, padx=5,
                                                                                sticky=tk.NSEW)

        # Create and place open file button (disabled initially)
        self.open_file_button = tk.Button(self.root, text="Open Output File", command=self.open_saved_file,
                                          state=tk.DISABLED)
        self.open_file_button.grid(row=3, column=0, pady=10, padx=5, sticky=tk.NSEW)
        # Create and place help button
        tk.Button(self.root, text="Help", command=self.show_help,bg="#ADD8E6").grid(row=3, column=2, pady=10, padx=5)

        # Run the main loop
        self.root.mainloop()

    def create_file_path_entry(self):
        file_path_entry = tk.Entry(self.file_paths_frame, width=50)
        browse_button = tk.Button(self.file_paths_frame, text="Browse",
                                  command=lambda: self.browse_files(file_path_entry))

        row_position = len(self.file_paths_entries)
        file_path_entry.grid(row=row_position, column=0, pady=5, padx=5, sticky=tk.W)
        browse_button.grid(row=row_position, column=1, pady=5, padx=5, sticky=tk.W)

        self.file_paths_entries.append((file_path_entry, browse_button))

    def browse_files(self, entry_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)

            # Enable the "-" button after adding a file path
            self.minus_button.config(state=tk.NORMAL, bg="#FFCCCC")
            # Update the file path added flag
            self.file_path_added = True

    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, file_path)

    def merge_files(self):
        output_file_path = self.output_entry.get()

        try:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                file_paths = [entry[0].get() for entry in self.file_paths_entries if entry[0].get()]
                file_iters = [iter(open(file_path, 'r', encoding='utf-8').readlines()) for file_path in file_paths]

                while True:
                    for file_iter in file_iters:
                        line = next(file_iter, None)
                        if line is not None:
                            output_file.write(line.strip() + "\n")
                        else:
                            break
                    else:
                        output_file.write("================\n")
                        continue
                    break

            messagebox.showinfo("Success", "Files text merged successfully!")
            self.open_file_button.config(state=tk.NORMAL)
            self.save_file_path(output_file_path)

        except FileNotFoundError:
            messagebox.showerror("Error", "One or more input files not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def toggle_file_path_entry(self):
        # Toggle between adding and removing file path entries
        if self.plus_minus_button.cget("text") == "+":
            self.create_file_path_entry()
            # Enable the "-" button after adding the first file path
            self.minus_button.config(state=tk.NORMAL, bg="#FFCCCC")
            # Update the file path added flag
            self.file_path_added = True
        else:
            self.remove_file_path_entry()

    def remove_file_path_entry(self):
        # Disable removing the initially added file path
        if len(self.file_paths_entries) > 1 or self.file_path_added:
            # Get the last file path entry and corresponding widgets
            file_path_entry, browse_button = self.file_paths_entries.pop()
            # Destroy the widgets
            file_path_entry.destroy()
            browse_button.destroy()

            # Disable "-" button if only one file path remains
            if len(self.file_paths_entries) == 1:
                self.minus_button.config(state=tk.DISABLED, bg="#D3D3D3")

            # Update the file path added flag
            self.file_path_added = False

    def save_file_path(self, file_path):
        with open('../../../saved_file_path.txt', 'w') as file:
            file.write(file_path)

    def show_help(self):
        help_text = (
            "                       File Text Merger merge only .txt files\n\n"
            "1. Enter the file paths in the respective input fields.\n"
            "2. Click the 'Browse' button next to each input field to select files.\n"
            "3. Enter the output file path.\n"
            "4. Click the 'Submit' button to merge text from files.\n"
            "5. A popup will appear indicating the success or failure of the merge.\n"
            "6. File Text Merger takes the first line from the first file and the second line from the second file.\n"
            "7. These lines are saved in the output file with a separator.\n"
            "8. The saved file is located at the path you chose for the output file.\n"
            "9. You can also open the saved file directly from File Text Merger.\n"
            "10. After clicking the submit button, a popup will appear indicating the success.\n"
            "11. The 'Open File' button becomes enabled, allowing you to open the file directly.\n"
            "12. You can add more browse fields by clicking '+' button and browse it.\n"
            "13. You can remove any browse field by clicking '-' button."
        )
        messagebox.showinfo("Help                         File Text Merger (SQA ENGG ADEEL)", help_text)

    def open_saved_file(self):
        try:
            with open('../../../saved_file_path.txt', 'r') as file:
                file_path = file.read().strip()
                if os.path.exists(file_path):
                    os.system(f'start "" "{file_path}"')
                else:
                    messagebox.showerror("Error", "File not found.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No file path saved yet.")


# Instantiate the FileTextMerger class to run the application
app = FileTextMerger()
