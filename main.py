import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageGrab, Image
import os
import subprocess
from datetime import datetime
import json
import re

class IncidentInvestigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Outil d'Investigation d'Incident de Sécurité")

        # Configuration de la fenêtre principale
        self.root.geometry("1200x1200")
        self.root.configure(bg="#f0f0f0")

        # Cadre principal pour diviser la fenêtre en deux parties
        self.left_frame = tk.Frame(self.root, bg="#e0e0e0", width=600, height=1200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root, bg="#d0d0d0", width=600, height=1200)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Widgets de la partie gauche
        self.create_left_widgets()

        # Widgets de la partie droite
        self.create_right_widgets()

    def create_left_widgets(self):
        # Titre de la partie gauche
        left_title = tk.Label(self.left_frame, text="Analyse et Recommandations", font=("Arial", 16), bg="#e0e0e0")
        left_title.pack(pady=10)

        # Synthèse managériale
        syn_frame = tk.LabelFrame(self.left_frame, text="Synthèse Managériale", bg="#e0e0e0")
        syn_frame.pack(fill=tk.X, padx=10, pady=5)
        self.syn_text = tk.Text(syn_frame, height=5, width=50)
        self.syn_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Analyse Technique
        tech_frame = tk.LabelFrame(self.left_frame, text="Analyse Technique", bg="#e0e0e0")
        tech_frame.pack(fill=tk.X, padx=10, pady=5)
        self.tech_text = tk.Text(tech_frame, height=10, width=50)
        self.tech_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Remédiation
        rem_frame = tk.LabelFrame(self.left_frame, text="Remédiation", bg="#e0e0e0")
        rem_frame.pack(fill=tk.X, padx=10, pady=5)
        self.rem_text = tk.Text(rem_frame, height=5, width=50)
        self.rem_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Axes d'amélioration
        improve_frame = tk.LabelFrame(self.left_frame, text="Axes d'Amélioration", bg="#e0e0e0")
        improve_frame.pack(fill=tk.X, padx=10, pady=5)
        self.improve_text = tk.Text(improve_frame, height=5, width=50)
        self.improve_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_right_widgets(self):
        # Titre de la partie droite
        right_title_frame = tk.Frame(self.right_frame, bg="#d0d0d0")
        right_title_frame.pack(fill=tk.X, pady=10)

        right_title = tk.Label(right_title_frame, text="Données de l'Incident", font=("Arial", 16), bg="#d0d0d0")
        right_title.pack(side=tk.LEFT, padx=10)

        # Bouton Save
        save_button = tk.Button(right_title_frame, text="Save", command=self.save_metadata)
        save_button.pack(side=tk.RIGHT, padx=10)

        # Métadonnées de l'incident
        meta_frame = tk.LabelFrame(self.right_frame, text="Métadonnées de l'Incident", bg="#d0d0d0")
        meta_frame.pack(fill=tk.X, padx=10, pady=5)

        # Titre de l'incident
        tk.Label(meta_frame, text="Titre de l'incident :", bg="#d0d0d0").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.incident_title = tk.Entry(meta_frame, width=40)
        self.incident_title.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(meta_frame, text="Créer Incident", command=self.create_incident_folder).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(meta_frame, text="Ouvrir Incident", command=self.open_existing_incident).grid(row=0, column=3, padx=5, pady=5)

        # ID de l'incident
        tk.Label(meta_frame, text="ID de l'incident :", bg="#d0d0d0").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.incident_id = tk.Entry(meta_frame, width=40, state="readonly")
        self.incident_id.grid(row=1, column=1, padx=5, pady=5)

        # Localisation des collectes
        tk.Label(meta_frame, text="Localisation des collectes :", bg="#d0d0d0").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.collection_path = tk.Label(meta_frame, text="", bg="#d0d0d0", anchor="w")
        self.collection_path.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Criticité
        tk.Label(meta_frame, text="Criticité :", bg="#d0d0d0").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.criticality = ttk.Combobox(meta_frame, values=["P1 (Critical)", "P2 (High)", "P3 (Medium)", "P4 (Low)"])
        self.criticality.grid(row=3, column=1, padx=5, pady=5)
        self.criticality.current(0)  # Définir la valeur par défaut

        # Auteur
        tk.Label(meta_frame, text="Auteur :", bg="#d0d0d0").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.author = tk.Entry(meta_frame, width=40)
        self.author.grid(row=4, column=1, padx=5, pady=5)
        self.author.insert(0, os.getlogin())  # Remplir par défaut avec le nom de l'utilisateur

        # IOC relevés (tableau)
        ioc_frame = tk.LabelFrame(self.right_frame, text="IOC Relevés", bg="#d0d0d0")
        ioc_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        self.ioc_table = ttk.Treeview(ioc_frame, columns=("Valeur", "Type", "Date/Heure"), show="headings")
        self.ioc_table.heading("Valeur", text="Valeur")
        self.ioc_table.heading("Type", text="Type")
        self.ioc_table.heading("Date/Heure", text="Date/Heure")
        self.ioc_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Ajouter un IOC
        add_ioc_frame = tk.Frame(ioc_frame, bg="#d0d0d0")
        add_ioc_frame.pack(fill=tk.X, padx=10, pady=5)
        self.ioc_entry = tk.Entry(add_ioc_frame, width=50)
        self.ioc_entry.pack(side=tk.LEFT, padx=5, pady=5)
        add_ioc_button = tk.Button(add_ioc_frame, text="Ajouter", command=self.add_ioc)
        add_ioc_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Systèmes affectés (tableau)
        systems_frame = tk.LabelFrame(self.right_frame, text="Systèmes Affectés", bg="#d0d0d0")
        systems_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        self.systems_table = ttk.Treeview(systems_frame, columns=("Système", "Type", "Date/Heure"), show="headings")
        self.systems_table.heading("Système", text="Système")
        self.systems_table.heading("Type", text="Type")
        self.systems_table.heading("Date/Heure", text="Date/Heure")
        self.systems_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Ajouter un Système affecté
        add_systems_frame = tk.Frame(systems_frame, bg="#d0d0d0")
        add_systems_frame.pack(fill=tk.X, padx=10, pady=5)
        self.system_entry = tk.Entry(add_systems_frame, width=50)
        self.system_entry.pack(side=tk.LEFT, padx=5, pady=5)
        add_system_button = tk.Button(add_systems_frame, text="Ajouter", command=self.add_system)
        add_system_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Captures d'écran (explorateur de fichiers)
        screenshots_frame = tk.LabelFrame(self.right_frame, text="Captures d'Écran", bg="#d0d0d0")
        screenshots_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        self.screenshots_list = tk.Listbox(screenshots_frame)
        self.screenshots_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Bouton pour ajouter une capture d'écran
        add_screenshot_button = tk.Button(screenshots_frame, text="Ajouter une capture d'écran", command=self.open_screenshot_interface)
        add_screenshot_button.pack(pady=5)

    def generate_incident_id(self):
        # Générer un GUID via PowerShell
        try:
            result = subprocess.run(["powershell", "-Command", "[guid]::NewGuid().ToString()"], capture_output=True, text=True)
            guid = result.stdout.strip()
            self.incident_id.config(state="normal")
            self.incident_id.delete(0, tk.END)
            self.incident_id.insert(0, guid)
            self.incident_id.config(state="readonly")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer l'ID : {e}")

    def create_incident_folder(self):
        # Générer l'ID de l'incident
        self.generate_incident_id()

        # Créer un dossier pour l'incident
        title = self.incident_title.get()
        if not title:
            messagebox.showwarning("Attention", "Veuillez saisir un titre pour l'incident.")
            return

        # Générer le nom du dossier au format YYYY-MM-DD_HH-MM_Titre
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")
        folder_name = f"{now}_{title}"
        incident_folder = os.path.join(os.path.expanduser("~"), "Documents", "Incidents", folder_name)

        try:
            os.makedirs(incident_folder, exist_ok=True)
            self.collection_path.config(text=incident_folder)  # Mettre à jour le label
            messagebox.showinfo("Succès", f"Dossier créé : {incident_folder}")

            # Créer un fichier JSON pour stocker les métadonnées
            self.save_metadata()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le dossier : {e}")

    def save_metadata(self):
        # Vérifier si un dossier d'incident est sélectionné
        if not self.collection_path.cget("text"):
            messagebox.showwarning("Attention", "Aucun incident n'est ouvert.")
            return
        metadata = {
            "titre": self.incident_title.get(),
            "id": self.incident_id.get(),
            "localisation": self.collection_path.cget("text"),
            "criticité": self.criticality.get(),
            "auteur": self.author.get(),
            "ioc_releves": [],  # Ajouter la liste des IOC
            "systems_affectes": [],  # Ajouter la liste des systèmes
            "captures_ecran": [], # Ajouter la liste des captures d'écran
            "synthèse_managériale": self.syn_text.get("1.0", tk.END).strip(),  # Ajouter la synthèse managériale
            "analyse_technique": self.tech_text.get("1.0", tk.END).strip(),  # Ajouter l'analyse technique
            "remédiation": self.rem_text.get("1.0", tk.END).strip(),  # Ajouter la remédiation
            "axes_amélioration": self.improve_text.get("1.0", tk.END).strip()  # Ajouter les axes d'amélioration
        }
        # Ajouter les IOC à la liste
        for item in self.ioc_table.get_children():
            values = self.ioc_table.item(item, "values")
            ioc = {
                "valeur": values[0],
               "type": values[1],
                "date/heure": values[2]
            }
            metadata["ioc_releves"].append(ioc)
        # Ajouter les systèmes affectés à la liste
        for item in self.systems_table.get_children():
            values = self.systems_table.item(item, "values")
            system = {
                "valeur": values[0],
                "type": values[1],
                "date/heure": values[2]
            }
            metadata["systems_affectes"].append(system)
        # Ajouter les captures d'écran à la liste
        for screenshot in self.screenshots_list.get(0, tk.END):
            screenshot_info = {
                "chemin": os.path.join(self.collection_path.cget("text"), screenshot),
                "date/heure": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            metadata["captures_ecran"].append(screenshot_info)
        # Enregistrer les métadonnées dans un fichier JSON
        metadata_file = os.path.join(self.collection_path.cget("text"), "metadata.json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

    def browse_screenshots(self):
        # Vérifier si le dossier de l'incident a été créé
        if not self.collection_path.cget("text"):
            messagebox.showwarning("Attention", "Veuillez d'abord créer un incident.")
            return

        # Chemin du dossier de l'incident
        folder_path = self.collection_path.cget("text")

        # Effacer la liste actuelle
        self.screenshots_list.delete(0, tk.END)

        # Parcourir le dossier et afficher les fichiers .png
        for file in os.listdir(folder_path):
            if file.lower().endswith(".png"):
                self.screenshots_list.insert(tk.END, file)

    def open_existing_incident(self):
        # Ouvrir une boîte de dialogue pour sélectionner un dossier d'incident
        incident_folder = filedialog.askdirectory(
            initialdir=os.path.join(os.path.expanduser("~"), "Documents", "Incidents"),
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
        self.incident_title.delete(0, tk.END)
        self.incident_title.insert(0, metadata["titre"])

        self.incident_id.config(state="normal")
        self.incident_id.delete(0, tk.END)
        self.incident_id.insert(0, metadata["id"])
        self.incident_id.config(state="readonly")

        self.collection_path.config(text=metadata["localisation"])

        self.criticality.set(metadata["criticité"])

        self.author.delete(0, tk.END)
        self.author.insert(0, metadata["auteur"])

        # Charger les IOC dans la table
        for ioc in metadata["ioc_releves"]:
           self.ioc_table.insert("", "end", values=(ioc["valeur"], ioc["type"], ioc["date/heure"]))

       # Charger les systèmes affectés dans la table
        for system in metadata["systems_affectes"]:
            self.systems_table.insert("", "end", values=(system["valeur"], system["type"], system["date/heure"]))

        # Charger les captures d'écran dans la liste
        for screenshot in metadata["captures_ecran"]:
            screenshot_name = os.path.basename(screenshot["chemin"])
            self.screenshots_list.insert(tk.END, screenshot_name)

       # Charger les éléments du cadre de gauche
        self.syn_text.delete("1.0", tk.END)
        self.syn_text.insert("1.0", metadata.get("synthèse_managériale", ""))

        self.tech_text.delete("1.0", tk.END)
        self.tech_text.insert("1.0", metadata.get("analyse_technique", ""))

        self.rem_text.delete("1.0", tk.END)
        self.rem_text.insert("1.0", metadata.get("remédiation", ""))

        self.improve_text.delete("1.0", tk.END)
        self.improve_text.insert("1.0", metadata.get("axes_amélioration", ""))

       # Actualiser les captures d'écran
        self.browse_screenshots()

    def open_screenshot_interface(self):
        # Vérifier si un dossier d'incident est sélectionné
        if not self.collection_path.cget("text"):
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
        folder_path = self.collection_path.cget("text")

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

    def add_ioc(self):
        ioc_value = self.ioc_entry.get()
        if not ioc_value:
            messagebox.showwarning("Attention", "Veuillez saisir une valeur pour l'IOC.")
            return

        ioc_type = self.determine_ioc_type(ioc_value)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ioc_table.insert("", "end", values=(ioc_type, ioc_value, now))
        self.ioc_entry.delete(0, tk.END)

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
        
    def add_system(self):
        system_value = self.system_entry.get()
        if not system_value:
            messagebox.showwarning("Attention", "Veuillez saisir une valeur pour le système affecté.")
            return

        system_type = self.determine_system_type(system_value)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.systems_table.insert("", "end", values=(system_type, system_value, now))
        self.system_entry.delete(0, tk.END)
    
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