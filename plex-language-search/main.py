import typer
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from plex_module import PlexService as plx

app = typer.Typer()


# Your init command remains unchanged
@app.command()
def init(
    dry_run: bool = typer.Option(
        False, help="Run the command in dry-run mode without making any changes"
    ),
):
    """
    Initializes the app.
    """
    typer.echo("Welcome to Plex Language Search.")
    if dry_run:
        typer.echo("Dry run activated. No changes will be made.")


@app.command()
def searchplex(
    library_name: str = typer.Argument(
        ..., help="The name of the Plex library to search."
    ),
):
    """
    Search Plex for media without English audio tracks.
    """
    searcher = PlexSearcher()
    print("Searching... ")
    non_english_media = searcher.find_media_without_english_audio(library_name)
    if non_english_media:
        for media in non_english_media:
            typer.echo(media)
    else:
        typer.echo("All media have English audio tracks or no media found.")


class PlexSearcher:
    def __init__(self) -> None:
        plex = plx()
        self.plex = plex.connect_plex()

    def find_media_without_english_audio(self, library_name: str) -> List[str]:
        non_english_media = []
        library = self.plex.library.section(library_name)
        items = library.all()

        # Use ThreadPoolExecutor to parallelize checks
        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = {executor.submit(self.process_item, item): item for item in items}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    non_english_media.extend(result)

        return non_english_media

    def process_item(self, item) -> List[str]:
        results = []
        if item.TYPE in ["movie", "show"]:
            if not self.has_english_audio(item):
                print(f"{item.title} added to list.")
                results.append(f"{item.TYPE.capitalize()}: {item.title}")
            if item.TYPE == "show":
                for episode in item.episodes():
                    if not self.has_english_audio(episode):
                        print(f"{episode.seasonEpisode} added to list.")
                        results.append(
                            f"Show: {item.title} - Episode: {episode.seasonEpisode}"
                        )
        return results

    def has_english_audio(self, item) -> bool:
        for audio_track in item.audioStreams():
            if (
                audio_track.languageCode in ["eng", "en", "jp", "ja"]
                or "Unknown" in audio_track.language
            ):
                return True
        return False


if __name__ == "__main__":
    app()
