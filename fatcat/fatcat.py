import requests
import json
import pprint as pp
import time
from bs4 import BeautifulSoup
import re



def scrape_container_archive(container_id):
    # alternatively:
    # https://search.fatcat.wiki/fatcat_release/_search?q=preservation:bright+AND+container_id:%22jgycezv425g3noofwb2asxefwi%22
    container_id = "jgycezv425g3noofwb2asxefwi"
    base_url = "https://fatcat.wiki/container/" + container_id + "/browse"
    bright_archives = []
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'browse?year=' in href and "&" not in href:
            urls.append(href)

    for url in urls:
        print(url)
        response = requests.get("https://fatcat.wiki/" + url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tds = soup.find_all('td')

        for td in tds:
            links = td.find_all('a')
            for link in links:
                if link.text == "bright archive":
                    links_in_td = td.find_all('a', href=True)
                    for link_in_td in links_in_td:
                        if '/release/' in link_in_td['href']:
                            print(link_in_td['href'].replace("/release/", ""))
                            bright_archives.append(link_in_td['href'].replace("/release/", ""))

    return bright_archives
  
    

def lookup_containers(glist):
    bright_total = 0
    dark_total = 0
    no_total = 0
    for qitem in glist:
        try:
            url = "https://api.fatcat.wiki/v0/container/lookup?wikidata_qid=" + qitem
            r = requests.get(url)
            json_content = json.loads(r.content)
            container_id = json_content["ident"]
            stats = container_stats(container_id)
            bright_total += stats[0]
            dark_total += stats[1]
            no_total += stats[2]
        except:
            print("well that didn't work")
    print(bright_total)
    print(dark_total)
    print(no_total)

def download_container_contents(id):
    r = requests.get("https://fatcat.wiki/container/jgycezv425g3noofwb2asxefwi/browse?year=2022&volume=45&issue=")

def download_containter_stats(id):
    r = requests.get("https://fatcat.wiki/container/jgycezv425g3noofwb2asxefwi")
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        column = soup.select("td:nth-child(1)")[2]
        #print(column)
        table = column.find_all(class_="right aligned")
        print(table[2].text)
        bright_raw = re.findall('(\d,\,)+',table[0].text)
        print(bright_raw)
        dark_raw = table[1]
        no_raw = table[2]
        #print(re.findall('\d+,*', column.text ))
        #total = int(soup.select("td:nth-child(2)")[0].text.replace('\n', '').replace(' ', '').replace(',', ''))
        #bright = int(soup.select("td:nth-child(3)")[0].text.replace('\n', '').replace(' ', '').replace(',', ''))

def container_stats(id):
    r = requests.get("https://fatcat.wiki/container/" + str(id) + "/preservation_by_year.json")
    if r.status_code == 200:
        response_list = r.json()["histogram"]
        bright = 0
        dark = 0
        no = 0
        for item in response_list:
            if "bright" in item:
                bright += item["bright"]
            if "dark" in item:
                dark += item["dark"]
            if "no" in item:
                no += item["no"]
        return [bright, dark, no]

if __name__ == "__main__":
    bright_archives = scrape_container_archive("erffsf")
    print(bright_archives)
    exit()


    # ISSN-L list of journals to request
    example_journals_list = [
        "0141-6790",
    ]
    lookup_containers(query_journals)

    exit()


    for issnl in example_journals_list:
        r = requests.get("https://api.fatcat.wiki/v0/container/lookup?issnl=" + issnl)
        json_content = json.loads(r.content)
        container_id = json_content["ident"]
        container_stats(container_id)
        #download_container_contents(container_id)


    exit()


    #r = requests.get("https://api.fatcat.wiki/v0/release/llihudpl6zgq7pwpz2bnmauega?expand=container,creators,files,filesets,webcaptures")
    r = requests.get("https://api.fatcat.wiki/v0/release/llihudpl6zgq7pwpz2bnmauega?expand=files")
    release = json.loads(r.content)
    archiveorg_url = release["files"][0]["urls"][1]["url"]
    print(archiveorg_url)
    print(json.dumps(release, indent=4))


    r = requests.get(archiveorg_url)
    with open('test/test.pdf', 'wb') as f:
        f.write(r.content)

    exit()

