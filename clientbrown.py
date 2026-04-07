import socket
import tkinter as tk
import tkinter.ttk as ttk

print('UDP Client')

class UDPClient:
    def __init__(self, win):
        self.win = win
        self.win.title("UDP Client")
        self.setup_brown_theme()
        self.gui()
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_rowconfigure(0, weight=1)
        
        # Create UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 12345)  # Change to your server IP and port

    def setup_brown_theme(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure brown color palette
        style.configure('.', background='#D2B48C')  # Tan background
        style.configure('TFrame', background='#D2B48C')
        style.configure('TLabel', background='#D2B48C', foreground='#5C4033')  # Dark brown text
        style.configure('TButton', background='#8B4513', foreground='white')  # SaddleBrown
        style.map('TButton', 
                 background=[('active', '#A0522D')],  # Sienna
                 foreground=[('active', 'white')])
        style.configure('TEntry', fieldbackground='#F5DEB3')  # Wheat background
        
        self.win.configure(bg='#D2B48C')

    def gui(self):
        self.main_frame = ttk.Frame(self.win, padding=20)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        
        # Message entry
        ttk.Label(self.main_frame, text="Message:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.message_entry = ttk.Entry(self.main_frame, width=40)
        self.message_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Send button
        self.send_button = ttk.Button(self.main_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Response area
        ttk.Label(self.main_frame, text="Server Response:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.response_text = tk.Text(self.main_frame, height=10, width=50, bg='#F5DEB3', fg='#5C4033')
        self.response_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(1, weight=1)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            try:
                # Send message via UDP
                self.udp_socket.sendto(message.encode('utf-8'), self.server_address)
                
                # Receive response (with timeout to prevent blocking)
                self.udp_socket.settimeout(2.0)
                data, _ = self.udp_socket.recvfrom(1024)
                
                self.response_text.insert(tk.END, f"Sent: {message}\n")
                self.response_text.insert(tk.END, f"Received: {data.decode('utf-8')}\n\n")
                self.response_text.see(tk.END)
                
            except socket.timeout:
                self.response_text.insert(tk.END, f"Sent: {message} (no response received)\n\n")
                self.response_text.see(tk.END)
            except Exception as e:
                self.response_text.insert(tk.END, f"Error: {str(e)}\n\n")
                self.response_text.see(tk.END)
            
            self.message_entry.delete(0, tk.END)

    def on_closing(self):
        self.udp_socket.close()
        self.win.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = UDPClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()