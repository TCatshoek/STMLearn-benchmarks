# Downloads the benchmarks from the radboud site
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def find_benchmark_pages(type):
    # Find the header above the benchmark links
    h3s = soup.findAll('h3')
    header = list(filter(
        lambda tag: any(map(lambda child: type in child, tag.children)),
        h3s)
    )[0]
    # Grab the benchmark links
    bench_list = header.find_next_sibling()
    bench_links = [x['href'] for x in bench_list.findAll('a')]
    return ["/".join(a.split('/')[0:-1]) for a in bench_links]

def find_download_links(link, type="Mealy"):
    download_page = f"{link}/{type}"
    r_d = requests.get(download_page)
    d_soup = BeautifulSoup(r_d.content, features="html.parser")

    # Find all dot links on this page
    links = d_soup.findAll("a", href=True)
    links = list(filter(lambda x: ".dot" in x['href'], links))

    return [x['href'] for x in links]

if __name__ == "__main__":
    base_url = "https://automata.cs.ru.nl"
    r = requests.get(f"{base_url}/Overview")
    soup = BeautifulSoup(r.content, features="html.parser")

    bps = find_benchmark_pages("Mealy")

    for bp in bps:
        # Grab the download links for the dot files
        name = bp.split('/')[-1]
        print("Downloading benchmark set:", name)
        dl_links = find_download_links(bp)

        # Create a folder if necessary
        dl_path = Path(f'benchmarks/{name}')
        dl_path.mkdir(exist_ok=True, parents=True)

        # Download the files
        for dl_link in tqdm(dl_links):
            file_name = dl_link.split("/")[-1]
            data = requests.get(dl_link)
            with dl_path.joinpath(file_name).open('wb') as file:
                file.write(data.content)







