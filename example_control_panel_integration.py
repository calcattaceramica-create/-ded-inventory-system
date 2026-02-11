"""
Example: How to integrate License Control into DED Control Panel
مثال: كيفية دمج التحكم في التراخيص في DED Control Panel
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.insert(0, 'C:/Users/DELL/Desktop/DED_Portable_App')
from license_control import LicenseControl

class LicenseControlDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("License Control Demo - مثال التحكم في التراخيص")
        self.root.geometry("900x600")
        
        # Initialize license control
        self.lc = LicenseControl()
        
        # Create UI
        self.create_ui()
        
        # Load licenses
        self.refresh_licenses()
    
    def create_ui(self):
        """Create user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#6c5ce7', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="🔐 مدير التراخيص - License Manager",
            font=('Arial', 18, 'bold'),
            bg='#6c5ce7',
            fg='white'
        ).pack(pady=20)
        
        # Refresh button
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="🔄 تحديث - Refresh",
            command=self.refresh_licenses,
            bg='#0984e3',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        ).pack()
        
        # Licenses list
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Canvas for licenses
        self.canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.canvas.yview)
        
        # Frame inside canvas
        self.licenses_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.licenses_frame, anchor='nw')
        
        # Bind canvas resize
        self.licenses_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
    
    def refresh_licenses(self):
        """Refresh licenses list"""
        # Clear existing widgets
        for widget in self.licenses_frame.winfo_children():
            widget.destroy()
        
        # Get licenses
        licenses = self.lc.get_all_licenses()
        
        # Display each license
        for i, lic in enumerate(licenses):
            self.create_license_card(lic, i)
    
    def create_license_card(self, lic, index):
        """Create a card for each license"""
        # Card frame
        card = tk.Frame(
            self.licenses_frame,
            bg='#2d3436',
            relief='raised',
            borderwidth=2
        )
        card.pack(fill='x', padx=10, pady=5)
        
        # Header
        header = tk.Frame(card, bg='#2d3436')
        header.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            header,
            text=f"🔑 {lic['license_key']}",
            font=('Arial', 12, 'bold'),
            bg='#2d3436',
            fg='white'
        ).pack(side='left')
        
        # Status badges
        status_frame = tk.Frame(header, bg='#2d3436')
        status_frame.pack(side='right')
        
        if lic['is_active']:
            tk.Label(
                status_frame,
                text="✅ نشط",
                bg='#00b894',
                fg='white',
                padx=10,
                pady=2
            ).pack(side='left', padx=2)
        else:
            tk.Label(
                status_frame,
                text="❌ غير نشط",
                bg='#d63031',
                fg='white',
                padx=10,
                pady=2
            ).pack(side='left', padx=2)
        
        if lic['is_suspended']:
            tk.Label(
                status_frame,
                text="⚠️ موقوف",
                bg='#fdcb6e',
                fg='black',
                padx=10,
                pady=2
            ).pack(side='left', padx=2)
        
        # Info
        info_frame = tk.Frame(card, bg='#2d3436')
        info_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            info_frame,
            text=f"👤 {lic['client_name']} | 🏢 {lic['client_company']} | 📅 {lic['expires_at']}",
            bg='#2d3436',
            fg='#dfe6e9'
        ).pack(side='left')
        
        # Buttons
        btn_frame = tk.Frame(card, bg='#2d3436')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        # Activate button
        tk.Button(
            btn_frame,
            text="✅ تفعيل",
            command=lambda: self.activate_license(lic['license_key']),
            bg='#00b894',
            fg='white',
            padx=10,
            pady=5
        ).pack(side='left', padx=2)
        
        # Suspend button
        tk.Button(
            btn_frame,
            text="⏸️ إيقاف",
            command=lambda: self.suspend_license(lic['license_key']),
            bg='#fdcb6e',
            fg='black',
            padx=10,
            pady=5
        ).pack(side='left', padx=2)
        
        # Extend button
        tk.Button(
            btn_frame,
            text="📅 تمديد 30 يوم",
            command=lambda: self.extend_license(lic['license_key'], 30),
            bg='#0984e3',
            fg='white',
            padx=10,
            pady=5
        ).pack(side='left', padx=2)
        
        # Extend 60 days button
        tk.Button(
            btn_frame,
            text="📅 تمديد 60 يوم",
            command=lambda: self.extend_license(lic['license_key'], 60),
            bg='#6c5ce7',
            fg='white',
            padx=10,
            pady=5
        ).pack(side='left', padx=2)
    
    def activate_license(self, license_key):
        """Activate a license"""
        success, message = self.lc.activate_license(license_key)
        if success:
            messagebox.showinfo("نجح - Success", message)
            self.refresh_licenses()
        else:
            messagebox.showerror("خطأ - Error", message)
    
    def suspend_license(self, license_key):
        """Suspend a license"""
        reason = "تم الإيقاف من لوحة التحكم"
        success, message = self.lc.suspend_license(license_key, reason)
        if success:
            messagebox.showinfo("نجح - Success", message)
            self.refresh_licenses()
        else:
            messagebox.showerror("خطأ - Error", message)
    
    def extend_license(self, license_key, days):
        """Extend a license"""
        success, message = self.lc.extend_license(license_key, days)
        if success:
            messagebox.showinfo("نجح - Success", message)
            self.refresh_licenses()
        else:
            messagebox.showerror("خطأ - Error", message)

if __name__ == '__main__':
    root = tk.Tk()
    app = LicenseControlDemo(root)
    root.mainloop()

