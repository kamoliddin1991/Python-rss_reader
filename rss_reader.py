
import argparse
import json
import feedparser


def print_console_output(channel_info, items):
    print(f"Feed: {channel_info['title']}")
    print(f"Link: {channel_info['link']}")
    print(f"Description: {channel_info['description']}")
    print(f"Last Build Date: {channel_info['lastBuildDate']}")
    print(f"Publish Date: {channel_info['pubDate']}")
    print(f"Language: {channel_info['language']}")
    if channel_info['categories']:
        print(f"Categories: {', '.join(tag['term'] for tag in channel_info['categories'])}")

    if channel_info['managingEditor']:
        print(f"Managing Editor: {channel_info['managingEditor']}")

    for item in items:
        print("\nTitle: " + item['title'])
        print("Published: " + item['pubDate'])
        print("Link: " + item['link'])
        if item['category']:
            print("Categories: " + ', '.join(tag['term'] for tag in item['category']))
        print("\n".join(["Description: " + line for line in item['description'].split('\n')]))
        print('-' * 30)


def generate_json_output(channel_info, items):
    output_data = {
        'title': channel_info['title'],
        'link': channel_info['link'],
        'description': channel_info['description'],
        'items': [
            {
                'title': item['title'],
                'pubDate': item['pubDate'],
                'link': item['link'],
                'description': item['description']
            }
            for item in items
        ]
    }
    return json.dumps(output_data, indent=2)


class RSSReader:
    def __init__(self, url, limit=None):
        self.url = url
        self.limit = limit

    def parse_rss(self):
        feed = feedparser.parse(self.url)
        channel_info = {
            'title': feed.feed.get('title', ''),
            'link': feed.feed.get('link', ''),
            'description': feed.feed.get('description', ''),
            'lastBuildDate': feed.feed.get('date', ''),
            'pubDate': feed.feed.get('published', ''),
            'language': feed.feed.get('language', ''),
            'categories': feed.feed.get('tags', []),
            'managingEditor': feed.feed.get('managingEditor', '')
        }

        items = []
        for entry in feed.entries[:self.limit]:
            item_info = {
                'title': entry.get('title', 'Some Other Title'),
                'author': entry.get('author', ''),
                'pubDate': entry.get('published', 'Sun, 20 Oct 2019 04:21:44 +0300'),
                'link': entry.get('link', 'https://www.example.com'),
                'category': entry.get('tags', []),
                'description': entry.get('summary', '')
            }
            items.append(item_info)

        return channel_info, items


def main():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument('source', help='RSS URL')
    parser.add_argument('--json', action='store_true', help="Print result as JSON in stdout")
    parser.add_argument('--limit', type=int, help="Limit news topics if this parameter is provided")

    args = parser.parse_args()

    rss_reader = RSSReader(url='https://www.example.com/rss', limit=args.limit)
    channel_info, items = rss_reader.parse_rss()

    if args.json:
        json_output = generate_json_output(channel_info, items)
        print(json_output)
    else:
        print_console_output(channel_info, items)


if __name__ == "__main__":
    main()
