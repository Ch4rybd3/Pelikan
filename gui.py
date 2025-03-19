import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageGrab
from datetime import datetime
from config import *
import os
import re
import json

# filepath: c:/Users/fsali/Documents/vscode/Working/gui.py

class IncidentInvestigationGUI:
    def __init__(self, root, app_logic):
        self.root = root
        self.app_logic = app_logic
        self.root.title("Pelikan - Plateforme d'Investigation d'Incidents")
        self.root.geometry(app_logic.get_window_size())
        self.root.configure(bg="#f0f0f0")

        # Cadres principaux
        self.left_frame = tk.Frame(self.root, bg="#e0e0e0", width=app_logic.left_frame_width, height=app_logic.window_height)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame = tk.Frame(self.root, bg="#d0d0d0", width=app_logic.right_frame_width, height=app_logic.window_height)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Widgets
        self.create_left_widgets()
        self.create_right_widgets()

    def create_left_widgets(self):
        # Titre de la partie gauche
        left_title = tk.Label(self.left_frame, text="Rédaction et analyses", font=("Arial", 16), bg="#e0e0e0")
        left_title.pack(pady=10)

        # Synthèse managériale
        syn_frame = tk.LabelFrame(self.left_frame, text="Synthèse Managériale", bg="#e0e0e0")
        syn_frame.pack(fill=tk.X, padx=10, pady=5)
        self.syn_text = tk.Text(syn_frame, height=5, width=50)
        self.syn_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Analyse Technique (tableau)
        analysis_frame = tk.LabelFrame(self.left_frame, text="Analyse Technique effectuées", bg="#d0d0d0")
        analysis_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        self.analysis_table = ttk.Treeview(analysis_frame, columns=("Valeur", "Date/Heure"), show="headings")
        self.analysis_table.heading("Valeur", text="Valeur")
        self.analysis_table.heading("Date/Heure", text="Date/Heure")
        self.analysis_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Ajouter une étape d'analyse technique
        add_analysis_frame = tk.Frame(analysis_frame, bg="#d0d0d0")
        add_analysis_frame.pack(fill=tk.X, padx=10, pady=5)
        self.analysis_entry = tk.Entry(add_analysis_frame, width=50)
        self.analysis_entry.pack(side=tk.LEFT, padx=5, pady=5)
        add_analysis_button = tk.Button(add_analysis_frame, text="Ajouter", command=self.app_logic.add_analysis)
        add_analysis_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Remédiation (tableau)
        remediate_frame = tk.LabelFrame(self.left_frame, text="Remédiation effectuée", bg="#d0d0d0")
        remediate_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        self.remediate_table = ttk.Treeview(remediate_frame, columns=("Système", "Date/Heure"), show="headings")
        self.remediate_table.heading("Système", text="Système")
        self.remediate_table.heading("Date/Heure", text="Date/Heure")
        self.remediate_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Ajouter une étape de remédiation
        add_remediate_frame = tk.Frame(remediate_frame, bg="#d0d0d0")
        add_remediate_frame.pack(fill=tk.X, padx=10, pady=5)
        self.remediate_entry = tk.Entry(add_remediate_frame, width=50)
        self.remediate_entry.pack(side=tk.LEFT, padx=5, pady=5)
        add_remediate_button = tk.Button(add_remediate_frame, text="Ajouter", command=self.app_logic.add_remediate)
        add_remediate_button.pack(side=tk.LEFT, padx=5, pady=5)

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
        save_button = tk.Button(right_title_frame, text="Save", command=self.app_logic.save_metadata)
        save_button.pack(side=tk.RIGHT, padx=10)

        # Métadonnées de l'incident
        meta_frame = tk.LabelFrame(self.right_frame, text="Métadonnées de l'Incident", bg="#d0d0d0")
        meta_frame.pack(fill=tk.X, padx=10, pady=5)

        # Titre de l'incident
        tk.Label(meta_frame, text="Titre de l'incident :", bg="#d0d0d0").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.incident_title = tk.Entry(meta_frame, width=40)
        self.incident_title.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(meta_frame, text="Créer Incident", command=self.app_logic.create_incident_folder).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(meta_frame, text="Ouvrir Incident", command=self.app_logic.open_existing_incident).grid(row=0, column=3, padx=5, pady=5)

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
        self.criticality.current(0)

        # Auteur
        tk.Label(meta_frame, text="Auteur :", bg="#d0d0d0").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.author = tk.Entry(meta_frame, width=40)
        self.author.grid(row=4, column=1, padx=5, pady=5)
        self.author.insert(0, os.getlogin())

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
        add_ioc_button = tk.Button(add_ioc_frame, text="Ajouter", command=self.app_logic.add_ioc)
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
        add_system_button = tk.Button(add_systems_frame, text="Ajouter", command=self.app_logic.add_system)
        add_system_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Captures d'écran (explorateur de fichiers)
        screenshots_frame = tk.LabelFrame(self.right_frame, text="Captures d'Écran", bg="#d0d0d0")
        screenshots_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        self.screenshots_list = tk.Listbox(screenshots_frame)
        self.screenshots_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Bouton pour ajouter une capture d'écran
        add_screenshot_button = tk.Button(screenshots_frame, text="Ajouter une capture d'écran", command=self.app_logic.open_screenshot_interface)
        add_screenshot_button.pack(pady=5)