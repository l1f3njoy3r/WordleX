from re import S
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import json
import os
import sys
import datetime
import urllib.request
import urllib.error
import threading
from PIL import Image, ImageDraw, ImageFont, ImageGrab
import io
import copy

# --- word list ---
BUILTIN_WORDS = [
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
    "agent", "agree", "ahead", "aimed", "alarm", "album", "alert", "alien", "align", "alike",
    "alive", "alley", "allow", "alone", "along", "alter", "amaze", "ample", "angel", "anger",
    "angle", "angry", "anime", "ankle", "annex", "antic", "apart", "apple", "apply", "arena",
    "argue", "arise", "armor", "aroma", "arose", "array", "arrow", "aside", "asset", "atlas",
    "attic", "audio", "audit", "avoid", "awake", "award", "aware", "awful", "bacon", "badge",
    "badly", "baker", "bases", "basic", "basin", "basis", "batch", "beach", "beard", "beast",
    "began", "begin", "being", "belly", "below", "bench", "berry", "bible", "birth", "black",
    "blade", "blame", "bland", "blank", "blast", "blaze", "bleak", "bleed", "blend", "bless",
    "blind", "blink", "bliss", "block", "blond", "blood", "bloom", "blown", "board", "boast",
    "bonus", "booth", "bound", "brain", "brand", "brave", "bread", "break", "breed", "brick",
    "bride", "brief", "bring", "broad", "broke", "brook", "brown", "brush", "buddy", "build",
    "built", "bunch", "burst", "buyer", "cabin", "cable", "camel", "candy", "cargo", "carry",
    "catch", "cater", "cause", "cease", "chain", "chair", "chalk", "champ", "chaos", "charm",
    "chart", "chase", "cheap", "check", "cheek", "cheer", "chess", "chest", "chief", "child",
    "chill", "china", "chunk", "cinch", "circa", "civic", "civil", "claim", "clamp", "clash",
    "class", "clean", "clear", "clerk", "click", "cliff", "climb", "cling", "clock", "clone",
    "close", "cloth", "cloud", "clown", "coach", "coast", "colon", "color", "comet", "comic",
    "coral", "couch", "could", "count", "court", "cover", "crack", "craft", "crane", "crash",
    "crazy", "cream", "creek", "creep", "crest", "crime", "crisp", "cross", "crowd", "crown",
    "cruel", "crush", "curve", "cycle", "daily", "dance", "datum", "dealt", "death", "debut",
    "decay", "delay", "delta", "dense", "depth", "derby", "devil", "diary", "diner", "dirty",
    "ditch", "dizzy", "dodge", "doing", "donor", "doubt", "dough", "draft", "drain", "drake",
    "drama", "drank", "drape", "drawl", "drawn", "dread", "dream", "dress", "dried", "drift",
    "drill", "drink", "drive", "drone", "droit", "drove", "drugs", "drums", "drunk", "dryer",
    "dully", "dummy", "dwell", "dying", "eager", "eagle", "early", "earth", "eight", "elbow",
    "elder", "elect", "elite", "ember", "emote", "empty", "endow", "enemy", "enjoy", "enter",
    "entry", "epoch", "equal", "equip", "erase", "error", "essay", "ethic", "evade", "event",
    "every", "exact", "exile", "exist", "extra", "fable", "facet", "facto", "faint", "fairy",
    "faith", "false", "fancy", "fatal", "fault", "feast", "fence", "ferry", "fetch", "fever",
    "fiber", "fibre", "field", "fiery", "fifth", "fifty", "fight", "final", "first", "fixed",
    "flame", "flash", "flask", "flesh", "flick", "float", "flock", "flood", "floor", "flora",
    "flour", "fluid", "flush", "focal", "focus", "force", "forge", "forth", "forum", "found",
    "frame", "frank", "fraud", "freak", "fresh", "front", "frost", "froze", "fruit", "fully",
    "funny", "fuzzy", "gamma", "gauge", "gavel", "genre", "ghost", "giant", "given", "gland",
    "glass", "glaze", "gleam", "glide", "gloom", "glory", "gloss", "glove", "going", "grace",
    "grade", "grain", "grand", "grant", "grape", "graph", "grasp", "grass", "grave", "great",
    "greed", "green", "greet", "grief", "grind", "groan", "groom", "gross", "group", "grove",
    "grown", "guard", "guess", "guest", "guide", "guild", "guilt", "guise", "quite", "quota",
    "habit", "happy", "harsh", "haste", "haunt", "haven", "heart", "heavy", "hedge", "heist",
    "hence", "herbs", "hitch", "hobby", "holly", "honor", "horse", "hotel", "house", "human",
    "humor", "hurry", "hyper", "ideal", "image", "imply", "incur", "index", "indie", "infer",
    "inner", "input", "intel", "inter", "intro", "ionic", "irate", "ivory", "jewel", "jimmy",
    "joint", "joker", "jolly", "judge", "juice", "juicy", "jumbo", "jumpy", "juror", "karma",
    "kayak", "kebab", "keyed", "knack", "kneel", "knelt", "knife", "knock", "known", "label",
    "labor", "lance", "large", "laser", "latch", "later", "laugh", "layer", "leach", "lease",
    "leave", "legal", "lemon", "level", "lever", "light", "limit", "linen", "liner", "lingo",
    "logic", "login", "loose", "lorry", "lover", "lower", "loyal", "lucid", "lucky", "lunar",
    "lunch", "lyric", "macro", "magic", "major", "maker", "manga", "manor", "maple", "march",
    "marry", "marsh", "match", "matte", "mayor", "meant", "medal", "media", "melee", "melon",
    "mercy", "merge", "merit", "merry", "metal", "meter", "midst", "might", "mimic", "minds",
    "minor", "minus", "mirth", "misty", "mixed", "model", "modem", "money", "month", "moral",
    "motif", "motor", "motto", "mould", "mount", "mourn", "mouse", "mouth", "moved", "movie",
    "mural", "music", "naive", "named", "naval", "nerve", "never", "niche", "night", "noble",
    "noise", "north", "noted", "novel", "nurse", "nylon", "occur", "ocean", "offal", "offer",
    "often", "olive", "onset", "opera", "orbit", "order", "organ", "other", "ought", "ounce",
    "outer", "outdo", "owner", "oxide", "ozone", "paint", "panel", "panic", "paper", "patch",
    "pause", "peace", "peach", "pearl", "pedal", "penny", "perch", "peril", "phase", "phone",
    "photo", "piano", "piece", "pilot", "pinch", "pitch", "pixel", "pizza", "place", "plain",
    "plane", "plant", "plate", "plaza", "plead", "pleat", "pluck", "plumb", "plume", "plump",
    "plunge","point", "polar", "porch", "poser", "pouch", "pound", "power", "prank", "prawn",
    "press", "price", "pride", "prime", "prince","print", "prior", "prize", "probe", "prone",
    "proof", "prose", "proud", "prove", "proxy", "prune", "psalm", "pulse", "punch", "pupil",
    "purse", "pushy", "quail", "qualm", "query", "quest", "queue", "quick", "quiet", "quilt",
    "quirk", "quota", "quote", "rabbi", "radar", "radio", "raise", "rally", "ranch", "range",
    "rapid", "ratio", "reach", "react", "ready", "realm", "rebel", "refer", "reign", "relax",
    "relay", "renal", "renew", "repay", "repel", "reply", "rider", "ridge", "rifle", "right",
    "rigid", "rigor", "rinse", "rival", "river", "robin", "robot", "rocky", "roman", "roost",
    "rouge", "rough", "round", "route", "royal", "rugby", "ruled", "ruler", "rumor", "rural",
    "sadly", "saint", "salad", "salon", "sandy", "sauce", "scale", "scare", "scarf", "scene",
    "scent", "scope", "score", "scout", "scrap", "screw", "seize", "sense", "serve", "setup",
    "seven", "shade", "shaft", "shake", "shall", "shame", "shape", "share", "shark", "sharp",
    "shave", "sheep", "sheer", "sheet", "shelf", "shell", "shift", "shire", "shirt", "shock",
    "shoot", "shore", "short", "shout", "shove", "shown", "siege", "sight", "sigma", "silly",
    "since", "sixth", "sixty", "sized", "skill", "skull", "slash", "slate", "slave", "sleep",
    "sleek", "slice", "slide", "slope", "small", "smart", "smell", "smile", "smoke", "snake",
    "solar", "solid", "solve", "sonic", "sorry", "south", "space", "spare", "spark", "spawn",
    "speak", "spear", "speed", "spell", "spend", "spent", "spice", "spicy", "spine", "spite",
    "split", "spoke", "spoon", "sport", "spots", "spray", "squad", "staff", "stage", "stain",
    "stake", "stale", "stall", "stamp", "stand", "stare", "stark", "start", "state", "stays",
    "steak", "steal", "steam", "steel", "steep", "steer", "stems", "stick", "stiff", "still",
    "sting", "stock", "stole", "stone", "stood", "stool", "store", "storm", "story", "stout",
    "stove", "strap", "straw", "stray", "strip", "stuck", "study", "stuff", "stump", "style",
    "sugar", "suite", "sunny", "super", "surge", "swamp", "swarm", "swear", "sweat", "sweep",
    "sweet", "swept", "swift", "swing", "swirl", "swore", "sworn", "swung", "table", "taste",
    "taxed", "teach", "teeth", "tempo", "tense", "tenth", "terry", "theft", "theme", "there",
    "thick", "thief", "thing", "think", "third", "thorn", "those", "three", "threw", "throw",
    "thumb", "tidal", "tiger", "tight", "timer", "tired", "titan", "title", "today", "token",
    "topic", "torch", "total", "touch", "tough", "towel", "tower", "toxic", "trace", "track",
    "trade", "trail", "train", "trait", "trash", "trawl", "treat", "trend", "trial", "tribe",
    "trick", "tried", "troop", "trout", "truck", "truly", "trump", "trunk", "trust", "truth",
    "tumor", "tuner", "tuple", "twice", "twist", "tying", "ultra", "uncle", "under", "undue",
    "unify", "union", "unite", "unity", "until", "upper", "upset", "urban", "usage", "usual",
    "utter", "valid", "valor", "value", "valve", "vapor", "vault", "venue", "verge", "verse",
    "vigor", "vinyl", "viola", "viral", "virus", "visit", "vista", "vital", "vivid", "vocal",
    "vodka", "voice", "voter", "vouch", "vulgar","waist", "waste", "watch", "water", "weary",
    "weave", "wedge", "weigh", "weird", "whale", "wheat", "wheel", "where", "which", "while",
    "whine", "whirl", "white", "whole", "whose", "wider", "wield", "windy", "witch", "woman",
    "women", "world", "worry", "worse", "worst", "worth", "would", "wound", "wrath", "wrist",
    "write", "wrote", "yacht", "yearn", "yield", "young", "youth", "zebra", "zesty",
]

