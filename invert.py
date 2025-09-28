import mido
import tkinter as tk
from tkinter import filedialog, messagebox
from mido import MidiFile, MidiTrack, Message
import os

def get_note_range(mid):
    notes = []
    for track in mid.tracks:
        for msg in track:
            if msg.type in ['note_on', 'note_off']:
                notes.append(msg.note)
    if not notes:
        return 60, 60
    return min(notes), max(notes)

def invert_note(note, center):
    return center - (note - center)

def invert_midi_auto_center(input_path, output_path):
    try:
        mid = MidiFile(input_path)
        inverted_mid = MidiFile()
        inverted_mid.ticks_per_beat = mid.ticks_per_beat

        low, high = get_note_range(mid)
        center_note = (low + high) // 2

        for track in mid.tracks:
            new_track = MidiTrack()
            for msg in track:
                if msg.type in ['note_on', 'note_off']:
                    inverted = invert_note(msg.note, center_note)
                    inverted = max(0, min(127, inverted))
                    new_msg = msg.copy(note=inverted)
                    new_track.append(new_msg)
                else:
                    new_track.append(msg)
            inverted_mid.tracks.append(new_track)

        inverted_mid.save(output_path)
        return True, f"Inverted MIDI saved to:\n{output_path}"

    except Exception as e:
        return False, f"Error: {str(e)}"

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def run_inversion():
    input_path = input_entry.get()
    if not os.path.isfile(input_path):
        messagebox.showerror("File Error", "Invalid input file.")
        return

    base = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(os.path.dirname(input_path), f"{base}_inverted.mid")

    success, msg = invert_midi_auto_center(input_path, output_path)
    if success:
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showerror("Error", msg)

# === GUI Setup ===
root = tk.Tk()
root.title("MIDI Inverter (Auto-Centered)")
root.geometry("500x150")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="Choose a MIDI file to invert:").pack(anchor='w')
input_entry = tk.Entry(frame, width=60)
input_entry.pack(side=tk.LEFT, padx=5, pady=5, expand=True)
browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=5)

invert_button = tk.Button(root, text="Invert Harmony", command=run_inversion, bg="#4CAF50", fg="white", height=2)
invert_button.pack(pady=10, fill=tk.X)

root.mainloop()
