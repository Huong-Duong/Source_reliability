import json, requests, re

def main():
    url_reliability = {}

    headers = {
        "User-Agent": "SourceReliabilityBot/1.0 (https://github.com/Huong-Duong)"
    }

    citehighlighter_sourcelist_url = "https://en.wikipedia.org/w/index.php?title=User:Novem_Linguae/Scripts/CiteHighlighter/SourcesJSON.js&action=raw&ctype=text/javascript"

    

    response = requests.get(citehighlighter_sourcelist_url, headers=headers)

    if response.status_code == 200:
        sl_json = response.text
        sl = json.loads(sl_json)

        for type in sl:
            for url in sl[type]:
                url_reliability[url] = type

    else:
        print(f"Error loading CiteHighlighter's list: HTTP {response.status_code}")

    viwiki_sourcelist_url = "https://vi.wikipedia.org/w/index.php?title=Wikipedia:Danh_s%C3%A1ch_ngu%E1%BB%93n_%C4%91%C3%A1ng_tin_c%E1%BA%ADy/Ti%E1%BA%BFng_Vi%E1%BB%87t&action=raw"

    response = requests.get(viwiki_sourcelist_url, headers=headers)
    
    if response.status_code == 200:
        sl_wikitext = response.text

        rows = sl_wikitext.split("|-")

        for row in rows:
            type_match = re.search(r"\{\{WP:NDTCTT\|([^|}]+)", row)

            domains_match = re.search(r"\{\{WP:NDTCSD\|([^}]+)\}\}", row)

            if type_match and domains_match:
                type = type_match.group(1).strip()

                if type == "gr":
                    color = "green"
                elif type == "nc":
                    color = "yellow"
                else: #if type == "gu" or type == "d":
                    color = "red"

                domains_raw = domains_match.group(1).split("|")

                if color == "green":
                    for domain in domains_raw:
                        if domain[-3:] == ".vn":
                            color = "yellow"
                            

                for domain in domains_raw:
                    domain = domain.strip()
                    if domain:
                        url_reliability[domain] = color

    else:
        print(f"Error loading Vietnamese Wikipedia's list: HTTP {response.status_code}")

    # VnExpress
    url_reliability["vnexpress.net"] = "yellow"

    # Znews
    url_reliability["znews.vn"] = "yellow"
    url_reliability["zingnews.vn"] = "yellow"
    url_reliability["news.zing.vn"] = "yellow"

    # Apple Music
    url_reliability["music.apple.com"] = "red"

    with open("source_reliability.json", "w", encoding="utf-8") as f:
        json.dump(url_reliability, f,  ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()