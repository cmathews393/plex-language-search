import typer
from typing import List
from plex_module import PlexService as plx

app = typer.Typer()


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
    non_english_media = searcher.find_media_without_english_audio(library_name)
    if non_english_media:
        for media in non_english_media:
            typer.echo(media)
    else:
        typer.echo("All media have English audio tracks or no media found.")


class PlexSearcher:
    def __init__(self) -> None:
        self.plex = plx()

    def find_media_without_english_audio(self, library_name: str) -> List[str]:
        non_english_media = []
        library = self.plex.library.section(library_name)
        for item in library.all():
            if item.TYPE in ["movie", "show"]:
                if not self.has_english_audio(item):
                    non_english_media.append(f"{item.TYPE.capitalize()}: {item.title}")
                if item.TYPE == "show":
                    for episode in item.episodes():
                        if not self.has_english_audio(episode):
                            non_english_media.append(
                                f"Show: {item.title} - Episode: {episode.seasonEpisode}"
                            )
        return non_english_media

    def has_english_audio(self, item) -> bool:
        for audio_track in item.audioStreams():
            if (
                audio_track.language
                and audio_track.language != "Unknown"
                and audio_track.languageCode == "eng"
            ):
                return True
        return False


if __name__ == "__init__":
    app()
