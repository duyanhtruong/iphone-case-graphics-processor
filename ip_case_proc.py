import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from PIL import Image, ImageDraw, ImageFont
import threading
from pathlib import Path

class iPhoneCaseProcessor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("iPhone Case Print Film Processor")
        self.root.geometry("800x600")
        
        # iPhone model specifications
        self.model_specs = {
            # iPhone 7/8 Series
            'iPhone 7': {'width_cm': 9.5, 'category': 'legacy'},
            'iPhone 7 Plus': {'width_cm': 10.8, 'category': 'legacy_plus'},
            'iPhone 8': {'width_cm': 9.5, 'category': 'legacy'},
            'iPhone 8 Plus': {'width_cm': 10.8, 'category': 'legacy_plus'},
            
            # Mini Models
            'iPhone 12 mini': {'width_cm': 9.0, 'category': 'mini'},  # CHANGED from 9.5 to 9.0
            'iPhone 13 mini': {'width_cm': 9.0, 'category': 'mini'},  # CHANGED from 9.5 to 9.0
            
            # Regular/Pro Models
            'iPhone 12': {'width_cm': 9.8, 'category': 'regular'},
            'iPhone 12 Pro': {'width_cm': 9.8, 'category': 'regular'},
            'iPhone 13': {'width_cm': 9.8, 'category': 'regular'},
            'iPhone 13 Pro': {'width_cm': 9.8, 'category': 'regular'},
            'iPhone 14': {'width_cm': 9.8, 'category': 'regular'},
            'iPhone 14 Pro': {'width_cm': 9.8, 'category': 'regular'},
            'iPhone 15': {'width_cm': 9.8, 'category': 'regular'},
            'iPhone 15 Pro': {'width_cm': 9.8, 'category': 'regular'},
            'iPhone 16': {'width_cm': 9.8, 'category': 'regular'},
            'iPhone 16 Pro': {'width_cm': 9.8, 'category': 'regular'},
            
            # XR/11 Models
            'iPhone XR': {'width_cm': 10.5, 'category': 'xr11'},        # CHANGED from 10.2 to 10.5
            'iPhone 11': {'width_cm': 10.5, 'category': 'xr11'},       # CHANGED from 10.2 to 10.5
            
            # XS Max/11 Pro Max 
            'iPhone XS Max': {'width_cm': 10.7, 'category': 'xs_max'}, # CHANGED from 10.45 to 10.7
            'iPhone 11 Pro Max': {'width_cm': 10.8, 'category': 'xs_max'}, # CHANGED from 10.45 to 10.8
            
            # Plus/Pro Max Models
            'iPhone 12 Pro Max': {'width_cm': 10.65, 'category': 'plus_max'},
            'iPhone 13 Pro Max': {'width_cm': 10.65, 'category': 'plus_max'},
            'iPhone 14 Plus': {'width_cm': 10.65, 'category': 'plus_max'},
            'iPhone 14 Pro Max': {'width_cm': 10.65, 'category': 'plus_max'},
            'iPhone 15 Plus': {'width_cm': 10.65, 'category': 'plus_max'},
            'iPhone 15 Pro Max': {'width_cm': 10.65, 'category': 'plus_max'},
            'iPhone 16 Plus': {'width_cm': 10.65, 'category': 'plus_max'},
            'iPhone 16 Pro Max': {'width_cm': 10.65, 'category': 'plus_max'},
            
            # X/XS/11 Pro Models
            'iPhone X': {'width_cm': 8.3, 'category': 'x_xs'},         # CHANGED from 11.3 to 8.3
            'iPhone XS': {'width_cm': 8.3, 'category': 'x_xs'},        # CHANGED from 11.3 to 8.3
            'iPhone 11 Pro': {'width_cm': 10.0, 'category': 'x_xs'},   # CHANGED from 11.3 to 10.0
        }
        
        # Print film specifications - Portrait orientation
        self.film_width_cm = 14.8
        self.film_height_cm = 25.5
        self.dpi = 300
        
        # Convert cm to pixels at 300 DPI with proper rounding (FIXED)
        self.film_width_px = round(self.film_width_cm * self.dpi / 2.54)
        self.film_height_px = round(self.film_height_cm * self.dpi / 2.54)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the main user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="iPhone Case Print Film Processor", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Folder processing section
        folder_frame = ttk.LabelFrame(main_frame, text="Batch Processing", padding="10")
        folder_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(folder_frame, text="Browse Folder", 
                  command=self.browse_folder).grid(row=0, column=0, padx=(0, 10))
        
        self.folder_path_var = tk.StringVar()
        ttk.Label(folder_frame, textvariable=self.folder_path_var, 
                 foreground="blue").grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # File processing section
        file_frame = ttk.LabelFrame(main_frame, text="Individual Files", padding="10")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="Browse Files", 
                  command=self.browse_files).grid(row=0, column=0, padx=(0, 10))
        
        self.files_count_var = tk.StringVar()
        ttk.Label(file_frame, textvariable=self.files_count_var).grid(row=0, column=1)
        
        # Output folder selection section
        output_frame = ttk.LabelFrame(main_frame, text="Output Location (Optional)", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(output_frame, text="Choose Output Folder", 
                  command=self.browse_output_folder).grid(row=0, column=0, padx=(0, 10))
        
        self.output_path_var = tk.StringVar()
        self.output_path_label = ttk.Label(output_frame, textvariable=self.output_path_var, 
                                          foreground="green")
        self.output_path_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Clear output folder button
        ttk.Button(output_frame, text="Use Default", 
                  command=self.clear_output_folder).grid(row=0, column=2, padx=(10, 0))
        
        # Configure output frame grid
        output_frame.columnconfigure(1, weight=1)
        
        # Processing controls
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.process_btn = ttk.Button(control_frame, text="Process All Images", 
                                     command=self.start_processing, state='disabled')
        self.process_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Select folder or files to begin")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=6, column=0, columnspan=3)
        
        # Results text area
        result_frame = ttk.LabelFrame(main_frame, text="Processing Results", padding="10")
        result_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.result_text = tk.Text(result_frame, height=10, width=80)
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(7, weight=1)  # Updated for new row number
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # Storage for processing data
        self.selected_folder = None
        self.selected_files = []
        self.custom_output_folder = None
        
        # Set initial output location status
        self.output_path_var.set("Using default location")
        
    def browse_folder(self):
        """Browse for a date folder to process"""
        folder_path = filedialog.askdirectory(title="Select Date Folder")
        if folder_path:
            self.selected_folder = folder_path
            self.selected_files = []
            self.folder_path_var.set(os.path.basename(folder_path))
            self.files_count_var.set("")
            self.process_btn.config(state='normal')
            self.log_message(f"Selected folder: {folder_path}")
            
    def browse_files(self):
        """Browse for individual image files"""
        file_paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if file_paths:
            self.selected_files = list(file_paths)
            self.selected_folder = None
            self.folder_path_var.set("")
            self.files_count_var.set(f"{len(file_paths)} files selected")
            self.process_btn.config(state='normal')
            self.log_message(f"Selected {len(file_paths)} individual files")
    
    def browse_output_folder(self):
        """Browse for custom output folder location"""
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.custom_output_folder = folder_path
            # Show shortened path for display
            display_path = os.path.basename(folder_path) if len(folder_path) > 50 else folder_path
            self.output_path_var.set(f"Custom: {display_path}")
            self.log_message(f"Custom output folder set: {folder_path}")
    
    def clear_output_folder(self):
        """Clear custom output folder and use default behavior"""
        self.custom_output_folder = None
        self.output_path_var.set("Using default location")
        self.log_message("Reset to default output location")
            
    def log_message(self, message):
        """Add a message to the results text area"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.root.update_idletasks()
        
    def extract_order_number(self, filename):
        """Extract order number from filename (supports letter suffixes like 3a, 3b, 3c)"""
        # Remove file extension
        name = os.path.splitext(filename)[0]
        
        # Look for leading digits optionally followed by a letter (e.g., 3, 3a, 3b, 3c)
        match = re.match(r'^(\d+[a-zA-Z]?)', name)
        if match:
            return match.group(1)  # Return as string to preserve letter suffix
        
        return None
        
    def detect_phone_model(self, filename):
        """Auto-detect phone model from filename using comprehensive fuzzy matching - UPDATED WITH NEW MODELS"""
        # Remove file extension and convert to lowercase
        name = os.path.splitext(filename.lower())[0]
        
        # Remove order number prefix (including leading zeros and letter suffixes like 3a, 3b)
        name = re.sub(r'^\d+[a-zA-Z]?[-_\s\.]*', '', name)
        
        # Normalize separators - replace any combination of separators with single space
        name = re.sub(r'[-_\s\.]+', ' ', name).strip()
        
        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name)
        
        # COMPREHENSIVE MODEL PATTERNS - UPDATED WITH iPhone 7/8 SERIES
        # Order is CRITICAL - most specific patterns first to avoid false matches
        
        model_patterns = {
            # ===== iPhone 16 Series =====
            # Pro Max patterns (must come before Pro)
            r'(?:i?phone?|iph?|ip|a|apple)?\s*16\s*(?:pro?\s*)?(?:max|mx|pm|prm|promax|promx)': 'iPhone 16 Pro Max',
            
            # Plus patterns  
            r'(?:i?phone?|iph?|ip|a|apple)?\s*16\s*(?:plus|pl|\+|p(?=\s|$))': 'iPhone 16 Plus',
            
            # Pro patterns (must come after Pro Max and Plus)
            r'(?:i?phone?|iph?|ip|a|apple)?\s*16\s*(?:pro?|pr|p)(?!\s*(?:max|mx|plus|pl|\+))': 'iPhone 16 Pro',
            
            # Base model - enhanced to handle "iphone16" and "iphone 16"
            r'(?:i?phone?|iph?|ip|a|apple)?\s*16(?!\d)(?!\s*(?:pro?|pr|p|plus|pl|\+|max|mx))': 'iPhone 16',
            
            # ===== iPhone 15 Series =====
            # Pro Max patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*15\s*(?:pro?\s*)?(?:max|mx|pm|prm|promax|promx)': 'iPhone 15 Pro Max',
            
            # Plus patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*15\s*(?:plus|pl|\+|p(?=\s|$))': 'iPhone 15 Plus',
            
            # Pro patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*15\s*(?:pro?|pr|p)(?!\s*(?:max|mx|plus|pl|\+))': 'iPhone 15 Pro',
            
            # Base model - enhanced to handle "iphone15" and "iphone 15"
            r'(?:i?phone?|iph?|ip|a|apple)?\s*15(?!\d)(?!\s*(?:pro?|pr|p|plus|pl|\+|max|mx))': 'iPhone 15',
            
            # ===== iPhone 14 Series =====
            # Pro Max patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*14\s*(?:pro?\s*)?(?:max|mx|pm|prm|promax|promx)': 'iPhone 14 Pro Max',
            
            # Plus patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*14\s*(?:plus|pl|\+|p(?=\s|$))': 'iPhone 14 Plus',
            
            # Pro patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*14\s*(?:pro?|pr|p)(?!\s*(?:max|mx|plus|pl|\+))': 'iPhone 14 Pro',
            
            # Base model - enhanced to handle "iphone14" and "iphone 14"
            r'(?:i?phone?|iph?|ip|a|apple)?\s*14(?!\d)(?!\s*(?:pro?|pr|p|plus|pl|\+|max|mx))': 'iPhone 14',
            
            # ===== iPhone 13 Series =====
            # Pro Max patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*13\s*(?:pro?\s*)?(?:max|mx|pm|prm|promax|promx)': 'iPhone 13 Pro Max',
            
            # Pro patterns (must come before base model to avoid conflicts)
            r'(?:i?phone?|iph?|ip|a|apple)?\s*13\s*(?:pro?|pr|p)(?!\s*(?:max|mx))': 'iPhone 13 Pro',
            
            # Mini patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*13\s*(?:mini?|mn|m)(?!\s*(?:ax|x))': 'iPhone 13 mini',
            
            # Base model - enhanced to handle "iphone13" and "iphone 13"
            r'(?:i?phone?|iph?|ip|a|apple)?\s*13(?!\d)(?!\s*(?:pro?|pr|p|mini?|mn|m|max|mx))': 'iPhone 13',
            
            # ===== iPhone 12 Series =====
            # Pro Max patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*12\s*(?:pro?\s*)?(?:max|mx|pm|prm|promax|promx)': 'iPhone 12 Pro Max',
            
            # Pro patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*12\s*(?:pro?|pr|p)(?!\s*(?:max|mx))': 'iPhone 12 Pro',
            
            # Mini patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*12\s*(?:mini?|mn|m)(?!\s*(?:ax|x))': 'iPhone 12 mini',
            
            # Base model - enhanced to handle "iphone12" and "iphone 12"
            r'(?:i?phone?|iph?|ip|a|apple)?\s*12(?!\d)(?!\s*(?:pro?|pr|p|mini?|mn|m|max|mx))': 'iPhone 12',
            
            # ===== iPhone 11 Series =====
            # Pro Max patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*11\s*(?:pro?\s*)?(?:max|mx|pm|prm|promax|promx)': 'iPhone 11 Pro Max',
            
            # Pro patterns
            r'(?:i?phone?|iph?|ip|a|apple)?\s*11\s*(?:pro?|pr|p)(?!\s*(?:max|mx))': 'iPhone 11 Pro',
            
            # Base model - enhanced to handle "iphone11" and "iphone 11"
            r'(?:i?phone?|iph?|ip|a|apple)?\s*11(?!\d)(?!\s*(?:pro?|pr|p|max|mx))': 'iPhone 11',
            
            # ===== iPhone X Series (Handle carefully due to conflicts) =====
            # XS Max - most specific first
            r'(?:i?phone?|iph?|ip|a|apple)?\s*xs?\s*(?:max|mx|m)(?!\s*(?:in))': 'iPhone XS Max',
            
            # XS (but not XS Max)
            r'(?:i?phone?|iph?|ip|a|apple)?\s*xs(?!\s*(?:max|mx|m))': 'iPhone XS',
            
            # XR
            r'(?:i?phone?|iph?|ip|a|apple)?\s*xr': 'iPhone XR',
            
            # iPhone X (most ambiguous - comes last)
            # Be very careful here - only match isolated X patterns
            r'(?:i?phone?|iph?|ip|a|apple)\s*x(?!\w)': 'iPhone X',
            r'^x$': 'iPhone X',  # Only standalone X
            
            # ===== iPhone 8 Series - NEW =====
            # Plus patterns (must come before base model)
            r'(?:i?phone?|iph?|ip|a|apple)?\s*8\s*(?:plus|pl|\+|p(?=\s|$))': 'iPhone 8 Plus',
            
            # Base model - enhanced to handle "iphone8" and "iphone 8"
            r'(?:i?phone?|iph?|ip|a|apple)?\s*8(?!\d)(?!\s*(?:plus|pl|\+|p))': 'iPhone 8',
            
            # ===== iPhone 7 Series - NEW =====
            # Plus patterns (must come before base model)
            r'(?:i?phone?|iph?|ip|a|apple)?\s*7\s*(?:plus|pl|\+|p(?=\s|$))': 'iPhone 7 Plus',
            
            # Base model - enhanced to handle "iphone7" and "iphone 7"
            r'(?:i?phone?|iph?|ip|a|apple)?\s*7(?!\d)(?!\s*(?:plus|pl|\+|p))': 'iPhone 7',
        }
        
        # Try to match patterns in order
        for pattern, model in model_patterns.items():
            if re.search(pattern, name):
                return model
        
        # ===== FALLBACK: Ultra-minimal number-only patterns =====
        # Only trigger if no other pattern matched
        number_only_patterns = {
            r'^16$': 'iPhone 16',
            r'^15$': 'iPhone 15', 
            r'^14$': 'iPhone 14',
            r'^13$': 'iPhone 13',
            r'^12$': 'iPhone 12',
            r'^11$': 'iPhone 11',
            r'^8$': 'iPhone 8',    # NEW
            r'^7$': 'iPhone 7',    # NEW
        }
        
        for pattern, model in number_only_patterns.items():
            if re.search(pattern, name):
                return model
                
        return None
        
    def standardize_model_name(self, model_name):
        """Convert model name to standardized filename format with proper case - UPDATED WITH NEW MODELS"""
        model_map = {
            'iPhone 16 Pro Max': 'iPhone16ProMax',
            'iPhone 16 Plus': 'iPhone16Plus',
            'iPhone 16 Pro': 'iPhone16Pro',
            'iPhone 16': 'iPhone16',
            'iPhone 15 Pro Max': 'iPhone15ProMax',
            'iPhone 15 Plus': 'iPhone15Plus',
            'iPhone 15 Pro': 'iPhone15Pro',
            'iPhone 15': 'iPhone15',
            'iPhone 14 Pro Max': 'iPhone14ProMax',
            'iPhone 14 Plus': 'iPhone14Plus',
            'iPhone 14 Pro': 'iPhone14Pro',
            'iPhone 14': 'iPhone14',
            'iPhone 13 Pro Max': 'iPhone13ProMax',
            'iPhone 13 mini': 'iPhone13mini',
            'iPhone 13 Pro': 'iPhone13Pro',
            'iPhone 13': 'iPhone13',
            'iPhone 12 Pro Max': 'iPhone12ProMax',
            'iPhone 12 mini': 'iPhone12mini',
            'iPhone 12 Pro': 'iPhone12Pro',
            'iPhone 12': 'iPhone12',
            'iPhone 11 Pro Max': 'iPhone11ProMax',
            'iPhone 11 Pro': 'iPhone11Pro',
            'iPhone 11': 'iPhone11',
            'iPhone XS Max': 'iPhoneXSMax',
            'iPhone XS': 'iPhoneXS',
            'iPhone XR': 'iPhoneXR',
            'iPhone X': 'iPhoneX',
            # NEW iPhone 8 Series
            'iPhone 8 Plus': 'iPhone8Plus',
            'iPhone 8': 'iPhone8',
            # NEW iPhone 7 Series
            'iPhone 7 Plus': 'iPhone7Plus',
            'iPhone 7': 'iPhone7',
        }
        return model_map.get(model_name, model_name.replace(' ', '_'))
        
    def format_display_model_name(self, model_name):
        """Convert model name for display on canvas - replace iPhone with IP and use proper case - UPDATED WITH NEW MODELS"""
        # Replace iPhone with IP and maintain proper case
        display_map = {
            'iPhone 16 Pro Max': 'IP 16 Pro Max',
            'iPhone 16 Plus': 'IP 16 Plus',
            'iPhone 16 Pro': 'IP 16 Pro',
            'iPhone 16': 'IP 16',
            'iPhone 15 Pro Max': 'IP 15 Pro Max',
            'iPhone 15 Plus': 'IP 15 Plus',
            'iPhone 15 Pro': 'IP 15 Pro',
            'iPhone 15': 'IP 15',
            'iPhone 14 Pro Max': 'IP 14 Pro Max',
            'iPhone 14 Plus': 'IP 14 Plus',
            'iPhone 14 Pro': 'IP 14 Pro',
            'iPhone 14': 'IP 14',
            'iPhone 13 Pro Max': 'IP 13 Pro Max',
            'iPhone 13 mini': 'IP 13 mini',
            'iPhone 13 Pro': 'IP 13 Pro',
            'iPhone 13': 'IP 13',
            'iPhone 12 Pro Max': 'IP 12 Pro Max',
            'iPhone 12 mini': 'IP 12 mini',
            'iPhone 12 Pro': 'IP 12 Pro',
            'iPhone 12': 'IP 12',
            'iPhone 11 Pro Max': 'IP 11 Pro Max',
            'iPhone 11 Pro': 'IP 11 Pro',
            'iPhone 11': 'IP 11',
            'iPhone XS Max': 'IP XS Max',
            'iPhone XS': 'IP XS',
            'iPhone XR': 'IP XR',
            'iPhone X': 'IP X',
            # NEW iPhone 8 Series
            'iPhone 8 Plus': 'IP 8 Plus',
            'iPhone 8': 'IP 8',
            # NEW iPhone 7 Series
            'iPhone 7 Plus': 'IP 7 Plus',
            'iPhone 7': 'IP 7',
        }
        return display_map.get(model_name, model_name.replace('iPhone', 'IP'))
        
    def start_processing(self):
        """Start the image processing in a separate thread"""
        self.process_btn.config(state='disabled')
        self.result_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        
        # Start processing in separate thread to keep UI responsive
        threading.Thread(target=self.process_images, daemon=True).start()
        
    def process_images(self):
        """Main image processing logic"""
        try:
            if self.selected_folder:
                self.process_folder()
            elif self.selected_files:
                self.process_file_list()
        except Exception as e:
            self.log_message(f"Error during processing: {str(e)}")
        finally:
            self.process_btn.config(state='normal')
            
    def process_folder(self):
        """Process all images in the selected folder structure"""
        self.log_message(f"Processing folder: {self.selected_folder}")
        
        # Determine output folder location
        if self.custom_output_folder:
            # Use custom output folder
            folder_name = os.path.basename(self.selected_folder)
            output_folder = os.path.join(self.custom_output_folder, f"{folder_name} (PRINT MODE)")
            self.log_message(f"Using custom output location: {output_folder}")
        else:
            # Use default behavior (same directory as input)
            folder_name = os.path.basename(self.selected_folder)
            output_folder = os.path.join(os.path.dirname(self.selected_folder), f"{folder_name} (PRINT MODE)")
            self.log_message(f"Using default output location: {output_folder}")
        
        os.makedirs(output_folder, exist_ok=True)
        
        # Find all image files in subfolders
        image_files = []
        for root, dirs, files in os.walk(self.selected_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, self.selected_folder)
                    image_files.append((file_path, relative_path, file))
        
        if not image_files:
            self.log_message("No image files found in the selected folder.")
            return
            
        self.log_message(f"Found {len(image_files)} image files to process")
        
        # Process each file
        processed_count = 0
        failed_files = []
        
        for i, (file_path, relative_folder, filename) in enumerate(image_files):
            try:
                # Update progress
                progress = (i / len(image_files)) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"Processing: {filename}")
                self.root.update_idletasks()
                
                # Process the image
                success = self.process_single_image(file_path, output_folder, relative_folder, filename)
                if success:
                    processed_count += 1
                else:
                    failed_files.append(filename)
                    
            except Exception as e:
                self.log_message(f"Error processing {filename}: {str(e)}")
                failed_files.append(filename)
        
        # Final update
        self.progress_var.set(100)
        self.status_var.set("Processing complete!")
        self.log_message(f"\nProcessing completed!")
        self.log_message(f"Successfully processed: {processed_count} files")
        if failed_files:
            self.log_message(f"Failed to process: {len(failed_files)} files")
            for failed_file in failed_files:
                self.log_message(f"  - {failed_file}")
        
    def process_file_list(self):
        """Process the selected individual files"""
        self.log_message(f"Processing {len(self.selected_files)} individual files")
        
        if not self.selected_files:
            return
        
        # Determine output folder location
        if self.custom_output_folder:
            # Use custom output folder
            output_folder = os.path.join(self.custom_output_folder, "PRINT_MODE_OUTPUT")
            self.log_message(f"Using custom output location: {output_folder}")
        else:
            # Use default behavior (same directory as first file)
            first_file_dir = os.path.dirname(self.selected_files[0])
            output_folder = os.path.join(first_file_dir, "PRINT_MODE_OUTPUT")
            self.log_message(f"Using default output location: {output_folder}")
        
        os.makedirs(output_folder, exist_ok=True)
        
        processed_count = 0
        failed_files = []
        
        for i, file_path in enumerate(self.selected_files):
            try:
                # Update progress
                progress = (i / len(self.selected_files)) * 100
                self.progress_var.set(progress)
                filename = os.path.basename(file_path)
                self.status_var.set(f"Processing: {filename}")
                self.root.update_idletasks()
                
                # Process the image
                success = self.process_single_image(file_path, output_folder, "", filename)
                if success:
                    processed_count += 1
                else:
                    failed_files.append(filename)
                    
            except Exception as e:
                filename = os.path.basename(file_path)
                self.log_message(f"Error processing {filename}: {str(e)}")
                failed_files.append(filename)
        
        # Final update
        self.progress_var.set(100)
        self.status_var.set("Processing complete!")
        self.log_message(f"\nProcessing completed!")
        self.log_message(f"Successfully processed: {processed_count} files")
        if failed_files:
            self.log_message(f"Failed to process: {len(failed_files)} files")
            
    def process_single_image(self, input_path, output_folder, relative_folder, filename):
        """Process a single image file"""
        try:
            # Extract order number
            order_number = self.extract_order_number(filename)
            if order_number is None:
                self.log_message(f"Warning: Could not extract order number from {filename}")
                order_number = "1"  # Default fallback as string
            
            # Detect phone model
            detected_model = self.detect_phone_model(filename)
            if detected_model is None:
                self.log_message(f"Warning: Could not auto-detect model for {filename}")
                # Show model selection dialog
                detected_model = self.show_model_selection_dialog(filename)
                if detected_model is None:
                    self.log_message(f"Skipped: {filename} (no model selected)")
                    return False
                    
            self.log_message(f"Processing: {filename} -> Order #{order_number}, {detected_model}")
            
            # Get model specifications
            model_spec = self.model_specs.get(detected_model)
            if not model_spec:
                self.log_message(f"Error: Unknown model specification for {detected_model}")
                return False
                
            # Load and process the image
            processed_image = self.create_print_ready_image(input_path, order_number, detected_model, model_spec)
            
            if processed_image is None:
                return False
                
            # Create output path
            output_subfolder = os.path.join(output_folder, relative_folder) if relative_folder else output_folder
            os.makedirs(output_subfolder, exist_ok=True)
            
            # Generate output filename
            standardized_model = self.standardize_model_name(detected_model)
            output_filename = f"{order_number}_{standardized_model}.png"
            output_path = os.path.join(output_subfolder, output_filename)
            
            # Save the processed image
            processed_image.save(output_path, "PNG")
            self.log_message(f"Saved: {output_filename}")
            
            return True
            
        except Exception as e:
            self.log_message(f"Error processing {filename}: {str(e)}")
            return False
            
    def create_print_ready_image(self, input_path, order_number, model_name, model_spec):
        """Create the final print-ready image with proper layout - graphics centered on full canvas
        
        NOTE: Adding 0.3cm to all target widths to compensate for systematic printing offset
        """
        try:
            # Load the original image
            original_image = Image.open(input_path)
            
            # Convert to RGBA if needed
            if original_image.mode != 'RGBA':
                original_image = original_image.convert('RGBA')
            
            # Horizontally flip the image
            flipped_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)
            
            # Calculate target width in pixels with 0.3cm compensation (HARDCODED FIX)
            target_width_cm = model_spec['width_cm'] + 0.3  # Add 0.3cm to compensate for systematic offset
            target_width_px = round(target_width_cm * self.dpi / 2.54)
            
            # Resize image maintaining aspect ratio
            original_width, original_height = flipped_image.size
            aspect_ratio = original_height / original_width
            target_height_px = round(target_width_px * aspect_ratio)
            
            resized_image = flipped_image.resize((target_width_px, target_height_px), Image.Resampling.LANCZOS)
            
            # Create transparent canvas at film sheet size
            canvas = Image.new('RGBA', (self.film_width_px, self.film_height_px), (0, 0, 0, 0))
            
            # Calculate positions for centering the image on the FULL canvas
            image_x = (self.film_width_px - target_width_px) // 2
            image_y = (self.film_height_px - target_height_px) // 2
            
            # Check if image will be clipped and warn user
            if target_height_px > self.film_height_px:
                self.log_message(f"Warning: {os.path.basename(input_path)} is very tall ({target_height_px}px > {self.film_height_px}px canvas) - image will be clipped to maintain {model_spec['width_cm']}cm width")
                # Center the image even if it extends beyond canvas
                image_y = (self.film_height_px - target_height_px) // 2
            
            # Paste the resized image onto the canvas (may clip if too tall)
            canvas.paste(resized_image, (image_x, image_y), resized_image)
            
            # Add text overlays with shortened model name (IP instead of iPhone)
            display_model_name = self.format_display_model_name(model_name)
            canvas = self.add_text_overlays(canvas, order_number, display_model_name)
            
            # Debug logging to verify dimensions
            original_target_cm = model_spec['width_cm']
            actual_width_cm = target_width_px * 2.54 / self.dpi
            self.log_message(f"Original: {original_target_cm}cm -> Compensated: {target_width_cm}cm ({target_width_px}px) -> Actual: {actual_width_cm:.3f}cm")
            
            return canvas
            
        except Exception as e:
            self.log_message(f"Error creating print-ready image: {str(e)}")
            return None
            
    def add_text_overlays(self, canvas, order_number, display_model_name):
        """Add order number and model name text to the canvas as overlay - INK SAVING VERSION (no bold)"""
        try:
            # Create a drawing context
            draw = ImageDraw.Draw(canvas)
            
            # Try to use system fonts with better fallback handling
            order_font = None
            model_font = None
            
            # Font file paths to try (Windows system fonts)
            font_paths = [
                "C:/Windows/Fonts/arialn.ttf",      # Arial Narrow (thinnest standard font)
                "C:/Windows/Fonts/calibril.ttf",    # Calibri Light  
                "C:/Windows/Fonts/segoeuil.ttf",    # Segoe UI Light
                "C:/Windows/Fonts/arial.ttf",       # Fallback
            ]
            
            # Try to load fonts
            for font_path in font_paths:
                try:
                    order_font = ImageFont.truetype(font_path, 104)
                    model_font = ImageFont.truetype(font_path, 64)
                    break
                except:
                    continue
            
            # Fallback to default font if none found
            if order_font is None:
                try:
                    order_font = ImageFont.load_default()
                    model_font = ImageFont.load_default()
                except:
                    # Last resort fallback
                    pass
            
            # Position both order number and model name on the same top line
            margin = round(0.5 * self.dpi / 2.54)  # 5mm margin in pixels (FIXED: use round())
            order_text = order_number  # Already a string (supports 3a, 3b, 3c format)
            
            # Add order number in top-left corner
            if order_font:
                # Draw the text once only to save ink
                draw.text((margin, margin), order_text, fill='#808080', font=order_font)
                
                # Calculate order number width to position model name after it
                order_bbox = draw.textbbox((0, 0), order_text, font=order_font)
                order_width = order_bbox[2] - order_bbox[0]
                
                # Add model name on the same line, with spacing after order number
                spacing = round(1.0 * self.dpi / 2.54)  # 1cm spacing between order and model (FIXED: use round())
                model_text_x = margin + order_width + spacing
                model_text_y = margin
                
                # Draw model name
                draw.text((model_text_x, model_text_y), display_model_name, fill='#808080', font=model_font)
            else:
                # Fallback without font
                draw.text((margin, margin), order_text, fill='black')
                # Simple fallback positioning for model name
                model_text_x = margin + 200  # Rough spacing
                draw.text((model_text_x, margin), display_model_name, fill='black')
            
            return canvas
            
        except Exception as e:
            self.log_message(f"Error adding text overlays: {str(e)}")
            return canvas
            
    def show_model_selection_dialog(self, filename):
        """Show a dialog to manually select the iPhone model - UPDATED WITH NEW MODELS"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Select Model for: {filename}")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, self.root.winfo_rooty() + 100))
        
        selected_model = tk.StringVar()
        
        # Title
        ttk.Label(dialog, text=f"Could not auto-detect model for:", 
                 font=('Arial', 10, 'bold')).pack(pady=10)
        ttk.Label(dialog, text=filename, foreground="blue").pack(pady=(0, 20))
        
        # Create scrollable frame for model list
        canvas = tk.Canvas(dialog, height=300)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Group models by category
        model_categories = {
            "iPhone 16 Series": [
                "iPhone 16 Pro Max", "iPhone 16 Plus", "iPhone 16 Pro", "iPhone 16"
            ],
            "iPhone 15 Series": [
                "iPhone 15 Pro Max", "iPhone 15 Plus", "iPhone 15 Pro", "iPhone 15"
            ],
            "iPhone 14 Series": [
                "iPhone 14 Pro Max", "iPhone 14 Plus", "iPhone 14 Pro", "iPhone 14"
            ],
            "iPhone 13 Series": [
                "iPhone 13 Pro Max", "iPhone 13 Pro", "iPhone 13", "iPhone 13 mini"
            ],
            "iPhone 12 Series": [
                "iPhone 12 Pro Max", "iPhone 12 Pro", "iPhone 12", "iPhone 12 mini"
            ],
            "iPhone 11 Series": [
                "iPhone 11 Pro Max", "iPhone 11 Pro", "iPhone 11"
            ],
            "iPhone X Series": [
                "iPhone XS Max", "iPhone XS", "iPhone XR", "iPhone X"
            ],
            "iPhone 8 Series": [
                "iPhone 8 Plus", "iPhone 8"
            ],
            "iPhone 7 Series": [
                "iPhone 7 Plus", "iPhone 7"
            ]
        }
        
        # Add radio buttons for each model
        for category, models in model_categories.items():
            # Category header
            ttk.Label(scrollable_frame, text=category, 
                     font=('Arial', 9, 'bold')).pack(anchor='w', pady=(10, 5), padx=20)
            
            # Model radio buttons
            for model in models:
                width_cm = self.model_specs[model]['width_cm']
                ttk.Radiobutton(scrollable_frame, 
                               text=f"{model} ({width_cm}cm)", 
                               variable=selected_model, 
                               value=model).pack(anchor='w', padx=40)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        result = {'model': None, 'cancelled': False}
        
        def on_select():
            if selected_model.get():
                result['model'] = selected_model.get()
                dialog.destroy()
            else:
                messagebox.showwarning("No Selection", "Please select a model.")
        
        def on_cancel():
            result['cancelled'] = True
            dialog.destroy()
        
        ttk.Button(button_frame, text="Select", command=on_select).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side='left')
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result['model'] if not result['cancelled'] else None
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = iPhoneCaseProcessor()
    app.run()