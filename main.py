import httpx
import feedparser

base_url = "https://www.magiccars.com/collections/all.atom"
current_url = base_url
all_entries = []
count = 0

while current_url and count < 10:
    # Fetch the current feed
    response = httpx.get(current_url)
    feed = feedparser.parse(response.content)

    # Add entries from the current page
    all_entries.extend(feed.entries)
    print(f"Fetched {len(feed.entries)} entries from {current_url}")
    print(response.content)

    # Find the "next" link for pagination
    next_link = None
    for link in feed.feed.get('links', []):
        if link.get('rel') == 'next':
            next_link = link.get('href')
            break

    # Move to the next page or exit if no more pages
    current_url = next_link
    count += 1

print(f"Total entries fetched: {len(all_entries)}")