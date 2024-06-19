from dataclasses import dataclass
from typing import Callable, List, Protocol


class MediaItem(Protocol):
    heading: str
    subheading: str
    text: str


@dataclass
class Movie:
    id: str
    title: str
    description: str
    director: str

    @property
    def heading(self):
        return self.title

    @property
    def subheading(self):
        return self.director

    @property
    def text(self):
        return self.description


@dataclass
class Series:
    id: str
    title: str
    summary: str
    episodes: int

    @property
    def heading(self):
        return self.title

    @property
    def subheading(self):
        return f"{self.episodes} episodes"

    @property
    def text(self):
        return self.summary
    

@dataclass
class Documentary:
    id: str
    title: str
    description: str

    @property
    def heading(self):
        return self.title

    @property
    def subheading(self):
        return self.description

    @property
    def text(self):
        return self.description


ViewMethod = Callable[[MediaItem], None]


def view_list(item: MediaItem):
    print(f"list: {item.heading}")


def view_preview(item: MediaItem):
    print(f"preview: {item.heading}, {item.subheading}")


def view_full(item: MediaItem):
    print(f"full: {item.heading}, {item.subheading}, text: {item.text}")


def view_teaser(item: MediaItem):
    print(f"teaser: {item.text[:10]}")


def main() -> None:
    media: List[MediaItem] = [
        Movie(
            id="1",
            title="Spirited Away",
            description="Chihiro ...",
            director="Hayao Miyazaki",
        ),
        Series(
            id="2",
            title="Fullmetal Alchemist: Brotherhood",
            summary="Edward ...",
            episodes=64,
        ),
        Documentary(
            id="3",
            title="Blue Planet",
            description="Documentary about ..."
        ),
    ]

    view_methods: List[ViewMethod] = [
        view_list,
        view_preview,
        view_full,
        view_teaser,
    ]

    for item in media:
        for view in view_methods:
            view(item)
        print("\n------\n")



if __name__ == "__main__":
    main()
