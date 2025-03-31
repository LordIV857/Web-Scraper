from flask import Flask, jsonify, request
from playwright.async_api import async_playwright
from urllib.parse import urljoin
import asyncio

app = Flask(__name__)

# Fonction Playwright pour récupérer les articles dynamiquement
def filter_articles(articles, keywords, url):
    filtered_articles = []
    seen_links = set()
    
    for article in articles:
        full_link = urljoin(url, article["link"])
        if any(keyword in article["title"].lower() or keyword in full_link.lower() for keyword in keywords):
            image = urljoin(url, article["image"]) if article["image"] else None
            if full_link not in seen_links and image:
                filtered_articles.append({"title": article["title"], "link": full_link, "image": image})
                seen_links.add(full_link)
    
    return filtered_articles

# Fonction asynchrone de scraping avec Playwright
async def scrape_with_playwright(url, keywords):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Utilise Chromium en mode headless
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        
        # Essayer plusieurs structures HTML pour les articles
        articles = await page.evaluate('''() => {
            let selectors = ['article', 'div.post', 'section.article', 'div.story'];
            let extracted = [];
            
            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(el => {
                    let linkEl = el.querySelector('a[href]');
                    let imgEl = el.querySelector('img');
                    let title = linkEl ? linkEl.innerText.trim() : '';
                    let link = linkEl ? linkEl.href : '';
                    let image = imgEl ? (imgEl.dataset.src || imgEl.src || (imgEl.srcset ? imgEl.srcset.split(',')[0].split(' ')[0] : '')) : '';
                    if (link && title) {
                        extracted.push({ title, link, image });
                    }
                });
            });
            
            return extracted;
        }''')
        
        await browser.close()
        return filter_articles(articles, keywords, url)

# Endpoint de l'API pour effectuer le scraping
@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')  # URL passée en paramètre
    keywords = request.args.get('type', '').lower().split(',')  # Mots-clés passés en paramètre
    if not url:
        return jsonify({"error": "L'URL est requise"}), 400  # Si l'URL est manquante, retourner une erreur
    
    # Exécuter le scraping et retourner les résultats sous forme de JSON
    articles = asyncio.run(scrape_with_playwright(url, keywords))
    return jsonify(articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
