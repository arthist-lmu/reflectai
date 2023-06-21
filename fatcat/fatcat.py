import requests
import json
import pprint as pp
import time
from bs4 import BeautifulSoup
import re
from journals.list_google import journals_list_google
from journals.list_wd_query import query_journals

import csv



def scrape_container_archive(container_id):
    container_id = "jgycezv425g3noofwb2asxefwi"
    base_url = "https://fatcat.wiki/container/" + container_id + "/browse"
    bright_releases = []
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'browse?year=' in href and "&" not in href:
            urls.append(href)

    for url in urls:
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
                            row = [link_in_td['href'].replace("/release/", ""), get_archive_link(links_in_td)]
                            bright_releases.append(row)
    return bright_releases

def get_archive_link(links):
    for link in links:
        if 'web.archive.org' in link['href']:
            return link['href']
  
def get_bright_releases(container_id):
    bright_releases = []
    for x in range(0,100000,40):
        base_url = "https://search.fatcat.wiki/fatcat_release/_search?q=preservation:bright+AND+container_id:" + container_id + "&size=40&from=" + str(x)
        r = requests.get(base_url)
        content = json.loads(r.content)
        if len(content["hits"]["hits"]) > 0:
            for hit in content["hits"]["hits"]: 
                #print(hit)
                try:
                    row = [hit["_id"], hit["_source"]["doi"], hit["_source"]["release_year"], hit["_source"]["language"], hit["_source"]["country_code"], hit["_source"]["ia_pdf_url"], hit["_source"]["title"]]
                    bright_releases.append(row)
                except:
                    print("some key error")
        else:
            break
        time.sleep(0.1)
    return bright_releases

def qid_to_fatcat_id(qid):
    try:
        url = "https://api.fatcat.wiki/v0/container/lookup?wikidata_qid=" + qid
        r = requests.get(url)
        json_content = json.loads(r.content)
        container_id = json_content["ident"]
        return container_id
    except:
        print("well that didn't work")
        return None

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

    writer = csv.writer(open("wd_query_list_download_links.csv", 'w'))
    #query_journals
    for i, journal in enumerate(query_journals):
        #if i > 1:
        #    break
        print("processing journal number: " + str(i) + " qid: " + journal)
        fatcat_id = qid_to_fatcat_id(journal)
        if fatcat_id is not None:
            bright_releases = get_bright_releases(fatcat_id)
            for row in bright_releases:
                writer.writerow(row)

    
    #bright_archives = scrape_container_archive("erffsf")
    #print(bright_archives)
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

