from textual import on
from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Label, Header, Footer, ProgressBar
import soco

TESTING = False

class URLItem(ListItem):
    def __init__(self, title: str, url: str) -> None:
        super().__init__()
        self.title = title
        self.url = url

    def compose(self) -> ComposeResult:
        yield Label(self.title)


class SocoTextualRemote(App[None]):

    def compose(self) -> ComposeResult:
        yield Label("Chosen will go here", id="result")
        yield ListView(
            URLItem("SR P1", "x-rincon-mp3radio://https://http-live.sr.se/p1-mp3-192"),
            URLItem("SR P2", "x-rincon-mp3radio://https://http-live.sr.se/p2-mp3-192"),
            URLItem("SR P3", "x-rincon-mp3radio://https://http-live.sr.se/p3-mp3-192"),
            URLItem("FM4", "x-rincon-mp3radio://https://orf-live.ors-shoutcast.at/fm4-q2a"),
        )
        yield ProgressBar(total=100, show_eta=False)
        yield Header()
        yield Footer()

    BINDINGS = [("s", "stop_sonos", "Stop"), ("+", "vol_up", "Vol +"), ("-", "vol_down", "Vol -"), ("q", "quit", "Quit")]

    def action_stop_sonos(self) -> None:
        if not TESTING:
            sonos_speaker.stop()
        else:
            print("def action_stop_sonos")

    def action_vol_up(self) -> None:
        sonos_speaker.volume +=2
        self.query_one(ProgressBar).advance(2)

    def action_vol_down(self) -> None:
        sonos_speaker.volume -=2
        self.query_one(ProgressBar).advance(-2)

    def action_quit(self) -> None:
        self.exit()


    def on_mount(self) -> None:
        self.title = "🔊 Now playing: "
        if not TESTING:
            """TODO: read on how to make below reactive methods"""
            self.sub_title = str(track['artist']+" · "+track['title'])
            self.query_one(ProgressBar).advance(sonos_speaker.volume)

        else:
            self.sub_title = "Sonos - TESTING MODE"

    @on(ListView.Selected)
    def url_choice(self, event: ListView.Selected) -> None:
        sonos_speaker.play_uri(event.item.url)
        self.query_one("#result", Label).update(event.item.url)

if __name__ == "__main__":
    if not TESTING:
        sonos_speaker = soco.discovery.any_soco()
        try:
            track = sonos_speaker.get_current_track_info()
        except:
            print("Error: speaker not found.")
            exit()
    else:
        pass
    
    SocoTextualRemote().run()
