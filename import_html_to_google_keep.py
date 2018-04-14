"""
Retrieve links from a html file (e.g. from getpocket) and import the links as
Nots to Google Keep.
"""
from bs4 import BeautifulSoup
import click
import gkeepapi
import logging

logging.getLogger().setLevel(logging.DEBUG)


def get_urls_from_html_doc(html):
    """Retrieve links from the given html file"""
    with open(html, "r") as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc)
    for link in soup.findAll("a"):
        yield link


class GoogleKeepClient:
    def __init__(self, user, password):
        self.keep = self._keep_client(user, password)

    def _keep_client(self, uname, upass):
        keep = gkeepapi.Keep()
        ret = keep.login(uname, upass)
        assert ret is True
        return keep

    def create_note_for_links(self, title, url, dryrun=False):
        """Create Google Keep Notes for the given url"""

        # Check if the note already exists
        gnotes = self.keep.find(func=lambda x : x.title == title or x.text == url)
        if gnotes:
            logging.info(f"Skip adding title:{title}, text:{url}")
            for i in gnotes:
                logging.info(f"Found: {i}")
            return False
        elif dryrun:
            logging.debug(f"DRYRUN: (new note): title:{title}, text:{url}")
            return False
        else:
            logging.debug(f"Import new note: title:{title}, text:{url}")
            self.keep.createNote(title-title, text=url)
            return True


@click.command()
@click.argument("user")     # Google login username
@click.argument("password") # Google login password
@click.argument("html")     # HTML file containing href links to be imported to Google Keep
@click.option("--dryrun", is_flag=True, default=False, help="Dry run without adding new Notes to Google Keep")
def main(user, password, html, dryrun):
    keep_client = GoogleKeepClient(user, password)

    updated = 0
    for link in get_urls_from_html_doc(html):
        if keep_client.create_note_for_links(title=link.string, url=link.get("href"), dryrun=dryrun) is True:
            updated += 1

    logging.info(f"Total updates: {updated}")
    if updated:
        keep_client.keep.sync()


if __name__ == "__main__":
    main()
