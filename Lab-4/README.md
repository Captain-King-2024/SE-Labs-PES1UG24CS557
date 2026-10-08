# Software Engineering Lab 4: VibeCoding — Helicopter

A small Pygame side-scroller with responsive vertical movement, wall collisions,
distance scoring, and a reusable one-hit shield.

## Run the corrected game

From the submission repository root, using PowerShell:

```powershell
cd Lab-4/helicopter
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Verified environment: Python 3.12.7 and Pygame 2.6.1. The original dependency
`pygame>=2.5.0` is unchanged. The workspace's existing Python 3.12 environment
already imports Pygame successfully; the system default Python is 3.14.3.
Use the verified interpreter instead of changing dependencies unnecessarily.

## Controls and behavior

- **Up / Down:** accelerate vertically, capped at 6 pixels per frame.
  Pressing the opposite direction clears opposing momentum immediately.
  Releasing the keys stops vertical movement immediately; pressing both also stops.
- **R:** start a fresh game, including from Game Over.
- **Space:** activate one shield charge. Repeated presses do not stack charges.
  A blue ring and `Shield: ACTIVE (1 hit)` identify an active shield.
- Close the window to exit.

The helicopter's position represents its centre. Clamping that centre between
half its height and the screen height minus half its height keeps the entire
body on screen. Previously, unlimited acceleration made the opposite key spend
many frames cancelling accumulated speed, and only the top boundary was checked.

The helicopter's rectangular body is checked against both obstacle walls.
Overlapping either wall ends an unprotected game; the open gap is safe.
At Game Over, movement, obstacle spawning, and distance stop. The banner shows
final distance and restart instructions.

Distance is measured in **pixels (`px`)**: each active update adds the world's
3-pixel scroll displacement, including the update on which a collision happens.
It is independent of how many obstacles have spawned or been passed.
The loop targets 60 frames per second, as in the starter.

A shield disappears immediately when it absorbs a collision. That particular
contact is ignored while the helicopter continues overlapping the same obstacle,
so it does not kill the player on the next frame. Other obstacles remain dangerous
unless a new shield is activated. Leaving the wall (including entering its gap)
ends that contact's protection; re-entering it requires another shield.
Space can activate a new charge during continued protected overlap, and that old
contact does not consume the new charge. Restart clears all shield/contact state.

## Source and original version

Submission destination: https://github.com/Captain-King-2024/SE-Labs-PES1UG24CS557,
branch `main`, folder `Lab-4`. All other labs are preserved.

Reference only: https://github.com/SETAPESU26/08_helicopter

- Original upstream commit: `4402faa66a1f3ee701c1dbdece783a08bc8c241e`.
- The provided workspace was an extracted folder with no Git metadata. Its nine
  source/documentation files matched that upstream commit after normalizing line endings.
- Unmodified starter setup commit in the submission repository:
  `2d11cfab300e2eaad3f9665ec0a97cc860ab94e1`.
- The original workspace game at `helicopter/main.py` remains untouched.
  The corrected game is at `submission/Lab-4/helicopter/main.py` within that workspace.
- A separate `original-reference` checkout also preserves the upstream original.
  No commits or pushes were made to the starter repository.

To recreate an original version without undoing corrections, run from the
submission repository root (the destination must not already exist):

```powershell
git worktree add --detach ../helicopter-before 2d11cfab300e2eaad3f9665ec0a97cc860ab94e1
cd ../helicopter-before/Lab-4/helicopter
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Checks and task history

Run from `Lab-4/helicopter` using an environment with Pygame installed:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests select SDL's dummy video/audio drivers. They are **headless checks**,
not a claim of live keyboard gameplay testing.

| Task | Commit | Checks passed at that step |
| --- | --- | --- |
| Starter setup | `2d11cfa` | Nine source files compared with upstream |
| 1. Movement and boundaries | `d18e6a2` | 3 tests: long holds, speed caps, reversals, full-body bounds |
| 2. Collision and Game Over | `72acaa6` | 8 cumulative tests: both walls, gap traversal, frozen state, restart, rendering |
| 3. Distance scoring | `0bf05c5` | 11 cumulative tests: scrolling distance, empty world, freeze/reset |
| 4. One-hit shield | `9b8e6ad` | 21 cumulative tests: consumption, no stacking, overlap, other obstacles, reactivation, reset, ring pixels |

A headless smoke check also exercised the actual main loop with Space, R, and
Quit events. Still renders of the active shield, consumed shield, and Game Over
were visually inspected. No video was recorded or generated.

The initial push failed with GitHub's message: `Invalid username or token.
Password authentication is not supported for Git operations.` The user chose to
continue locally while fixing authentication. These commits are local; no
successful push is claimed. Once Git authentication has write access, push from
the submission repository root and compare the two hashes:

```powershell
git remote get-url --push origin
# Must be https://github.com/Captain-King-2024/SE-Labs-PES1UG24CS557.git
git push origin main:main
git rev-parse main
git ls-remote origin refs/heads/main
```

Do not force-push. If main advanced remotely, fetch and inspect the new commits
before integrating them without rewriting existing history.

## Manual verification and submission checklist

- [ ] Play the corrected game: hold both directions separately, reverse quickly,
  check both screen bounds, fly through gaps, and hit each wall without a shield.
- [ ] Check that distance freezes at Game Over and R restores a fresh game.
- [ ] Activate Space; confirm the ring disappears on one hit, continued overlap
  survives, another obstacle is dangerous, and Space can activate again.
- [ ] Personally record a **10-second before video** using the untouched original:
  show delayed reversal, leaving the bottom edge, or passing through a wall.
- [ ] Personally record a **10-second after video** using the corrected game:
  show responsive controls, distance, shield use, Game Over, and restart.
- [ ] Place the real recordings under `Lab-4`, for example `before.mp4` and
  `after.mp4`. Neither video has been completed by the coding assistant.
- [ ] Export the actual complete AI conversation into `Lab-4`, or add the real
  share URL in `Lab-4/AI_CONVERSATION.md`. Include the request, explanations,
  fixes, test results, and authentication blocker. This README is a work log,
  not a substitute for the actual chat history; no chat export is fabricated.
- [ ] Commit the real submission artifacts and verify the successful push to
  the specified repository's `main` branch. Keep virtual environments, caches,
  credentials, and temporary verification images out of Git.

## Structure

```text
Lab-4/
  .gitignore
  README.md
  helicopter/
    main.py
    requirements.txt
    game/
      __init__.py
      helicopter.py
      obstacle.py
      game_engine.py
      renderer.py
    tests/
      test_game.py
```
