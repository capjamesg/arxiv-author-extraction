from bs4 import BeautifulSoup
from TexSoup import TexSoup
import requests
import re
import tarfile
from io import BytesIO
import tqdm

RSS = "https://granary.io/url?url=https://rss.arxiv.org/rss/cs.cv&output=json&input=rss"

data = requests.get(RSS)

for entry in tqdm.tqdm(data.json()["items"]):
    url = entry["url"]
    html = url.replace("/abs/", "/html/")
    paper_html = requests.get(html)
    soup = BeautifulSoup(paper_html.text, "html.parser")
    title = soup.title.string
    authors = soup.find_all("span", {"class": "ltx_contact ltx_role_affiliation"})

    if authors == []:
        authors = soup.find_all("span", {"class": "ltx_creator ltx_role_author"})
    authors = [author.get_text() for author in authors]
    authors = [author.encode('ascii', 'ignore').decode() for author in authors]
    authors = [re.sub(r'[\n\t]', '', author) for author in authors]
    authors = " ".join(authors)
    
    if "Google" in authors:
        print(title, authors)
    # src = url.replace("/abs/", "/src/")

    # data = requests.get(src)
    # tar = tarfile.open(fileobj=BytesIO(data.content))

    # tex_files = [x for x in tar.getnames() if x.endswith(".tex")]
    # tex = tar.extractfile(tex_files[0]).read().decode("utf-8")

    # soup = TexSoup(tex)
    # authors = soup.find_all("author")

    # print(authors)
