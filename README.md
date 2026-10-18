# Needle Drop song list

A community list that maps **Spotify tracks to YouTube videos**, used by the
[Needle Drop](https://github.com/Burgersim/qr-music-game-app) app to play
music-guessing cards (QR Music Game and other cards with Spotify links)
without Spotify.

The app downloads this list automatically, so a card whose song is listed here
starts playing right away, with a version someone already checked, instead of
the app searching YouTube on the spot.

## Format

[`spotify.csv`](spotify.csv) — one song per line, sorted by Spotify ID:

```csv
spotify_id,youtube_id
0MFEyNAn08HvzfbteolLWT,dQw4w9WgXcQ
```

- `spotify_id`: the 22-character ID from a Spotify track link
  (`https://open.spotify.com/track/<spotify_id>`). This is what a card's QR
  code contains.
- `youtube_id`: the 11-character ID of the YouTube video to play
  (`https://www.youtube.com/watch?v=<youtube_id>`).

The list is keyed by the song, not by a card or a game: if two decks contain
the same Spotify track, both benefit from one entry. It deliberately contains
no titles, artists, years or card numbers — the app reads those from Spotify.

### What makes a good match

- The **original studio recording**, not a live version, cover, remix or
  sped-up edit.
- Close to the **same length** as the Spotify track (within a few seconds), so
  random snippets land in the same part of the song.
- Preferably an upload without a long video intro (official audio or
  "Topic" channel uploads are usually ideal).

## Contributing

The easiest way is the app itself: use **Prepare cards**, scan your deck,
review the matches and tap **Export**. Then either

- add the exported lines to `spotify.csv` on GitHub (open the file → ✏️ edit →
  paste → "Propose changes") and open a pull request, or
- merge the export locally and open a pull request with the result:

  ```sh
  python3 tools/merge.py my-export.csv
  ```

  New songs are added; songs that are already listed keep their video unless
  you pass `--replace` (for exports that contain fixes).

Fixing a wrong match works the same way: change the `youtube_id` on that line.

Every pull request is checked automatically (IDs well-formed, no duplicates,
sorted). To tidy the file locally before submitting:

```sh
python3 tools/check.py --fix
```

## License

MIT — see [LICENSE](LICENSE).
