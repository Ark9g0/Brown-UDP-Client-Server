import socket
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread

print('UDP Server')

class UDPServer:
    def __init__(self, win):
        self.win = win
        self.win.title("UDP Server")
        self.setup_brown_theme()
        self.gui()
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_rowconfigure(0, weight=1)
        
        # Create UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 12345)  # Same port as client
        self.udp_socket.bind(self.server_address)
        
        # Start listening thread
        self.listening = True
        self.thread = Thread(target=self.receive_messages, daemon=True)
        self.thread.start()

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
        style.configure('TText', fieldbackground='#F5DEB3', foreground='#5C4033')
        
        self.win.configure(bg='#D2B48C')

    def gui(self):
        self.main_frame = ttk.Frame(self.win, padding=20)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        
        # Server status
        ttk.Label(self.main_frame, text="Server Status:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.status_label = ttk.Label(self.main_frame, text="Listening on port 12345", font=('Arial', 10, 'bold'))
        self.status_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Client address display
        ttk.Label(self.main_frame, text="Client Address:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.client_label = ttk.Label(self.main_frame, text="No client connected", font=('Arial', 10))
        self.client_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Received messages
        ttk.Label(self.main_frame, text="Received Messages:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.NW)
        self.received_text = tk.Text(self.main_frame, height=10, width=50, bg='#F5DEB3', fg='#5C4033')
        self.received_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # Response section
        ttk.Label(self.main_frame, text="Response:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.response_entry = ttk.Entry(self.main_frame, width=40)
        self.response_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Send button
        self.send_button = ttk.Button(self.main_frame, text="Send Response", command=self.send_response)
        self.send_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Store the last client address
        self.last_client = None

    def receive_messages(self):
        while self.listening:
            try:
                data, client_address = self.udp_socket.recvfrom(1024)
                self.last_client = client_address
                
                # Update GUI in main thread
                self.win.after(0, self.update_received_messages, data.decode('utf-8'), client_address)
                
            except OSError:
                break  # Socket closed

    def update_received_messages(self, message, client_address):
        self.client_label.config(text=f"{client_address[0]}:{client_address[1]}")
        self.received_text.insert(tk.END, f"Client: {message}\n")
        self.received_text.see(tk.END)

    def send_response(self):
        if self.last_client and self.response_entry.get():
            message = "Server: " + self.response_entry.get()
            try:
                self.udp_socket.sendto(message.encode('utf-8'), self.last_client)
                self.received_text.insert(tk.END, f"{message}\n")
                self.received_text.see(tk.END)
                self.response_entry.delete(0, tk.END)
            except Exception as e:
                self.received_text.insert(tk.END, f"Error sending: {str(e)}\n")
                self.received_text.see(tk.END)

    def on_closing(self):
        self.listening = False
        self.udp_socket.close()
        self.win.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    server = UDPServer(root)
    root.protocol("WM_DELETE_WINDOW", server.on_closing)
    root.mainloop()
