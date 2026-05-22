# Final-game-SE-2517-Gulsezim-Kapizova

BlazeDash is a 2D side-scrolling platformer in the style of Sonic Rush. The player controls Blaze, a purple cat with fire magic. Task: Run through the level, collect gold rings, defeat enemies by trampling or fireballs, and find the Emerald Sol at the end of the level. The game demonstrates object-oriented programming, a state system, record keeping in JSON, and modular architecture.

Gameplay
Smooth scrolling with the camera that follows the Blaze
Collecting gold rings — each one gives +10 points
Two types of enemies: Motobug (100 points) and Crabmeat (200 points)
Defeating enemies: by trampling from above or by fireball
Sol Emerald at the end of the level — +200 points, completes the level
Life system: 3 lives, if you lose rings, you lose rings, without rings, you lose your life
Level Timer — is shown on the Game Over screen and wins

Screens and statuses
Start Menu — a screensaver with top records and a start button
Play — the main gameplay with HUD
Game Over — final score + time + high score table
Stage Clear — the winning screen when finding the Emerald Sol

HUD (during the game)
SCORE — current score
RINGS — the number of rings
LIVES — remaining lives
BEST — record from a file
TIME — the current time of the level in MM:SS.T format

Control
WASD or arrows
S/F fire


Project structure
blazedash/
├── main.py # entry point — starts the game
├── settings.py# constants: screen, physics, colors, paths
,── game.py # Game — a fortune machine
├── player.py # Player — Blaze (movement, jump, shot)
├── enemy.py # Enemy → Motobug, Crabmeat (polymorphism)
├── fireball.py # Fireball — Projectile Blaze
├── level.py             # Level, Platform, Ring, SolEmerald
,── camera.py # Camera — follows the player
├── score_manager.py # ScoreManager — JSON records
,── utils.py # Entity (database), Animator, GameTimer
├── requirements.txt # dependencies
├── assets/
│   └── images/
│ ├── blaze_run.png # 384×48 — running animation
│ ├── blaze_jump.png # 192×48 — jump animation
│ ├── blaze_shoot.png # 144x48 — shot animation
│ ├── fireball.png # 144x24 - fireball animation
│ ├── motobug.png # 160×32 - animation of a beetle
│ ├── crabmeat.png # 264×36 — crab animation
│ ├── ring.png # 128×16 - ring animation
─── sol_emerald.png # 240×40 - animation of the emerald
,── platform.png # 128×20 - platform tile
│ └── background.png # 800×480 - background of the level
└── data/
    └── highscores.json# is created automatically

OOP Architecture
Entity (utils.py ) ← base class
,── Player (player.py ) ← inherits Entity
,── Fireball (fireball.py ) ← inherits Entity
,── Platform (level.py ) ← inherits Entity
,── Ring (level.py ) ← inherits Entity
,── SolEmerald (level.py ) ← inherits Entity
,── Enemy (enemy.py ) ← inherits Entity
    ,── Motobug (enemy.py ) ← inherits Enemy
    ,── Crabmeat (enemy.py ) ← inherits Enemy


Polymorphism
The draw() method is defined differently in each Enemy subclass. 
The game loop calls e.draw() without knowing the type of the object — this is polymorphism:
# game.py — The same challenge for different types of enemies
for e in self.level.enemies:
    if e.alive:
e.draw(surface, cam_x) # Motobug or Crabmeat — it doesn't matter


Encapsulation
Private methods start with _ and are not called from outside the class.:
# player.py — internal methods are hidden
def _handle_input(self, keys): ...
def _apply_gravity(self):      ...
def _move_and_collide(self, platforms):

Data storage (JSON)
File data/highscores.json is created automatically the first time the result is saved. 
Keeps the top 5 records. Example of content:
[
{ "name": "BLAZE", "score": 1450 },
{ "name": "BLAZE", "score": 1200 },
{ "name": "BLAZE", "score": 980 }
]
The ScoreManager class in score_manager.py handles all operations with the file.
All reads and writes are wrapped in try/except — the game will not crash if the file is corrupted or missing.