# remove duplicates and ensure all lowercase
BUILTIN_WORDS = list(set(w.lower() for w in BUILTIN_WORDS if len(w) == 5))

SAVE_FILE = "wordlex_data.json"

ENCOURAGING_WORDS = {
    1: "Brilliant! 🧠",
    2: "Magnificent! ✨",
    3: "Impressive! 🎯",
    4: "Splendid! 👏",
    5: "Great Job! 💪",
    6: "Phew! Close one! 😅",
}

LOSS_MESSAGE = "Better luck next time! 😢"


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def is_real_word_api(word):
    """Check if a word is a real English word using Free Dictionary API."""
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
        req = urllib.request.Request(url, headers={"User-Agent": "WordleX/1.0"})
        response = urllib.request.urlopen(req, timeout=5)
        if response.getcode() == 200:
            return True
        return False
    except urllib.error.HTTPError:
        return False
    except Exception:
        return True  # if api is down, allow the word


def get_definition_api(word):
    """Get definition of a word using Free Dictionary API."""
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
        req = urllib.request.Request(url, headers={"User-Agent": "WordleX/1.0"})
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode())
        if data and isinstance(data, list):
            meanings = data[0].get("meanings", [])
            if meanings:
                definitions = meanings[0].get("definitions", [])
                if definitions:
                    return definitions[0].get("definition", "No definition found.")
        return "No definition found."
    except Exception:
        return "Could not fetch definition."


