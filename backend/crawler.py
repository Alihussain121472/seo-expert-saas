import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_page(url: str):
    """
    Crawls a single page and extracts basic SEO metrics:
    - Title
    - Meta Description
    - H1, H2 tags
    - Word count
    - Internal and External links count
    - Images without alt text
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html_content = response.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. Title
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else None
        
        # 2. Meta Description
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_desc_tag['content'].strip() if meta_desc_tag and 'content' in meta_desc_tag.attrs else None
        
        # 3. Headings
        h1_tags = [h1.text.strip() for h1 in soup.find_all('h1')]
        h2_tags = [h2.text.strip() for h2 in soup.find_all('h2')]
        
        # 4. Word count (basic approximation)
        text_content = soup.get_text(separator=' ')
        word_count = len(text_content.split())
        
        # 5. Links analysis
        internal_links = 0
        external_links = 0
        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            parsed_href = urlparse(href)
            if not parsed_href.netloc or parsed_href.netloc == base_domain:
                internal_links += 1
            else:
                external_links += 1
                
        # 6. Images analysis
        images = soup.find_all('img')
        images_missing_alt = sum(1 for img in images if not img.get('alt'))
        
        return {
            "url": url,
            "status_code": response.status_code,
            "title": title,
            "title_length": len(title) if title else 0,
            "meta_description": meta_description,
            "meta_description_length": len(meta_description) if meta_description else 0,
            "h1_count": len(h1_tags),
            "h1_content": h1_tags,
            "h2_count": len(h2_tags),
            "word_count": word_count,
            "internal_links": internal_links,
            "external_links": external_links,
            "total_images": len(images),
            "images_missing_alt": images_missing_alt
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test crawler
    print(crawl_page("https://example.com"))
