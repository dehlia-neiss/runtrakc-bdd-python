import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import csv
from tkinter import filedialog
import matplotlib.pyplot as plt

def show_pie_chart():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT category.nom, COUNT(*) FROM product JOIN category ON product.id_category = category.id GROUP BY category.nom")
    data = cursor.fetchall()
    conn.close()

    labels, sizes = zip(*data)

    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Répartition des produits par catégorie")
    plt.show()

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"])

        for row_id in tree.get_children():
            writer.writerow(tree.item(row_id)["values"])

    messagebox.showinfo("Succès", "Produits exportés en CSV avec succès !")

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Adeletdehlia21!",
        database="store"
    )

def load_categories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM category")
    categories = cursor.fetchall()
    conn.close()

    # Remplir la liste des catégories dans le combobox
    category_filter["values"] = [f"{cat[0]} - {cat[1]}" for cat in categories]

    # Sélectionner la première catégorie par défaut
    if categories:
        category_filter.current(0)

def filter_products():
    selected_category = category_filter.get().split(" - ")[0]

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product.id, product.nom, product.description, product.price, product.quantity, category.nom 
        FROM product 
        JOIN category ON product.id_category = category.id
        WHERE product.id_category = %s
    """, (selected_category,))

    for product in cursor.fetchall():
        tree.insert("", "end", values=product)

    conn.close()

def load_products():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product.id, product.nom, product.description, product.price, product.quantity, category.nom 
        FROM product 
        JOIN category ON product.id_category = category.id
    """)

    for product in cursor.fetchall():
        tree.insert("", "end", values=product)

    conn.close()

def add_product():
    nom = entry_nom.get()
    description = entry_desc.get()
    price = entry_price.get()
    quantity = entry_qty.get()
    category_id = entry_category.get()

    if not nom or not description or not price.isdigit() or not quantity.isdigit() or not category_id.isdigit():
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO product (nom, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)",
                   (nom, description, int(price), int(quantity), int(category_id)))
    conn.commit()
    conn.close()

    load_products()
    messagebox.showinfo("Succès", "Produit ajouté avec succès !")

def load_selected_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Attention", "Veuillez sélectionner un produit à modifier.")
        return

    global selected_product_id
    item = tree.item(selected_item, "values")

    selected_product_id = item[0]
    entry_nom.delete(0, tk.END)
    entry_nom.insert(0, item[1])
    entry_desc.delete(0, tk.END)
    entry_desc.insert(0, item[2])
    entry_price.delete(0, tk.END)
    entry_price.insert(0, item[3])
    entry_qty.delete(0, tk.END)
    entry_qty.insert(0, item[4])
    entry_category.delete(0, tk.END)
    entry_category.insert(0, item[5])

    btn_update["state"] = "normal"

def update_product():
    if not selected_product_id:
        messagebox.showwarning("Attention", "Aucun produit sélectionné.")
        return

    nom = entry_nom.get()
    description = entry_desc.get()
    price = entry_price.get()
    quantity = entry_qty.get()
    category_id = entry_category.get()

    if not nom or not description or not price.isdigit() or not quantity.isdigit() or not category_id.isdigit():
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE product SET nom=%s, description=%s, price=%s, quantity=%s, id_category=%s WHERE id=%s
    """, (nom, description, int(price), int(quantity), int(category_id), selected_product_id))
    conn.commit()
    conn.close()

    load_products()
    messagebox.showinfo("Succès", "Produit modifié avec succès !")

def show_context_menu(event):
    selected_item = tree.identify_row(event.y)
    if selected_item:
        tree.selection_set(selected_item)
        context_menu.post(event.x_root, event.y_root)

def delete_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Attention", "Veuillez sélectionner un produit à supprimer.")
        return

    item = tree.item(selected_item, "values")
    product_id = item[0]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM product WHERE id=%s", (product_id,))
    conn.commit()
    conn.close()

    load_products()
    messagebox.showinfo("Succès", "Produit supprimé avec succès !")

root = tk.Tk()
root.title("Gestion des Produits")

frame_form = tk.Frame(root)
frame_form.pack()

tk.Label(frame_form, text="Nom").grid(row=0, column=0)
entry_nom = tk.Entry(frame_form)
entry_nom.grid(row=0, column=1)

tk.Label(frame_form, text="Description").grid(row=1, column=0)
entry_desc = tk.Entry(frame_form)
entry_desc.grid(row=1, column=1)

tk.Label(frame_form, text="Prix").grid(row=2, column=0)
entry_price = tk.Entry(frame_form)
entry_price.grid(row=2, column=1)

tk.Label(frame_form, text="Quantité").grid(row=3, column=0)
entry_qty = tk.Entry(frame_form)
entry_qty.grid(row=3, column=1)

tk.Label(frame_form, text="ID Catégorie").grid(row=4, column=0)
entry_category = tk.Entry(frame_form)
entry_category.grid(row=4, column=1)

btn_add = tk.Button(frame_form, text="Ajouter", command=add_product)
btn_add.grid(row=5, column=0, columnspan=2)

btn_update = tk.Button(frame_form, text="Modifier", command=update_product, state="disabled")
btn_update.grid(row=6, column=0, columnspan=2)

btn_chart = tk.Button(root, text="Afficher graphique", command=show_pie_chart)
btn_chart.pack(pady=10)

btn_export = tk.Button(root, text="Exporter en CSV", command=export_to_csv)
btn_export.pack(pady=10)

# Combobox pour le filtre des catégories
category_filter = ttk.Combobox(root)
category_filter.pack(pady=10)
category_filter.bind("<<ComboboxSelected>>", lambda event: filter_products())

# Charger les catégories dès le démarrage
load_categories()

tree = ttk.Treeview(root, columns=("ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nom", text="Nom")
tree.heading("Description", text="Description")
tree.heading("Prix", text="Prix")
tree.heading("Quantité", text="Quantité")
tree.heading("Catégorie", text="Catégorie")
tree.pack()

tree.bind("<Button-3>", show_context_menu)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Modifier", command=load_selected_product)
context_menu.add_command(label="Supprimer", command=delete_product)

load_products()

root.mainloop()