class WordleX:
    def __init__(self, root):
        self.root = root
        self.root.title("WordleX")
        self.root.geometry("540x820")
        self.root.minsize(510, 780)
        self.root.resizable(True, True)

        # --- data ---
        self.load_data()

        # --- theme ---
        self.dark_mode = self.data.get("dark_mode", True)

        # --- game state ---
        self.game_mode = "default"  # "default" or "user"
        # self.current_user_list_name = self.data.get("current_user_list", None)
        self.selected_user_lists = self.data.get("selected_user_lists", [])
        self.target_word = ""
        self.current_row = 0
        self.current_col = 0
        self.game_over = False
        self.game_won = False
        self.board = [["" for _ in range(5)] for _ in range(6)]
        self.board_colors = [[None for _ in range(5)] for _ in range(6)]
        self.key_colors = {}
        self.tile_labels = []
        self.popup_open = False
        self.user_input_active = False  # track if user word input bar is active
        self.game_history_for_share = []  # store color results per row
        self._popup_on_close = None

        # --- colors ---
        self.colors = {}
        self.set_theme_colors()

        # --- ui ---
        self.build_ui()
        self.apply_theme()

        # bind keys
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Escape>", self.on_escape)
        # width and height of the window output in the cmd
        # self.root.bind("<Configure>", lambda e: print(self.root.winfo_width(), self.root.winfo_height()))

        # start a new game
        self.start_new_game()

    # ========================
    # DATA PERSISTENCE
    # ========================
    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}
        else:
            self.data = {}

        # ensure structure
        self.data.setdefault("dark_mode", True)
        self.data.setdefault("user_lists", {})
        # self.data.setdefault("current_user_list", None) - old format
        self.data.setdefault("selected_user_lists", []) # multiple lists selection (new) format

        # new structure of statistics
        self.data.setdefault("statistics", {})
        stats = self.data["statistics"]
        stats.setdefault("overall", self._empty_stats())
        stats.setdefault("default", self._empty_stats())
        stats.setdefault("user_configs", {})

        # migration of old format
        if "stats" in self.data:
            old = self.data.pop("stats")
            stats["overall"] = old
            stats["default"] = copy.deepcopy(old)

        if "current_user_list" in self.data:
            old = self.data.pop("current_user_list")
            if old and old not in self.data.get("selected_user_lists", []):
                self.data["selected_user_lists"].append(old)

    def save_data(self):
        self.data["dark_mode"] = self.dark_mode
        self.data["selected_user_lists"] = self.selected_user_lists
        with open(SAVE_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    # ========================
    # THEME
    # ========================
    def set_theme_colors(self):
        if self.dark_mode:
            self.colors = {
                "bg": "#121213",
                "bar_bg": "#1a1a1b",
                "tile_bg": "#3a3a3c",
                "tile_border": "#3a3a3c",
                "tile_empty_border": "#565758",
                "text": "#ffffff",
                "text_secondary": "#aaaaaa",
                "correct": "#538d4e",
                "present": "#b59f3b",
                "absent": "#3a3a3c",
                "key_bg": "#818384",
                "key_text": "#ffffff",
                "popup_bg": "#1a1a1b",
                "popup_border": "#3a3a3c",
                "button_bg": "#538d4e",
                "button_text": "#ffffff",
                "entry_bg": "#2a2a2b",
                "entry_fg": "#ffffff",
                "mode_btn_bg": "#3a3a3c",
                "mode_btn_active": "#538d4e",
                "scrollbar": "#3a3a3c",
            }
        else:
            self.colors = {
                "bg": "#ffffff",
                "bar_bg": "#f0f0f0",
                "tile_bg": "#ffffff",
                "tile_border": "#d3d6da",
                "tile_empty_border": "#d3d6da",
                "text": "#1a1a1b",
                "text_secondary": "#666666",
                "correct": "#6aaa64",
                "present": "#c9b458",
                "absent": "#787c7e",
                "key_bg": "#d3d6da",
                "key_text": "#1a1a1b",
                "popup_bg": "#ffffff",
                "popup_border": "#d3d6da",
                "button_bg": "#6aaa64",
                "button_text": "#ffffff",
                "entry_bg": "#f5f5f5",
                "entry_fg": "#1a1a1b",
                "mode_btn_bg": "#d3d6da",
                "mode_btn_active": "#6aaa64",
                "scrollbar": "#d3d6da",
            }

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.set_theme_colors()
        self.apply_theme()
        self.save_data()

    def apply_theme(self):
        bg = self.colors["bg"]
        bar_bg = self.colors["bar_bg"]
        text = self.colors["text"]

        # root and main frame
        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg, highlightthickness=0)

        # top bar
        self.top_bar.configure(bg=bar_bg, highlightthickness=0)
        self.title_label.configure(bg=bar_bg, fg=text)

        # rules frame
        self.rules_frame = self.rules_btn.master
        self.rules_frame.configure(bg=bar_bg, highlightthickness=0)
        self.rules_icon.configure(
            bg=bar_bg, fg=text,
            highlightbackground=bar_bg, highlightcolor=bar_bg,
        )
        self.rules_btn.configure(
            bg=bar_bg, fg=text,
            activebackground=bar_bg, activeforeground=text,
            highlightbackground=bar_bg, highlightcolor=bar_bg,
        )

        # top bar buttons
        for btn in [self.theme_btn, self.stats_btn, self.new_game_btn]:
            btn.configure(
                bg=bar_bg, fg=text,
                activebackground=bar_bg, activeforeground=text,
                highlightbackground=bar_bg, highlightcolor=bar_bg,
            )

        # theme button icon
        self.theme_btn.configure(text=" ☀ " if self.dark_mode else " 🌙 ") #spaces around emojies

        # mode frame
        self.mode_frame.configure(bg=bg, highlightthickness=0)
        self.mode_inner.configure(bg=bg, highlightthickness=0)

        for btn_name, btn in [("default", self.default_mode_btn), ("user", self.user_mode_btn)]:
            active = (btn_name == self.game_mode)
            btn_bg = self.colors["mode_btn_active"] if active else self.colors["mode_btn_bg"]
            btn_fg = "#ffffff" if active else text
            btn.configure(
                bg=btn_bg, fg=btn_fg,
                activebackground=btn_bg, activeforeground=btn_fg,
                highlightbackground=btn_bg, highlightcolor=btn_bg,
            )

        list_btn_bg = self.colors["mode_btn_bg"]
        self.user_list_btn.configure(
            bg=list_btn_bg, fg=text,
            activebackground=list_btn_bg, activeforeground=text,
            highlightbackground=list_btn_bg, highlightcolor=list_btn_bg,
        )

        # board frame
        self.board_frame.configure(bg=bg, highlightthickness=0)
        for row_frame in self.tile_row_frames:
            row_frame.configure(bg=bg, highlightthickness=0)

        # tiles
        for r in range(6):
            for c in range(5):
                lbl = self.tile_labels[r][c]
                frame = self.tile_frames[r][c]
                color = self.board_colors[r][c]
                if color:
                    tile_bg = self.colors.get(color, self.colors["tile_bg"])
                    frame.configure(
                        bg=tile_bg,
                        highlightbackground=tile_bg,
                        highlightcolor=tile_bg,
                    )
                    lbl.configure(bg=tile_bg, fg="#ffffff")
                else:
                    has_letter = self.board[r][c] != ""
                    border_color = self.colors["tile_border"] if has_letter else self.colors["tile_empty_border"]
                    tile_bg = "#ffffff" if not self.dark_mode else self.colors["bg"]
                    frame.configure(
                        bg=tile_bg,
                        highlightbackground=border_color,
                        highlightcolor=border_color,
                    )

                    lbl.configure(bg=tile_bg, fg=text)

        # keyboard frame
        self.keyboard_frame.configure(bg=bg, highlightthickness=0)
        for row_frame in self.keyboard_row_frames:
            row_frame.configure(bg=bg, highlightthickness=0)

        # keyboard buttons
        for key, btn in self.key_buttons.items():
            kc = self.key_colors.get(key)
            if kc:
                key_bg = self.colors.get(kc, self.colors["key_bg"])
                key_fg = "#ffffff"
            else:
                key_bg = self.colors["key_bg"]
                key_fg = self.colors["key_text"]
            btn.configure(
                bg=key_bg, fg=key_fg,
                activebackground=key_bg, activeforeground=key_fg,
                highlightbackground=key_bg, highlightcolor=key_bg,
            )

        # popup overlay - close and reopen if theme changed
        if hasattr(self, 'popup_overlay') and self.popup_overlay and self.popup_overlay.winfo_exists():
            self.popup_overlay.configure(bg=self.colors["bg"])
            self.close_popup()

    # ========================
    # BUILD UI
    # ========================
    def build_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # --- top bar ---
        self.top_bar = tk.Frame(self.main_frame, height=50)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        self.rules_frame = tk.Frame(self.top_bar)
        self.rules_frame.pack(side="left", padx=8, anchor="s", pady=6)

        self.rules_icon = tk.Label(
            self.rules_frame, text="📖", font=("Helvetica", 17), #18 16
            bd=0, highlightthickness=0, pady=0,
        )
        self.rules_icon.pack(side="left", pady=(0, 7))

        self.rules_icon.bind("<Button-1>", lambda e: self.show_rules())
        self.rules_icon.configure(cursor="hand2")

        self.rules_btn = tk.Button(
            self.rules_frame, text="Rules", font=("Helvetica", 13, "bold"),#space before Rules
            bd=0, highlightthickness=0, relief="flat", cursor="hand2",
            pady=0,
            command=self.show_rules,
        )
        self.rules_btn.pack(side="left", pady=(4, 0))

        self.theme_btn = tk.Button(
        self.top_bar, text="🌙", font=("Helvetica", 14), #14
        bd=0, highlightthickness=0, relief="flat", cursor="hand2",
        width=3,
        command=self.toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=6)

        self.stats_btn = tk.Button(
        self.top_bar, text="📊", font=("Helvetica", 14),
        bd=0, highlightthickness=0, relief="flat", cursor="hand2",
        width=3,
        command=self.show_stats,
        )
        self.stats_btn.pack(side="right", padx=6)

        self.new_game_btn = tk.Button(
        self.top_bar, text="🔄", font=("Helvetica", 15), #14
        bd=0, highlightthickness=0, relief="flat", cursor="hand2",
        width=3,
        command=self.start_new_game,
        )
        self.new_game_btn.pack(side="right", padx=6, pady=(0, 1))

        self.title_label = tk.Label(
        self.top_bar, text="WordleX", font=("Helvetica", 20, "bold"),
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor="center", y=1)

        # --- mode selection ---
        self.mode_frame = tk.Frame(self.main_frame)
        self.mode_frame.pack(fill="x", pady=4)

        self.mode_inner = tk.Frame(self.mode_frame)
        self.mode_inner.pack()

        self.default_mode_btn = tk.Button(
        self.mode_inner, text="Default Mode", font=("Helvetica", 11, "bold"),
        bd=0, highlightthickness=0, relief="flat", padx=14, pady=4, cursor="hand2",
        command=lambda: self.set_mode("default"),
        )
        self.default_mode_btn.pack(side="left", padx=4)

        self.user_mode_btn = tk.Button(
        self.mode_inner, text="User Mode", font=("Helvetica", 11, "bold"),
        bd=0, highlightthickness=0, relief="flat", padx=14, pady=4, cursor="hand2",
        command=lambda: self.set_mode("user"),
        )
        self.user_mode_btn.pack(side="left", padx=4)

        self.user_list_btn = tk.Button(
        self.mode_inner, text="📝 Lists", font=("Helvetica", 11),
        bd=0, highlightthickness=0, relief="flat", padx=8, pady=4, cursor="hand2",
        command=self.show_user_lists_popup,
        )
        self.user_list_btn.pack(side="left", padx=4)
        self.user_list_btn.pack_forget()

        # --- board ---
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(pady=8)

        TILE_SIZE = 58

        self.tile_labels = []
        self.tile_row_frames = []
        self.tile_frames = []

        for r in range(6):
            row_labels = []
            row_tiles = []
            row_frame = tk.Frame(self.board_frame)
            row_frame.pack()
            self.tile_row_frames.append(row_frame)
            for c in range(5):
                tile_frame = tk.Frame(
                    row_frame,
                    width=TILE_SIZE,
                    height=TILE_SIZE,
                    highlightthickness=2,
                    relief="flat",
                )
                tile_frame.pack(side="left", padx=3, pady=3)
                tile_frame.pack_propagate(False)

                lbl = tk.Label(
                    tile_frame, text="",
                    font=("Helvetica", 24, "bold"),
                )
                lbl.pack(expand=True)

                row_labels.append(lbl)
                row_tiles.append(tile_frame)

            self.tile_labels.append(row_labels)
            self.tile_frames.append(row_tiles)


        # --- keyboard ---
        self.keyboard_frame = tk.Frame(self.main_frame)
        self.keyboard_frame.pack(pady=4, fill="x")

        keyboard_rows = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "⌫"],
        ]

        self.key_buttons = {}
        self.keyboard_row_frames = []
        for row in keyboard_rows:
            row_frame = tk.Frame(self.keyboard_frame)
            row_frame.pack()
            self.keyboard_row_frames.append(row_frame)
            for key in row:
                width = 5 if key in ("ENTER", "⌫") else 3
                font_size = 9 if key in ("ENTER", "⌫") else 13
                btn = tk.Button(
                    row_frame, text=key, width=width,
                    font=("Helvetica", font_size, "bold"),
                    bd=0, highlightthickness=0, relief="flat",
                    padx=2, pady=8, cursor="hand2",
                    command=lambda k=key: self.on_virtual_key(k),
                )
                btn.pack(side="left", padx=2, pady=2)
                self.key_buttons[key] = btn

        self.popup_overlay = None

    # ========================
    # GAME MODE
    # ========================
    def set_mode(self, mode):
        self.game_mode = mode
        if mode == "user":
            self.user_list_btn.pack(side="left", padx=4)
        else:
            self.user_list_btn.pack_forget()
        self.apply_theme()
        self.start_new_game()

    def get_word_list(self):
        if self.game_mode == "user" and self.selected_user_lists:
            combined = []
            for list_name in self.selected_user_lists:
                words = self.data["user_lists"].get(list_name, [])
                combined.extend([w.lower() for w in words])
            # removing duplicates
            combined = list(set(combined))
            if combined:
                return combined
        return BUILTIN_WORDS 
            
        

    # ========================
    # GAME LOGIC
    # ========================
    def start_new_game(self):
        word_list = self.get_word_list()
        if not word_list:
            self.show_popup_message("Word list is empty! Add words first.")
            return

        self.target_word = random.choice(word_list).lower()
        self.current_row = 0
        self.current_col = 0
        self.game_over = False
        self.game_won = False
        self.board = [["" for _ in range(5)] for _ in range(6)]
        self.board_colors = [[None for _ in range(5)] for _ in range(6)]
        self.key_colors = {}
        self.game_history_for_share = []
        self.user_input_active = False

        # reset tiles
        for r in range(6):
            for c in range(5):
                self.tile_labels[r][c].configure(text="")
        # reset keyboard colors
        self.apply_theme()

    def on_key_press(self, event):
        if self.popup_open:
            return
        if self.user_input_active:
            return  # don't interact with game board when user list input is active

        key = event.keysym
        char = event.char

        if key == "Return":
            self.submit_guess()
        elif key == "BackSpace":
            self.delete_letter()
        elif char.isalpha() and len(char) == 1:
            self.type_letter(char.upper())

    def on_virtual_key(self, key):
        if self.popup_open:
            return
        if self.user_input_active:
            return

        if key == "ENTER":
            self.submit_guess()
        elif key == "⌫":
            self.delete_letter()
        else:
            self.type_letter(key)

    def type_letter(self, letter):
        if self.game_over:
            return
        if self.current_col < 5:
            self.board[self.current_row][self.current_col] = letter
            lbl = self.tile_labels[self.current_row][self.current_col]
            frame = self.tile_frames[self.current_row][self.current_col]
            tile_bg = "#ffffff" if not self.dark_mode else self.colors["bg"]
            lbl.configure(text=letter, fg=self.colors["text"], bg=tile_bg)
            frame.configure(
                bg=tile_bg,
                highlightbackground=self.colors["tile_border"],
                highlightcolor=self.colors["tile_border"],
            )
            self.current_col += 1

    def delete_letter(self):
        if self.game_over:
            return
        if self.current_col > 0:
            self.current_col -= 1
            self.board[self.current_row][self.current_col] = ""
            lbl = self.tile_labels[self.current_row][self.current_col]
            frame = self.tile_frames[self.current_row][self.current_col]
            tile_bg = "#ffffff" if not self.dark_mode else self.colors["bg"]
            lbl.configure(text="", bg=tile_bg)
            frame.configure(
                bg=tile_bg,
                highlightbackground=self.colors["tile_empty_border"],
                highlightcolor=self.colors["tile_empty_border"],
            )

    def submit_guess(self):
        if self.game_over:
            return
        if self.current_col < 5:
            self.show_popup_message("Not enough letters!")
            return

        guess = "".join(self.board[self.current_row]).lower()

        # validate word
        word_list = self.get_word_list()
        valid_in_list = guess in [w.lower() for w in word_list]
        valid_in_builtin = guess in BUILTIN_WORDS

        if not valid_in_list and not valid_in_builtin:
            # check API
            if not is_real_word_api(guess):
                self.show_popup_message("Not a valid word!")
                return

        # calculate colors
        colors = self.calculate_colors(guess, self.target_word)
        self.board_colors[self.current_row] = colors
        self.game_history_for_share.append(colors[:])

        # update tiles
        for c in range(5):
            lbl = self.tile_labels[self.current_row][c]
            frame = self.tile_frames[self.current_row][c]
            bg = self.colors[colors[c]]
            lbl.configure(bg=bg, fg="#ffffff")
            frame.configure(bg=bg, highlightbackground=bg, highlightcolor=bg)

        # update keyboard colors
        for c in range(5):
            letter = guess[c].upper()
            new_color = colors[c]
            old_color = self.key_colors.get(letter)
            ## priority: correct > present > absent
            priority = {"correct": 3, "present": 2, "absent": 1}
            if old_color is None or priority.get(new_color, 0) > priority.get(old_color, 0):
                self.key_colors[letter] = new_color
            if letter in self.key_buttons:
                kc = self.key_colors[letter]
                bg = self.colors[kc]
                self.key_buttons[letter].configure(bg=bg, fg="#ffffff",
                                                   activebackground=bg, activeforeground="#ffffff")

        # check win/loss
        if guess == self.target_word:
            self.game_over = True
            self.game_won = True
            self.update_stats(won=True, guesses=self.current_row + 1)
            msg = ENCOURAGING_WORDS.get(self.current_row + 1, "Well done! 🎉")
            self.show_popup_message(msg, after_callback=lambda: self.show_end_game_stats())
        elif self.current_row >= 5:
            self.game_over = True
            self.game_won = False
            self.update_stats(won=False)
            self.show_popup_message(
                f'{LOSS_MESSAGE}\nThe word was: {self.target_word.upper()}',
                after_callback=lambda: self.show_end_game_stats()
            )
        else:
            self.current_row += 1
            self.current_col = 0

    def calculate_colors(self, guess, target):
        colors = ["absent"] * 5
        target_list = list(target)
        guess_list = list(guess)

        # first pass: correct
        for i in range(5):
            if guess_list[i] == target_list[i]:
                colors[i] = "correct"
                target_list[i] = None
                guess_list[i] = None

        # second pass: present
        for i in range(5):
            if guess_list[i] is not None:
                if guess_list[i] in target_list:
                    colors[i] = "present"
                    target_list[target_list.index(guess_list[i])] = None

        return colors

    # ========================
    # STATS METHODS
    # ========================
    def _empty_stats(self):
        """Empty stats template."""
        return {
            "played": 0,
            "wins": 0,
            "current_streak": 0,
            "max_streak": 0,
            "guess_distribution": {str(i): 0 for i in range(1, 7)},
        }

    def _get_config_key(self):
        """Get the key of current (lists/game modes) configuration for statistics"""
        if self.game_mode == "default":
            return "default"
        else:
            if not self.selected_user_lists:
                return "default"
            # sorting so that the order does not affect
            sorted_lists = sorted(self.selected_user_lists)
            return " + ".join(sorted_lists)

    def _get_stats_for_key(self, key):
        """Get statistics by the key. Doesn't create if the key doesn't exist."""
        stats = self.data["statistics"]
        if key == "overall":
            return stats["overall"]
        elif key == "default":
            return stats["default"]
        else:
            return stats["user_configs"].get(key, None)

    def _ensure_stats_for_key(self, key):
        """Get or create statistics by the key"""
        stats = self.data["statistics"]
        if key == "overall":
            return stats["overall"]
        elif key == "default":
            return stats["default"]
        else:
            if key not in stats["user_configs"]:
                stats["user_configs"][key] = self._empty_stats()
            return stats["user_configs"][key]

    def _get_all_stats_keys(self):
        """Get the list of all statistics keys for UI"""
        keys = [
            ("🌐 Overall", "overall"),
            ("📚 Default Mode", "default"),
        ]
        for config_name in sorted(self.data["statistics"]["user_configs"].keys()):
            # checking whether lists have been deleted
            list_names = config_name.split(" + ")
            all_exist = all(n in self.data["user_lists"] for n in list_names)
            if all_exist:
                prefix = "📝"
            else:
                prefix = "📝⚠️"
            keys.append((f"{prefix} {config_name}", config_name))
        return keys

    def update_stats(self, won, guesses=None):
        config_key = self._get_config_key()

        # updating overall statistics and statistics for a specific configuration
        keys_to_update = ["overall", config_key]
        # removing the duplicate if "default"
        keys_to_update = list(dict.fromkeys(keys_to_update))

        for key in keys_to_update:
            s = self._ensure_stats_for_key(key)
            s["played"] += 1
            if won:
                s["wins"] += 1
                s["current_streak"] += 1
                if s["current_streak"] > s["max_streak"]:
                    s["max_streak"] = s["current_streak"]
                if guesses:
                    s["guess_distribution"][str(guesses)] += 1
            else:
                s["current_streak"] = 0

        # if user mode uses multiple lists selection ->
        # -> updating the statistics of each individual list too
        if self.game_mode == "user" and len(self.selected_user_lists) > 1:
            for single_list in self.selected_user_lists:
                single_stats = self._ensure_stats_for_key(single_list)
                single_stats["played"] += 1
                if won:
                    single_stats["wins"] += 1
                    single_stats["current_streak"] += 1
                    if single_stats["current_streak"] > single_stats["max_streak"]:
                        single_stats["max_streak"] = single_stats["current_streak"]
                    if guesses:
                        single_stats["guess_distribution"][str(guesses)] += 1
                else:
                    single_stats["current_streak"] = 0

        self.save_data()

    # ========================
    # POPUPS
    # ========================
    def on_escape(self, event=None):
        if self.popup_open:
            if hasattr(self, '_popup_on_close') and self._popup_on_close:
                self._popup_on_close()
            else:
                self.close_popup()

    def bind_mousewheel(self, canvas):
        """
        Bind scroll with mousewheel to all widgets inside some area 
        (e. g.: canvas).
        """

        def on_mousewheel(event):
            """
            Mouse wheel event handler
            """
            # getting actual position of scrolling
            # yview() returns cortege (top, bottom)
            # top = 0.0 - means the very top
            # bottom = 1.0 - means the very bottom
            # if (0.0, 1.0) - all content inside some area can be seen without scrolling
            current_view = canvas.yview()

            # if all content fits inside some area - no need in scroll
            if current_view == (0.0, 1.0):
                return
            
            # defining the direction of scrolling
            # -1 = up, 1 = down
            direction = 0

            if event.delta:
                # win and mac
                direction = -1 if event.delta > 0 else 1
            elif event.num == 4:
                # linux - scroll up
                direction = -1
            elif event.num == 5:
                # linux - scroll down
                direction = 1
            else:
                # if unknown event - ignoring
                return

            # checking borders of scrolling
            # if trying to scroll up, but already in the very top
            if direction < 0 and current_view[0] <= 0.0:
                return

            # if trying to scroll down, but already in the very bottom
            if direction > 0 and current_view[1] >= 1.0:
                return

            canvas.yview_scroll(direction, "units")

        def bind_to_widget(widget):
            # win and mac
            widget.bind("<MouseWheel>", on_mousewheel)
            # linux
            widget.bind("<Button-4>", on_mousewheel)
            widget.bind("<Button-5>", on_mousewheel)

        def bind_recursive(widget):
            bind_to_widget(widget)
            for child in widget.winfo_children():
                bind_recursive(child)

        # bind to canvas
        bind_to_widget(canvas)

        # bind to all children widgets inside some area
        # must be called after all widgets have been created
        canvas.after(100, lambda: bind_recursive(canvas))

    def show_popup_overlay(self, build_func, on_close=None):
        """Show a popup overlay inside the game window."""
        # if popup is already opened - just destroying old one without canceling flags
        if self.popup_overlay and self.popup_overlay.winfo_exists():
            self.popup_overlay.destroy()

        self.popup_open = True

        # saving a custom closing handler
        self._popup_on_close = on_close

        self.popup_overlay = tk.Frame(self.root, bg=self.colors["bg"])
        self.popup_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        # outer frame with frame
        outer = tk.Frame(
            self.popup_overlay,
            bg=self.colors["popup_bg"],
            highlightthickness=2,
            highlightbackground=self.colors["popup_border"],
            highlightcolor=self.colors["popup_border"],
        )
        outer.place(relx=0.05, rely=0.03, relwidth=0.9, relheight=0.94)

        # top bar for close button("x") (fixed, not scrollable)
        top_panel = tk.Frame(outer, bg=self.colors["popup_bg"], height=36)
        top_panel.pack(fill="x", side="top")
        top_panel.pack_propagate(False)

        # close button calls custom or standard "close"
        close_command = on_close if on_close else self.close_popup

        # close button
        close_btn = tk.Button(
            top_panel, text="✕", font=("Helvetica", 16, "bold"),
            bg=self.colors["popup_bg"], fg=self.colors["text"],
            bd=0, highlightthickness=0, relief="flat",
            cursor="hand2", command=close_command,
            activebackground=self.colors["popup_bg"],
            activeforeground=self.colors["text"],
        )
        close_btn.pack(side="right", padx=10, pady=2)

        # frame for content under the top bar and close button (scrollable)
        content = tk.Frame(outer, bg=self.colors["popup_bg"])
        content.pack(fill="both", expand=True)

        build_func(content)

    def close_popup(self):
        if self.popup_overlay and self.popup_overlay.winfo_exists():
            self.popup_overlay.destroy()
            self.popup_overlay = None
        self.popup_open = False
        self.user_input_active = False
        self._popup_on_close = None

    def close_popup_and_return_to_lists(self):
        """Closes editing popup and returns to user's lists popup"""
        if self.popup_overlay and self.popup_overlay.winfo_exists():
            self.popup_overlay.destroy()
            self.popup_overlay = None
        self.popup_open = False
        self.user_input_active = False
        self._popup_on_close = None
        # opening user's lists popup with new data
        self.show_user_lists_popup()

    def show_popup_message(self, message, duration=2500, after_callback=None):
        """Show a small temporary popup message at top of game."""
        msg_frame = tk.Frame(
            self.root,
            bg=self.colors["text"],
            highlightthickness=0,
        )
        msg_label = tk.Label(
            msg_frame, text=message,
            font=("Helvetica", 13, "bold"),
            bg=self.colors["text"],
            fg=self.colors["bg"],
            padx=18, pady=10,
        )
        msg_label.pack()
        msg_frame.place(relx=0.5, rely=0.12, anchor="center")
        msg_frame.lift()

        def remove():
            if msg_frame.winfo_exists():
                msg_frame.destroy()
            if after_callback:
                after_callback()

        self.root.after(duration, remove)

    # ========================
    # RULES POPUP
    # ========================
    def show_rules(self):
        def build(parent):
            title = tk.Label(
                parent, text="How To Play", font=("Helvetica", 20, "bold"),
                bg=self.colors["popup_bg"], fg=self.colors["text"],
            )
            title.pack(pady=(5, 10))

            rules_text = (
                "Guess the word in 6 tries.\n\n"
                "• Each guess must be a valid 5-letter English word.\n"
                "• Press ENTER to submit your guess.\n\n"
                "After each guess, the color of the tiles will\n"
                "change to show how close your guess was:\n\n"
            )
            body = tk.Label(
                parent, text=rules_text, font=("Helvetica", 12),
                bg=self.colors["popup_bg"], fg=self.colors["text"],
                justify="left",
            )
            body.pack(padx=20)

            # Color examples
            examples_frame = tk.Frame(parent, bg=self.colors["popup_bg"])
            examples_frame.pack(pady=5)

            for color, letter, desc in [
                ("correct", "G", "  Green — Correct letter, correct spot"),
                ("present", "Y", "  Yellow — Correct letter, wrong spot"),
                ("absent", "X", "  Gray — Letter not in the word"),
            ]:
                row = tk.Frame(examples_frame, bg=self.colors["popup_bg"])
                row.pack(anchor="w", pady=3, padx=20)
                tile = tk.Label(
                    row, text=letter, width=2, height=1,
                    font=("Helvetica", 16, "bold"),
                    bg=self.colors[color], fg="#ffffff",
                )
                tile.pack(side="left", padx=(0, 10))
                desc_lbl = tk.Label(
                    row, text=desc, font=("Helvetica", 11),
                    bg=self.colors["popup_bg"], fg=self.colors["text"],
                )
                desc_lbl.pack(side="left")

            modes_text = (
                "\n\n🎮 Game Modes:\n\n"
                "• Default Mode — Random words from built-in list\n"
                "• User Mode — Your custom word lists for learning\n"
                "  vocabulary! Create multiple lists and switch\n"
                "  between them.\n"
            )
            modes = tk.Label(
                parent, text=modes_text, font=("Helvetica", 12),
                bg=self.colors["popup_bg"], fg=self.colors["text"],
                justify="left",
            )
            modes.pack(padx=20)

        self.show_popup_overlay(build)

    # ========================
    # STATS POPUP
    # ========================
    def show_stats(self):
        self._show_stats_popup()

    def show_end_game_stats(self):
        self._show_stats_popup(end_game=True)

    def _show_stats_popup(self, end_game=False):
        def build(parent):
            # --- scrollable frame ---
            canvas = tk.Canvas(parent, highlightthickness=0)
            scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas)

            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            # centering stats
            canvas_window = canvas.create_window(
                (0, 0), window=scroll_frame, anchor="n"
            )

            # configuring canvas_window width to canvas width
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
                canvas.coords(canvas_window, event.width / 2, 0)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True, padx=10, pady=(5, 10))
            scrollbar.pack(side="right", fill="y")

            # painting canvas and scrollbar
            canvas.configure(bg=self.colors["popup_bg"])
            scroll_frame.configure(bg=self.colors["popup_bg"])

            # --- title ---
            tk.Label(
                scroll_frame, text="Statistics", font=("Helvetica", 20, "bold"),
                bg=self.colors["popup_bg"], fg=self.colors["text"],
            ).pack(pady=(5, 10))

            # --- statistics selector ---
            selector_frame = tk.Frame(scroll_frame, bg=self.colors["popup_bg"])
            selector_frame.pack(pady=(0, 10))

            tk.Label(
                selector_frame, text="View:",
                font=("Helvetica", 11),
                bg=self.colors["popup_bg"], fg=self.colors["text"],
            ).pack(side="left", padx=5)

            stats_keys = self._get_all_stats_keys()
            display_names = [item[0] for item in stats_keys]
            key_values = [item[1] for item in stats_keys]

            # current choice
            if end_game:
                current_config = self._get_config_key()
                if current_config in key_values:
                    default_idx = key_values.index(current_config)
                else:
                    default_idx = 0
            else:
                default_idx = 0

            selected_var = tk.StringVar(value=display_names[default_idx])

            combo = ttk.Combobox(
                selector_frame, textvariable=selected_var,
                values=display_names, state="readonly",
                width=35, font=("Helvetica", 10),
            )
            combo.pack(side="left", padx=5)

            # --- frame for content of statistics ---
            stats_content = tk.Frame(scroll_frame, bg=self.colors["popup_bg"])
            stats_content.pack(fill="x", pady=5)

            def render_stats(stats_key):
                # cleaning
                for widget in stats_content.winfo_children():
                    widget.destroy()

                stats = self._get_stats_for_key(stats_key)
                if stats is None:
                    tk.Label(
                        stats_content, text="No games played yet in this configuration.",
                        font=("Helvetica", 12),
                        bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
                    ).pack(pady=20)
                    return

                # --- stats row ---
                stats_row = tk.Frame(stats_content, bg=self.colors["popup_bg"])
                stats_row.pack(pady=5)

                win_pct = int(stats["wins"] / stats["played"] * 100) if stats["played"] > 0 else 0
                for value, label in [
                    (stats["played"], "Played"),
                    (win_pct, "Win %"),
                    (stats["current_streak"], "Current\nStreak"),
                    (stats["max_streak"], "Max\nStreak"),
                ]:
                    col = tk.Frame(stats_row, bg=self.colors["popup_bg"])
                    col.pack(side="left", padx=12)
                    tk.Label(
                        col, text=str(value), font=("Helvetica", 24, "bold"),
                        bg=self.colors["popup_bg"], fg=self.colors["text"],
                    ).pack()
                    tk.Label(
                        col, text=label, font=("Helvetica", 10),
                        bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
                    ).pack()

                # --- guess distribution ---
                tk.Label(
                    stats_content, text="Guess Distribution",
                    font=("Helvetica", 14, "bold"),
                    bg=self.colors["popup_bg"], fg=self.colors["text"],
                ).pack(pady=(15, 5))

                dist = stats["guess_distribution"]
                max_val = max(int(v) for v in dist.values()) if any(int(v) > 0 for v in dist.values()) else 1

                dist_frame = tk.Frame(stats_content, bg=self.colors["popup_bg"])
                dist_frame.pack(pady=3)

                for i in range(1, 7):
                    row = tk.Frame(dist_frame, bg=self.colors["popup_bg"])
                    row.pack(fill="x", padx=30, pady=1)
                    tk.Label(
                        row, text=str(i), font=("Helvetica", 12, "bold"),
                        bg=self.colors["popup_bg"], fg=self.colors["text"],
                        width=2,
                    ).pack(side="left")
                    val = int(dist[str(i)])
                    is_current = (end_game and self.game_won and (self.current_row + 1) == i 
                        and stats_key == self._get_config_key())
                    bar_color = self.colors["correct"] if is_current else self.colors["absent"]
                    bar_width = max(3, int(val / max_val * 15) + 3) if max_val > 0 else 3
                    tk.Label(
                        row, text=f" {val} ", font=("Helvetica", 11, "bold"),
                        bg=bar_color, fg="#ffffff",
                        width=bar_width,
                        anchor="e",
                    ).pack(side="left", padx=4)

            def on_combo_change(event=None):
                idx = display_names.index(selected_var.get())
                render_stats(key_values[idx])

            combo.bind("<<ComboboxSelected>>", on_combo_change)

            # initial render
            render_stats(key_values[default_idx])

            # --- end game details ---
            if end_game:
                tk.Frame(scroll_frame, bg=self.colors["popup_border"],
                    height=2
                ).pack(fill="x", padx=40, pady=15) #padx=20

                result_text = "YOU WON! 🎉" if self.game_won else "YOU LOST 😢"
                result_color = self.colors["correct"] if self.game_won else "#e74c3c"
                tk.Label(
                    scroll_frame, text=result_text,
                    font=("Helvetica", 16, "bold"),
                    bg=self.colors["popup_bg"], fg=result_color,
                ).pack(pady=5)

                tk.Label(
                    scroll_frame, text=f"The word was: {self.target_word.upper()}",
                    font=("Helvetica", 14, "bold"),
                    bg=self.colors["popup_bg"], fg=self.colors["text"],
                ).pack(pady=3)

                ## --- game mode ---
                config_key = self._get_config_key()
                if config_key == "default":
                    mode_display = "Mode: Default"
                else:
                    total_words = len(self.get_word_list())
                    mode_display = f"Mode: User ({config_key}) — {total_words} words"

                tk.Label(
                    scroll_frame, text=mode_display, font=("Helvetica", 10),
                    bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
                ).pack(pady=2)

                ## --- definition ---
                def fetch_def():
                    defn = get_definition_api(self.target_word)
                    if def_label.winfo_exists():
                        def_label.configure(text=f"Definition: {defn}")

                def_label = tk.Label(
                    scroll_frame, text="Definition: Loading...",
                    font=("Helvetica", 11, "italic"),
                    bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
                    justify="center",
                )
                def_label.pack(pady=5, padx=20, fill="x")

                ## dinamicly configuring wraplength which would equals the width of the parent
                def update_wraplength(event):
                    if def_label.winfo_exists():
                        ### width of the parent minus indentations
                        new_width = event.width - 60
                        if new_width > 50:
                            def_label.configure(wraplength=new_width)

                scroll_frame.bind("<Configure>", lambda e: update_wraplength(e), add="+")

                threading.Thread(target=fetch_def, daemon=True).start()

                ## --- game board copy ---
                tk.Label(
                    scroll_frame, text="Your Game:",
                    font=("Helvetica", 12, "bold"),
                    bg=self.colors["popup_bg"], fg=self.colors["text"],
                ).pack(pady=(10, 3))

                board_copy = tk.Frame(scroll_frame, bg=self.colors["popup_bg"])
                board_copy.pack(pady=3)

                rows_played = self.current_row + 1 if self.game_won else min(self.current_row + 1, 6)

                for r in range(rows_played):
                    row_f = tk.Frame(board_copy, bg=self.colors["popup_bg"])
                    row_f.pack()
                    for c in range(5):
                        color = self.board_colors[r][c]
                        bg_c = self.colors.get(color, self.colors["tile_bg"]) if color else self.colors["tile_bg"]
                        letter = self.board[r][c]
                        tk.Label(
                            row_f, text=letter, width=2, height=1,
                            font=("Helvetica", 16, "bold"),
                            bg=bg_c, fg="#ffffff",
                            highlightthickness=1,
                            highlightbackground=bg_c,
                            highlightcolor=bg_c,
                        ).pack(side="left", padx=1, pady=1)

                ## --- share buttons ---
                share_frame = tk.Frame(scroll_frame, bg=self.colors["popup_bg"])
                share_frame.pack(pady=15)

                tk.Button(
                    share_frame, text="📋 Copy to Clipboard",
                    font=("Helvetica", 12, "bold"),
                    bg=self.colors["button_bg"], fg=self.colors["button_text"],
                    bd=0, highlightthickness=0, relief="flat",
                    padx=15, pady=8, cursor="hand2",
                    command=self.share_text,
                    activebackground=self.colors["correct"],
                ).pack(side="left", padx=5)

                tk.Button(
                    share_frame, text="🖼️ Save as Image",
                    font=("Helvetica", 12, "bold"),
                    bg=self.colors["button_bg"], fg=self.colors["button_text"],
                    bd=0, highlightthickness=0, relief="flat",
                    padx=15, pady=8, cursor="hand2",
                    command=self.share_image,
                    activebackground=self.colors["correct"],
                ).pack(side="left", padx=5)

                ## --- new game button ---
                def new_game_and_close():
                    self.close_popup()
                    self.start_new_game()

                tk.Button(
                    scroll_frame, text="🔄 New Game",
                    font=("Helvetica", 14, "bold"),
                    bg=self.colors["button_bg"], fg=self.colors["button_text"],
                    bd=0, highlightthickness=0, relief="flat",
                    padx=25, pady=10, cursor="hand2",
                    command=new_game_and_close,
                    activebackground=self.colors["correct"],
                ).pack(pady=(5, 20))

            # bind scroll with mousewheel to all widgets inside canvas
            self.bind_mousewheel(canvas)

        self.show_popup_overlay(build)

    # ========================
    # SHARING
    # ========================
    def share_text(self):
        """Copy game result as emoji text to clipboard."""
        color_emoji = {
            "correct": "🟩",
            "present": "🟨",
            "absent": "⬛",
        }
        today = datetime.date.today().strftime("%Y-%m-%d")
        rows = len(self.game_history_for_share)
        score = f"{'X' if not self.game_won else rows}/6"

        # defining the game mode
        if self.game_mode == "user" and self.selected_user_lists:
            lists_names = ", ".join(self.selected_user_lists)
            total_words = len(self.get_word_list())
            mode_text = f"Mode: User ({lists_names}) — {total_words} words"
        else:
            mode_text = "Mode: Default"

        result = f"WordleX {today} {score}\n"
        result += f"{mode_text}\n\n"

        for row_colors in self.game_history_for_share:
            result += "".join(color_emoji.get(c, "⬛") for c in row_colors) + "\n"

        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.show_popup_message("Copied to clipboard! 📋")

    def share_image(self):
        """Save game result as PNG image."""
        color_map = {
            "correct": (106, 170, 100),
            "present": (201, 180, 88),
            "absent": (120, 124, 126),
        }
        tile_size = 62
        gap = 5
        padding = 30
        rows = len(self.game_history_for_share)
        if rows == 0:
            return

        width = padding * 2 + 5 * tile_size + 4 * gap
        header_height = 90 #60
        height = header_height + padding + rows * (tile_size + gap) + padding

        bg_color = (18, 18, 19) if self.dark_mode else (255, 255, 255)
        text_color = (255, 255, 255) if self.dark_mode else (0, 0, 0)
        mode_color = (170, 170, 170) if self.dark_mode else (100, 100, 100)

        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        try:
            font_title = ImageFont.truetype("arial.ttf", 24)
            font_mode = ImageFont.truetype("arial.ttf", 14)
            font_letter = ImageFont.truetype("arial.ttf", 28)
        except Exception:
            font_title = ImageFont.load_default()
            font_mode = ImageFont.load_default()
            font_letter = ImageFont.load_default()

        # title
        today = datetime.date.today().strftime("%Y-%m-%d")
        score = f"{'X' if not self.game_won else rows}/6"
        title_text = f"WordleX  {today}  {score}"
        bbox = draw.textbbox((0, 0), title_text, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, 12), title_text, fill=text_color, font=font_title)

        # mode string
        if self.game_mode == "user" and self.selected_user_lists:
            lists_names = ", ".join(self.selected_user_lists)
            total_words = len(self.get_word_list())
            mode_text = f"Mode: User ({lists_names}) — {total_words} words"
        else:
            mode_text = "Mode: Default"

        bbox = draw.textbbox((0, 0), mode_text, font=font_mode)
        mw = bbox[2] - bbox[0]
        draw.text(((width - mw) // 2, 45), mode_text, fill=mode_color, font=font_mode)

        # tiles
        y = header_height + padding // 2
        for r_idx, row_colors in enumerate(self.game_history_for_share):
            x = padding
            for c_idx in range(5):
                color = color_map.get(row_colors[c_idx], (120, 124, 126))
                draw.rectangle([x, y, x + tile_size, y + tile_size], fill=color)
                letter = self.board[r_idx][c_idx]
                bbox = draw.textbbox((0, 0), letter, font=font_letter)
                lw = bbox[2] - bbox[0]
                lh = bbox[3] - bbox[1]
                draw.text(
                    (x + (tile_size - lw) // 2, y + (tile_size - lh) // 2 - 4),
                    letter, fill=(255, 255, 255), font=font_letter,
                )
                x += tile_size + gap
            y += tile_size + gap

        # save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=f"WordleX_{today}.png",
        )
        if file_path:
            img.save(file_path)
            self.show_popup_message("Image saved! 🖼️")

    # ========================
    # USER LISTS POPUP
    # ========================
    def show_user_lists_popup(self):
        self.user_input_active = True

        def build(parent):
            title = tk.Label(
                parent, text="📝 User Word Lists", font=("Helvetica", 18, "bold"),
                bg=self.colors["popup_bg"], fg=self.colors["text"],
            )
            title.pack(pady=(5, 5))

            instructions = tk.Label(
                parent, text=(
                    "Create custom 5-letter word lists for learning vocabulary.\n"
                    "Words are validated against the dictionary.\n"
                    "Select one or more lists to use in User Mode."
                ),
                font=("Helvetica", 10),
                bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
                justify="center",
            )
            instructions.pack(pady=(0, 10))

            # --- creating new list ---
            new_list_frame = tk.Frame(parent, bg=self.colors["popup_bg"])
            new_list_frame.pack(pady=5)

            tk.Label(
                new_list_frame, text="New List Name:",
                font=("Helvetica", 11),
                bg=self.colors["popup_bg"], fg=self.colors["text"],
            ).pack(side="left", padx=5)

            new_list_entry = tk.Entry(
                new_list_frame, font=("Helvetica", 12),
                bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
                insertbackground=self.colors["text"],
                width=15, relief="flat",
                highlightthickness=1,
                highlightbackground=self.colors["popup_border"],
            )
            new_list_entry.pack(side="left", padx=5)

            def create_list():
                name = new_list_entry.get().strip()
                if not name:
                    self.show_popup_message("Enter a list name!")
                    return
                if name in self.data["user_lists"]:
                    self.show_popup_message("List already exists!")
                    return
                self.data["user_lists"][name] = []
                self.save_data()
                # repainting the popup
                if self.popup_overlay and self.popup_overlay.winfo_exists():
                    self.popup_overlay.destroy()
                    self.popup_overlay = None
                self.popup_open = False
                self.user_input_active = False
                self.show_user_lists_popup()

            tk.Button(
                new_list_frame, text="Create",
                font=("Helvetica", 11, "bold"),
                bg=self.colors["button_bg"], fg=self.colors["button_text"],
                bd=0, highlightthickness=0, relief="flat",
                padx=10, pady=3, cursor="hand2",
                command=create_list,
            ).pack(side="left", padx=5)

            # --- delimiter ---
            tk.Frame(parent, bg=self.colors["popup_border"], height=2
            ).pack(fill="x", padx=20, pady=10)

            # --- lists ---
            lists_canvas = tk.Canvas(parent, bg=self.colors["popup_bg"], highlightthickness=0)
            lists_scrollbar = tk.Scrollbar(parent, orient="vertical", command=lists_canvas.yview)
            lists_frame = tk.Frame(lists_canvas, bg=self.colors["popup_bg"])

            lists_frame.bind(
                "<Configure>",
                lambda e: lists_canvas.configure(scrollregion=lists_canvas.bbox("all"))
            )

            canvas_window = lists_canvas.create_window((0, 0), window=lists_frame, anchor="nw")

            def on_lists_canvas_configure(event):
                lists_canvas.itemconfig(canvas_window, width=event.width)

            lists_canvas.bind("<Configure>", on_lists_canvas_configure)
            lists_canvas.configure(yscrollcommand=lists_scrollbar.set)

            lists_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
            lists_scrollbar.pack(side="right", fill="y")

            # reading the data right now from self.data
            user_lists = self.data.get("user_lists", {})
            selected = self.selected_user_lists

            if not user_lists:
                tk.Label(
                    lists_frame, text="No lists yet. Create one above!",
                    font=("Helvetica", 12), bg=self.colors["popup_bg"],
                    fg=self.colors["text_secondary"],
                ).pack(pady=20)
            else:
                for list_name in user_lists:
                    words = user_lists[list_name]
                    is_active = (list_name in selected)

                    lf = tk.Frame(
                        lists_frame, bg=self.colors["popup_bg"],
                        highlightthickness=2,
                        highlightbackground=self.colors["correct"] if is_active else self.colors["popup_border"],
                        highlightcolor=self.colors["correct"] if is_active else self.colors["popup_border"],
                    )
                    lf.pack(fill="x", padx=10, pady=4, expand=False)

                    header = tk.Frame(lf, bg=self.colors["popup_bg"])
                    header.pack(fill="x", padx=5, pady=3)

                    # emoji depends on is_active
                    emoji = "✅" if is_active else "⬜"
                    tk.Label(
                        header,
                        text=f"{emoji} {list_name} ({len(words)} words)",
                        font=("Helvetica", 12, "bold"),
                        bg=self.colors["popup_bg"], fg=self.colors["text"],
                        anchor="w",
                    ).pack(side="left", fill="x", expand=True)

                    btn_frame = tk.Frame(header, bg=self.colors["popup_bg"])
                    btn_frame.pack(side="right")

                    # a text and a colour of the button depend on is_active
                    select_text = "Deselect" if is_active else "Select"
                    select_bg = self.colors["absent"] if is_active else self.colors["correct"]

                    tk.Button(
                        btn_frame, text=select_text,
                        font=("Helvetica", 9, "bold"),
                        bg=select_bg, fg="#ffffff",
                        bd=0, highlightthickness=0, relief="flat",
                        padx=6, pady=2, cursor="hand2",
                        command=lambda n=list_name: self.select_user_list(n),
                    ).pack(side="left", padx=2)

                    tk.Button(
                        btn_frame, text="Edit",
                        font=("Helvetica", 9, "bold"),
                        bg=self.colors["present"], fg="#ffffff",
                        bd=0, highlightthickness=0, relief="flat",
                        padx=6, pady=2, cursor="hand2",
                        command=lambda n=list_name: self.edit_user_list(n),
                    ).pack(side="left", padx=2)

                    tk.Button(
                        btn_frame, text="Delete",
                        font=("Helvetica", 9, "bold"),
                        bg="#e74c3c", fg="#ffffff",
                        bd=0, highlightthickness=0, relief="flat",
                        padx=6, pady=2, cursor="hand2",
                        command=lambda n=list_name: self.delete_user_list(n),
                    ).pack(side="left", padx=2)

                    # words preview
                    if words:
                        preview = ", ".join(words[:10])
                        if len(words) > 10:
                            preview += f", ... (+{len(words) - 10} more)"
                        tk.Label(
                            lf, text=preview, font=("Helvetica", 9),
                            bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
                            wraplength=380, justify="left",
                        ).pack(padx=10, pady=(0, 5), anchor="w")

                # total selected
                if selected:
                    total_words = sum(
                        len(user_lists.get(n, []))
                        for n in selected
                        if n in user_lists
                    )
                    selected_text = f"Selected: {len(selected)} lists, {total_words} words total"

                    tk.Label(
                        lists_frame, text=selected_text,
                        font=("Helvetica", 11, "bold"),
                        bg=self.colors["popup_bg"], fg=self.colors["correct"],
                    ).pack(pady=(10, 5))

            self.bind_mousewheel(lists_canvas)

        self.show_popup_overlay(build)

    def select_user_list(self, name):
        if name in self.selected_user_lists:
            self.selected_user_lists.remove(name)
        else:
            self.selected_user_lists.append(name)
        self.save_data()

        # destroying the popup
        if self.popup_overlay and self.popup_overlay.winfo_exists():
            self.popup_overlay.destroy()
            self.popup_overlay = None
        self.popup_open = False
        self.user_input_active = False

        # restarting the game with the new selection of the user's lists
        if self.game_mode == "user":
            self.start_new_game()

        # repainting the popup
        self.show_user_lists_popup()

    def delete_user_list(self, name):
        if name in self.data["user_lists"]:
            del self.data["user_lists"][name]
        if name in self.selected_user_lists:
            self.selected_user_lists.remove(name)
        # not deleting statistics, it will remain as archived
        self.save_data()

        # destroying the popup
        if self.popup_overlay and self.popup_overlay.winfo_exists():
            self.popup_overlay.destroy()
            self.popup_overlay = None
        self.popup_open = False
        self.user_input_active = False

        # restarting the game with the new selection of the user's lists
        if self.game_mode == "user":
            self.start_new_game()

        # repainting the popup
        self.show_user_lists_popup()

    def edit_user_list(self, name):
        self.user_input_active = True

        # saving the actual name to have an ability to rename
        current_name = [name]

        def build(parent):

            # --- header with an ability to rename ---
            title_frame = tk.Frame(parent, bg=self.colors["popup_bg"], height=40) #there wasn't height=40
            title_frame.pack(pady=(5, 5), fill="x", padx=20)
            title_frame.pack_propagate(False)

            title_label = tk.Label(
                title_frame, text=f"Edit: {current_name[0]}",
                font=("Helvetica", 18, "bold"),
                bg=self.colors["popup_bg"], fg=self.colors["text"],
            )
            title_label.place(relx=0.5, rely=0.5, anchor="center")

            ## button for renaming
            rename_btn = tk.Button(
                title_frame, text="✏️ Rename",
                font=("Helvetica", 10, "bold"),
                bg="#3498db", fg="#ffffff",
                bd=0, highlightthickness=0, relief="flat",
                padx=8, pady=2, cursor="hand2",
            )
            rename_btn.pack(side="right")

            # --- frame for renaming (hidden by default) ---
            rename_frame = tk.Frame(parent, bg=self.colors["popup_bg"])

            rename_inner = tk.Frame(rename_frame, bg=self.colors["popup_bg"])
            rename_inner.pack()

            rename_entry = tk.Entry(
                rename_inner, font=("Helvetica", 14),
                bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
                insertbackground=self.colors["text"],
                width=20, relief="flat",
                highlightthickness=2,
                highlightbackground=self.colors["popup_border"],
                highlightcolor=self.colors["correct"],
            )
            rename_entry.pack(side="left", padx=5)

            rename_status = tk.Label(
                rename_frame, text="",
                font=("Helvetica", 9, "italic"),
                bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
            )

            rename_save_btn = tk.Button(
                rename_inner, text="Save",
                font=("Helvetica", 10, "bold"),
                bg=self.colors["correct"], fg="#ffffff",
                bd=0, highlightthickness=0, relief="flat",
                padx=8, pady=2, cursor="hand2",
            )
            rename_save_btn.pack(side="left", padx=3)

            rename_cancel_btn = tk.Button(
                rename_inner, text="Cancel",
                font=("Helvetica", 10, "bold"),
                bg=self.colors["absent"], fg="#ffffff",
                bd=0, highlightthickness=0, relief="flat",
                padx=8, pady=2, cursor="hand2",
            )
            rename_cancel_btn.pack(side="left", padx=3)

            rename_status.pack(pady=(3, 0))

            def show_rename():
                rename_frame.pack(after=title_frame, pady=5, padx=20, fill="x")
                rename_entry.delete(0, tk.END)
                rename_entry.insert(0, current_name[0])
                rename_entry.select_range(0, tk.END)
                rename_entry.focus_set()
                rename_btn.configure(state="disabled")

            def hide_rename():
                rename_frame.pack_forget()
                rename_status.configure(text="")
                rename_btn.configure(state="normal")
                word_entry.focus_set()

            def do_rename(event=None):
                new_name = rename_entry.get().strip()
                old_name = current_name[0]

                if not new_name:
                    rename_status.configure(text="Name cannot be empty!", fg="#e74c3c")
                    return
                if new_name == old_name:
                    hide_rename()
                    return
                if new_name in self.data["user_lists"]:
                    rename_status.configure(text="Name already exists!", fg="#e74c3c")
                    return

                # transfering data
                self.data["user_lists"][new_name] = self.data["user_lists"].pop(old_name)

                # updating selected lists
                if old_name in self.selected_user_lists:
                    idx = self.selected_user_lists.index(old_name)
                    self.selected_user_lists[idx] = new_name

                # migration of statistics
                user_configs = self.data["statistics"]["user_configs"]
                keys_to_rename = {}
                for config_key in list(user_configs.keys()):
                    list_names = config_key.split(" + ")
                    if old_name in list_names:
                        new_list_names = [new_name if n == old_name else n for n in list_names]
                        new_key = " + ".join(sorted(new_list_names))
                        keys_to_rename[config_key] = new_key

                for old_key, new_key in keys_to_rename.items():
                    if new_key not in user_configs:
                        user_configs[new_key] = user_configs.pop(old_key)
                    else:
                        # if new key already exists -> uniting
                        user_configs.pop(old_key)

                current_name[0] = new_name
                self.save_data()

                # updating the header
                title_label.configure(text=f"Edit: {new_name}")
                words_header.configure(text=f"Words in '{new_name}': ({len(self.data['user_lists'].get(new_name, []))})")
                hide_rename()

            rename_entry.bind("<Return>", do_rename)
            rename_entry.bind("<Escape>", lambda e: hide_rename())
            rename_save_btn.configure(command=do_rename)
            rename_cancel_btn.configure(command=hide_rename)
            rename_btn.configure(command=show_rename)

            # --- instructions ---
            instructions = tk.Label(
                parent, text=(
                    "Type a 5-letter English word and press Enter to add it.\n"
                    "Only valid English words are accepted (verified via dictionary).\n"
                    "Maximum 5 letters — extra characters are ignored."
                ),
                font=("Helvetica", 10),
                bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
                justify="center",
            )
            instructions.pack(pady=(0, 10))

            # --- input bar ---
            input_frame = tk.Frame(parent, bg=self.colors["popup_bg"])
            input_frame.pack(pady=5)

            ## custom entry that limits to 5 letters
            word_var = tk.StringVar()

            def validate_input(*args):
                val = word_var.get()
                # only alphabetic, max 5
                filtered = ''.join(c for c in val if c.isalpha())[:5]
                if filtered != val:
                    word_var.set(filtered)

            word_var.trace_add("write", validate_input)

            word_entry = tk.Entry(
                input_frame, textvariable=word_var,
                font=("Helvetica", 18, "bold"),
                bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
                insertbackground=self.colors["text"],
                width=8, justify="center",
                relief="flat",
                highlightthickness=2,
                highlightbackground=self.colors["popup_border"],
                highlightcolor=self.colors["correct"],
            )
            word_entry.pack(side="left", padx=5)
            word_entry.focus_set()

            status_label = tk.Label(
                parent, text="",
                font=("Helvetica", 10, "italic"),
                bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
            )
            status_label.pack(pady=3)

            def add_word(event=None):
                word = word_var.get().strip().lower()
                if len(word) != 5:
                    status_label.configure(text="Word must be exactly 5 letters!", fg="#e74c3c")
                    return

                # reading actual words from self.data
                list_name = current_name[0]
                current_words = [w.lower() for w in self.data["user_lists"].get(list_name, [])]
                if word in current_words:
                    status_label.configure(text="Word already in list!", fg="#e74c3c")
                    return

                status_label.configure(text="Checking dictionary...",
                    fg=self.colors["text_secondary"])
                parent.update()

                def check():
                    is_valid = is_real_word_api(word)
                    if not parent.winfo_exists():
                        return
                    if is_valid:
                        # directly adding word to self.data
                        ln = current_name[0]
                        if ln in self.data["user_lists"]:
                            self.data["user_lists"][ln].append(word.upper())
                            self.save_data()
                        word_var.set("")
                        status_label.configure(text=f"✅ '{word.upper()}' added!", fg=self.colors["correct"])
                        refresh_word_list()
                    else:
                        status_label.configure(text=f"❌ '{word.upper()}' is not a valid English word.", fg="#e74c3c")

                threading.Thread(target=check, daemon=True).start()

            word_entry.bind("<Return>", add_word)

            enter_btn = tk.Button(
                input_frame, text="Enter",
                font=("Helvetica", 12, "bold"),
                bg=self.colors["button_bg"], fg=self.colors["button_text"],
                bd=0, highlightthickness=0, relief="flat",
                padx=12, pady=6, cursor="hand2",
                command=add_word,
            )
            enter_btn.pack(side="left", padx=5)

            # bind backspace for this entry
            def on_backspace(event):
                pass    # default behavior handles it

            word_entry.bind("<BackSpace>", on_backspace)

            tk.Frame(parent, bg=self.colors["popup_border"], height=2,
            ).pack(fill="x", padx=20, pady=10)

            # --- words list ---
            ## words list header
            words_header = tk.Label(
                parent, text="",font=("Helvetica", 12, "bold"),
                bg=self.colors["popup_bg"], fg=self.colors["text"],
            )
            words_header.pack(pady=(5, 3))

            ## scrollable word list
            words_canvas = tk.Canvas(parent, bg=self.colors["popup_bg"],
                highlightthickness=0)
            words_scrollbar = tk.Scrollbar(parent, orient="vertical",
                command=words_canvas.yview)
            words_frame = tk.Frame(words_canvas, bg=self.colors["popup_bg"])

            words_frame.bind(
                "<Configure>",
                lambda e: words_canvas.configure(scrollregion=words_canvas.bbox("all"))
            )
            canvas_window = words_canvas.create_window((0, 0), window=words_frame, anchor="nw")

            # make the inner frame fill the canvas width
            def on_words_canvas_configure(event):
                words_canvas.itemconfig(canvas_window, width=event.width)

            words_canvas.bind("<Configure>", on_words_canvas_configure)
            words_canvas.configure(yscrollcommand=words_scrollbar.set)
            words_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
            words_scrollbar.pack(side="right", fill="y")

            def refresh_word_list():
                for widget in words_frame.winfo_children():
                    widget.destroy()

                list_name = current_name[0]

                # reading words directly from self.data
                words = self.data["user_lists"].get(list_name, [])

                # refreshing words_header
                words_header.configure(text=f"Words in '{list_name}': ({len(words)})")

                if not words:
                    tk.Label(
                        words_frame, text="No words yet. Add some above!",
                        font=("Helvetica", 11),
                        bg=self.colors["popup_bg"], fg=self.colors["text_secondary"],
                    ).pack(pady=10)
                else:
                    for i, w in enumerate(words):
                        wf = tk.Frame(words_frame, bg=self.colors["popup_bg"])
                        wf.pack(fill="x", padx=5, pady=1)
                        tk.Label(
                            wf, text=f"{i + 1}. {w}",
                            font=("Helvetica", 11),
                            bg=self.colors["popup_bg"], fg=self.colors["text"],
                            anchor="w",
                        ).pack(side="left", padx=5)
                        tk.Button(
                            wf, text="✕", font=("Helvetica", 9, "bold"),
                            bg="#e74c3c", fg="#ffffff",
                            bd=0, highlightthickness=0, relief="flat",
                            padx=5, pady=1, cursor="hand2",
                            command=lambda word=w: remove_word(word),
                        ).pack(side="right", padx=5)

            def remove_word(word):
                list_name = current_name[0]
                if list_name in self.data["user_lists"]:
                    if word in self.data["user_lists"][list_name]:
                        self.data["user_lists"][list_name].remove(word)
                        self.save_data()
                        refresh_word_list()

            # instantly showing words when opening editing popup
            refresh_word_list()

            # bind scroll with mousewheel to all widgets inside words_canvas
            self.bind_mousewheel(words_canvas)

        self.show_popup_overlay(build, on_close=self.close_popup_and_return_to_lists)

# ========================
# MAIN
# ========================
def main():
    root = tk.Tk()

    # set icon if available
    try:
        icon_path = resource_path("wordlex_icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        pass

    app = WordleX(root)
    root.mainloop()

if __name__ == "__main__":
    main()
