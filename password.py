import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        window_width = 600
        window_height = 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.passwords = {}
        self.current_file = "passwords.json"
        
        if os.path.exists(self.current_file):
            self.load_passwords()
        
        self.label = tk.Label(self.master, text="Password Manager", font=("Helvetica", 20), fg="blue")
        self.label.pack(pady=10)
        
        self.site_label = tk.Label(self.master, text="Site/App Name:", font=("Helvetica", 12))
        self.site_label.pack()
        
        self.site_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.site_entry.pack()
        
        self.username_label = tk.Label(self.master, text="Username:", font=("Helvetica", 12))
        self.username_label.pack()
        
        self.username_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.username_entry.pack()
        
        self.password_label = tk.Label(self.master, text="Password:", font=("Helvetica", 12))
        self.password_label.pack()
        
        self.password_entry = tk.Entry(self.master, show="*", font=("Helvetica", 12))
        self.password_entry.pack()
        
        self.save_button = tk.Button(self.master, text="Save Password", command=self.save_password, font=("Helvetica", 12), bg="green", fg="white")
        self.save_button.pack(pady=5)
        
        self.retrieve_button = tk.Button(self.master, text="Retrieve Password", command=self.retrieve_password, font=("Helvetica", 12), bg="orange", fg="white")
        self.retrieve_button.pack(pady=5)
        
        self.view_button = tk.Button(self.master, text="View Passwords", command=self.view_passwords, font=("Helvetica", 12), bg="purple", fg="white")
        self.view_button.pack(pady=5)
        
    def save_password(self):
        site = self.site_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if site and username and password:
            self.passwords[site] = {"username": username, "password": password}
            self.save_passwords()
            messagebox.showinfo("Success", "Password saved successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
        
    def retrieve_password(self):
        site = self.site_entry.get()
        if site in self.passwords:
            username = self.passwords[site]["username"]
            password = self.passwords[site]["password"]
            messagebox.showinfo("Password Details", f"Site/App: {site}\nUsername: {username}\nPassword: {password}")
        else:
            messagebox.showerror("Error", "Password not found for this site.")
    
    def view_passwords(self):
        passwords_window = tk.Toplevel(self.master)
        passwords_window.title("Saved Passwords")
        
        window_width = 600
        window_height = 400
        x = (self.master.winfo_screenwidth() - window_width) // 2
        y = (self.master.winfo_screenheight() - window_height) // 2
        passwords_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        tree = ttk.Treeview(passwords_window, columns=("Site/App", "Username", "Password"), show="headings")
        tree.heading("#1", text="Site/App")
        tree.heading("#2", text="Username")
        tree.heading("#3", text="Password")
        
        for site, details in self.passwords.items():
            tree.insert("", "end", values=(site, details["username"], details["password"]))
        
        tree.pack(expand=True, fill="both")
        
        delete_button = tk.Button(passwords_window, text="Delete Password", command=lambda: self.delete_password(tree))
        delete_button.pack(pady=5)
        
        refresh_button = tk.Button(passwords_window, text="Refresh", command=self.load_passwords)
        refresh_button.pack(pady=5)
        
    def delete_password(self, tree):
        selected_item = tree.selection()[0]
        site = tree.item(selected_item)["values"][0]
        del self.passwords[site]
        self.save_passwords()
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Password deleted successfully!")
    
    def save_passwords(self):
        with open(self.current_file, "w") as f:
            json.dump(self.passwords, f)
    
    def load_passwords(self):
        with open(self.current_file, "r") as f:
            self.passwords = json.load(f)

def main():
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
