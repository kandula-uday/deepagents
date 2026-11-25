"""M2.4: Ask a question about Chinook and check the agent's answer.

Run from the practice repository root after completing the TODOs:
    python -m homework.module_02.interpreter
"""

import json
import re
import sqlite3
from pathlib import Path
from uuid import uuid4

from deepagents import create_deep_agent
from langchain.tools import tool
from langchain_quickjs import CodeInterpreterMiddleware

from hello_agent import model

DB_PATH = Path(__file__).resolve().parent / "chinook.db"

SYSTEM_PROMPT = (
    "You are a sales analyst for the Chinook Digital Music Store. "
    "Use the query_chinook tool to query the database. "
    "Key tables: Artist(ArtistId, Name), Album(AlbumId, Title, ArtistId), "
    "Track(TrackId, Name, AlbumId, GenreId), Genre(GenreId, Name), "
    "Customer(CustomerId, FirstName, LastName, Country), "
    "Invoice(InvoiceId, CustomerId), "
    "InvoiceLine(InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity). "
    "Revenue is InvoiceLine.UnitPrice * InvoiceLine.Quantity. "
    "The eval tool can run JavaScript that calls query_chinook "
    "using tools.queryChinook()."
)


@tool
def query_chinook(sql: str) -> str:
    """Execute a read-only SQL query against Chinook and return JSON rows."""
    conn = sqlite3.connect(f"{DB_PATH.as_uri()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = [dict(row) for row in conn.execute(sql).fetchall()]
        return json.dumps(rows)
    finally:
        conn.close()


TASK = (
    "Which artist has the most albums in the Chinook database? "
    "Give the artist's name, the number of albums, and the title of their "
    "first album alphabetically (using SQLite's default ordering). "
    "If artists have the same number of albums, choose the one with the "
    "smallest ArtistId. Use eval to connect the dependent queries."
)


def eval_answer(answer_text: str) -> None:
    """Independently check whether the agent's answer is correct."""
    conn = sqlite3.connect(f"{DB_PATH.as_uri()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        artist = conn.execute(
            """
            SELECT Artist.ArtistId, Artist.Name, COUNT(Album.AlbumId) AS album_count
            FROM Artist
            JOIN Album ON Album.ArtistId = Artist.ArtistId
            GROUP BY Artist.ArtistId
            ORDER BY album_count DESC, Artist.ArtistId ASC
            LIMIT 1
            """
        ).fetchone()
        if artist is None:
            raise ValueError("The database contains no artists with albums.")

        album = conn.execute(
            """
            SELECT Title
            FROM Album
            WHERE ArtistId = ?
            ORDER BY Title ASC, AlbumId ASC
            LIMIT 1
            """,
            (artist["ArtistId"],),
        ).fetchone()
        if album is None:
            raise ValueError("No album found for the selected artist.")
    finally:
        conn.close()

    print("\n--- Answer check ---")
    print(f"Expected artist: {artist['Name']}")
    print(f"Expected album count: {artist['album_count']}")
    print(f"Expected first album: {album['Title']}")

    checks = {
        "mentions artist": artist["Name"].casefold() in answer_text.casefold(),
        "mentions album count": bool(
            re.search(rf"(?<!\d){artist['album_count']}(?!\d)", answer_text)
        ),
        "mentions album title": album["Title"].casefold() in answer_text.casefold(),
    }
    for label, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {label}")


def main() -> None:
    if not TASK.strip():
        raise ValueError("Complete TODO 1: write a question in TASK.")
    if not DB_PATH.is_file():
        raise FileNotFoundError(f"Chinook database not found: {DB_PATH}")

    agent = create_deep_agent(
        model=model,
        tools=[query_chinook],
        middleware=[CodeInterpreterMiddleware(ptc=["query_chinook"])],
        system_prompt=SYSTEM_PROMPT,
    )
    result = agent.invoke(
        {"messages": [{"role": "user", "content": TASK}]},
        config={"configurable": {"thread_id": str(uuid4())}},
    )
    answer = result["messages"][-1].text
    print(f"\nAgent answer:\n{answer}")
    eval_answer(answer)


if __name__ == "__main__":
    main()
