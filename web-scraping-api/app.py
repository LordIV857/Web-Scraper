from playwright.async_api import async_playwright
from urllib.parse import urljoin
import asyncio

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

# Fonction principale qui exécute le scraping
def main():
    url = input("Entrez l'URL à scraper: ")  # Demande à l'utilisateur l'URL à scraper
    keywords_input = input("Entrez les mots-clés, séparés par des virgules: ").lower()
    keywords = keywords_input.split(',')

    # Exécute la fonction de scraping et affiche les résultats
    articles = asyncio.run(scrape_with_playwright(url, keywords))
    for article in articles:
        print(f"Title: {article['title']}\nLink: {article['link']}\nImage: {article['image']}\n")

if __name__ == "__main__":
    main()