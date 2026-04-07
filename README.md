# UDP Brown Chat

A simple UDP client-server messaging application with a brown-themed GUI built using Python's Tkinter.

## Features
- **UDP Server**: Listens on `localhost:12345`, displays received messages, shows client address, and can send custom responses.
- **UDP Client**: Sends messages to the server, receives responses (with a 2-second timeout), and displays the conversation.
- **Brown Color Theme**: Warm brown/tan color palette for a classic look.
- **Multithreading**: Server uses a background thread to receive messages without blocking the GUI.

## Requirements
- Python 3.x (standard libraries only: `socket`, `tkinter`, `threading`)

## How to Run
1. Start the server:
   ```bash
   python serverbrown.py
2. Start the client:
   ```bash
   python clientbrown.py
3. Type a message in the client and click "Send". The server will show the message; type a response and click "Send Response" to reply.
