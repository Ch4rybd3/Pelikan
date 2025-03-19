import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageGrab, Image
import os
import subprocess
from datetime import datetime
import json
import re
from config import *
from gui import IncidentInvestigationGUI

class IncidentInvestigationApp:
    def __init__(self, root):
        self.root = root
        self.window_height = root_Frame_Size_Heigth
        self.window_width = root_Frame_Size_Length
        self.left_frame_width = left_Frame_Size_Length
        self.right_frame_width = right_Frame_Size_Length

        # Initialize the GUI
        self.gui = IncidentInvestigationGUI(root, self)

    def get_window_size(self):
        return f"{self.window_width}x{self.window_height}"

    def generate_incident_id(self):
        # Générer un GUID via PowerShell
        try:
            result = subprocess.run(["powershell", "-Command", "[guid]::NewGuid().ToString()"], capture_output=True, text=True)
            guid = result.stdout.strip()
            self.gui.incident_id.config(state="normal")
            self.gui.incident_id.delete(0, tk.END)
            self.gui.incident_id.insert(0, guid)
            self.gui.incident_id.config(state="readonly")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer l'ID : {e}")

    def add_analysis(self):
        analysis_value = self.gui.analysis_entry.get()
        if not analysis_value:
            messagebox.showwarning("Attention", "Veuillez saisir une valeur pour l'étape d'analyse technique.")
            return
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.gui.analysis_table.insert("", "end", values=(analysis_value, now))
        self.gui.analysis_entry.delete(0, tk.END)

    def add_remediate(self):
        remediate_value = self.gui.remediate_entry.get()
        if not remediate_value:
            messagebox.showwarning("Attention", "Veuillez saisir une valeur pour l'étape de remédiation.")
            return
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.gui.remediate_table.insert("", "end", values=(remediate_value, now))
        self.gui.remediate_entry.delete(0, tk.END)

    def add_ioc(self):
        ioc_value = self.gui.ioc_entry.get()
        if not ioc_value:
            messagebox.showwarning("Attention", "Veuillez saisir une valeur pour l'IOC.")
            return
        ioc_type = self.determine_ioc_type(ioc_value)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.gui.ioc_table.insert("", "end", values=(ioc_value, ioc_type, now))
        self.gui.ioc_entry.delete(0, tk.END)

    def add_system(self):
        system_value = self.gui.system_entry.get()
        if not system_value:
            messagebox.showwarning("Attention", "Veuillez saisir une valeur pour le système affecté.")
            return
        system_type = self.determine_system_type(system_value)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.gui.systems_table.insert("", "end", values=(system_value, system_type, now))
        self.gui.system_entry.delete(0, tk.END)

    def create_incident_folder(self):
        # Générer l'ID de l'incident
        self.generate_incident_id()
        # Créer un dossier pour l'incident
        title = self.gui.incident_title.get()
        if not title:
            messagebox.showwarning("Attention", "Veuillez saisir un titre pour l'incident.")
            return
        # Générer le nom du dossier au format YYYY-MM-DD_HH-MM_Titre
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")
        folder_name = f"{now}_{title}"
        incident_folder = os.path.join(incident_FolderPath, folder_name)
        try:
            os.makedirs(incident_folder, exist_ok=True)
            self.gui.collection_path.config(text=incident_folder)  # Mettre à jour le label
            messagebox.showinfo("Succès", f"Dossier créé : {incident_folder}")
            # Créer un fichier JSON pour stocker les métadonnées
            self.save_metadata()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le dossier : {e}")

    def open_existing_incident(self):
        # Ouvrir une boîte de dialogue pour sélectionner un dossier d'incident
        incident_folder = filedialog.askdirectory(
            initialdir=os.path.join(incident_FolderPath),
            title="Sélectionner un dossier d'incident"
        )
        if incident_folder:
            # Charger les métadonnées et les captures d'écran
            self.load_incident(incident_folder)

    def load_incident(self, incident_folder):
        # Charger les métadonnées depuis le fichier JSON
        metadata_file = os.path.join(incident_folder, "metadata.json")
        if not os.path.exists(metadata_file):
            messagebox.showerror("Erreur", "Fichier de métadonnées introuvable.")
            return
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        # Mettre à jour les champs avec les métadonnées
        self.gui.incident_title.delete(0, tk.END)
        self.gui.incident_title.insert(0, metadata["titre"])
        self.gui.incident_id.config(state="normal")
        self.gui.incident_id.delete(0, tk.END)
        self.gui.incident_id.insert(0, metadata["id"])
        self.gui.incident_id.config(state="readonly")
        self.gui.collection_path.config(text=metadata["localisation"])
        self.gui.criticality.set(metadata["criticité"])
        self.gui.author.delete(0, tk.END)
        self.gui.author.insert(0, metadata["auteur"])
        # Charger les étapes d'analyse technique dans la table
        for analysis in metadata["analyse_technique"]:
           self.gui.analysis_table.insert("", "end", values=(analysis["valeur"], analysis["date/heure"]))
        # Charger les étapes de remédiation dans la table
        for remediate in metadata["remédiation"]:
            self.gui.remediate_table.insert("", "end", values=(remediate["valeur"], remediate["date/heure"]))
        # Charger les captures d'écran dans la liste
        for screenshot in metadata["captures_ecran"]:
            screenshot_name = os.path.basename(screenshot["chemin"])
            self.gui.screenshots_list.insert(tk.END, screenshot_name)
        # Charger les éléments du cadre de gauche
        self.gui.syn_text.delete("1.0", tk.END)
        self.gui.syn_text.insert("1.0", metadata.get("synthèse_managériale", ""))
        for ioc in metadata["ioc_releves"]:
           self.gui.ioc_table.insert("", "end", values=(ioc["valeur"], ioc["type"], ioc["date/heure"]))
        # Charger les systèmes affectés dans la table
        for system in metadata["systems_affectes"]:
            self.gui.systems_table.insert("", "end", values=(system["valeur"], system["type"], system["date/heure"]))
        self.gui.improve_text.delete("1.0", tk.END)
        self.gui.improve_text.insert("1.0", metadata.get("axes_amélioration", ""))
        # Actualiser les captures d'écran
        self.browse_screenshots()

    def browse_screenshots(self):
        # Vérifier si le dossier de l'incident a été créé
        if not self.gui.collection_path.cget("text"):
            messagebox.showwarning("Attention", "Veuillez d'abord créer un incident.")
            return
        # Chemin du dossier de l'incident
        folder_path = self.gui.collection_path.cget("text")
        # Effacer la liste actuelle
        self.gui.screenshots_list.delete(0, tk.END)
        # Parcourir le dossier et afficher les fichiers .png
        for file in os.listdir(folder_path):
            if file.lower().endswith(".png"):
                self.gui.screenshots_list.insert(tk.END, file)

    def save_metadata(self):
        # Vérifier si un dossier d'incident est sélectionné
        if not self.gui.collection_path.cget("text"):
            messagebox.showwarning("Attention", "Aucun incident n'est ouvert.")
            return
        metadata = {
            "titre": self.gui.incident_title.get(),
            "id": self.gui.incident_id.get(),
            "localisation": self.gui.collection_path.cget("text"),
            "criticité": self.gui.criticality.get(),
            "auteur": self.gui.author.get(),
            "ioc_releves": [],  # Ajouter la liste des IOC
            "systems_affectes": [],  # Ajouter la liste des systèmes
            "captures_ecran": [], # Ajouter la liste des captures d'écran
            "synthèse_managériale": self.gui.syn_text.get("1.0", tk.END).strip(),  # Ajouter la synthèse managériale
            "analyse_technique": [], # Ajouter la liste des analyses techniques
            "remédiation": [], # Ajouter la liste des remédiations
            "axes_amélioration": self.gui.improve_text.get("1.0", tk.END).strip()  # Ajouter les axes d'amélioration
        }
        # Ajouter les étapes d'analyse technique à la liste
        for item in self.gui.analysis_table.get_children():
            values = self.gui.analysis_table.item(item, "values")
            analysis = {
                "valeur": values[0],
                "date/heure": values[1]
            }
            metadata["analyse_technique"].append(analysis)
        # Ajouter les étapes de remédiation à la liste
        for item in self.gui.remediate_table.get_children():
            values = self.gui.remediate_table.item(item, "values")
            remediate = {
                "valeur": values[0],
                "date/heure": values[1]
            }
            metadata["remédiation"].append(remediate)
        # Ajouter les IOC à la liste
        for item in self.gui.ioc_table.get_children():
            values = self.gui.ioc_table.item(item, "values")
            ioc = {
                "valeur": values[0],
               "type": values[1],
                "date/heure": values[2]
            }
            metadata["ioc_releves"].append(ioc)
        # Ajouter les systèmes affectés à la liste
        for item in self.gui.systems_table.get_children():
            values = self.gui.systems_table.item(item, "values")
            system = {
                "valeur": values[0],
                "type": values[1],
                "date/heure": values[2]
            }
            metadata["systems_affectes"].append(system)
        # Ajouter les captures d'écran à la liste
        for screenshot in self.gui.screenshots_list.get(0, tk.END):
            screenshot_info = {
                "chemin": os.path.join(self.gui.collection_path.cget("text"), screenshot),
                "date/heure": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            metadata["captures_ecran"].append(screenshot_info)
        # Enregistrer les métadonnées dans un fichier JSON
        metadata_file = os.path.join(self.gui.collection_path.cget("text"), "metadata.json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

    def open_screenshot_interface(self):
        # Vérifier si un dossier d'incident est sélectionné
        if not self.gui.collection_path.cget("text"):
            messagebox.showwarning("Attention", "Veuillez d'abord créer ou ouvrir un incident.")
            return
        # Créer une nouvelle fenêtre modale
        screenshot_window = tk.Toplevel(self.root)
        screenshot_window.title("Ajouter une capture d'écran")
        screenshot_window.geometry("400x200")
        # Champ pour le nom de la capture
        tk.Label(screenshot_window, text="Nom de la capture :").pack(pady=5)
        screenshot_name = tk.Entry(screenshot_window, width=40)
        screenshot_name.pack(pady=5)
        # Bouton pour coller la capture
        paste_button = tk.Button(screenshot_window, text="Coller la capture", command=lambda: self.paste_screenshot(screenshot_name.get(), screenshot_window))
        paste_button.pack(pady=10)
    
    def paste_screenshot(self, name, window):
        # Vérifier si un nom a été saisi
        if not name:
            messagebox.showwarning("Attention", "Veuillez saisir un nom pour la capture.")
            return
        # Chemin du dossier de l'incident
        folder_path = self.gui.collection_path.cget("text")
        # Récupérer l'image du presse-papiers
        try:
            image = ImageGrab.grabclipboard()
            if image is None:
                messagebox.showerror("Erreur", "Aucune image trouvée dans le presse-papiers.")
                return
            # Enregistrer l'image dans le dossier de l'incident
            screenshot_path = os.path.join(folder_path, f"{name}.png")
            image.save(screenshot_path, "PNG")
            # Actualiser l'affichage des captures d'écran
            self.browse_screenshots()
            # Fermer la fenêtre modale
            window.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de coller la capture : {e}")

    def determine_ioc_type(self, ioc_value):
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ioc_value):
            return "IP"
        elif re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", ioc_value):
            return "Domain"
        elif re.match(r"^https?://[^\s/$.?#].[^\s]*$", ioc_value):
            return "URL"
        elif re.match(r"^[a-fA-F0-9]{32}$", ioc_value) or re.match(r"^[a-fA-F0-9]{40}$", ioc_value) or re.match(r"^[a-fA-F0-9]{64}$", ioc_value):
            return "Hash"
        elif re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", ioc_value):
            return "Email Address"
        else:
            return "String"

    def determine_system_type(self, system_value):
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", system_value):
            return "IP"
        elif re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", system_value):
            return "Domain"
        elif re.match(r"^https?://[^\s/$.?#].[^\s]*$", system_value):
            return "URL"
        elif re.match(r"^[a-fA-F0-9]{32}$", system_value) or re.match(r"^[a-fA-F0-9]{40}$", system_value) or re.match(r"^[a-fA-F0-9]{64}$", system_value):
            return "Hash"
        elif re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", system_value):
            return "Email Address"
        else:
            return "String"

# Point d'entrée de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = IncidentInvestigationApp(root)
    root.mainloop()