import tkinter as tk
from tkinter import ttk, messagebox
import random

class AlgorithmsVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title(" Algorithms Visualizer - Sorting & Searching")
        self.root.geometry("1200x900")
        self.root.configure(bg="#1e1b4b")
        
        # ตัวแปรสำหรับ Sorting
        self.array = [64, 34, 25, 12, 22, 11, 90, 88]
        self.selected_sorting_algorithm = "Bubble Sort"
        self.sorting = False
        self.sorting_speed = 300
        
        # ตัวแปรสำหรับ Searching
        self.searching_data = [64, 34, 25, 12, 22, 11, 90, 88]
        self.sorted_data = sorted(self.searching_data.copy())
        self.target_value = 25
        self.searching = False
        self.selected_searching_algorithm = "Sequential Search"
        self.searching_speed = 300
        self.comparisons = 0
        
        # สร้าง UI
        self.create_widgets()
        self.draw_array()             
        self.update_info()            
        self.update_searching_display() 
        self.update_searching_info()
    
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#1e1b4b")
        header_frame.pack(pady=20)
        
        title_label = tk.Label(
            header_frame,
            text=" Algorithms Visualizer - Sorting & Searching",
            font=("Comic Sans MS", 28, "bold"), 
            bg="#1e1b4b",
            fg="white"
        )
        title_label.pack()
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sorting Tab
        self.sorting_frame = tk.Frame(self.notebook, bg="#1e1b4b")
        self.notebook.add(self.sorting_frame, text=" Sorting Algorithms")
        
        # Searching Tab
        self.searching_frame = tk.Frame(self.notebook, bg="#1e1b4b")
        self.notebook.add(self.searching_frame, text=" Searching Algorithms")
        
        # สร้าง UI สำหรับ Sorting
        self.create_sorting_ui()
        
        # สร้าง UI สำหรับ Searching
        self.create_searching_ui()

        # เพิ่ม Event Binding เมื่อมีการเปลี่ยนแท็บ
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def on_tab_change(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 1: # Index 1 คือ Searching Tab
            self.update_searching_display()
            self.update_searching_info()

    def create_sorting_ui(self):
        # Algorithm Selection Frame
        algo_frame = tk.Frame(self.sorting_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        algo_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            algo_frame,
            text=" เลือกอัลกอริทึม Sorting:",
            font=("Comic Sans MS", 14, "bold"),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        algorithms = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"]
        self.sorting_algo_var = tk.StringVar(value="Bubble Sort")
        
        for algo in algorithms:
            rb = tk.Radiobutton(
                algo_frame,
                text=algo,
                variable=self.sorting_algo_var,
                value=algo,
                font=("Comic Sans MS", 11),
                bg="#2d2654",   
                fg="white",
                selectcolor="#7c3aed",
                activebackground="#2d2654",
                activeforeground="white",
                command=self.update_sorting_algorithm
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Input Frame (ตำแหน่งที่ 1)
        input_frame = tk.Frame(self.sorting_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            input_frame,
            text="ใส่ตัวเลข:",
            font=("Comic Sans MS", 12, "bold"),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.input_entry = tk.Entry(
            input_frame,
            font=("Comic Sans MS", 12),
            width=40,
            bg="#1e1b4b",
            fg="white",
            insertbackground="white"
        )
        self.input_entry.pack(side=tk.LEFT, padx=5)
        self.input_entry.insert(0, "64, 34, 25, 12, 22, 11, 90, 88")
        
        self.apply_input_button = tk.Button(
            input_frame,
            text=" ใช้ตัวเลขนี้",
            font=("Comic Sans MS", 10, "bold"),
            bg="#8b5cf6",
            fg="white",
            activebackground="#7c3aed",
            command=self.apply_custom_input,
            cursor="hand2"
        )
        self.apply_input_button.pack(side=tk.LEFT, padx=10)
        
        # Random Options Frame (ตำแหน่งที่ 2: ถูกย้ายมาจากด้านล่าง)
        random_frame = tk.Frame(self.sorting_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        random_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            random_frame,
            text=" ตั้งค่าการสุ่ม:",
            font=("Comic Sans MS", 12, "bold"),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(
            random_frame,
            text="จำนวนตัวเลข:",
            font=("Comic Sans MS", 10),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        self.count_spinbox = tk.Spinbox(
            random_frame,
            from_=3,
            to=15,
            width=5,
            font=("Comic Sans MS", 10),
            bg="#1e1b4b",
            fg="white",
            buttonbackground="#7c3aed"
        )
        self.count_spinbox.delete(0, tk.END)
        self.count_spinbox.insert(0, "8")
        self.count_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            random_frame,
            text="ค่าต่ำสุด:",
            font=("Comic Sans MS", 10),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.min_spinbox = tk.Spinbox(
            random_frame,
            from_=1,
            to=50,
            width=5,
            font=("Comic Sans MS", 10),
            bg="#1e1b4b",
            fg="white",
            buttonbackground="#7c3aed"
        )
        self.min_spinbox.delete(0, tk.END)
        self.min_spinbox.insert(0, "10")
        self.min_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            random_frame,
            text="ค่าสูงสุด:",
            font=("Comic Sans MS", 10),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.max_spinbox = tk.Spinbox(
            random_frame,
            from_=50,
            to=200,
            width=5,
            font=("Comic Sans MS", 10),
            bg="#1e1b4b",
            fg="white",
            buttonbackground="#7c3aed"
        )
        self.max_spinbox.delete(0, tk.END)
        self.max_spinbox.insert(0, "100")
        self.max_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Control Panel Frame (ตำแหน่งที่ 3)
        control_frame = tk.Frame(self.sorting_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # ปุ่มควบคุม Sorting
        self.start_sorting_button = tk.Button(
            control_frame,
            text="▶ เริ่มเรียงลำดับ",
            font=("Comic Sans MS", 12, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            command=self.start_sorting,
            width=15,
            height=2,
            cursor="hand2"
        )
        self.start_sorting_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.random_button = tk.Button(
            control_frame,
            text="🔀 สุ่มข้อมูลใหม่",
            font=("Comic Sans MS", 12, "bold"),
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            command=self.generate_random_array,
            width=15,
            height=2,
            cursor="hand2"
        )
        self.random_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.reset_button = tk.Button(
            control_frame,
            text="↻ รีเซ็ต",
            font=("Comic Sans MS", 12, "bold"),
            bg="#a855f7",
            fg="white",
            activebackground="#9333ea",
            command=self.reset_sorting,
            width=15,
            height=2,
            cursor="hand2"
        )
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Speed Control
        tk.Label(
            control_frame,
            text=" ความเร็ว:",
            font=("Comic Sans MS", 11),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=10)
        
        self.sorting_speed_scale = tk.Scale(
            control_frame,
            from_=50,
            to=1000,
            orient=tk.HORIZONTAL,
            bg="#2d2654",
            fg="white",
            highlightthickness=0,
            length=150,
            command=self.update_sorting_speed
        )
        self.sorting_speed_scale.set(300)
        self.sorting_speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Canvas Frame
        canvas_frame = tk.Frame(self.sorting_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        canvas_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Canvas สำหรับวาดกราฟ Sorting
        self.sorting_canvas = tk.Canvas(
            canvas_frame,
            bg="#1e1b4b",
            height=350,
            highlightthickness=0
        )
        self.sorting_canvas.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Legend Frame
        legend_frame = tk.Frame(canvas_frame, bg="#2d2654")
        legend_frame.pack(pady=10)
        
        legends = [
            ("ยังไม่เรียง", "#3b82f6"),
            ("กำลังเปรียบเทียบ", "#fbbf24"),
            ("เรียงเรียบร้อย", "#22c55e")
        ]
        
        for text, color in legends:
            frame = tk.Frame(legend_frame, bg="#2d2654")
            frame.pack(side=tk.LEFT, padx=15)
            
            color_box = tk.Canvas(frame, width=30, height=20, bg=color, highlightthickness=0)
            color_box.pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                frame,
                text=text,
                font=("Comic Sans MS", 10),
                bg="#2d2654",
                fg="white"
            ).pack(side=tk.LEFT)
        
        # Info Frame
        self.sorting_info_frame = tk.Frame(self.sorting_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        self.sorting_info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.sorting_info_label = tk.Label(
            self.sorting_info_frame,
            text="",
            font=("Comic Sans MS", 11),
            bg="#2d2654",
            fg="white",
            justify=tk.LEFT,
            anchor="w"
        )
        self.sorting_info_label.pack(pady=10, padx=20, fill=tk.X)
    
    def create_searching_ui(self):
        # Algorithm Selection Frame
        algo_frame = tk.Frame(self.searching_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        algo_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            algo_frame,
            text=" เลือกอัลกอริทึม Searching:",
            font=("Comic Sans MS", 14, "bold"),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        algorithms = ["Sequential Search", "Binary Search"]
        self.searching_algo_var = tk.StringVar(value="Sequential Search")
        
        for algo in algorithms:
            rb = tk.Radiobutton(
                algo_frame,
                text=algo,
                variable=self.searching_algo_var,
                value=algo,
                font=("Comic Sans MS", 11),
                bg="#2d2654",
                fg="white",
                selectcolor="#7c3aed",
                activebackground="#2d2654",
                activeforeground="white",
                command=self.update_searching_algorithm
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Data Controls Frame (ตำแหน่งที่ 1)
        data_frame = tk.Frame(self.searching_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        data_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Data input
        tk.Label(
            data_frame,
            text=" ข้อมูล:",
            font=("Comic Sans MS", 12, "bold"),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.searching_data_entry = tk.Entry(
            data_frame,
            font=("Comic Sans MS", 12),
            width=30,
            bg="#1e1b4b",
            fg="white",
            insertbackground="white"
        )
        self.searching_data_entry.pack(side=tk.LEFT, padx=5)
        self.searching_data_entry.insert(0, "64, 34, 25, 12, 22, 11, 90, 88")
        
        # Target value
        tk.Label(
            data_frame,
            text=" ค่าที่ค้นหา:",
            font=("Comic Sans MS", 12, "bold"),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.target_entry = tk.Entry(
            data_frame,
            font=("Comic Sans MS", 12),
            width=10,
            bg="#1e1b4b",
            fg="white",
            insertbackground="white"
        )
        self.target_entry.pack(side=tk.LEFT, padx=5)
        self.target_entry.insert(0, "25")
        
        # Random Options Frame (ตำแหน่งที่ 2)
        random_search_frame = tk.Frame(self.searching_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        random_search_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            random_search_frame,
            text=" ตั้งค่าการสุ่ม:",
            font=("Comic Sans MS", 12, "bold"),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(
            random_search_frame,
            text="จำนวนตัวเลข:",
            font=("Comic Sans MS", 10),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        self.search_count_spinbox = tk.Spinbox(
            random_search_frame,
            from_=3,
            to=15,
            width=5,
            font=("Comic Sans MS", 10),
            bg="#1e1b4b",
            fg="white",
            buttonbackground="#7c3aed"
        )
        self.search_count_spinbox.delete(0, tk.END)
        self.search_count_spinbox.insert(0, "8")
        self.search_count_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            random_search_frame,
            text="ค่าต่ำสุด:",
            font=("Comic Sans MS", 10),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.search_min_spinbox = tk.Spinbox(
            random_search_frame,
            from_=1,
            to=50,
            width=5,
            font=("Comic Sans MS", 10),
            bg="#1e1b4b",
            fg="white",
            buttonbackground="#7c3aed"
        )
        self.search_min_spinbox.delete(0, tk.END)
        self.search_min_spinbox.insert(0, "10")
        self.search_min_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            random_search_frame,
            text="ค่าสูงสุด:",
            font=("Comic Sans MS", 10),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.search_max_spinbox = tk.Spinbox(
            random_search_frame,
            from_=50,
            to=200,
            width=5,
            font=("Comic Sans MS", 10),
            bg="#1e1b4b",
            fg="white",
            buttonbackground="#7c3aed"
        )
        self.search_max_spinbox.delete(0, tk.END)
        self.search_max_spinbox.insert(0, "100")
        self.search_max_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Control Buttons Frame (ตำแหน่งที่ 3)
        control_frame = tk.Frame(self.searching_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # ปุ่มควบคุม Searching
        self.start_searching_button = tk.Button(
            control_frame,
            text="▶ เริ่มค้นหา",
            font=("Comic Sans MS", 12, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            command=self.start_searching,
            width=15,
            height=2,
            cursor="hand2"
        )
        self.start_searching_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # สลับตำแหน่งปุ่ม: สุ่มข้อมูลก่อนใช้ข้อมูล
        self.random_search_data_button = tk.Button(
            control_frame,
            text="🔀 สุ่มข้อมูลใหม่",
            font=("Comic Sans MS", 12, "bold"),
            bg="#a855f7",
            fg="white",
            activebackground="#9333ea",
            command=self.generate_random_search_data,
            width=15,
            height=2,
            cursor="hand2"
        )
        self.random_search_data_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.use_data_button = tk.Button(
            control_frame,
            text="📥 ใช้ข้อมูลนี้",
            font=("Comic Sans MS", 12, "bold"),
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            command=self.use_searching_data,
            width=15,
            height=2,
            cursor="hand2"
        )
        self.use_data_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Speed Control
        tk.Label(
            control_frame,
            text=" ความเร็ว:",
            font=("Comic Sans MS", 11),
            bg="#2d2654",
            fg="white"
        ).pack(side=tk.LEFT, padx=10)
        
        self.searching_speed_scale = tk.Scale(
            control_frame,
            from_=50,
            to=1000,
            orient=tk.HORIZONTAL,
            bg="#2d2654",
            fg="white",
            highlightthickness=0,
            length=150,
            command=self.update_searching_speed
        )
        self.searching_speed_scale.set(300)
        self.searching_speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Canvas Frame
        canvas_frame = tk.Frame(self.searching_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        canvas_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Canvas สำหรับวาดกราฟ Searching
        self.searching_canvas = tk.Canvas(
            canvas_frame,
            bg="#1e1b4b",
            height=350,
            highlightthickness=0
        )
        self.searching_canvas.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Legend Frame
        legend_frame = tk.Frame(canvas_frame, bg="#2d2654")
        legend_frame.pack(pady=10)
        
        legends = [
            ("ข้อมูลปกติ", "#3b82f6"),
            ("กำลังตรวจสอบ", "#fbbf24"),
            ("พบค่า", "#22c55e"),
            ("ช่วงค้นหา", "#8b5cf6")
        ]
        
        for text, color in legends:
            frame = tk.Frame(legend_frame, bg="#2d2654")
            frame.pack(side=tk.LEFT, padx=15)
            
            color_box = tk.Canvas(frame, width=30, height=20, bg=color, highlightthickness=0)
            color_box.pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                frame,
                text=text,
                font=("Comic Sans MS", 10),
                bg="#2d2654",
                fg="white"
            ).pack(side=tk.LEFT)
        
        # Info Frame
        self.searching_info_frame = tk.Frame(self.searching_frame, bg="#2d2654", relief=tk.RAISED, bd=2)
        self.searching_info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.searching_info_text = tk.Text(
            self.searching_info_frame,
            height=4,
            font=("Comic Sans MS", 11),
            bg="#2d2654",
            fg="white",
            wrap=tk.WORD
        )
        self.searching_info_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.searching_info_text.insert(tk.END, "ข้อมูล: \nตำแหน่ง: \nจำนวนการเปรียบเทียบ: 0")
        self.searching_info_text.config(state=tk.DISABLED)
    
    # ==================== METHODS FOR SORTING ====================
    
    def apply_custom_input(self):
        """ใช้ตัวเลขที่ผู้ใช้ใส่เองสำหรับ Sorting"""
        if not self.sorting:
            try:
                input_text = self.input_entry.get().strip()
                numbers = [int(x.strip()) for x in input_text.split(',') if x.strip()]
                
                if len(numbers) == 0:
                    messagebox.showwarning("คำเตือน", "กรุณาใส่ตัวเลขอย่างน้อย 1 ตัว")
                    return
                
                if len(numbers) > 20:
                    messagebox.showwarning("คำเตือน", "ใส่ตัวเลขได้ไม่เกิน 20 ตัว")
                    return
                
                self.array = numbers
                self.draw_array()
                
            except ValueError:
                messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่ตัวเลขที่ถูกต้อง คั่นด้วยเครื่องหมายจุลภาค\nตัวอย่าง: 5, 2, 8, 1, 9")
    
    def update_sorting_algorithm(self):
        self.selected_sorting_algorithm = self.sorting_algo_var.get()
        self.update_info()
    
    def update_sorting_speed(self, value):
        self.sorting_speed = int(value)
    
    def update_info(self):
        info_dict = {
            "Bubble Sort": "⏱️ Time: O(n²) | 💾 Space: O(1) | 📝 เปรียบเทียบคู่ติดกันจากขวาไปซ้ายในแต่ละรอบ ค่าน้อยสุดจะลอยมาด้านซ้าย",
            "Selection Sort": "⏱️ Time: O(n²) | 💾 Space: O(1) | 📝 หาค่าน้อยสุดและสลับกับตำแหน่งที่ถูกต้อง",
            "Insertion Sort": "⏱️ Time: O(n²) | 💾 Space: O(1) | 📝 สลับที่ตัวปัจจุบันกับตัวหน้าจนอยู่ตำแหน่งที่ถูกต้อง",
            "Merge Sort": "⏱️ Time: O(n log n) | 💾 Space: O(n) | 📝 แบ่งครึ่งและผสานกลับพร้อมเรียงลำดับ"
        }
        self.sorting_info_label.config(text=f"📖 {self.selected_sorting_algorithm}\n{info_dict[self.selected_sorting_algorithm]}")
    
    def draw_array(self, color_array=None):
        self.sorting_canvas.delete("all")
        self.sorting_canvas.update_idletasks() # ต้องเรียกเพื่อให้ได้ขนาดจริง

        canvas_width = self.sorting_canvas.winfo_width()
        canvas_height = self.sorting_canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 1100
        if canvas_height <= 1:
            canvas_height = 350
        
        if not self.array:
            return

        bar_width = (canvas_width - 100) / len(self.array)
        max_value = max(self.array) if self.array else 1
        
        for i, value in enumerate(self.array):
            x0 = i * bar_width + 50
            y0 = canvas_height - 50
            x1 = (i + 1) * bar_width + 50 - 5
            y1 = canvas_height - 50 - (value / max_value * (canvas_height - 100))
            
            color = "#3b82f6"  # สีน้ำเงิน (ปกติ)
            if color_array:
                if i in color_array.get("sorted", []):
                    color = "#22c55e"  # สีเขียว (เรียงแล้ว)
                elif i in color_array.get("comparing", []):
                    color = "#fbbf24"  # สีเหลือง (กำลังเปรียบเทียบ)
            
            self.sorting_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)
            self.sorting_canvas.create_text(
                (x0 + x1) / 2,
                y1 - 15,
                font=("Comic Sans MS", 10, "bold"),
                text=str(value),
                fill="white"
            )
    
    def generate_random_array(self):
        """สุ่มตัวเลขตามค่าที่ตั้งไว้สำหรับ Sorting"""
        if not self.sorting:
            try:
                # ใช้ spinbox ของ sorting
                count = int(self.count_spinbox.get())
                min_val = int(self.min_spinbox.get())
                max_val = int(self.max_spinbox.get())
                
                if min_val >= max_val:
                    messagebox.showerror("ข้อผิดพลาด", "ค่าต่ำสุดต้องน้อยกว่าค่าสูงสุด")
                    return
                
                self.array = [random.randint(min_val, max_val) for _ in range(count)]
                
                # อัพเดท input entry ด้วย
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, ', '.join(map(str, self.array)))
                
                self.draw_array()
                
            except ValueError:
                messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่ค่าที่ถูกต้อง")
    
    def reset_sorting(self):
        if not self.sorting:
            self.array = [64, 34, 25, 12, 22, 11, 90, 88]
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, ', '.join(map(str, self.array)))
            self.draw_array()
    
    def start_sorting(self):
        if not self.sorting:
            self.sorting = True
            self.disable_sorting_buttons()
            
            if self.selected_sorting_algorithm == "Bubble Sort":
                self.bubble_sort()
            elif self.selected_sorting_algorithm == "Selection Sort":
                self.selection_sort()
            elif self.selected_sorting_algorithm == "Insertion Sort":
                self.insertion_sort()
            elif self.selected_sorting_algorithm == "Merge Sort":
                self.merge_sort()
    
    def disable_sorting_buttons(self):
        self.start_sorting_button.config(state=tk.DISABLED)
        self.random_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.apply_input_button.config(state=tk.DISABLED)
    
    def enable_sorting_buttons(self):
        self.start_sorting_button.config(state=tk.NORMAL)
        self.random_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.apply_input_button.config(state=tk.NORMAL)
        self.sorting = False
    
    def bubble_sort(self):
        def sort_step(i, j):
            if i < len(self.array) - 1:
                if j > i:
                    self.draw_array({
                        "comparing": [j - 1, j],
                        "sorted": list(range(i))
                    })

                    if self.array[j - 1] > self.array[j]:
                        self.array[j - 1], self.array[j] = self.array[j], self.array[j - 1]
                    
                    self.root.after(self.sorting_speed, lambda: sort_step(i, j - 1))
                else:
                    self.root.after(self.sorting_speed, lambda: sort_step(i + 1, len(self.array) - 1))
            else:
                self.draw_array({"sorted": list(range(len(self.array)))})
                self.enable_sorting_buttons()

        sort_step(0, len(self.array) - 1)
    
    def selection_sort(self):
        def sort_step(i, j, min_idx):
            if i < len(self.array):
                if j < len(self.array):
                    self.draw_array({"comparing": [min_idx, j], "sorted": list(range(i))})
                    
                    if self.array[j] < self.array[min_idx]:
                        min_idx = j
                    
                    self.root.after(self.sorting_speed, lambda: sort_step(i, j + 1, min_idx))
                else:
                    self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                    self.root.after(self.sorting_speed, lambda: sort_step(i + 1, i + 1, i + 1))
            else:
                self.draw_array({"sorted": list(range(len(self.array)))})
                self.enable_sorting_buttons()
        
        sort_step(0, 0, 0)
    
    def insertion_sort(self):
        self.sorted_array = self.array.copy()
        
        def sort_step(i):
            if i < len(self.sorted_array):
                j = i
                
                def insert_step(j):
                    # ถ้า j > 0 และตัวหน้ามากกว่าตัวปัจจุบัน ให้สลับที่
                    if j > 0 and self.sorted_array[j - 1] > self.sorted_array[j]:
                        self.draw_array({"comparing": [j - 1, j], "sorted": list(range(i))})
                        
                        # สลับที่
                        self.sorted_array[j - 1], self.sorted_array[j] = self.sorted_array[j], self.sorted_array[j - 1]
                        self.array = self.sorted_array.copy()
                        
                        self.root.after(self.sorting_speed, lambda: insert_step(j - 1))
                    else:
                        # เจอตำแหน่งที่เหมาะสมแล้ว
                        self.array = self.sorted_array.copy()
                        self.draw_array({"comparing": [j], "sorted": list(range(i + 1))})
                        self.root.after(self.sorting_speed, lambda: sort_step(i + 1))
                
                insert_step(j)
            else:
                self.draw_array({"sorted": list(range(len(self.array)))})
                self.enable_sorting_buttons()
        
        sort_step(1)

    
    
    def merge_sort(self):
        self.merge_steps = []
        self.generate_merge_steps(self.array.copy(), 0, len(self.array) - 1)
        self.animate_merge_steps(0)
    
    def generate_merge_steps(self, arr, left, right):
        if left < right:
            mid = (left + right) // 2
            self.generate_merge_steps(arr, left, mid)
            self.generate_merge_steps(arr, mid + 1, right)
            self.merge_step(arr, left, mid, right)
    
    def merge_step(self, arr, left, mid, right):
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_arr) and j < len(right_arr):
            self.merge_steps.append((arr.copy(), [left + i, mid + 1 + j]))
            
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
            
            self.merge_steps.append((arr.copy(), [k - 1]))
        
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
        
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1

        # บันทึกสถานะหลังผสานเสร็จ (รวมตัวที่เหลือ) เพื่อให้ภาพสุดท้ายเรียงครบ
        self.merge_steps.append((arr.copy(), list(range(left, right + 1))))
    
    def animate_merge_steps(self, step):
        if step < len(self.merge_steps):
            self.array, comparing = self.merge_steps[step]
            self.draw_array({"comparing": comparing, "sorted": []})
            self.root.after(self.sorting_speed, lambda: self.animate_merge_steps(step + 1))
        else:
            self.draw_array({"sorted": list(range(len(self.array)))})
            self.enable_sorting_buttons()
    
    # ==================== METHODS FOR SEARCHING ====================
    
    def update_searching_algorithm(self):
        self.selected_searching_algorithm = self.searching_algo_var.get()
        self.update_searching_display()
    
    def update_searching_speed(self, value):
        self.searching_speed = int(value)
    
    def generate_random_search_data(self):
        """สุ่มตัวเลขสำหรับ Searching"""
        if self.searching:
            messagebox.showwarning("คำเตือน", "กำลังค้นหาอยู่! กรุณารอให้เสร็จสิ้นก่อน")
            return
            
        try:
            # ใช้ค่าจาก Spinbox ของ searching
            count = int(self.search_count_spinbox.get())
            min_val = int(self.search_min_spinbox.get())
            max_val = int(self.search_max_spinbox.get())
            
            if min_val >= max_val:
                messagebox.showerror("ข้อผิดพลาด", "ค่าต่ำสุดต้องน้อยกว่าค่าสูงสุด")
                return
            
            self.searching_data = [random.randint(min_val, max_val) for _ in range(count)]
            self.sorted_data = sorted(self.searching_data.copy())
            
            # สุ่มค่าเป้าหมาย
            self.target_value = random.choice(self.searching_data + [random.randint(min_val, max_val)])
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, str(self.target_value))
            
            # อัพเดท input entry
            self.searching_data_entry.delete(0, tk.END)
            self.searching_data_entry.insert(0, ', '.join(map(str, self.searching_data)))
            
            self.update_searching_display()
            self.update_searching_info(additional_info="สุ่มข้อมูลใหม่สำเร็จ")
            
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่ค่าตั้งค่าการสุ่มที่ถูกต้อง")
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการสุ่มข้อมูล: {e}")

    def use_searching_data(self):
        """ใช้ข้อมูลที่ผู้ใช้ป้อนสำหรับ Searching"""
        if self.searching:
            messagebox.showwarning("คำเตือน", "กำลังค้นหาอยู่! กรุณารอให้เสร็จสิ้นก่อน")
            return

        try:
            input_text = self.searching_data_entry.get()
            self.searching_data = [int(x.strip()) for x in input_text.split(',') if x.strip()]
            
            if not self.searching_data:
                messagebox.showwarning("คำเตือน", "กรุณาใส่ตัวเลขอย่างน้อย 1 ตัว")
                return

            self.sorted_data = sorted(self.searching_data.copy())
            
            # ดึงค่าเป้าหมายล่าสุด
            try:
                self.target_value = int(self.target_entry.get())
            except ValueError:
                # ตั้งค่าเริ่มต้นถ้าไม่มี
                self.target_value = self.searching_data[0] if self.searching_data else 0
                self.target_entry.delete(0, tk.END)
                self.target_entry.insert(0, str(self.target_value))

            self.update_searching_display()
            self.update_searching_info(additional_info="ใช้ข้อมูลใหม่สำเร็จ")
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกตัวเลขที่ถูกต้อง (คั่นด้วย comma)")
    
    def update_searching_display(self, current_index=None, found_index=None, low=None, high=None, mid=None):
        """แสดงข้อมูลในรูปแบบกราฟแท่งสำหรับ Searching"""
        self.searching_canvas.delete("all")      # ล้างทุกอย่างบน canvas
        self.searching_canvas.update_idletasks() 
        
        # เลือกข้อมูลที่แสดงผล: ข้อมูลเรียงแล้วสำหรับ Binary Search, ข้อมูลเดิมสำหรับ Sequential Search
        display_data = self.sorted_data if self.selected_searching_algorithm == "Binary Search" else self.searching_data
        
        if not display_data:
            return
        
        canvas_width = self.searching_canvas.winfo_width()
        canvas_height = self.searching_canvas.winfo_height()
        
        # กำหนดขนาดสำรองในกรณีที่ยังไม่มีการวาด
        if canvas_width <= 1:
            canvas_width = 1100
        if canvas_height <= 1:
            canvas_height = 350
        
        bar_width = (canvas_width - 100) / len(display_data)
        max_value = max(display_data) if display_data else 1
        scale_factor = (canvas_height - 100) / max_value
        
        for i, value in enumerate(display_data):
            x0 = 50 + i * bar_width
            y0 = canvas_height - 50
            x1 = x0 + bar_width - 5
            y1 = y0 - value * scale_factor
            
            # เลือกสีตามสถานะ
            color = '#3b82f6'  # สีปกติ
            if found_index is not None and i == found_index:
                color = '#22c55e'  # สีสำหรับค่าที่พบ
            elif mid is not None and i == mid:
                color = '#ec4899'  # สีสำหรับตำแหน่งกลาง (Binary Search)
            elif low is not None and high is not None and low <= i <= high and self.selected_searching_algorithm == "Binary Search":
                color = '#8b5cf6'  # สีสำหรับช่วงที่กำลังค้นหา (Binary Search)
            elif current_index is not None and i == current_index and self.selected_searching_algorithm == "Sequential Search":
                color = '#fbbf24'  # สีสำหรับค่าที่กำลังตรวจสอบ (Sequential Search)

            
            self.searching_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='white', width=2)
            
            # แสดงค่า
            self.searching_canvas.create_text(
                (x0 + x1) / 2,
                y1 - 15,
                text=str(value),
                font=("Comic Sans MS", 10, "bold"),
                fill="white"
            )
            
            # แสดง index
            self.searching_canvas.create_text(
                (x0 + x1) / 2,
                y0 - 10,
                text=str(i),
                fill="#cccccc",
                font=("Comic Sans MS", 9)
            )
    
    def update_searching_info(self, position=None, comparisons=0, additional_info=""):
        """อัพเดทข้อมูลใน Info Panel สำหรับ Searching"""
        display_data = self.sorted_data if self.selected_searching_algorithm == "Binary Search" else self.searching_data
        
        self.searching_info_text.config(state=tk.NORMAL)
        self.searching_info_text.delete(1.0, tk.END)
        
        info_text = f"ข้อมูล: {display_data}\n"
        
        if position is not None:
            if position == -1:
                info_text += f"ตำแหน่ง: ไม่พบค่า\n"
            else:
                # ในระหว่างค้นหา จะแสดงตำแหน่งที่กำลังตรวจสอบ
                info_text += f"ตำแหน่ง: กำลังตรวจสอบ...\n"
        else:
            info_text += f"ตำแหน่ง: -\n"
        
        info_text += f"จำนวนการเปรียบเทียบ: {comparisons}\n"
        info_text += additional_info
        
        self.searching_info_text.insert(tk.END, info_text)
        self.searching_info_text.config(state=tk.DISABLED)
    
    def disable_searching_buttons(self):
        self.start_searching_button.config(state=tk.DISABLED)
        self.use_data_button.config(state=tk.DISABLED)
        self.random_search_data_button.config(state=tk.DISABLED)
        self.searching = True
        
    def enable_searching_buttons(self):
        self.start_searching_button.config(state=tk.NORMAL)
        self.use_data_button.config(state=tk.NORMAL)
        self.random_search_data_button.config(state=tk.NORMAL)
        self.searching = False

    def finish_searching_and_show_result(self, result_message_detail, is_found, final_position):
        """แสดงผลลัพธ์ใน Toplevel Window และเปิดใช้งานปุ่มอีกครั้ง"""
        self.enable_searching_buttons()
        self.update_searching_info(additional_info=result_message_detail)

        # 1. สร้างหน้าต่าง Toplevel
        result_window = tk.Toplevel(self.root)
        result_window.title(" สรุปผล: " + self.selected_searching_algorithm)
        result_window.geometry("500x300+700+150")
        result_window.configure(bg="#1e1b4b")
        result_window.resizable(False, False)
        
        # ทำให้หน้าต่างอยู่ด้านบนสุดและเป็นโมดัล (บังคับให้ปิดก่อนทำอย่างอื่น)
        result_window.transient(self.root)
        result_window.grab_set()
        
        # 2. ข้อความสรุปหลัก
        if is_found:
            main_text = "การค้นหาสำเร็จ "
            main_color = "#22c55e" # สีเขียว
            
            if self.selected_searching_algorithm == "Binary Search":
                original_indices = [i for i, x in enumerate(self.searching_data) if x == self.target_value]
                pos_info = f"ตำแหน่งในข้อมูลเรียง (Index): {final_position}\nตำแหน่งในข้อมูลต้นฉบับ (Indices): {', '.join(map(str, original_indices))}"
            else:
                pos_info = f"พบค่าที่ตำแหน่ง (Index): {final_position} "
        else:
            main_text = "ไม่พบข้อมูลที่ค้นหา "
            main_color = "#ef4444" # สีแดง
            pos_info = f"ไม่พบค่า {self.target_value}"

        tk.Label(
            result_window,
            text=main_text,
            font=("Comic Sans MS", 24, "bold"),
            bg="#1e1b4b",
            fg=main_color
        ).pack(pady=(20, 10))

        # 3. รายละเอียด
        tk.Label(
            result_window,
            text=f"อัลกอริทึม: {self.selected_searching_algorithm}",
            font=("Comic Sans MS", 16),
            bg="#1e1b4b",
            fg="white"
        ).pack(pady=5)

        tk.Label(
            result_window,
            text=pos_info,
            font=("Comic Sans MS", 16),
            bg="#1e1b4b",
            fg="white"
        ).pack(pady=5)
        
        tk.Label(
            result_window,
            text=f"จำนวนการเปรียบเทียบ: {self.comparisons}",
            font=("Comic Sans MS", 16),
            bg="#1e1b4b",
            fg="white"
        ).pack(pady=5)

        # 4. แสดงข้อมูลที่ใช้ค้นหา
        display_data = self.sorted_data if self.selected_searching_algorithm == "Binary Search" else self.searching_data
        data_label_text = f"ข้อมูลที่ใช้ค้นหา: [{', '.join(map(str, display_data))}]"
        
        tk.Label(
            result_window,
            text=data_label_text,
            font=("Comic Sans MS", 10),
            bg="#1e1b4b",
            fg="#9ca3af", # สีเทา
            wraplength=450,
            justify=tk.CENTER
        ).pack(pady=10)

        # รอจนกว่าผู้ใช้จะปิดหน้าต่างสรุปผลลัพธ์
        self.root.wait_window(result_window)

    # ==================== LOGIC METHODS (เรียกใช้ finish_searching) ====================
    
    def start_searching(self):
        """เริ่มกระบวนการค้นหา"""
        if self.searching:
            return
        
        try:
            self.target_value = int(self.target_entry.get())
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกค่าที่ต้องการค้นหาเป็นตัวเลข")
            return
        
        if not self.searching_data:
            messagebox.showwarning("คำเตือน", "กรุณาใส่ข้อมูลเพื่อทำการค้นหา")
            return
            
        if self.selected_searching_algorithm == "Binary Search":
            if self.sorted_data != sorted(self.searching_data):
                self.sorted_data = sorted(self.searching_data.copy())
                messagebox.showinfo("ข้อมูล Binary Search", "Binary Search จำเป็นต้องใช้ข้อมูลที่เรียงลำดับแล้ว\nโปรแกรมจะทำการเรียงข้อมูลโดยอัตโนมัติ")
                self.update_searching_display() 

        
        self.disable_searching_buttons()
        self.comparisons = 0
        
        if self.selected_searching_algorithm == "Sequential Search":
            self.sequential_search(0)
        elif self.selected_searching_algorithm == "Binary Search":
            self.binary_search(low=0, high=len(self.sorted_data) - 1)
    
    def sequential_search(self, current_index):
        """Sequential Search Algorithm"""
        if not self.searching:
            return
        
        if current_index < len(self.searching_data):
            self.comparisons += 1
            
            self.update_searching_display(current_index=current_index)
            self.update_searching_info(current_index, self.comparisons,
                                      f"กำลังตรวจสอบตำแหน่ง {current_index}: {self.searching_data[current_index]}")
            
            if self.searching_data[current_index] == self.target_value:
                self.update_searching_display(found_index=current_index)
                result_message = f"พบค่า {self.target_value} ที่ตำแหน่ง {current_index} (ในข้อมูลต้นฉบับ)\nจำนวนการเปรียบเทียบ: {self.comparisons}"
                self.finish_searching_and_show_result(result_message, True, current_index)
                return
            else:
                self.root.after(self.searching_speed, lambda: self.sequential_search(current_index + 1))
        else:
            self.update_searching_display()
            result_message = f"ไม่พบค่า {self.target_value} ในข้อมูล\nจำนวนการเปรียบเทียบ: {self.comparisons}"
            self.finish_searching_and_show_result(result_message, False, -1)
    
    def binary_search(self, low, high):
        """Binary Search Algorithm"""
        if not self.searching:
            return
        
        if low <= high:
            mid = (low + high) // 2
            self.comparisons += 1
            
            self.update_searching_display(low=low, high=high, mid=mid)
            self.update_searching_info(mid, self.comparisons,
                                      f"ช่วงค้นหา: [{low}, {high}]\nตำแหน่งกลาง: {mid} → ค่า: {self.sorted_data[mid]}")
            
            if self.sorted_data[mid] == self.target_value:
                # Binary Search ทำบน sorted_data
                original_indices = [i for i, x in enumerate(self.searching_data) if x == self.target_value]
                
                self.update_searching_display(found_index=mid)
                result_message = (
                    f"พบค่า {self.target_value}!\n"
                    f"ตำแหน่งในข้อมูลเรียง (Index): {mid}\n"
                    f"ตำแหน่งในข้อมูลต้นฉบับ (Indices): {', '.join(map(str, original_indices))}\n"
                    f"จำนวนการเปรียบเทียบ: {self.comparisons}"
                )
                self.finish_searching_and_show_result(result_message, True, mid)
                return
            elif self.sorted_data[mid] < self.target_value:
                self.root.after(self.searching_speed, lambda: self.binary_search(mid + 1, high))
            else:
                self.root.after(self.searching_speed, lambda: self.binary_search(low, mid - 1))
        else:
            self.update_searching_display()
            result_message = f"ไม่พบค่า {self.target_value} ในข้อมูล\nจำนวนการเปรียบเทียบ: {self.comparisons}"
            self.finish_searching_and_show_result(result_message, False, -1)


if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmsVisualizer(root)
    root.mainloop()