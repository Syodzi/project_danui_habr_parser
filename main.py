from bs4 import BeautifulSoup
import requests
import json
import tkinter as tk 
import webbrowser

def parse_habr():
    article_dict = {}
    url = f'https://habr.com/ru/feed/'
    req = requests.get(url, 'lxml').text

    soup = BeautifulSoup(req, 'lxml')
    all_hrefs_articles = soup.find_all('a', class_='tm-title__link') 

    for article in all_hrefs_articles: 
        article_name = article.find('span').text
        article_link = f'https://habr.com{article.get("href")}' 
        article_dict[article_name] = article_link


    with open(f"articles.json", "w", encoding='utf-8') as f: 
        json.dump(article_dict, f, indent=4, ensure_ascii=False)
        
def show_articles():
    with open("articles.json", "r", encoding='utf-8') as f:
        article_dict = json.load(f)
        for i, (name, link) in enumerate(article_dict.items(), start=1):
            article_name_label = tk.Label(window, text=f"{i}. {name}", bg="azure4")
            article_name_label.grid(row=i, column=0, padx=5, pady=5)

            article_link_text = tk.Text(window, height=1, width=50, wrap="word", bd=0, bg="azure4")
            article_link_text.insert(tk.END, link)
            article_link_text.tag_config("link", foreground="azure4", underline=True)
            article_link_text.grid(row=i, column=1, padx=5, pady=5)

            article_link_text.bind("<Button-1>", lambda event, url=link: webbrowser.open_new(url))
            article_link_text.config(cursor="hand2")

window = tk.Tk()
window.title("Habr Parser")
window.configure(bg="azure4")

parse_button = tk.Button(window, text="Parse Habr and Show Articles", command=lambda: [parse_habr(), show_articles()])
parse_button.grid(row=0, column=0, columnspan=2, pady=10)

window.mainloop()

