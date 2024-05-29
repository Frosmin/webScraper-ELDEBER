import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import pandas as pd

def scrape_url():
    url = url_entry.get()

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Ajustar el selector según la estructura del sitio
            articles = soup.find_all('div', class_='jsx-742874305')  # Ajuste basado en la captura de pantalla

            result_text.delete('1.0', tk.END)
            for article in articles:
                title_element = article.find('a', class_='nota-link')  # Ajuste basado en la captura de pantalla
                if title_element:
                    title = title_element.text.strip()
                    link = title_element['href']
                    result_text.insert(tk.END, f"Título: {title}\nEnlace: https://eldeber.com.bo{link}\n\n")
        else:
            messagebox.showerror("Error", "No se pudo obtener el contenido de la página.")
    except requests.RequestException as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la URL: {e}")

def export_to_excel():
    text = result_text.get('1.0', tk.END)
    data = [[line.split(': ')[1] for line in item.split('\n') if line.startswith('Título') or line.startswith('Enlace')] for item in text.split('\n\n') if item.strip()]

    df = pd.DataFrame(data, columns=['Título', 'Enlace'])
    df = df.drop_duplicates(subset=['Título'])
    df.to_excel("C:/Users/Simon/Desktop/el_deber_news.xlsx", index=False)
    messagebox.showinfo("Éxito", "Los datos se han exportado correctamente a 'el_deber_news.xlsx'.")

# Crear ventana principal
root = tk.Tk()
root.title("Web Scraping de Noticias de El Deber")
root.configure(bg='gray')

# Crear y posicionar elementos en la ventana
url_label = tk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

scrape_button = tk.Button(root, text="Obtener datos", command=scrape_url, bg="blue", fg="white")
scrape_button.grid(row=0, column=2, padx=5, pady=5)

export_button = tk.Button(root, text="Exportar a Excel", command=export_to_excel, bg="green", fg="white")
export_button.grid(row=0, column=3, padx=5, pady=5)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=1, column=3, sticky='ns')

result_text = tk.scrolledtext.ScrolledText(root, width=100, height=20, wrap=tk.WORD, yscrollcommand=scrollbar.set)
result_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

scrollbar.config(command=result_text.yview)

# Ejecutar la ventana principal
root.mainloop()