import click


YEAR_LIST_FILE = '../../year_list.txt'
OUTPUT_DIRECTORY = '../../output'


@click.command()
def cli():
    """ List songs by year. """
    # NOTE: list, AND generate the year_list.txt file

    # file = open(YEAR_LIST_FILE, 'r')
    #
    # for file in os.listdir(OUTPUT_DIRECTORY):
    #     song_name = os.path.splitext(file)[0]
    #     for date, name in dates:
    #         if name == song_name:
    #             song_date = date
    #     print song
