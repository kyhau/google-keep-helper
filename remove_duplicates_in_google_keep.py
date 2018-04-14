"""
Remote notes which are the same in Google Keep.
"""
import click
import gkeepapi
import logging

logging.getLogger().setLevel(logging.DEBUG)


class GoogleKeepClient:
    def __init__(self, user, password):
        self.keep = self._keep_client(user, password)

    def _keep_client(self, uname, upass):
        keep = gkeepapi.Keep()
        ret = keep.login(uname, upass)
        assert ret is True
        return keep

    def find_and_remove_duplicates(self, dryrun=False):
        distinct_note_dict = {}
        deleted = 0

        gnotes = self.keep.all()
        for n in gnotes:
            key = n.title if n.title else n.text
            if key in distinct_note_dict.keys():
                if n.text == distinct_note_dict[key]:
                    logging.info(f"Found duplicate: {n.title} : {n.text}")
                    if dryrun is False:
                        n.delete()
                        deleted += 1
            else:
                distinct_note_dict[key] = n.text

        if deleted:
            self.keep.sync()
            logging.info(f"Total deleted: {deleted}")


@click.command()
@click.argument("user")     # Google login username
@click.argument("password") # Google login password
@click.option("--dryrun", is_flag=True, default=False, help="Dry run without adding new Notes to Google Keep")
def main(user, password, dryrun):
    keep_client = GoogleKeepClient(user, password)
    keep_client.find_and_remove_duplicates(dryrun)

if __name__ == "__main__":
    main()
