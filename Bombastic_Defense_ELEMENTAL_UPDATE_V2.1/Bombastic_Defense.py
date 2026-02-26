from tkinter import *
from tkinter import font as tkfont
import math
import random
import pygame
from PIL import Image, ImageTk
import time

DIFFICULTIES = {
    "easy": {
        "label": "🟢 Easy",
        "enemy_hp": 0.8,
        "start_money": 1000000,
        "wave_size": 0.85,
        "boss_hp_mult": 0.7,
        "bank_bonus": 1.2,
        "color": "#2ecc71",
        "player_hp": 50,
        "enemy_speed_mult": 1.0,
        "tower_cost_mult": 1.0,
        "desc": "850 startcash\nweak boss\nweaker enemies\nfat bank bonus"
    },
    "normal": {
        "label": "🟡 Medium",
        "enemy_hp": 1.0,
        "start_money": 450,
        "wave_size": 1.1,
        "boss_hp_mult": 1.0,
        "bank_bonus": 1.0,
        "color": "#f1c40f",
        "player_hp": 50,
        "enemy_speed_mult": 1.0,
        "tower_cost_mult": 1.0,
        "desc": "450 startcash\nstandard boss\nstandard enemies"
    },
    "hard": {
        "label": "🔴 hard",
        "enemy_hp": 1.3,
        "start_money": 400,
        "wave_size": 1.5,
        "boss_hp_mult": 1.4,
        "bank_bonus": 0.9,
        "color": "#e74c3c",
        "player_hp": 50,
        "enemy_speed_mult": 1.0,
        "tower_cost_mult": 1.0,
        "desc": "400 startcash\nbigger waves\nmega boss\nevery wave hurts"
    },
    "nightmare": {
        "label": "💀 Impossible",
        "enemy_hp": 2.2,
        "start_money": 350,
        "wave_size": 2.4,
        "boss_hp_mult": 3.0,
        "bank_bonus": 0.5,
        "color": "#9b00ff",
        "player_hp": 20,
        "enemy_speed_mult": 1.4,
        "tower_cost_mult": 1.3,
        "desc": "350 startcash\n20 player HP\n2.2x enemy hp\n+40% enemy speed\ntowers cost +30%\nboss is a monster"
    },
}

MAPS = {
    "classic": {
        "name": "OG map",
        "desc": "The one and only \noriginal map",
        "color": "#2ecc71",
        "path": [(20,470),(310,470),(310,300),(60,300),(60,180),(850,180),(850,500),(950,500)],
        "use_png": True,
        "road_color":  "#b8860b",
        "grass_color": "#1a3a1a",
    },
    "serpentine": {
        "name": "Highway",
        "desc": "good crowd control\n nice starter map",
        "color": "#e74c3c",
        "path": [
            (30,  640), (1040, 640),
            (1040, 510),(50,  510),
            (50,  380), (1040, 380),
            (1040, 250),(50,  250),
            (50,  120), (540, 120),
        ],
        "use_png": False,
        "road_color":  "#8B6914",
        "grass_color": "#162a16",
    },
    "circle": {
        "name": "Circle",
        "desc": "circular map\nlimited placement",
        "color": "#a29bfe",
        "path": [
            (1070, 350),
            (1070, 620), (550, 660), (80,  620),
            (50,  350),  (80,  80),  (550, 40),  (1020, 80),
            (980, 350),  (920, 570), (550, 610), (180, 570),
            (150, 350),  (180, 130), (550, 90),  (870, 130),
            (870, 350),  (820, 510), (550, 545), (280, 510),
            (260, 350),  (550, 350),
        ],
        "use_png": False,
        "road_color":  "#6B4E8B",
        "grass_color": "#0f0f28",
    },

    # ── NEW MAPS ────────────────────────────────────────────────────────────

    "twin_gates": {
        "name": "Twin Gates",
        "desc": "Two spawn points!\nDivide your defenses.",
        "color": "#00cec9",
        # Two separate entry paths that merge into one shared route
        "paths": [
            # TOP path: enters top-left, sweeps down to merge point, then exits right
            [(20, 130), (340, 130), (340, 370), (700, 370), (700, 540), (1080, 540)],
            # BOTTOM path: enters bottom-left, sweeps up to merge point, then exits right
            [(20, 590), (340, 590), (340, 370), (700, 370), (700, 540), (1080, 540)],
        ],
        # 'path' = primary path for map preview / fallback
        "path": [(20, 130), (340, 130), (340, 370), (700, 370), (700, 540), (1080, 540)],
        "use_png": False,
        "road_color":  "#7B5E2A",
        "grass_color": "#162a16",
    },

    "tunnel_run": {
        "name": "Tunnel Run",
        "desc": "Towers can't see enemies\nin tunnels — use Snipers!",
        "color": "#636e72",
        "path": [
            (20,  360),
            (190, 360), (190, 110),   # shoot up into top tunnel
            (570, 110), (570, 590),   # shoot down into bottom tunnel
            (930, 590), (930, 360),   # back to center, exit right
            (1080, 360),
        ],
        # Rectangular zones where towers cannot target enemies (like canyon walls / tunnels)
        "blind_zones": [
            (145, 55,  615, 195),    # top tunnel  (covers the top horizontal segment)
            (525, 510, 975, 655),    # bottom tunnel (covers the bottom horizontal segment)
        ],
        "use_png": False,
        "road_color":  "#8B7355",
        "grass_color": "#1a1510",
    },

    "the_maze": {
        "name": "Highway 2",
        "desc": "Insanely long path.\nanother easy map!",
        "color": "#fd79a8",
        "path": [
            (20,  650),
            (1000, 650),
            (1000, 490),
            (120,  490),
            (120,  330),
            (880,  330),
            (880,  170),
            (220,  170),
            (220,   65),
            (1080,  65),
        ],
        "use_png": False,
        "road_color":  "#7a4fa0",
        "grass_color": "#0d0a18",
    },

    "tunnel_twins": {
        "name": "intersection B",
        "desc": "two paths \n split waves with two exits",
        "color": "#00b894",
        "paths": [
        [(20, 120), (300, 120), (300, 300), (540, 300), (540, 420), (900, 420), (1080, 420)],
        [(20, 620), (300, 620), (300, 440), (540, 440), (540, 320), (900, 320), (1080, 320)],],

        "path": [(20, 120), (300, 120), (300, 300), (540, 300), (540, 420), (900, 420), (1080, 420)],
        "blind_zones":[
        (280, 100, 560, 340),
        (280, 420, 560, 660),],
        "use_png": False,
        "road_color": "#6ab04c",
        "grass_color": "#071014",
    },
    "orbital_ring": {
        "name": "Orbital Ring",
        "desc": "Enemies orbit the ring\nrotating gates open/close",
        "color": "#00a8ff",
        "path": [(600 + int(260 * math.cos(theta)), 360 + int(260 * math.sin(theta))) for theta in [i * 2 * math.pi / 48 for i in range(48)] ],
        "use_png": False,
        "road_color": "#4dd0e1",
        "grass_color": "#071022",
        "rotating_gates": [ {
            "cx": 600, "cy": 360, "r": 260, "start": -20, "span": 40, "open_ms": 3000, "closed_ms": 3000, "initial_closed": False},
            {"cx": 600, "cy": 360, "r": 260, "start": 160, "span": 40, "open_ms": 2500, "closed_ms": 3500, "initial_closed": True},
        ],
        "radial_blind_zones": [
            (600, 360, 0, 220),
        ],
    },
    "die_time_rule": {
        "name": "TIMERULE",
        "desc": "idk.\nGENUENTLY",
        "color": "#fd79a8",
        "path": [
            (20,  650),
            (300, 400),
            (1000, 600),
            (500, 100),
            (500,300)
        ],
        "use_png": False,
        "road_color":  "#7a4fa0",
        "grass_color": "#0d0a18",
    },
}

# Boss / wave tuning
BOSS_WAVE = 70        # Boss erscheint auf dieser Welle (setze 60 oder 70)
FINAL_WAVE = BOSS_WAVE


ZEPPELIN_PAYLOADS = [
    {"min_wave": 1,  "spawn": [("blue", 3), ("yellow", 2)]},
    {"min_wave": 15, "spawn": [("armored", 2), ("yellow", 3), ("blue", 2)]},
    {"min_wave": 30, "spawn": [("armored", 4), ("yellow", 4), ("blue", 3)]},
]

# ── Wave type definitions ─────────────────────────────────────────────────────
# Each entry: (name, label_color, pool_overrides, count_mult, spawn_delay_ms)
WAVE_TYPES = {
    "normal":      ("",            "#6bc5ff", {},                                    1.0,  380),
    "swarm":       ("💨 SWARM",    "#feca57", {"yellow": 80, "normal": 20},          2.0,  160),
    "armored":     ("🛡 ARMORED",  "#a29bfe", {"armored": 70, "normal": 20, "blue": 10}, 1.2, 400),
    "stealth":     ("👻 STEALTH",  "#2ed573", {"shadow": 70, "normal": 30},          1.3,  350),
    "nuclear":     ("☢️ NUCLEAR",  "#ff6348", {"nuclear": 60, "blue": 30, "normal": 10}, 0.6, 600),
    "tank":        ("🛡 TANK WAVE","#ff4757", {"blue": 50, "armored": 40, "normal": 10}, 0.9, 500),
    "air":         ("🎈 AIR RAID", "#48dbfb", {"zeppelin1": 40, "yellow": 40, "normal": 20}, 0.8, 500),
    "chaos":       ("🌀 CHAOS",    "#ff4757", {"shadow":20,"nuclear":15,"armored":25,"yellow":20,"blue":20}, 1.5, 280),
}

TOWER_UPGRADES = {
    "Tower": {
        "A": [
            ("Rapid Fire",    "🔥", 80,  "Faster shoot speed",           lambda t: setattr(t, "fire_rate", 700)),
            ("Bullet Storm",  "💥", 200, "Fast fire, wider range",       lambda t: (setattr(t, "fire_rate", 450), setattr(t, "range", 210))),
            ("Overdrive",     "⚡", 450, "Hyperspeed",   lambda t: (setattr(t, "fire_rate", 260), setattr(t, "damage", 2))),
        ],
        "B": [
            ("Sharpshooter",  "🎯", 100, "+70 range, faster bullets",   lambda t: (setattr(t, "range", 220), setattr(t, "bullet_speed", 16))),
            ("Eagle Eye",     "👁", 200, "+130 range, targets farthest", lambda t: (setattr(t, "range", 280), setattr(t, "target_mode", "farthest"))),
            ("Sniper Mode",   "🔭", 400, "Extreme range, +2 damage",    lambda t: (setattr(t, "range", 420), setattr(t, "damage", 3))),
        ],
        "C": [
            ("Hollow Points", "💀", 80,  "+1 damage per shot",          lambda t: setattr(t, "damage", t.damage + 1)),
            ("Incendiary",    "🔴", 160, "Shots slow enemies on hit",   lambda t: setattr(t, "slowing_shots", True)),
            ("Devastator",    "☠️", 350, "+2 damage, AoE on impact",    lambda t: (setattr(t, "damage", t.damage + 2), setattr(t, "aoe_shots", True))),
        ],
    },
    "BallTower": {
        "A": [
            ("More Balls",    "🔵", 170, "+3 bullets per volley",        lambda t: setattr(t, "projectiles", t.projectiles + 3)),
            ("Ball Lightning","⚡", 540, "+4 bullets, electric sparks",  lambda t: (setattr(t, "projectiles", t.projectiles + 4), setattr(t, "shock", True))),
            ("Smartball®",  "🌀", 1700, "12 bullets, homing mode",      lambda t: (setattr(t, "projectiles", 12), setattr(t, "homing", True))),
        ],
        "B": [
            ("Turbo Spin",    "💨", 130, "30% faster volleys",           lambda t: setattr(t, "fire_rate", int(t.fire_rate * 0.7))),
            ("Hyperspin",     "🌪", 430, "50% faster, larger range",     lambda t: (setattr(t, "fire_rate", int(t.fire_rate * 0.6)), setattr(t, "range", t.range + 30))),
            ("Maelstrom",     "🌊", 910, "Continuous fire storm",        lambda t: (setattr(t, "fire_rate", 500), setattr(t, "range", 160))),
        ],
        "C": [
            ("Big Balls",     "🟠", 200, "+25 range, bigger hitbox",     lambda t: (setattr(t, "range", t.range + 25), setattr(t, "bullet_size", 2))),
            ("Mega Balls",    "🔴", 600, "+40 range, +1 damage",         lambda t: (setattr(t, "range", t.range + 40), setattr(t, "damage", 2))),
            ("Planet Crusher","🪐", 1500,"Orbital devastation, +3 dmg",  lambda t: (setattr(t, "range", 200), setattr(t, "damage", 4))),
        ],
    },
    "AngryTower": {
        "A": [
            ("precision", "🎯", 500,  "-10° spread, +40 range",      lambda t: (setattr(t, "spread_angle", max(5, t.spread_angle - 10)), setattr(t, "range", t.range + 40))),
            ("Laser Focus",   "🔦", 1600,"Tight beam, faster bullets",   lambda t: (setattr(t, "spread_angle", 4), setattr(t, "bullet_speed", 26))),
            ("Death Ray",     "☢️", 3500,"Penetrating laser, +2 dmg",    lambda t: (setattr(t, "spread_angle", 0), setattr(t, "damage", t.damage + 2), setattr(t, "pierce", True))),
        ],
        "B": [
            ("Extra Barrel",  "🔫", 1300,  "+1 bullet per shot",          lambda t: setattr(t, "spread_shots", t.spread_shots + 1)),
            ("Tri Barrel",    "💥", 2700,"3 bullets per shot",           lambda t: setattr(t, "spread_shots", 3)),
            ("Gatling Mode",  "🌋", 7000,"5 bullets, 40% faster fire",  lambda t: (setattr(t, "spread_shots", 5), setattr(t, "fire_rate", int(t.fire_rate * 0.6)))),
        ],
        "C": [
            ("AP Rounds",     "🔩", 600,  "+1 damage, armor piercing",   lambda t: setattr(t, "damage", t.damage + 1)),
            ("Explosive Tip", "💣", 1800,"+2 dmg, small explosion",      lambda t: (setattr(t, "damage", t.damage + 2), setattr(t, "aoe_shots", True))),
            ("Warhead",       "☢️", 5000,"Massive damage + huge AoE",    lambda t: (setattr(t, "damage", t.damage + 3), setattr(t, "aoe_shots", True), setattr(t, "aoe_radius", 60))),
        ],
    },
    "BombTower": {
        "A": [
            ("Bigger Boom",   "💥", 200, "+25 explosion radius",         lambda t: setattr(t, "bomb_radius", t.bomb_radius + 25)),
            ("Cluster Bomb",  "🧨", 400, "Bombs split into 3 on impact", lambda t: setattr(t, "cluster", True)),
            ("Nuke",          "☢️", 800, "Massive AoE, melts shields",   lambda t: (setattr(t, "bomb_radius", 130), setattr(t, "shield_pierce", True))),
        ],
        "B": [
            ("Speed Loader",  "⏩", 200, "25% faster fire rate",         lambda t: setattr(t, "fire_rate", int(t.fire_rate * 0.75))),
            ("Auto Cannon",   "🔄", 400, "40% faster, wider range",      lambda t: (setattr(t, "fire_rate", int(t.fire_rate * 0.6)), setattr(t, "range", t.range + 40))),
            ("Siege Mode",    "🏰", 600, "60% faster, +100 range",       lambda t: (setattr(t, "fire_rate", int(t.fire_rate * 0.5)), setattr(t, "range", t.range + 100))),
        ],
        "C": [
            ("Sticky Tar",    "🕸", 300, "Bombs slow enemies 40%",       lambda t: setattr(t, "slow_on_hit", 0.6)),
            ("Napalm",        "🔥", 600, "Bombs burn — DoT for 3s",      lambda t: setattr(t, "burn_on_hit", True)),
            ("Hellfire",      "😈", 1000,"+2 dmg, burn + slow combo",    lambda t: (setattr(t, "damage", t.damage + 2), setattr(t, "burn_on_hit", True), setattr(t, "slow_on_hit", 0.5))),
        ],
    },
    "SniperTower": {
        "A": [
            ("High Velocity", "💨", 450, "+5 damage, faster bullet",     lambda t: setattr(t, "damage", t.damage + 5)),
            ("Railgun",       "⚡", 900, "+8 dmg, bullet pierces all",   lambda t: (setattr(t, "damage", t.damage + 8), setattr(t, "pierce_all", True))),
            ("Antimatter",    "💀", 1800,"+15 dmg, one-shots most foes", lambda t: (setattr(t, "damage", t.damage + 15), setattr(t, "pierce_all", True))),
        ],
        "B": [
            ("Quick Scope",   "🎯", 450, "800ms faster reload",          lambda t: setattr(t, "reload_time", t.reload_time - 800)),
            ("Instincts",     "🦅", 900, "1200ms faster + auto-retarget",lambda t: (setattr(t, "reload_time", max(600, t.reload_time - 1200)), setattr(t, "auto_retarget", True))),
            ("Hair Trigger",  "⚡", 1800,"Max speed — 500ms reload",     lambda t: setattr(t, "reload_time", 500)),
        ],
        "C": [
            ("Recon Scope",   "🔭", 500, "+250 range, reveals shadows",  lambda t: (setattr(t, "range", t.range + 250), setattr(t, "recon", True), setattr(t, "mark_boost", 1.5))),
            ("Overwatch",     "👁", 900, "Covers entire map",            lambda t: setattr(t, "range", 9999)),
            ("Death Mark",    "💀", 2000,"Marked enemies take 2x dmg",   lambda t: setattr(t, "mark_multiplier", 2.0)),
        ],
    },
    "PulseTower": {
        "A": [
            ("Amplifier",     "📡", 540, "+40 range, stronger pulse",    lambda t: (setattr(t, "range", t.range + 40), setattr(t, "damage", t.damage + 1))),
            ("Resonance",     "🌊", 2300,"Double pulse every 2s",        lambda t: setattr(t, "double_pulse", True)),
            ("Supernova",     "🌟", 4600,"Triple pulse, +2 dmg",         lambda t: (setattr(t, "triple_pulse", True), setattr(t, "damage", t.damage + 2))),
        ],
        "B": [
            ("Overcharge",    "⚡", 540, "30% faster pulse rate",        lambda t: setattr(t, "pulse_rate", int(t.pulse_rate * 0.7))),
            ("Overdrive",     "🔋", 2300,"50% faster, crackling visual", lambda t: (setattr(t, "pulse_rate", int(t.pulse_rate * 0.5)), setattr(t, "crackle", True))),
            ("Infinite Loop",  "♾", 4600,"Rapid-fire pulses, 400ms",    lambda t: setattr(t, "pulse_rate", 400)),
        ],
        "C": [
            ("Slow Field",    "🕸", 800, "Pulse slows enemies 30%",      lambda t: setattr(t, "pulse_slow", 0.7)),
            ("Stun Pulse",    "😵", 2000,"10% chance to stun 1s",        lambda t: setattr(t, "stun_chance", 0.1)),
            ("EMP Surge",     "💀", 5000,"Stuns all in range 2s",        lambda t: (setattr(t, "stun_chance", 0.5), setattr(t, "stun_duration", 2000))),
        ],
    },
    "Bank": {
        "A": [
            ("Investment",    "📈", 180, "+30c income per wave",         lambda t: setattr(t, "base_income", t.base_income + 30)),
            ("Bull Market",   "🐂", 360, "+50c income, +5% interest",    lambda t: (setattr(t, "base_income", t.base_income + 50), setattr(t, "interest", t.interest + 0.05))),
            ("Money Printer", "💸", 720, "+100c income, doubles cap",    lambda t: (setattr(t, "base_income", t.base_income + 100), setattr(t, "cap", t.cap * 2))),
        ],
        "B": [
            ("Compound",      "🏦", 180, "+8% interest rate",            lambda t: setattr(t, "interest", t.interest + 0.08)),
            ("Hedge Fund",    "💹", 360, "+15% interest, +200 cap",      lambda t: (setattr(t, "interest", t.interest + 0.15), setattr(t, "cap", t.cap + 200))),
            ("Wall Street",   "🤑", 720, "+25% interest, huge cap",      lambda t: (setattr(t, "interest", t.interest + 0.25), setattr(t, "cap", t.cap + 600))),
        ],
        "C": [
            ("Auto Collect",  "🤖", 250, "Auto-collects each wave",      lambda t: setattr(t, "auto_collect", True)),
            ("credit loan",     "💳", 500, "Lend yourself up to 200c",     lambda t: setattr(t, "overdraft", 200)),
            ("Emergency button",       "🏛", 1000,"Emergency 500c if <50c",       lambda t: setattr(t, "bailout", 500)),
        ],
    },
    "MineTower": {
        "A": [
            ("Dense Field",    "💣", 150, "+3 mines, closer spacing",      lambda t: (setattr(t, "mine_count", t.mine_count + 3), setattr(t, "mine_spacing", max(20, t.mine_spacing - 8)))),
            ("Saturation",     "🌋", 400, "+5 mines, wider range",         lambda t: (setattr(t, "mine_count", t.mine_count + 5), setattr(t, "range", t.range + 30))),
            ("Carpet Bomb",    "🗺", 900, "25 mines total",               lambda t: setattr(t, "mine_count", 25)),
        ],
        "B": [
            ("Bigger Charge",  "💥", 200, "+1 dmg, +20 blast radius",      lambda t: (setattr(t, "mine_damage", t.mine_damage + 1), setattr(t, "mine_radius", t.mine_radius + 20))),
            ("Shrapnel",       "🔩", 500, "+30 blast, hits more enemies",  lambda t: setattr(t, "mine_radius", t.mine_radius + 30)),
            ("Nuke Mine",      "☢️", 1200,"Massive blast + shield pierce",  lambda t: (setattr(t, "mine_damage", t.mine_damage + 3), setattr(t, "mine_radius", t.mine_radius + 50), setattr(t, "mine_shield_pierce", True))),
        ],
        "C": [
            ("Sticky Mines",   "🕸", 200, "Mines slow enemies 40%",        lambda t: setattr(t, "mine_slow", 0.6)),
            ("Napalm Mines",   "🔥", 600, "Mines burn — DoT 3s",           lambda t: setattr(t, "mine_burn", True)),
            ("cluster mines", "🪤", 1400,"Explosion spawns 3 sub-mines",  lambda t: setattr(t, "mine_cluster", True)),
        ],
    },
    "Barricade": {
        "A": [
            ("Deeper Mud",    "🪨", 60,  "Slows 35% instead of 30%",    lambda t: setattr(t, "slow", 0.65)),
            ("Quicksand",     "⏳", 240, "Slows 50%, lasts 3s longer",   lambda t: (setattr(t, "slow", 0.5), setattr(t, "linger_time", t.linger_time + 3))),
            ("Tar Pit",       "🖤", 960, "75% slow, sticks for 6s",      lambda t: (setattr(t, "slow", 0.25), setattr(t, "linger_time", t.linger_time + 6))),
        ],
        "B": [
            ("Wider Aura",    "🔵", 60,  "+20 radius",                   lambda t: setattr(t, "radius", t.radius + 20)),
            ("Massive Aura",  "🟣", 240, "+40 radius",                   lambda t: setattr(t, "radius", t.radius + 40)),
            ("Zone Control",  "🌐", 960, "+80 radius, entire lane",      lambda t: setattr(t, "radius", t.radius + 80)),
        ],
        "C": [
            ("Spikes",        "🌵", 80,  "Deals 1 dmg when enemy enters",lambda t: setattr(t, "spike_damage", 1)),
            ("Razor Wire",    "⚡", 300, "2 dmg, mini stun on entry",    lambda t: (setattr(t, "spike_damage", 2), setattr(t, "spike_stun", 500))),
            ("Minefield",     "💣", 800, "3 dmg + chance to pop shield", lambda t: (setattr(t, "spike_damage", 3), setattr(t, "mine_shield_pop", True))),
        ],
    },

    "ice": {
        "A": [   # ── GLACIATION: slow depth & root
            ("Cold Snap",     "❄️", 150, "Freeze lasts 1.5s longer, +15% slow",
             lambda t: (setattr(t, "ice_slow", max(0.08, t.ice_slow - 0.12)),
                        setattr(t, "ice_linger", getattr(t, "ice_linger", 2.5) + 1.5))),
            ("Permafrost",    "🧊", 400, "Fully roots frozen enemies for 0.8s",
             lambda t: setattr(t, "ice_root", True)),
            ("Absolute Zero", "☃️", 980, "Near-instant freeze, 3× bonus dmg on frozen",
             lambda t: (setattr(t, "ice_slow", 0.02),
                        setattr(t, "ice_damage_mult", 3.0),
                        setattr(t, "ice_root", True))),
        ],
        "B": [   # ── BLIZZARD: AoE & range
            ("Ice Field",     "🌨", 200, "+40 range, AoE freeze around each target",
             lambda t: (setattr(t, "range", t.range + 40),
                        setattr(t, "freeze_aoe", True))),
            ("Blizzard Cone", "🌪", 520, "Hits up to 6 enemies per shot, +25 range",
             lambda t: (setattr(t, "range", t.range + 25),
                        setattr(t, "ice_max_targets", 6))),
            ("Arctic Storm",  "🌀", 1300, "Pulses AoE freeze every 0.5s across full range",
             lambda t: (setattr(t, "ice_storm_mode", True),
                        setattr(t, "fire_rate", 500))),
        ],
        "C": [   # ── SHATTER: death explosions & brittle
            ("Brittle Ice",   "💎", 180, "Frozen enemies take 50% more dmg from all sources",
             lambda t: setattr(t, "ice_brittle", True)),
            ("Frostbite",     "🩸", 450, "Deeply frozen foes lose 2 HP/s passively",
             lambda t: setattr(t, "ice_frostbite", True)),
            ("Ice Nova",      "💥", 1150, "Enemies killed while frozen explode, chaining freeze",
             lambda t: setattr(t, "ice_nova_on_death", True)),
        ],
    },
    "fire": {
        "A": [   # ── COMBUSTION: raw burn power
            ("Fuel Injected", "🔥", 150, "Burn ticks 2× faster, +1 dmg/tick",
             lambda t: (setattr(t, "burn_dps", t.burn_dps + 1),
                        setattr(t, "burn_interval", max(200, getattr(t, "burn_interval", 500) - 200)))),
            ("Flash Ignite",  "💥", 400, "+5 instant burst dmg on hit then full burn",
             lambda t: setattr(t, "fire_ignition_burst", 5)),
            ("Inferno Core",  "☢️", 980, "Burns forever until dead — 4 dmg/tick, +6 burst",
             lambda t: (setattr(t, "burn_dps", 4),
                        setattr(t, "burn_duration", 9999999),
                        setattr(t, "fire_ignition_burst", 6))),
        ],
        "B": [   # ── WILDFIRE: spreading chain burns
            ("Chain Ignite",  "🔗", 200, "Fire jumps to 2 nearest on enemy death",
             lambda t: setattr(t, "burn_chain", 2)),
            ("Wildfire",      "🌲", 520, "Burning enemies radiate fire to nearby foes",
             lambda t: setattr(t, "burn_spread_radius", 55)),
            ("Firestorm",     "🌋", 1300, "All enemies in range ignite simultaneously",
             lambda t: (setattr(t, "burn_spread", True),
                        setattr(t, "burn_spread_radius", 9999),
                        setattr(t, "burn_chain", 6))),
        ],
        "C": [   # ── SCORCHED EARTH: terrain & debuffs
            ("Ash Zone",      "🪨", 180, "Slain enemies leave a slow patch for 5s",
             lambda t: setattr(t, "fire_ash_zone", True)),
            ("Cinder Shred",  "☁️", 450, "Burning enemies take +30% dmg from all towers",
             lambda t: setattr(t, "fire_armor_shred", 0.30)),
            ("Hellgate",      "😈", 1150, "Tower aura — any enemy entering range auto-ignites",
             lambda t: setattr(t, "fire_aura", True)),
        ],
    },
    "wind": {
        "A": [   # ── HURRICANE: raw pushback
            ("Gale Force",    "💨", 150, "Push back 3 path segments instead of 1",
             lambda t: setattr(t, "push_segments", 3)),
            ("Hurricane",     "🌀", 400, "Push back 5 segments + 50% slow after landing",
             lambda t: (setattr(t, "push_segments", 5),
                        setattr(t, "wind_slow", 0.50))),
            ("Cyclone Banish","🌪", 980, "Teleports target back to wave start!",
             lambda t: setattr(t, "wind_banish", True)),
        ],
        "B": [   # ── GALE FORCE: side-arc area blasts
            ("Crosswind",     "🌬", 200, "Each shot also blasts ±60° side arcs for 1 dmg",
             lambda t: setattr(t, "wind_arc", True)),
            ("Windshear",     "💨", 520, "Arc dmg +1, slows all arc-hit enemies 30% for 1.5s",
             lambda t: (setattr(t, "wind_arc_dmg", 2),
                        setattr(t, "wind_arc_slow", 0.70))),
            ("Maelstrom",     "🌀", 1300, "360° ring: 3 dmg + 40% slow to ALL enemies in range",
             lambda t: (setattr(t, "wind_ring", True),
                        setattr(t, "wind_arc_dmg", 3),
                        setattr(t, "wind_arc_slow", 0.60))),
        ],

        "C": [   # ── THUNDER: chain lightning
            ("Static Field",  "⚡", 180, "Each push stuns enemy 0.5s",
             lambda t: setattr(t, "wind_push_stun", 500)),
            ("Lightning Rod", "⚡", 450, "Push chains 3-target lightning for 3 dmg",
             lambda t: setattr(t, "wind_lightning", 3)),
            ("Thundergod",    "🌩", 1150, "AoE push + auto-lightning storm every 2s",
             lambda t: (setattr(t, "wind_aoe", True),
                        setattr(t, "wind_lightning", 6),
                        setattr(t, "wind_auto_storm", True))),
        ],
    },
}





ELEMENTAL_UPGRADES = {k: TOWER_UPGRADES[k] for k in ("ice", "fire", "wind")}
PATH_COLORS  = {"A": "#ff6b6b", "B": "#feca57", "C": "#48dbfb"}
PATH_LABELS  = {"A": "PATH I",  "B": "PATH II", "C": "PATH III"}
PATH_FILL    = {"A": "#2a1010", "B": "#2a2005", "C": "#081820"}
PATH_OUTLINE = {"A": "#773333", "B": "#886600", "C": "#225566"}

TOWER_GLOW_COLOR = {
    "Tower":          "#3498db",
    "BallTower":      "#ff9f1c",
    "AngryTower":     "#ff4757",
    "BombTower":      "#ff6348",
    "SniperTower":    "#2ed573",
    "PulseTower":     "#70a1ff",
    "Bank":           "#feca57",
    "Barricade":      "#a29bfe",
    "MineTower":      "#e84393",
    "ElementalTower": "#aaaaff",
}

def _upgrade_tier(total_level):
    if total_level == 0: return 0
    if total_level <= 2: return 1
    if total_level <= 5: return 2
    return 3


# ─── UPGRADE PANEL ───────────────────────────────────────────────────────────

class UpgradePanel:
    W = 260
    H = 700

    def __init__(self, root, on_upgrade_cb, on_sell_cb, on_close_cb, on_set_target_cb):
        self.on_upgrade    = on_upgrade_cb
        self.on_sell       = on_sell_cb
        self.on_close      = on_close_cb
        self.on_set_target = on_set_target_cb
        self.building      = None
        self.visible       = False

        self.frame = Frame(root, bg="#0d0d1a", width=self.W)
        self.cv = Canvas(self.frame, width=self.W, height=self.H,
                         bg="#0d0d1a", highlightthickness=0)
        self.cv.pack(fill=BOTH, expand=True)
        self._buttons = []
        self.cv.bind("<Button-1>", self._on_click)
        self.cv.bind("<Motion>",   self._on_hover)

    def show(self, building):
        self.building = building
        self.visible = True
        self.redraw()

    def hide(self):
        self.visible = False
        self.building = None
        self._draw_idle()

    def redraw(self):
        if not self.visible or not self.building:
            self._draw_idle()
            return
        self.cv.delete("all")
        self._buttons.clear()
        self._draw_panel()

    def _draw_idle(self):
        self.cv.delete("all")
        self._buttons.clear()
        W, H = self.W, self.H
        # gradient background
        for i in range(20):
            shade = int(13 + i / 20 * 8)
            blue = min(shade + 10, 255)
            yb = i * (H // 20)
            self.cv.create_rectangle(0, yb, W, yb + H // 20 + 1,
                                     fill=f"#{shade:02x}{shade:02x}{blue:02x}", outline="")
        self.cv.create_text(W // 2, H // 2 - 60,
                            text="🏗", font=("Arial", 36), fill="#2a2a4a")
        self.cv.create_text(W // 2, H // 2 + 10,
                            text="SELECT A TOWER", fill="#333366",
                            font=("Courier", 11, "bold"))
        self.cv.create_text(W // 2, H // 2 + 32,
                            text="right-click to upgrade", fill="#222244",
                            font=("Courier", 8))
        # decorative dots
        for row in range(5):
            for col in range(7):
                x = 20 + col * 32
                y = H - 120 + row * 18
                self.cv.create_oval(x - 2, y - 2, x + 2, y + 2,
                                    fill="#1a1a33", outline="")

    def _draw_element_chooser(self, b, y):
        """Shown when no element is chosen yet."""
        cv, W = self.cv, self.W

        cv.create_text(W // 2, y + 10, text="⚗  CHOOSE YOUR ELEMENT",
                       fill="#aaaaff", font=("Courier", 10, "bold"))
        cv.create_text(W // 2, y + 26, text="Permanent — choose wisely",
                       fill="#444466", font=("Courier", 8))
        y += 42

        CHOICES = {
            "A": dict(name="ICE", icon="❄️", color="#00d4ff", fill="#071828",
                      hover="#0a2535",
                      desc="Freeze · Root · Shatter\nSlow enemies to a crawl"),
            "B": dict(name="FIRE", icon="🔥", color="#ff6600", fill="#2a0500",
                      hover="#3a0a00",
                      desc="Burn · Spread · Scorch\nDoT and chain devastation"),
            "C": dict(name="WIND", icon="💨", color="#00ff88", fill="#051a0a",
                      hover="#0a2a14",
                      desc="Push · Pull · Thunder\nCrowd-control dominance"),
        }

        for path, cfg in CHOICES.items():
            col = cfg["color"]
            cv.create_rectangle(10, y, W - 10, y + 74,
                                fill=cfg["fill"], outline=col, width=2)
            cv.create_text(W // 2, y + 18,
                           text=f"{cfg['icon']}  {cfg['name']}",
                           fill=col, font=("Courier", 15, "bold"))
            cv.create_text(W // 2, y + 40,
                           text=cfg["desc"], fill="#aaaacc",
                           font=("Courier", 8), justify="center")
            cv.create_text(W // 2, y + 60,
                           text="▶ SELECT", fill=col, font=("Courier", 9, "bold"))

            def make_cb(p=path):
                return lambda: self.on_upgrade(self.building, p)

            self._add_button(cv, 10, y, W - 10, y + 74,
                             None, cfg["fill"], cfg["hover"], make_cb())
            y += 84

    def _draw_elemental_paths(self, b, y):
        """Shown once an element has been chosen."""
        cv, W = self.cv, self.W

        ELEM_COLOR = {"ice": "#00d4ff", "fire": "#ff6600", "wind": "#00ff88"}
        ELEM_PATH_NAMES = {
            "ice": {"A": "❄ GLACIATION", "B": "🌨 BLIZZARD", "C": "💥 SHATTER"},
            "fire": {"A": "🔥 COMBUSTION", "B": "🌲 WILDFIRE", "C": "🪨 SCORCHED"},
            "wind": {"A": "💨 HURRICANE", "B": "🌬 GALE FORCE", "C": "⚡ THUNDER"},
        }

        elem = b.element
        col = ELEM_COLOR.get(elem, "#aaaaff")
        upgrades = ELEMENTAL_UPGRADES.get(elem, {})
        names = ELEM_PATH_NAMES.get(elem, {})

        for path in ["A", "B", "C"]:
            tiers = upgrades.get(path, [])
            path_level = getattr(b, f"_path_{path}_level", 0)
            pname = names.get(path, f"PATH {path}")

            # Header row
            cv.create_rectangle(10, y, W - 10, y + 22,
                                fill="#0a0a1a", outline=col, width=1)
            cv.create_text(20, y + 11, text=pname, fill=col,
                           font=("Courier", 9, "bold"), anchor="w")
            for ti in range(3):
                px = W - 20 - (2 - ti) * 16
                cv.create_oval(px - 5, y + 6, px + 5, y + 16,
                               fill=col if ti < path_level else "#1a1a3a",
                               outline=col, width=1)
            y += 26

            if path_level < len(tiers):
                uname, uicon, ucost, udesc, _ = tiers[path_level]
                can_afford = Game.money >= ucost
                bg = "#1e2040" if can_afford else "#1a1a2a"
                border = col if can_afford else "#333355"

                cv.create_rectangle(10, y, W - 10, y + 62,
                                    fill=bg, outline=border, width=1)
                cv.create_text(18, y + 10, text=f"{uicon} {uname}",
                               fill="white" if can_afford else "#666688",
                               font=("Courier", 10, "bold"), anchor="w")
                cv.create_text(18, y + 26, text=udesc, fill="#aaaacc",
                               font=("Courier", 8), anchor="w", width=W - 36)

                badge_fill = "#002020" if can_afford else "#200808"
                badge_out = "#00ffcc" if can_afford else "#ff4757"
                badge_txt = "#00ffcc" if can_afford else "#ff4757"
                cv.create_rectangle(W - 70, y + 40, W - 10, y + 58,
                                    fill=badge_fill, outline=badge_out, width=1)
                cv.create_text(W - 40, y + 49, text=f"{ucost}c",
                               fill=badge_txt, font=("Courier", 10, "bold"))
                if can_afford:
                    def make_cb(p=path):
                        return lambda: self.on_upgrade(self.building, p)

                    self._add_button(cv, 10, y, W - 10, y + 62,
                                     None, bg, "#2a2a60", make_cb())
            else:
                cv.create_rectangle(10, y, W - 10, y + 30,
                                    fill="#0a2a1a", outline="#1a6644", width=1)
                cv.create_text(W // 2, y + 15, text="✅  PATH MAXED",
                               fill="#00ff88", font=("Courier", 9, "bold"))
            y += 68

    def _draw_panel(self):
        b  = self.building
        cv = self.cv
        W  = self.W

        band_h = max(1, self.H // 20)
        for i in range(20):
            shade = int(13 + i / 20 * 8)
            blue  = min(shade + 10, 255)
            yb    = i * band_h
            cv.create_rectangle(0, yb, W, yb + band_h + 1,
                                fill=f"#{shade:02x}{shade:02x}{blue:02x}", outline="")

        cls   = b.__class__.__name__
        names = {
            "Tower": "Trooper", "BallTower": "All-Rounder",
            "AngryTower": "Gunner", "BombTower": "Bomber",
            "SniperTower": "Sniper", "PulseTower": "Pulse Tower",
            "Bank": "Bank", "Barricade": "Barricade",
            "MineTower": "Mine Tower",
        }
        icons = {
            "Tower": "🔵", "BallTower": "🟠", "AngryTower": "🔴",
            "BombTower": "💣", "SniperTower": "🎯", "PulseTower": "📡",
            "Bank": "🏦", "Barricade": "🛡", "MineTower": "🪤",
        }
        name = names.get(cls, cls)
        icon = icons.get(cls, "🏗")

        cv.create_rectangle(0, 0, W, 70, fill="#1a1a3a", outline="")
        cv.create_text(W//2, 20, text=f"{icon}  {name}",
                       fill="white", font=("Courier", 14, "bold"))

        total_done = sum(getattr(b, f"_path_{p}_level", 0) for p in "ABC")
        dot_r, dot_total = 5, 9
        dot_spacing = (W - 40) / (dot_total - 1)
        for i in range(dot_total):
            dx     = 20 + i * dot_spacing
            filled = i < total_done
            cv.create_oval(dx - dot_r, 48 - dot_r, dx + dot_r, 48 + dot_r,
                           fill="#00ffcc" if filled else "#2a2a4a",
                           outline="#00ffcc" if filled else "#3a3a5a", width=1)

        self._add_button(cv, W - 30, 5, W - 5, 30, "✕", "#ff4757",
                         "#ff6b81", self.on_close, text_color="white")

        y = 80

        cv.create_rectangle(10, y, W - 10, y + 60, fill="#111128",
                            outline="#2a2a5a", width=1)
        stats   = self._get_stats(b)
        col_w   = (W - 20) // max(len(stats), 1)
        for i, (label, value) in enumerate(stats):
            sx = 10 + i * col_w + col_w // 2
            cv.create_text(sx, y + 12, text=value, fill="#00ffcc",
                           font=("Courier", 11, "bold"))
            cv.create_text(sx, y + 30, text=label, fill="#666699",
                           font=("Courier", 8))
        y += 70

        if cls == "AngryTower":
            has_target = getattr(b, "fixed_target", False) and b.target_pos is not None
            btn_label  = "🎯 CLEAR TARGET" if has_target else "🎯 SET TARGET"
            btn_col    = "#1a3a1a" if not has_target else "#3a1a1a"
            btn_out    = "#2ed573" if not has_target else "#ff4757"
            btn_txt    = "#2ed573" if not has_target else "#ff4757"
            cv.create_rectangle(10, y, W - 10, y + 32,
                                fill=btn_col, outline=btn_out, width=1)
            cv.create_text(W // 2, y + 16, text=btn_label,
                           fill=btn_txt, font=("Courier", 10, "bold"))
            if has_target:
                tx, ty = b.target_pos
                cv.create_text(W // 2, y + 28, text=f"pos ({int(tx)}, {int(ty)})",
                               fill="#888888", font=("Courier", 7))
            def _target_cb():
                if getattr(self.building, "fixed_target", False):
                    self.building.clear_target()
                    self.redraw()
                else:
                    self.on_set_target(self.building)
            self._add_button(cv, 10, y, W - 10, y + 32,
                             None, btn_col, "#1a4a2a", _target_cb)
            y += 42

        # ── ElementalTower gets its own two-phase panel ───────────────────────────
        if cls == "ElementalTower":
            if b.element is None:
                self._draw_element_chooser(b, y)
            else:
                self._draw_elemental_paths(b, y)
        else:
            upgrades = TOWER_UPGRADES.get(cls, {})
            for path in ["A", "B", "C"]:

                tiers      = upgrades.get(path, [])
                path_level = getattr(b, f"_path_{path}_level", 0)
                color      = PATH_COLORS[path]
                fill_col   = PATH_FILL[path]
                out_col    = PATH_OUTLINE[path]
                label      = PATH_LABELS[path]

                cv.create_rectangle(10, y, W - 10, y + 22,
                                    fill=fill_col, outline=out_col, width=1)
                cv.create_text(20, y + 11, text=label, fill=color,
                            font=("Courier", 9, "bold"), anchor="w")
                for ti in range(3):
                    px = W - 20 - (2 - ti) * 16
                    cv.create_oval(px - 5, y + 6, px + 5, y + 16,
                                fill=color if ti < path_level else "#1a1a3a",
                                outline=color, width=1)
                y += 26

                if path_level < len(tiers):
                    uname, uicon, ucost, udesc, _ = tiers[path_level]
                    can_afford = Game.money >= ucost
                    bg         = "#1e2040" if can_afford else "#1a1a2a"
                    border     = color     if can_afford else "#333355"

                    cv.create_rectangle(10, y, W - 10, y + 62,
                                        fill=bg, outline=border, width=1)
                    cv.create_text(18, y + 10, text=f"{uicon} {uname}",
                                    fill="white" if can_afford else "#666688",
                                    font=("Courier", 10, "bold"), anchor="w")
                    cv.create_text(18, y + 24, text=udesc, fill="#aaaacc",
                                    font=("Courier", 8), anchor="w", width=W - 36)

                    badge_fill    = "#002020" if can_afford else "#200808"
                    badge_outline = "#00ffcc" if can_afford else "#ff4757"
                    badge_text    = "#00ffcc" if can_afford else "#ff4757"
                    cv.create_rectangle(W - 70, y + 40, W - 10, y + 58,
                                        fill=badge_fill, outline=badge_outline, width=1)
                    cv.create_text(W - 40, y + 49, text=f"{ucost}c",
                                    fill=badge_text, font=("Courier", 10, "bold"))

                    if can_afford:
                        def make_cb(p=path):
                            return lambda: self.on_upgrade(self.building, p)
                        self._add_button(self.cv, 10, y, W - 10, y + 62,
                                        None, bg, "#2a2a60", make_cb())
                else:
                    cv.create_rectangle(10, y, W - 10, y + 30,
                                        fill="#0a2a1a", outline="#1a6644", width=1)
                    cv.create_text(W // 2, y + 15, text="✅  PATH MAXED",
                                    fill="#00ff88", font=("Courier", 9, "bold"))
                y += 68

        y      = self.H - 55
        refund = b.get_refund_amount()
        cv.create_rectangle(10, y, W - 10, y + 40,
                            fill="#3a0a0a", outline="#ff4757", width=1)
        cv.create_text(W // 2, y + 11, text="SELL TOWER",
                       fill="#ff4757", font=("Courier", 11, "bold"))
        cv.create_text(W // 2, y + 27, text=f"Refund: {refund}c",
                       fill="#ff8888", font=("Courier", 9))
        self._add_button(cv, 10, y, W - 10, y + 40,
                         None, "#3a0a0a", "#5a1010", self.on_sell)

    def _get_stats(self, b):
        cls = b.__class__.__name__
        if cls == "Tower":
            return [("DMG", str(b.damage)), ("RATE", f"{b.fire_rate}ms"), ("RNG", str(b.range))]
        if cls == "BallTower":
            return [("BALLS", str(b.projectiles)), ("RATE", f"{b.fire_rate}ms"), ("RNG", str(b.range))]
        if cls == "AngryTower":
            return [("DMG", str(b.damage)), ("RATE", f"{b.fire_rate}ms"), ("SHOTS", str(b.spread_shots))]
        if cls == "BombTower":
            return [("DMG", str(b.damage)), ("AOE", str(b.bomb_radius)), ("RNG", str(b.range))]
        if cls == "SniperTower":
            return [("DMG", str(b.damage)), ("RLD", f"{b.reload_time}ms"), ("RNG", str(b.range))]
        if cls == "PulseTower":
            return [("DMG", str(b.damage)), ("RATE", f"{b.pulse_rate}ms"), ("RNG", str(b.range))]
        if cls == "Bank":
            return [("INC", f"{b.base_income}c"), ("INT", f"{int(b.interest*100)}%"), ("CAP", str(b.cap))]
        if cls == "Barricade":
            return [("SLOW", f"{int((1-b.slow)*100)}%"), ("RNG", str(b.radius)), ("TIME", f"{b.linger_time:.0f}s")]
        if cls == "MineTower":
            return [("MINES", str(b.mine_count)), ("DMG", str(b.mine_damage)), ("AOE", str(b.mine_radius))]
        if cls == "ElementalTower":
            elem = getattr(b, "element", None) or "?"
            return [("ELEM", elem.upper()[:4] if elem != "?" else "NONE"),
            ("RNG",  str(b.range)),
            ("RATE", f"{b.fire_rate}ms")]
        return []

    def _add_button(self, cv, x1, y1, x2, y2, text, bg, hover_bg, callback, text_color="#ffffff"):
        if text:
            cv.create_rectangle(x1, y1, x2, y2, fill=bg, outline="", tags=f"btn_{len(self._buttons)}")
            cv.create_text((x1+x2)//2, (y1+y2)//2, text=text,
                           fill=text_color, font=("Courier", 10, "bold"),
                           tags=f"btn_{len(self._buttons)}")
        self._buttons.append((x1, y1, x2, y2, callback, bg, hover_bg))

    def _on_click(self, e):
        for (x1, y1, x2, y2, cb, _, __) in self._buttons:
            if x1 <= e.x <= x2 and y1 <= e.y <= y2:
                cb()
                break

    def _on_hover(self, e):
        self.cv.delete("hover_highlight")
        for (x1, y1, x2, y2, cb, bg, hover_bg) in self._buttons:
            if x1 <= e.x <= x2 and y1 <= e.y <= y2:
                self.cv.create_rectangle(x1, y1, x2, y2,
                                         fill=hover_bg, outline="",
                                         tags="hover_highlight")
                self.cv.tag_lower("hover_highlight")  # ← push behind text
                break


# ─── BULLETS / BOMBS ────────────────────────────────────────────────────────

class SniperBullet:
    def __init__(self, canvas, x, y, img, target, damage, pierce_all=False):
        self.canvas      = canvas
        self.target      = target
        self.damage      = damage
        self.speed       = 35
        self.pierce_all  = pierce_all
        self.hit_enemies = set()
        self.alive       = True
        self.sprite      = canvas.create_image(x, y, image=img)
        self._move()

    def _move(self):
        if not self.alive:
            return
        if not self.target or not self.target.sprite:
            self._destroy()
            return
        pos = self.target.get_position()
        if not pos:
            self._destroy()
            return
        coords = self.canvas.coords(self.sprite)
        if not coords:
            self.alive = False
            return
        x, y   = coords
        tx, ty = pos
        dx, dy = tx - x, ty - y
        dist   = (dx**2 + dy**2)**0.5
        if dist < self.speed:
            if self.target not in self.hit_enemies:
                self.target.remove_sniper_mark(self.canvas)
                self.target.apply_damage(self.damage)
                self.hit_enemies.add(self.target)
            if not self.pierce_all:
                self._destroy()
                return
        vx, vy = dx / dist * self.speed, dy / dist * self.speed
        self.canvas.move(self.sprite, vx, vy)
        self.canvas.after(16, self._move)

    def _destroy(self):
        if self.alive:
            self.alive = False
            self.canvas.delete(self.sprite)
            self.sprite = None


class Bullet:
    def __init__(self, canvas, x, y, img, dx, dy, reach, damage=1,
                 slow=None, aoe=False, aoe_radius=40, pierce=False):
        self.canvas     = canvas
        self.sprite     = canvas.create_image(x, y, image=img)
        self.dx, self.dy = dx, dy
        self.start_x, self.start_y = x, y
        self.reach      = reach
        self.damage     = damage
        self.slow       = slow
        self.aoe        = aoe
        self.aoe_radius = aoe_radius
        self.pierce     = pierce
        self.alive      = True

    def move(self, enemies):
        if not self.alive:
            return False
        self.canvas.move(self.sprite, self.dx, self.dy)
        coords = self.canvas.coords(self.sprite)
        if not coords or len(coords) < 2:
            self.alive = False
            return False
        x, y = coords
        if ((x-self.start_x)**2 + (y-self.start_y)**2)**0.5 > self.reach:
            self.delete()
            return False
        for e in list(enemies):
            pos = e.get_position()
            if not pos:
                continue
            ex, ey = pos
            if ((x-ex)**2 + (y-ey)**2)**0.5 < e.get_collision_radius():
                if self.aoe:
                    for ae in list(enemies):
                        apos = ae.get_position()
                        if apos and ((x-apos[0])**2 + (y-apos[1])**2)**0.5 < self.aoe_radius:
                            ae.apply_damage(self.damage)
                            if self.slow:
                                ae.slow_effects["bullet_slow"] = (self.slow, time.time() + 2)
                else:
                    e.apply_damage(self.damage)
                    if self.slow:
                        e.slow_effects["bullet_slow"] = (self.slow, time.time() + 2)
                if not self.pierce:
                    self.delete()
                    return False
        return True

    def delete(self):
        if self.alive:
            self.canvas.delete(self.sprite)
            self.sprite = None
            self.alive  = False


class Bomb:
    bombs = []

    def __init__(self, canvas, x, y, img, tx, ty, radius=80, damage=3,
                 slow_on_hit=None, burn_on_hit=False, cluster=False, shield_pierce=False):
        self.canvas       = canvas
        self.tx, self.ty  = tx, ty
        self.radius       = radius
        self.damage       = damage
        self.slow_on_hit  = slow_on_hit
        self.burn_on_hit  = burn_on_hit
        self.cluster      = cluster
        self.shield_pierce = shield_pierce
        self.alive        = True
        self.sprite       = canvas.create_image(x, y, image=img)
        self.canvas.after(30, self._move)
        self.canvas.after(3000, self.explode)
        Bomb.bombs.append(self)

    def _move(self):
        if not self.alive:
            return
        if not self.sprite:
            return
        coords = self.canvas.coords(self.sprite)
        if not coords:
            return
        bx, by = coords
        dx, dy = self.tx - bx, self.ty - by
        dist   = (dx**2 + dy**2)**0.5
        if dist <= 5:
            self.explode()
            return
        speed = 4
        self.canvas.move(self.sprite, dx/dist*speed, dy/dist*speed)
        self.canvas.after(30, self._move)

    def explode(self):
        if not self.alive:
            return
        self.alive = False
        if not self.sprite:
            return
        coords = self.canvas.coords(self.sprite)
        if not coords:
            self.canvas.delete(self.sprite)
            self.sprite = None
            return
        bx, by = coords
        self.canvas.delete(self.sprite)
        self.sprite = None

        for e in list(Enemy.enemies):
            pos = e.get_position()
            if not pos:
                continue
            ex, ey = pos
            if ((bx-ex)**2 + (by-ey)**2)**0.5 < self.radius:
                if self.shield_pierce and hasattr(e, "shield_hp"):
                    e.shield_hp = 0
                    e.break_shield()
                e.apply_damage(self.damage)
                if self.slow_on_hit:
                    e.slow_effects["bomb_slow"] = (self.slow_on_hit, time.time() + 2.5)
                if self.burn_on_hit:
                    self.canvas.after(500,  lambda en=e: en.apply_damage(1) if en.sprite else None)
                    self.canvas.after(1000, lambda en=e: en.apply_damage(1) if en.sprite else None)
                    self.canvas.after(1500, lambda en=e: en.apply_damage(1) if en.sprite else None)

        if self.cluster:
            for angle in [0, 120, 240]:
                rad = math.radians(angle)
                tx2 = bx + math.cos(rad) * 60
                ty2 = by + math.sin(rad) * 60
                Bomb(self.canvas, bx, by, game.bomb_img, tx2, ty2,
                     radius=self.radius // 2, damage=max(1, self.damage // 2))

        ring = self.canvas.create_oval(bx-self.radius, by-self.radius,
                                        bx+self.radius, by+self.radius,
                                        outline="red", width=3)
        if self in Bomb.bombs:
            Bomb.bombs.remove(self)
        self.canvas.after(200, lambda r=ring: self.canvas.delete(r))


# ─── ENEMIES ────────────────────────────────────────────────────────────────

class Enemy:
    enemies  = []
    base_hp  = 3
    health   = 50   # player HP

    def __init__(self, canvas, img, path, speed, hp_label, money_label):
        self.canvas      = canvas
        self.img         = img
        self.path        = path
        self.speed       = speed
        self.point       = 0
        self.sprite      = None
        self.hp          = Enemy.base_hp
        self.radius      = 40
        self.reward      = 3
        self.hp_label    = hp_label
        self.money_label = money_label
        self.sniper_mark = None
        self.sniper_mark_count = 0
        self.slow_effects = {}
        self.is_shadow = False  # shadow enemies are invisible to non-recon towers
        self._wind_pushed = False  # can only be pushed back once
        self._wind_orbited = False

    def get_position(self):
        if not self.sprite:
            return None
        coords = self.canvas.coords(self.sprite)
        if not coords or len(coords) != 2:
            return None
        return coords[0], coords[1]

    def add_sniper_mark(self, canvas):
        self.sniper_mark_count += 1
        if self.sniper_mark is None:
            pos = self.get_position()
            if not pos:
                return
            x, y = pos
            self.sniper_mark = canvas.create_image(x, y - 18, image=game.mark_img)
            canvas.tag_raise(self.sniper_mark)

    def remove_sniper_mark(self, canvas):
        self.sniper_mark_count -= 1
        if self.sniper_mark_count <= 0:
            if self.sniper_mark:
                canvas.delete(self.sniper_mark)
                self.sniper_mark = None
            self.sniper_mark_count = 0

    def get_collision_radius(self):
        return self.radius

    def apply_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.delete()

    def spawn(self):
        x, y = self.path[0]
        self.sprite = self.canvas.create_image(x, y, image=self.img)
        Enemy.enemies.append(self)
        self._move()

    def slow_factor(self):
        if not hasattr(self, "slow_effects"):
            self.slow_effects = {}
        if hasattr(self, "immune_to_slow") and self.immune_to_slow:
            return 1
        now    = time.time()
        pos    = self.get_position()
        if pos:
            ex, ey = pos
            for b in Barricade.barricades:
                bpos = b.get_position()
                if not bpos:
                    continue
                bx, by = bpos
                if ((ex-bx)**2 + (ey-by)**2)**0.5 < b.get_radius():
                    b.apply_slow(self)
        expired = [s for s, (f, exp) in self.slow_effects.items() if exp < now]
        for s in expired:
            del self.slow_effects[s]
        slowest = 1
        for f, exp in self.slow_effects.values():
            slowest = min(slowest, f)
        return slowest

    # In Enemy._move, replace the method with this:
    def _move(self):
        if game.game_over or not self.sprite:
            return
        if self.sniper_mark:
            coords = self.canvas.coords(self.sprite)
            if coords:
                x, y = coords
                self.canvas.coords(self.sniper_mark, x, y - 18)
                self.canvas.tag_raise(self.sniper_mark)
        if self.point >= len(self.path) - 1:
            dmg = max(1, int(self.hp))
            self._do_delete(give_reward=False)
            Enemy.health -= dmg
            self.hp_label.config(text=f"❤️ {max(0,Enemy.health)} / {getattr(game, '_player_max_hp', 50)}")
            if Enemy.health <= 0:
                game.trigger_game_over()
            return
        x1, y1 = self.path[self.point]
        x2, y2 = self.path[self.point + 1]
        dx, dy  = x2 - x1, y2 - y1
        dist    = (dx**2 + dy**2)**0.5

        my_gen = getattr(self, '_push_gen', 0)   # ← capture generation at move start

        def step():
            if not self.sprite or game.game_over:
                return
            if getattr(self, '_push_gen', 0) != my_gen:   # ← a push happened; abort old loop
                return
            c = self.canvas.coords(self.sprite)
            if not c:
                return
            slow   = self.slow_factor()
            sx, sy = dx/dist*self.speed*slow, dy/dist*self.speed*slow
            cx, cy = c
            if ((cx-x2)**2 + (cy-y2)**2)**0.5 < 5:
                self.point += 1
                self._move()
            else:
                self.canvas.move(self.sprite, sx, sy)
                self.canvas.after(20, step)
        step()

    def _do_delete(self, give_reward=True):
        """Internal clean deletion — removes all canvas items and list refs."""
        # Guard against double-delete: if sprite is gone AND not in list, we're done
        if not self.sprite and self not in Enemy.enemies:
            return
        if self.sniper_mark:
            self.canvas.delete(self.sniper_mark)
            self.sniper_mark = None
            self.sniper_mark_count = 0
        if self.sprite:
            self.canvas.delete(self.sprite)
            self.sprite = None
        if self in Enemy.enemies:
            Enemy.enemies.remove(self)
        if give_reward:
            game.play_balloon_pop()
            Game.money += self.reward
            game.total_kills += 1
            game.update_hud()
        if not Enemy.enemies:
            game.wave_running = False

    def delete(self):
        self._do_delete(give_reward=True)

    def spawn_from_position(self, x, y, start_index=None):
        if start_index is None:
            self.sprite = self.canvas.create_image(x, y, image=self.img)
            best_i = 0
            best_d = float("inf")
            for i in range(len(self.path) - 1):
                px, py = self.path[i]
                d = (px - x) ** 2 + (py - y) ** 2
                if d < best_d:
                    best_d = d
                    best_i = i

            self.point = best_i
        else:
            self.point = max(0,min(start_index,len(self.path) - 2))

        self.sprite = self.canvas.create_image(x, y, image=self.img)
        Enemy.enemies.append(self)
        self._move()

class BlueEnemy(Enemy):
    def __init__(self, canvas, img, path, hp_label, money_label):
        super().__init__(canvas, img, path, speed=1.8, hp_label=hp_label, money_label=money_label)
        self.hp     = Enemy.base_hp * 3
        self.reward = 4


class YellowEnemy(Enemy):
    def __init__(self, canvas, img, path, hp_label, money_label):
        super().__init__(canvas, img, path, speed=4.5, hp_label=hp_label, money_label=money_label)
        self.hp     = max(1, Enemy.base_hp // 2)
        self.reward = 2


class StarEnemy(Enemy):
    def __init__(self, canvas, img, path, hp_label, money_label, normal_img):
        super().__init__(canvas, img, path, speed=3, hp_label=hp_label, money_label=money_label)
        self.hp         = 8
        self.reward     = random.randint(0, 40)
        self.normal_img = normal_img


class NuclearEnemy(Enemy):
    def __init__(self, canvas, img, path, hp_label, money_label):
        super().__init__(canvas, img, path, speed=1.2, hp_label=hp_label, money_label=money_label)
        self.hp     = 70
        self.radius = 50
        self.reward = 70


class ShadowEnemy(Enemy):
    """Invisible to towers without recon. Uses Shadow.png."""
    def __init__(self, canvas, img, path, hp_label, money_label):
        super().__init__(canvas, img, path, speed=2.2, hp_label=hp_label, money_label=money_label)
        self.hp        = int(12 * Enemy.base_hp)
        self.reward    = 15
        self.is_shadow = True
        self.radius    = 38

class Juggernaut(Enemy):
    def __init__(self, canvas, img, path, hp_label, money_label):
        super().__init__(canvas, img, path, speed=0.6, hp_label=hp_label, money_label=money_label)
        self.hp = 220
        self.reward = 90
        self.radius = 56
        self.armor = 0.5  # reduces incoming damage by 50% until armor broken
        self.armor_hp = 40

    def apply_damage(self, dmg):
        if self.armor_hp > 0:
            reduced = max(1, int(dmg * (1 - self.armor)))
            self.armor_hp -= reduced
            if self.armor_hp <= 0:
                # armor broken visual
                pos = self.get_position()
                if pos:
                    self.canvas.create_text(*pos, text="⚠", fill="#ffcc00")
            return
        super().apply_damage(dmg)

class PhaseRunner(Enemy):
    def __init__(self, canvas, img, path, hp_label, money_label):
        super().__init__(canvas, img, path, speed=3.6, hp_label=hp_label, money_label=money_label)
        self.hp = 18
        self.reward = 6
        self.phase_cooldown = 0
        self.phase_interval = 1.2  # seconds
        self.is_phased = False

    def _move(self):
        # override to occasionally become invulnerable for a short burst
        if not hasattr(self, "_last_phase"):
            self._last_phase = time.time()
        now = time.time()
        if not self.is_phased and now - self._last_phase > self.phase_interval:
            self.is_phased = True
            self._last_phase = now
            if self.sprite:
                self.canvas.itemconfig(self.sprite, state="hidden")
            self.canvas.after(400, self._end_phase)
        super()._move()

    def _end_phase(self):
        self.is_phased = False
        if self.sprite:
            self.canvas.itemconfig(self.sprite, state="normal")

    def apply_damage(self, dmg):
        if self.is_phased:
            return
        super().apply_damage(dmg)

class Regenerator(Enemy):
    def __init__(self, canvas, img, path, hp_label, money_label):
        super().__init__(canvas, img, path, speed=1.6, hp_label=hp_label, money_label=money_label)
        self.hp = 40
        self.reward = 10
        self.regen_amount = 1
        self.regen_interval = 1000  # ms
        self._regen_loop()

    def _regen_loop(self):
        if self.sprite and not game.game_over:
            self.hp += self.regen_amount
            self.canvas.after(self.regen_interval, self._regen_loop)

class BomberDrone(Enemy):
    def __init__(self, canvas, img, path, hp_label, money_label):
        super().__init__(canvas, img, path, speed=2.0, hp_label=hp_label, money_label=money_label)
        self.hp = 6
        self.reward = 3
        self.radius = 28
        self.explosion_radius = 60
        self.explosion_damage = 3

    def delete(self):
        # ── FIX: grab position BEFORE super() removes the sprite ──────────
        pos = self.get_position()
        # Remove self from Enemy.enemies first so the splash doesn't hit a
        # half-deleted object (sprite already gone but still in the list).
        super().delete()
        if pos:
            x, y = pos
            ring = self.canvas.create_oval(
                x - self.explosion_radius, y - self.explosion_radius,
                x + self.explosion_radius, y + self.explosion_radius,
                outline="#ff6b6b", width=3)
            for e in list(Enemy.enemies):
                if not e.sprite:          # skip already-deleted enemies
                    continue
                p = e.get_position()
                if p and math.hypot(p[0] - x, p[1] - y) <= self.explosion_radius:
                    e.apply_damage(self.explosion_damage)
            # capture ring in default arg to avoid closure-over-loop bug
            self.canvas.after(200, lambda r=ring: self.canvas.delete(r))

class ShieldedBrute(Enemy):
    def __init__(self, canvas, img, shield_img, shield_break_img, path, hp_label, money_label):
        super().__init__(canvas, img, path, speed=1.2, hp_label=hp_label, money_label=money_label)
        self.hp = 36
        self.reward = 12
        self.shield_hp = 18
        self.shield_img = shield_img
        self.shield_sprite = None

    def spawn(self):
        x, y = self.path[0]
        self.sprite = self.canvas.create_image(x, y, image=self.img)
        self.shield_sprite = self.canvas.create_image(x, y, image=self.shield_img)
        Enemy.enemies.append(self)
        self._move()

    def apply_damage(self, dmg):
        if self.shield_hp > 0:
            self.shield_hp -= dmg
            if self.shield_hp <= 0:
                self.break_shield()
            return
        super().apply_damage(dmg)

    def break_shield(self):
        if self.shield_sprite:
            coords = self.canvas.coords(self.shield_sprite)
            if coords:
                fx = self.canvas.create_image(coords[0], coords[1], image=game.shield_break_img)
                self.canvas.after(300, lambda: self.canvas.delete(fx))
            self.canvas.delete(self.shield_sprite)
            self.shield_sprite = None

    def _do_delete(self, give_reward=True):
        # Clean up shield sprite first
        if self.shield_sprite:
            self.canvas.delete(self.shield_sprite)
            self.shield_sprite = None
        if self.sniper_mark:
            self.canvas.delete(self.sniper_mark)
            self.sniper_mark = None
            self.sniper_mark_count = 0
        if self.sprite:
            self.canvas.delete(self.sprite)
            self.sprite = None
        if self in Enemy.enemies:
            Enemy.enemies.remove(self)
        if give_reward:
            game.play_balloon_pop()
            Game.money += self.reward
            self.money_label.config(text=f"💰 {Game.money}c")
        if not Enemy.enemies:
            game.wave_running = False


class ArmoredEnemy(Enemy):
    def __init__(self, canvas, armored_img, shield_img, shield_break_img, path, hp_label, money_label):
        super().__init__(canvas, armored_img, path, speed=1.4, hp_label=hp_label, money_label=money_label)
        self.max_shield      = 12
        self.shield_hp       = self.max_shield
        self.reward          = 8
        self.radius          = 42
        self.shield_img      = shield_img
        self.shield_break_img = shield_break_img
        self.shield_sprite   = None

    def spawn(self):
        x, y = self.path[0]
        self.sprite        = self.canvas.create_image(x, y, image=self.img)
        self.shield_sprite = self.canvas.create_image(x, y, image=self.shield_img)
        Enemy.enemies.append(self)
        self._move()

    def apply_damage(self, dmg):
        if self.shield_hp > 0:
            self.shield_hp -= dmg
            if self.shield_hp <= 0:
                self.break_shield()
            return
        super().apply_damage(dmg)

    def break_shield(self):
        if not self.shield_sprite:
            return
        coords = self.canvas.coords(self.shield_sprite)
        if coords:
            x, y = coords
            fx = self.canvas.create_image(x, y, image=self.shield_break_img)
            self.canvas.after(300, lambda: self.canvas.delete(fx))
        self.canvas.delete(self.shield_sprite)
        self.shield_sprite = None

    def _move(self):
        if game.game_over or not self.sprite:
            return
        coords = self.canvas.coords(self.sprite)
        if not coords:
            return
        if self.point >= len(self.path) - 1:
            dmg = max(1, int(self.hp))
            self._do_delete(give_reward=False)
            Enemy.health -= dmg
            self.hp_label.config(text=f"❤️ {max(0,Enemy.health)} / {getattr(game, '_player_max_hp', 50)}")
            if Enemy.health <= 0:
                game.trigger_game_over()
            return
        x1, y1 = self.path[self.point]
        x2, y2 = self.path[self.point + 1]
        dx, dy  = x2 - x1, y2 - y1
        dist    = (dx**2 + dy**2)**0.5

        my_gen = getattr(self, '_push_gen', 0)
        def step():
            if not self.sprite or game.game_over:
                return
            if getattr(self, '_push_gen', 0) != my_gen:  # ← add this line
                return
            c = self.canvas.coords(self.sprite)
            if not c:
                return
            slow   = self.slow_factor()
            sx, sy = dx/dist*self.speed*slow, dy/dist*self.speed*slow
            cx, cy = c
            if ((cx-x2)**2 + (cy-y2)**2)**0.5 < 5:
                self.point += 1
                self._move()
            else:
                self.canvas.move(self.sprite, sx, sy)
                if self.shield_sprite:
                    self.canvas.move(self.shield_sprite, sx, sy)
                self.canvas.after(20, step)
        step()

    def _do_delete(self, give_reward=True):
        if self.shield_sprite:
            self.canvas.delete(self.shield_sprite)
            self.shield_sprite = None
        super()._do_delete(give_reward)


class BossEnemy(Enemy):
    def __init__(self, canvas, imgs, path, hp_label, money_label):
        super().__init__(canvas, imgs[0], path, speed=0.3,
                         hp_label=hp_label, money_label=money_label)
        self.stage_imgs  = imgs
        self.max_hp      = 1000
        self.hp          = self.max_hp
        self.stage       = 1
        self.reward      = 400
        self.radius      = 60
        self.immune_to_slow = True
        self.pulse_timer = 0
        self.spawn_timer = 0

    def apply_damage(self, dmg):
        self.hp -= dmg
        self.update_stage()
        if self.hp <= 0:
            self.die()

    def update_stage(self):
        hp_pct = self.hp / self.max_hp
        if hp_pct <= 0.33 and self.stage != 3:
            self.stage = 3
            self.speed = 1.2
            if self.sprite:
                self.canvas.itemconfig(self.sprite, image=self.stage_imgs[2])
        elif hp_pct <= 0.66 and self.stage != 2:
            self.stage = 2
            self.speed = 0.9
            if self.sprite:
                self.canvas.itemconfig(self.sprite, image=self.stage_imgs[1])

    def _move(self):
        if game.game_over or not self.sprite:
            return
        if self.point >= len(self.path) - 1:
            dmg = max(1, int(self.hp))
            self._do_delete(give_reward=False)
            Enemy.health -= dmg
            self.hp_label.config(text=f"❤️ {max(0,Enemy.health)} / {getattr(game, '_player_max_hp', 50)}")
            if Enemy.health <= 0:
                game.trigger_game_over()
            return
        coords = self.canvas.coords(self.sprite)
        if not coords:
            return
        cx, cy  = coords
        x2, y2  = self.path[self.point + 1]
        dx, dy  = x2 - cx, y2 - cy
        dist    = (dx**2 + dy**2)**0.5
        if dist == 0 or dist < self.speed + 1:
            self.point += 1
        else:
            self.canvas.move(self.sprite, dx/dist*self.speed, dy/dist*self.speed)
        if self.stage >= 2:
            self.pulse_timer += 1
            if self.pulse_timer >= 60:
                self.emit_shockwave()
                self.pulse_timer = 0
        if self.stage == 3:
            self.spawn_timer += 1
            if self.spawn_timer >= 120:
                self.spawn_minions()
                self.spawn_timer = 0
        self.canvas.after(20, self._move)

    def emit_shockwave(self):
        if not self.sprite:
            return
        coords = self.canvas.coords(self.sprite)
        if not coords:
            return
        x, y = coords
        ring = self.canvas.create_oval(x-20, y-20, x+20, y+20, outline="#ff4757", width=3)
        def expand(r=20):
            if r > 120:
                self.canvas.delete(ring)
                return
            self.canvas.coords(ring, x-r, y-r, x+r, y+r)
            for tower in game.towers:
                tx, ty = tower.get_center()
                if math.hypot(tx-x, ty-y) <= r and hasattr(tower, "put_to_sleep"):
                    tower.put_to_sleep(2000)
            self.canvas.after(30, lambda: expand(r+10))
        expand()

    def spawn_minions(self):
        if not self.sprite:
            return
        coords = self.canvas.coords(self.sprite)
        if not coords:
            return
        x, y = coords
        for _ in range(2):
            Enemy(self.canvas, game.enemy_img, self.path[self.point:],
                  speed=2.4, hp_label=self.hp_label,
                  money_label=self.money_label).spawn_from_position(x, y)

    def spawn(self):
        x, y = self.path[0]
        self.sprite = self.canvas.create_image(x, y, image=self.img)
        Enemy.enemies.append(self)
        self._move()

    def die(self):
        if not self.sprite:
            return
        coords = self.canvas.coords(self.sprite)
        if coords:
            x, y = coords
            boom = self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill="#ff6b81")
            self.canvas.after(400, lambda: self.canvas.delete(boom))
        self._do_delete(give_reward=True)
        # Trigger victory when boss dies
        try:
            game.trigger_victory()
        except Exception:
            pass


class ZeppelinEnemy(Enemy):
    def __init__(self, canvas, dir_imgs, path, hp_label, money_label,
                 wave, speed=0.9, hp=200, reward=45):
        super().__init__(canvas, dir_imgs["R"], path, speed, hp_label, money_label)
        self.dir_imgs        = dir_imgs
        self.hp              = hp
        self.max_hp          = hp
        self.reward          = reward
        self.wave            = wave
        self.payload         = self._get_payload()
        self.payload_released = False

    def _get_payload(self):
        selected = []
        for entry in ZEPPELIN_PAYLOADS:
            if self.wave >= entry["min_wave"]:
                selected = entry["spawn"]
        return selected[:]

    def _get_direction_img(self, dx, dy):
        if abs(dx) >= abs(dy):
            key = "R" if dx > 0 else "L"
        else:
            key = "D" if dy > 0 else "U"
        return self.dir_imgs[key]

    def _move(self):
        if game.game_over or not self.sprite:
            return
        coords = self.canvas.coords(self.sprite)
        if not coords:
            return
        if self.point >= len(self.path) - 1:
            dmg = max(1, int(self.hp))
            self._do_delete(give_reward=False)
            Enemy.health -= dmg
            self.hp_label.config(text=f"❤️ {max(0,Enemy.health)} / {getattr(game, '_player_max_hp', 50)}")
            if Enemy.health <= 0:
                game.trigger_game_over()
            return
        x1, y1 = self.path[self.point]
        x2, y2 = self.path[self.point + 1]
        dx, dy  = x2 - x1, y2 - y1
        dist    = (dx**2 + dy**2)**0.5
        # Set sprite for this segment direction
        self.canvas.itemconfig(self.sprite, image=self._get_direction_img(dx, dy))

        def step():
            if not self.sprite or game.game_over:
                return
            c = self.canvas.coords(self.sprite)
            if not c:
                return
            cx, cy = c
            sx, sy = dx/dist*self.speed, dy/dist*self.speed
            if ((cx-x2)**2 + (cy-y2)**2)**0.5 < 5:
                self.point += 1
                self._move()
            else:
                self.canvas.move(self.sprite, sx, sy)
                self.canvas.after(30, step)
        step()

    def _do_delete(self, give_reward=True):
        if not self.payload_released:
            self.payload_released = True
            pos = self.get_position()
            if pos:
                self._release_payload(pos[0], pos[1])
        super()._do_delete(give_reward)

    def delete(self):
        self._do_delete(give_reward=True)

    def _release_payload(self, x, y):
        delay = 0
        for enemy_type, count in self.payload:
            for _ in range(count):
                def spawn_child(t=enemy_type):
                    self._spawn_child(t, x, y)
                self.canvas.after(delay, spawn_child)
                delay += 250

    def spawn(self):
        x, y = self.path[0]
        self.sprite = self.canvas.create_image(x, y, image=self.dir_imgs["R"])
        Enemy.enemies.append(self)
        self._move()

    def _spawn_child(self, enemy_type, x, y):
        start_index = self.point

        if enemy_type == "armored":
            e = ArmoredEnemy(self.canvas, game.armored_img, game.shield_img,
                         game.shield_break_img, self.path,
                         self.hp_label, self.money_label)
        elif enemy_type == "yellow":
            e = YellowEnemy(self.canvas, game.yellow_img, self.path,
                        self.hp_label, self.money_label)
        elif enemy_type == "blue":
            e = BlueEnemy(self.canvas, game.blue_img, self.path,
                      self.hp_label, self.money_label)
        else:
            e = Enemy(self.canvas, game.enemy_img, self.path, 2,
                 self.hp_label, self.money_label)

        e.spawn_from_position(x, y, start_index=start_index)

# ─── UPGRADE VISUALS ────────────────────────────────────────────────────────

class UpgradeVisuals:
    @staticmethod
    def tag(tower_id):
        return f"upg_visual_{tower_id}"

    @staticmethod
    def refresh(canvas, tower):
        tag = UpgradeVisuals.tag(id(tower))
        canvas.delete(tag)

        total = sum(getattr(tower, f"_path_{p}_level", 0) for p in "ABC")
        if total == 0:
            return

        cls  = tower.__class__.__name__
        glow = TOWER_GLOW_COLOR.get(cls, "#ffffff")
        cx, cy = tower.get_center()

        bx, by  = cx + 14, cy - 14
        badge_r = 8
        label   = "★" if total >= 9 else str(total)

        canvas.create_oval(bx - badge_r, by - badge_r,
                           bx + badge_r, by + badge_r,
                           fill="#0d0d1a", outline=glow, width=2, tags=tag)
        canvas.create_text(bx, by, text=label,
                           fill=glow, font=("Courier", 7, "bold"), tags=tag)
        canvas.tag_raise(tag)


# ─── TOWERS ─────────────────────────────────────────────────────────────────

class UpgradableMixin:
    def _init_upgrades(self):
        self.alive           = True   # ── FIX: guards all after() loops
        self._path_A_level   = 0
        self._path_B_level   = 0
        self._path_C_level   = 0
        self.pierce          = False
        self.pierce_all      = False
        self.aoe_shots       = False
        self.aoe_radius      = 40
        self.slowing_shots   = False
        self.bullet_speed    = 12
        self.target_mode     = "nearest"
        self.auto_retarget   = False
        self.mark_boost      = 1.0
        self.mark_multiplier = 1.0
        self.shock           = False
        self.homing          = False
        self.triple_pulse    = False
        self.crackle         = False
        self.pulse_slow      = None
        self.stun_chance     = 0
        self.stun_duration   = 1000
        self.slow_on_hit     = None
        self.burn_on_hit     = False
        self.cluster         = False
        self.shield_pierce   = False
        self.bullet_size     = 1
        self.auto_collect    = False
        self.overdraft       = 0
        self.bailout         = 0
        self.spike_damage    = 0
        self.spike_stun      = 0
        self.mine_shield_pop = False
        self.recon           = False   # if True, can see/target shadow enemies AND see through blind zones
        # MineTower extras
        self.mine_count      = 6
        self.mine_spacing    = 35
        self.mine_damage     = 2
        self.mine_radius     = 40
        self.mine_shield_pierce = False
        self.mine_slow       = None
        self.mine_burn       = False
        self.mine_cluster    = False

    def can_target(self, enemy):
        """Returns True if this tower can see/target the given enemy."""
        if enemy.is_shadow and not self.recon:
            return False
        # ── Blind-zone check (canyon walls, tunnels) ──────────────────────
        if not self.recon and hasattr(game, "blind_zones") and game.blind_zones:
            pos = enemy.get_position()
            if pos:
                ex, ey = pos
                for (bx1, by1, bx2, by2) in game.blind_zones:
                    if bx1 <= ex <= bx2 and by1 <= ey <= by2:
                        return False
        return True

    def apply_path_upgrade(self, path):
        cls      = self.__class__.__name__
        upgrades = TOWER_UPGRADES.get(cls, {})
        tiers    = upgrades.get(path, [])
        level_attr = f"_path_{path}_level"
        current  = getattr(self, level_attr, 0)
        if current >= len(tiers):
            return False
        _, _, cost, _, effect_fn = tiers[current]
        if Game.money < cost:
            return False
        Game.money -= cost
        self.invested += cost
        effect_fn(self)
        setattr(self, level_attr, current + 1)
        UpgradeVisuals.refresh(self.canvas, self)
        return True

    def get_upgrade_cost(self):
        cls      = self.__class__.__name__
        upgrades = TOWER_UPGRADES.get(cls, {})
        costs    = []
        for path in "ABC":
            tiers = upgrades.get(path, [])
            lvl   = getattr(self, f"_path_{path}_level", 0)
            if lvl < len(tiers):
                costs.append(tiers[lvl][2])
        return min(costs) if costs else None

    def get_refund_amount(self):
        return getattr(self, "invested", 0) // 2


class Tower(UpgradableMixin):
    def __init__(self, canvas, sprite, bullet_img):
        self.canvas       = canvas
        self.sprite       = sprite
        self.base_pil_img = Image.open("tower.png")
        self.tk_img       = ImageTk.PhotoImage(self.base_pil_img)
        self.img          = bullet_img
        self.bullets      = []
        self.placement_radius = 5
        self.sleeping     = False
        self.sleep_overlay = None
        self.fire_rate    = 1200
        self.range        = 150
        self.damage       = 1
        self.invested     = 100
        self._init_upgrades()
        self.canvas_id    = self.sprite
        self.canvas.tag_bind(self.sprite, "<Button-3>", self.select)
        self.canvas.tag_bind(self.sprite, "<Enter>",    self.on_hover)
        self.canvas.tag_bind(self.sprite, "<Leave>",    self.on_leave)
        self._shoot()
        self._update()


    def put_to_sleep(self, duration=2000):
        if self.sleeping: return
        self.sleeping = True
        x, y = self.get_center()
        self.sleep_overlay = self.canvas.create_text(x, y-25, text="💤", font=("Arial", 18))
        self.canvas.after(duration, self.wake_up)

    def wake_up(self):
        self.sleeping = False
        if self.sleep_overlay:
            self.canvas.delete(self.sleep_overlay)
            self.sleep_overlay = None

    def select(self, e): game.select_building(self)
    def get_range(self): return self.range

    def get_center(self):
        coords = self.canvas.coords(self.sprite)
        if not coords: return (0, 0)
        if len(coords) == 2: return coords[0], coords[1]
        x1, y1, x2, y2 = coords
        return (x1+x2)/2, (y1+y2)/2

    def on_hover(self, e):
        x, y = self.get_center()
        game.show_range(x, y, self.range)

    def on_leave(self, e):
        if game.selected_building != self:
            game.hide_range()

    def rotate_towards(self, target):
        center = self.get_center()
        pos    = target.get_position()
        if not center or not pos: return
        cx, cy = center
        tx, ty = pos
        angle  = math.degrees(math.atan2(ty-cy, tx-cx)) + 90
        rotated = self.base_pil_img.rotate(-angle, expand=True)
        self.tk_img = ImageTk.PhotoImage(rotated)
        self.canvas.itemconfig(self.sprite, image=self.tk_img)

    def get_target(self):
        center = self.get_center()
        if not center: return None
        cx, cy = center
        best, best_dist = None, float("inf")
        best_prog = -1
        for e in Enemy.enemies:
            if not self.can_target(e): continue
            pos = e.get_position()
            if not pos: continue
            ex, ey = pos
            dist = ((cx-ex)**2 + (cy-ey)**2)**0.5
            if dist <= self.range:
                if self.target_mode == "farthest":
                    if e.point > best_prog:
                        best_prog = e.point
                        best = e
                else:
                    if dist < best_dist:
                        best_dist = dist
                        best = e
        return best

    def _shoot(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if game.game_over or not self.alive: return
        if self.sleeping:
            self.canvas.after(self.fire_rate, self._shoot)
            return
        target = self.get_target()
        if target:
            self.rotate_towards(target)
            x, y   = self.get_center()
            pos    = target.get_position()
            if pos:
                ex, ey = pos
                dx, dy = ex-x, ey-y
                dist   = (dx**2+dy**2)**0.5
                if dist > 0:
                    spd    = self.bullet_speed
                    vx, vy = dx/dist*spd, dy/dist*spd
                    slow   = self.slow_on_hit if self.slowing_shots else None
                    b      = Bullet(self.canvas, x, y, self.img, vx, vy, self.range,
                                   self.damage, slow=slow, aoe=self.aoe_shots,
                                   aoe_radius=self.aoe_radius, pierce=self.pierce)
                    self.bullets.append(b)
        self.canvas.after(self.fire_rate, self._shoot)

    def _update(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if game.game_over or not self.alive: return
        for b in list(self.bullets):
            if not b.move(Enemy.enemies):
                self.bullets.remove(b)
        self.canvas.after(50, self._update)

    def upgrade(self): pass


class ElementalTower(UpgradableMixin):
    """
    Elemental Tower — neutral until first upgrade locks in Ice / Fire / Wind.
    Each element uses ALL THREE upgrade slots (A / B / C) for a single element;
    once an element is chosen the other two paths are locked out in the panel.
    """

    # Visual theme per element
    _THEME = {
        None:   dict(fill="#1a1a3a", outline="#6666cc", ring="#4444aa",
                     icon="⚗",  glow="#aaaaff"),
        "ice":  dict(fill="#071828", outline="#00d4ff", ring="#006688",
                     icon="❄",  glow="#00d4ff"),
        "fire": dict(fill="#2a0500", outline="#ff6600", ring="#883300",
                     icon="🔥", glow="#ff4400"),
        "wind": dict(fill="#051a0a", outline="#00ff88", ring="#008844",
                     icon="💨", glow="#00ff88"),
    }

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x, self.y = x, y

        # Combat stats
        self.range     = 170
        self.fire_rate = 1400
        self.damage    = 2
        self.sleeping  = False
        self.sleep_overlay = None
        self.placement_radius = 5
        self.invested  = 180

        self._init_upgrades()

        # Element identity — set on first path upgrade
        self.element = None

        # Ice-specific
        self.ice_slow        = 0.5
        self.ice_damage_mult = 1.0
        self.freeze_aoe      = False

        # Fire-specific
        self.burn_duration = 2000
        self.burn_dps      = 1
        self.burn_spread   = False

        self.push_segments = 1
        self.wind_slow = 1.0
        self.wind_aoe = False
        self.wind_arc = False
        self.wind_arc_dmg = 1
        self.wind_arc_slow = 0.0
        self.wind_ring = False

        # Canvas item IDs (built / rebuilt on each element change)
        self._sprite_ids = []
        self.sprite      = None
        self.canvas_id   = None

        self._build_sprite()
        self._start_aura_pulse()
        self._shoot()

        self.ice_linger = 2.5
        self.ice_root = False
        self.ice_brittle = False
        self.ice_frostbite = False
        self.ice_nova_on_death = False
        self.ice_max_targets = 1
        self.ice_storm_mode = False
        self.fire_ignition_burst = 0
        self.burn_chain = 0
        self.burn_spread_radius = 0
        self.burn_interval = 500
        self.fire_ash_zone = False
        self.fire_armor_shred = 0.0
        self.fire_aura = False
        self.wind_banish = False
        self.wind_push_stun = 0
        self.wind_lightning = 0
        self.wind_auto_storm = False


    # ── Sprite construction ───────────────────────────────────────────────────

    def _build_sprite(self):
        """Tear down existing sprite items and draw a fresh themed one."""
        for sid in self._sprite_ids:
            try:
                self.canvas.delete(sid)
            except Exception:
                pass
        self._sprite_ids.clear()

        theme = self._THEME[self.element]
        x, y  = self.x, self.y
        R     = 24  # outer radius

        ids = []

        # Outer glow ring (dashed)
        ids.append(self.canvas.create_oval(
            x - R - 5, y - R - 5, x + R + 5, y + R + 5,
            outline=theme["ring"], width=1, fill="", dash=(3, 4),
        ))

        # Body circle
        body = self.canvas.create_oval(
            x - R, y - R, x + R, y + R,
            fill=theme["fill"], outline=theme["outline"], width=3,
        )
        ids.append(body)

        # Inner detail ring
        ids.append(self.canvas.create_oval(
            x - R + 7, y - R + 7, x + R - 7, y + R - 7,
            fill="", outline=theme["outline"], width=1, dash=(2, 3),
        ))

        # Element icon
        icon = self.canvas.create_text(
            x, y, text=theme["icon"], font=("Arial", 16), fill="white",
        )
        ids.append(icon)

        # Element label strip below the tower (only when element chosen)
        if self.element is not None:
            label_text = {"ice": "❄ ICE", "fire": "🔥 FIRE", "wind": "💨 WIND"}[self.element]
            ids.append(self.canvas.create_text(
                x, y + R + 10,
                text=label_text,
                fill=theme["outline"],
                font=("Courier", 8, "bold"),
            ))

        self._sprite_ids = ids
        self.sprite    = body
        self.canvas_id = body

        # Bind events to the body circle
        self.canvas.tag_bind(body, "<Button-3>", self.select)
        self.canvas.tag_bind(body, "<Enter>",    self.on_hover)
        self.canvas.tag_bind(body, "<Leave>",    self.on_leave)
        # Also bind icon so clicking it selects
        self.canvas.tag_bind(icon, "<Button-3>", self.select)

    # ── Generic projectile traveller ─────────────────────────────────────────────
    def _fire_projectile(self, target, color, outline, size, on_hit):
        """Spawns a small orb that travels to `target`, then calls on_hit(target)."""
        pos = target.get_position()
        if not pos:
            return
        proj = self.canvas.create_oval(
            self.x - size, self.y - size,
            self.x + size, self.y + size,
            fill=color, outline=outline, width=2,
        )
        self._travel(proj, self.x, self.y, target, on_hit, speed=9, size=size)

    def _travel(self, proj, cx, cy, target, on_hit, speed, size):
        if not self.alive or game.game_over:
            try:
                self.canvas.delete(proj)
            except:
                pass
            return
        if not target.sprite:
            try:
                self.canvas.delete(proj)
            except:
                pass
            return
        pos = target.get_position()
        if not pos:
            try:
                self.canvas.delete(proj)
            except:
                pass
            return
        tx, ty = pos
        dx, dy = tx - cx, ty - cy
        dist = math.hypot(dx, dy)
        if dist < speed:
            try:
                self.canvas.delete(proj)
            except:
                pass
            if target.sprite:  # still alive when we arrive
                on_hit(target)
            return
        nx = cx + dx / dist * speed
        ny = cy + dy / dist * speed
        try:
            self.canvas.coords(proj, nx - size, ny - size, nx + size, ny + size)
        except:
            return
        self.canvas.after(16, lambda: self._travel(proj, nx, ny, target, on_hit, speed, size))

    # ── ICE — replace _shoot_ice ──────────────────────────────────────────────────
    def _shoot_ice(self, targets):
        hit = targets[:getattr(self, "ice_max_targets", 1)] if self.freeze_aoe else [targets[0]]
        for e in hit:
            if not e.sprite:
                continue

            def on_ice_hit(enemy, dmg=self.damage, slow=self.ice_slow, mult=self.ice_damage_mult):
                if not enemy.sprite:
                    return
                actual = int(dmg * mult) if enemy.slow_effects.get("ice_freeze") else dmg
                enemy.apply_damage(actual)
                enemy.slow_effects["ice_freeze"] = (slow, time.time() + 2.5)
                self._vfx_ice(enemy)

            self._fire_projectile(e, "#00d4ff", "#aaeeff", 5, on_ice_hit)

    # ── FIRE — replace _shoot_fire ────────────────────────────────────────────────
    def _shoot_fire(self, targets):
        hit = targets[:4] if self.burn_spread else [targets[0]]
        for e in hit:
            if not e.sprite:
                continue

            def on_fire_hit(enemy, dmg=self.damage):
                if not enemy.sprite:
                    return
                burst = getattr(self, "fire_ignition_burst", 0)
                if burst:
                    enemy.apply_damage(burst)
                enemy.apply_damage(dmg)
                self._apply_burn(enemy)

            self._fire_projectile(e, "#ff6600", "#ffaa00", 6, on_fire_hit)

    # ── WIND — replace _shoot_wind ────────────────────────────────────────────────
    def _shoot_wind(self, targets):
        # Path A: pushback (+ optional AoE from Thundergod)
        hit = targets if self.wind_aoe else [targets[0]]
        for e in hit:
            if not e.sprite:
                continue
            e.apply_damage(self.damage)
            self._apply_pushback(e)
            if getattr(self, "wind_lightning", 0) > 0:
                self._chain_lightning(e, self.wind_lightning)
                break

        # Path B: arc / ring blasts — pure damage, never moves sprites
        if getattr(self, "wind_ring", False):
            self._shoot_wind_ring()
        elif getattr(self, "wind_arc", False) and targets:
            pos = targets[0].get_position()
            if pos:
                self._shoot_wind_arc(pos[0], pos[1])

    def cleanup_sprites(self):
        """Called on sell — removes all canvas items this tower owns."""
        for sid in self._sprite_ids:
            try:
                self.canvas.delete(sid)
            except:
                pass
        self._sprite_ids.clear()
        try:
            self.canvas.delete(self._pulse_ring)
        except:
            pass

    # ── Aura pulse animation ──────────────────────────────────────────────────

    def _start_aura_pulse(self):
        """Gentle pulsing ring — color changes when element is chosen."""
        self._pulse_ring = self.canvas.create_oval(
            self.x, self.y, self.x, self.y,
            outline=self._THEME[self.element]["outline"], width=2, fill="",
        )
        self._pulse_step = 0
        self._animate_pulse()

    def _animate_pulse(self):
        if game.game_over or not self.alive:
            return
        self._pulse_step += 1
        r = 28 + 10 * abs(math.sin(self._pulse_step * 0.15))
        x, y = self.x, self.y
        try:
            self.canvas.coords(self._pulse_ring, x - r, y - r, x + r, y + r)
            self.canvas.itemconfig(
                self._pulse_ring,
                outline=self._THEME[self.element]["outline"],
            )
        except Exception:
            pass
        self.canvas.after(40, self._animate_pulse)

    # ── UpgradableMixin override — lock element after first pick ──────────────

    def apply_path_upgrade(self, path):
        path_to_element = {"A": "ice", "B": "fire", "C": "wind"}

        # ── Phase 1: element not chosen yet — free selection ─────────────────
        if self.element is None:
            self.element = path_to_element[path]
            self._path_A_level = 0
            self._path_B_level = 0
            self._path_C_level = 0
            if self.element == "wind":
                self.fire_rate = 3000  # wind blasts every 3 seconds
            self._build_sprite()
            self._burst_vfx()
            return True

        # ── Phase 2: element chosen — use ELEMENTAL_UPGRADES ─────────────────
        upgrades = ELEMENTAL_UPGRADES.get(self.element, {})
        tiers = upgrades.get(path, [])
        level_attr = f"_path_{path}_level"
        current = getattr(self, level_attr, 0)
        if current >= len(tiers):
            return False
        _, _, cost, _, effect_fn = tiers[current]
        if Game.money < cost:
            return False
        Game.money -= cost
        self.invested += cost
        effect_fn(self)
        setattr(self, level_attr, current + 1)
        UpgradeVisuals.refresh(self.canvas, self)

        # Thundergod: kick off the auto-storm loop exactly once
        if (self.element == "wind"
                and getattr(self, "wind_auto_storm", False)
                and not getattr(self, "_auto_storm_running", False)):
            self._auto_storm_running = True
            self.canvas.after(2000, self._start_auto_storm)

        return True

    def _burst_vfx(self):
        """Short particle burst when element is first chosen."""
        theme = self._THEME[self.element]
        x, y  = self.x, self.y
        burst_ids = []
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            ex  = x + math.cos(rad) * 40
            ey  = y + math.sin(rad) * 40
            lid = self.canvas.create_line(x, y, ex, ey,
                                          fill=theme["outline"], width=2)
            burst_ids.append(lid)

        def clear():
            for lid in burst_ids:
                try:
                    self.canvas.delete(lid)
                except Exception:
                    pass

        self.canvas.after(300, clear)

    # ── Standard tower interface ──────────────────────────────────────────────

    def get_center(self):  return self.x, self.y
    def get_range(self):   return self.range
    def select(self, e):   game.select_building(self)
    def upgrade(self):     pass

    def on_hover(self, e):
        theme = self._THEME[self.element]
        game.show_range(self.x, self.y, self.range, theme["outline"])

    def on_leave(self, e):
        if game.selected_building != self:
            game.hide_range()

    def put_to_sleep(self, duration=2000):
        if self.sleeping:
            return
        self.sleeping = True
        self.sleep_overlay = self.canvas.create_text(
            self.x, self.y - 32, text="💤", font=("Arial", 18),
        )
        self.canvas.after(duration, self.wake_up)

    def wake_up(self):
        self.sleeping = False
        if self.sleep_overlay:
            self.canvas.delete(self.sleep_overlay)
            self.sleep_overlay = None

    # ── Target acquisition ────────────────────────────────────────────────────

    def _get_targets(self):
        """Return enemies in range sorted nearest-first."""
        cx, cy   = self.x, self.y
        in_range = []
        for e in Enemy.enemies:
            if not self.can_target(e):
                continue
            pos = e.get_position()
            if not pos:
                continue
            d = math.hypot(cx - pos[0], cy - pos[1])
            if d <= self.range:
                in_range.append((d, e))
        in_range.sort(key=lambda t: t[0])
        return [e for _, e in in_range]

    # ── Main shoot loop ───────────────────────────────────────────────────────

    def _shoot(self):
        if game.game_over or not self.alive:
            return
        if self.sleeping or self.element is None:
            self.canvas.after(self.fire_rate, self._shoot)
            return

        targets = self._get_targets()
        if targets:
            if self.element == "ice":
                self._shoot_ice(targets)
            elif self.element == "fire":
                self._shoot_fire(targets)
            elif self.element == "wind":
                self._shoot_wind(targets)

        self.canvas.after(self.fire_rate, self._shoot)

    # ── ICE ───────────────────────────────────────────────────────────────────

    def _shoot_ice(self, targets):
        hit = targets if self.freeze_aoe else [targets[0]]
        for e in hit:
            if not e.sprite:
                continue
            # Bonus damage if already frozen
            dmg = self.damage
            if e.slow_effects.get("ice_freeze"):
                dmg = int(dmg * self.ice_damage_mult)
            e.apply_damage(dmg)
            # Apply slow / freeze
            e.slow_effects["ice_freeze"] = (self.ice_slow, time.time() + 2.5)
            self._vfx_ice(e)

    def _vfx_ice(self, enemy):
        pos = enemy.get_position()
        if not pos:
            return
        x, y = pos

        # ── Impact burst: expanding crystal spokes ───────────────────────
        spokes = []
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            ex = x + math.cos(rad) * 18
            ey = y + math.sin(rad) * 18
            spokes.append(self.canvas.create_line(
                x, y, ex, ey, fill="#aaeeff", width=2,
            ))
        ring = self.canvas.create_oval(
            x - 18, y - 18, x + 18, y + 18,
            outline="#00d4ff", width=2, dash=(2, 2),
        )

        def clear_burst(step=0):
            if step >= 5:
                for s in spokes:
                    try:
                        self.canvas.delete(s)
                    except:
                        pass
                try:
                    self.canvas.delete(ring)
                except:
                    pass
                return
            self.canvas.after(55, lambda: clear_burst(step + 1))

        clear_burst()

        # ── Persistent freeze crust (replaced each time for fresh pulse) ─
        self._remove_ice_crust(enemy)
        cx_outer = self.canvas.create_oval(
            x - 20, y - 20, x + 20, y + 20,
            outline="#00d4ff", width=2, dash=(3, 2), fill="",
        )
        cx_inner = self.canvas.create_oval(
            x - 11, y - 11, x + 11, y + 11,
            outline="#aaeeff", width=1, dash=(2, 3), fill="",
        )
        flake = self.canvas.create_text(
            x, y - 24, text="❄", fill="#aaeeff", font=("Arial", 9),
        )
        enemy._ice_crust = (cx_outer, cx_inner, flake)
        self._animate_ice_crust(enemy)

    def _animate_ice_crust(self, enemy, step=0):
        """Follows enemy + shimmers the crust while frozen."""
        if game.game_over or not self.alive:
            self._remove_ice_crust(enemy)
            return
        if not enemy.sprite or not getattr(enemy, "_ice_crust", None):
            self._remove_ice_crust(enemy)
            return
        freeze = enemy.slow_effects.get("ice_freeze")
        if not freeze or freeze[1] < time.time():
            self._remove_ice_crust(enemy)
            return
        pos = enemy.get_position()
        if not pos:
            self._remove_ice_crust(enemy)
            return
        x, y = pos
        outer, inner, flake = enemy._ice_crust
        # Shimmer: alternate dash phase
        da = (3, 2) if step % 2 == 0 else (2, 3)
        db = (2, 3) if step % 2 == 0 else (3, 2)
        try:
            self.canvas.coords(outer, x - 20, y - 20, x + 20, y + 20)
            self.canvas.itemconfig(outer, dash=da)
            self.canvas.coords(inner, x - 11, y - 11, x + 11, y + 11)
            self.canvas.itemconfig(inner, dash=db)
            self.canvas.coords(flake, x, y - 24)
            self.canvas.tag_raise(outer)
            self.canvas.tag_raise(inner)
            self.canvas.tag_raise(flake)
        except Exception:
            self._remove_ice_crust(enemy)
            return
        self.canvas.after(180, lambda: self._animate_ice_crust(enemy, step + 1))

    def _remove_ice_crust(self, enemy):
        crust = getattr(enemy, "_ice_crust", None)
        if crust:
            for sid in crust:
                try:
                    self.canvas.delete(sid)
                except:
                    pass
        enemy._ice_crust = None

        def fade(step=0):
            if step >= 5:
                for s in spokes:
                    try: self.canvas.delete(s)
                    except Exception: pass
                try: self.canvas.delete(ring)
                except Exception: pass
                return
            self.canvas.after(70, lambda: fade(step + 1))

        fade()

    # ── FIRE ──────────────────────────────────────────────────────────────────

    def _shoot_fire(self, targets):
        hit = targets[:4] if self.burn_spread else [targets[0]]
        for e in hit:
            if not e.sprite:
                continue
            e.apply_damage(self.damage)
            self._apply_burn(e)

    def _apply_burn(self, enemy):
        if getattr(enemy, "_burning", False):
            return
        enemy._burning = True
        ticks_remaining = self.burn_duration // 500
        burn_dps = self.burn_dps
        self._start_embers(enemy)

        def tick(n):
            if n <= 0 or not enemy.sprite or game.game_over:
                enemy._burning = False
                self._stop_embers(enemy)
                sid = getattr(enemy, "_fire_sprite", None)
                if sid:
                    try:
                        self.canvas.delete(sid)
                    except:
                        pass
                    enemy._fire_sprite = None
                return
            pos = enemy.get_position()
            if pos:
                x, y = pos
                icon = "🔥" if burn_dps < 3 else "💥"
                size = 10 + min(burn_dps * 2, 8)
                if not getattr(enemy, "_fire_sprite", None):
                    enemy._fire_sprite = self.canvas.create_text(
                        x, y - 20, text=icon, font=("Arial", size),
                    )
                else:
                    try:
                        self.canvas.coords(enemy._fire_sprite, x, y - 20)
                        self.canvas.itemconfig(enemy._fire_sprite, text=icon,
                                               font=("Arial", size))
                        self.canvas.tag_raise(enemy._fire_sprite)
                    except:
                        pass
            enemy.apply_damage(burn_dps)
            self.canvas.after(500, lambda: tick(n - 1))

        tick(ticks_remaining)

    def _start_embers(self, enemy):
        enemy._ember_active = True
        self._emit_ember(enemy)

    def _stop_embers(self, enemy):
        enemy._ember_active = False

    def _emit_ember(self, enemy):
        if not getattr(enemy, "_ember_active", False) or game.game_over:
            return
        if not enemy.sprite:
            return
        pos = enemy.get_position()
        if not pos:
            return
        x, y = pos
        col = random.choice(["#ff4500", "#ff6600", "#ffaa00", "#ff2200", "#ffcc00"])
        ox = x + random.randint(-10, 10)
        ember = self.canvas.create_oval(ox - 2, y - 2, ox + 2, y + 2,
                                        fill=col, outline="")
        self._float_ember(ember, random.uniform(-1.0, 1.0), 20)
        self.canvas.after(110, lambda: self._emit_ember(enemy))

    def _float_ember(self, ember_id, drift_x, steps):
        if steps <= 0:
            try:
                self.canvas.delete(ember_id)
            except:
                pass
            return
        try:
            self.canvas.move(ember_id, drift_x + random.uniform(-0.5, 0.5), -1.8)
            # Fade to dark as ember dies
            if steps < 7:
                self.canvas.itemconfig(ember_id, fill="#551100")
        except:
            return
        self.canvas.after(35, lambda: self._float_ember(ember_id, drift_x, steps - 1))

    # ── WIND ──────────────────────────────────────────────────────────────────

    def _apply_pushback(self, enemy):
        """Push enemy back along the path — one-time per enemy, no slide animation."""
        if not enemy.sprite:
            return
        if getattr(enemy, "_wind_pushed", False):
            return  # already pushed once this life

        new_point = 0 if getattr(self, "wind_banish", False) \
                    else max(0, enemy.point - self.push_segments)
        if new_point == enemy.point:
            return

        pos = enemy.get_position()
        if not pos:
            return
        ex, ey = pos

        enemy._wind_pushed = True

        # Kill the current _move loop
        enemy._push_gen = getattr(enemy, "_push_gen", 0) + 1
        enemy.point = new_point

        self._tornado_vfx()

        # Gust VFX line from enemy toward tower
        gust = self.canvas.create_line(
            ex, ey, self.x, self.y,
            fill="#00ff88", width=2, dash=(6, 4))
        self.canvas.after(200, lambda: self.canvas.delete(gust))

        # Snap sprite directly to the target waypoint — clean re-entry into _move
        tx, ty = enemy.path[new_point]
        try:
            self.canvas.coords(enemy.sprite, tx, ty)
            self._sync_attached(enemy, tx, ty)
        except Exception:
            pass

        if self.wind_slow < 1.0:
            enemy.slow_effects["wind_slow"] = (self.wind_slow, time.time() + 1.8)
        stun_ms = getattr(self, "wind_push_stun", 0)
        if stun_ms:
            enemy.slow_effects["wind_stun"] = (0.01, time.time() + stun_ms / 1000)

        enemy._move()

    def _tornado_vfx(self):
        """Spiralling green particles that suck into the tower center."""
        cx, cy = self.x, self.y
        NUM = 12
        particles = []
        for i in range(NUM):
            ang = i * (360 / NUM)
            rad = math.radians(ang)
            px = cx + math.cos(rad) * 48
            py = cy + math.sin(rad) * 48
            col = random.choice(["#00ff88", "#aaffcc", "#00cc66", "#ffffff"])
            p = self.canvas.create_oval(px - 4, py - 4, px + 4, py + 4,
                                        fill=col, outline="")
            particles.append([p, ang, 48.0])

        def spin(step=0, pts=particles):
            if step >= 20:
                for item in pts:
                    try:
                        self.canvas.delete(item[0])
                    except Exception:
                        pass
                return
            new_pts = []
            for item in pts:
                p, ang, r = item
                ang += 22
                r = max(3, r - 2.3)
                rad = math.radians(ang)
                px = cx + math.cos(rad) * r
                py = cy + math.sin(rad) * r
                try:
                    self.canvas.coords(p, px - 3, py - 3, px + 3, py + 3)
                except Exception:
                    pass
                new_pts.append([p, ang, r])
            self.canvas.after(32, lambda: spin(step + 1, new_pts))

        spin()

    def _shoot_wind_arc(self, target_x, target_y):
        """Crosswind / Windshear: blast ±60° side arcs from the primary shot direction."""
        base_angle = math.degrees(math.atan2(target_y - self.y, target_x - self.x))
        arc_dmg  = getattr(self, "wind_arc_dmg", 1)
        arc_slow = getattr(self, "wind_arc_slow", 0.0)

        for side_angle in (base_angle - 60, base_angle + 60):
            rad = math.radians(side_angle)
            ex  = self.x + math.cos(rad) * self.range
            ey  = self.y + math.sin(rad) * self.range

            # VFX: sweeping gust line + endpoint flash
            gust = self.canvas.create_line(
                self.x, self.y, ex, ey,
                fill="#00ff88", width=3, dash=(8, 4))
            flash = self.canvas.create_oval(
                ex - 12, ey - 12, ex + 12, ey + 12,
                outline="#aaffcc", width=2, fill="")
            self.canvas.after(200, lambda a=gust, f=flash: (
                self.canvas.delete(a), self.canvas.delete(f)))

            # Hit enemies inside the 60° cone (±30° around side_angle)
            for e in list(Enemy.enemies):
                if not e.sprite:
                    continue
                pos = e.get_position()
                if not pos:
                    continue
                dist = math.hypot(pos[0] - self.x, pos[1] - self.y)
                if dist > self.range:
                    continue
                enemy_angle = math.degrees(math.atan2(pos[1] - self.y, pos[0] - self.x))
                diff = abs((enemy_angle - side_angle + 180) % 360 - 180)
                if diff <= 30:
                    e.apply_damage(arc_dmg)
                    if arc_slow > 0:
                        e.slow_effects["wind_arc"] = (arc_slow, time.time() + 1.5)

    def _shoot_wind_ring(self):
        """Maelstrom: 360° ring blast — damages and slows every enemy in range."""
        arc_dmg  = getattr(self, "wind_arc_dmg", 3)
        arc_slow = getattr(self, "wind_arc_slow", 0.0)
        R = self.range

        # VFX: expanding ring + spokes
        ring = self.canvas.create_oval(
            self.x - R, self.y - R, self.x + R, self.y + R,
            outline="#00ff88", width=4)
        inner = self.canvas.create_oval(
            self.x - R // 2, self.y - R // 2,
            self.x + R // 2, self.y + R // 2,
            outline="#aaffcc", width=2)
        spokes = []
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            s = self.canvas.create_line(
                self.x, self.y,
                self.x + math.cos(rad) * R,
                self.y + math.sin(rad) * R,
                fill="#00ff88", width=1, dash=(5, 8))
            spokes.append(s)

        def clear_ring():
            self.canvas.delete(ring)
            self.canvas.delete(inner)
            for s in spokes:
                try: self.canvas.delete(s)
                except: pass
        self.canvas.after(280, clear_ring)

        # Damage every enemy in range — no position changes
        for e in list(Enemy.enemies):
            if not e.sprite:
                continue
            pos = e.get_position()
            if not pos:
                continue
            if math.hypot(pos[0] - self.x, pos[1] - self.y) <= R:
                e.apply_damage(arc_dmg)
                if arc_slow > 0:
                    e.slow_effects["wind_arc"] = (arc_slow, time.time() + 2.0)

    def _sync_attached_move(self, enemy, dx, dy):
        """Move shield, sniper mark, and fire sprites alongside enemy."""
        for attr in ("shield_sprite", "sniper_mark", "_fire_sprite"):
            sid = getattr(enemy, attr, None)
            if sid:
                try:
                    self.canvas.move(sid, dx, dy)
                except Exception:
                    pass

    def _sync_attached(self, enemy, x, y):
        """Teleport attached sprites to exact position (with per-sprite offsets)."""
        offsets = {
            "shield_sprite": (0, 0),
            "sniper_mark": (0, -18),
            "_fire_sprite": (0, -20),
        }
        for attr, (ox, oy) in offsets.items():
            sid = getattr(enemy, attr, None)
            if sid:
                try:
                    self.canvas.coords(sid, x + ox, y + oy)
                except Exception:
                    pass

    def _chain_lightning(self, origin, chain_count):
        """Jump lightning from origin to the chain_count nearest enemies for 3 dmg each."""
        pos = origin.get_position()
        if not pos:
            return
        lx, ly = pos

        candidates = []
        for e in Enemy.enemies:
            if e is origin or not e.sprite:
                continue
            p = e.get_position()
            if not p:
                continue
            d = math.hypot(p[0] - lx, p[1] - ly)
            if d <= self.range * 1.6:
                candidates.append((d, e))
        candidates.sort(key=lambda x: x[0])

        hit_targets = [e for _, e in candidates[:chain_count]]
        cur_x, cur_y = lx, ly

        for target in hit_targets:
            p = target.get_position()
            if not p:
                continue
            tx, ty = p
            # Main bolt
            bolt = self.canvas.create_line(
                cur_x, cur_y, tx, ty,
                fill="#ffff44", width=2, dash=(5, 2))
            self.canvas.after(200, lambda b=bolt: self.canvas.delete(b))
            # Zigzag accent through midpoint
            mx = (cur_x + tx) / 2 + random.randint(-18, 18)
            my = (cur_y + ty) / 2 + random.randint(-18, 18)
            zag = self.canvas.create_line(
                cur_x, cur_y, mx, my, tx, ty,
                fill="#aaffff", width=1)
            self.canvas.after(130, lambda z=zag: self.canvas.delete(z))
            # Impact flash
            flash = self.canvas.create_oval(
                tx - 8, ty - 8, tx + 8, ty + 8,
                fill="#ffffff", outline="#ffff44")
            self.canvas.after(80, lambda f=flash: self.canvas.delete(f))

            target.apply_damage(3)
            cur_x, cur_y = tx, ty

    def _start_auto_storm(self):
        """Thundergod: every 2s, fire a lightning storm hitting all enemies in range."""
        if game.game_over or not self.alive:
            return
        if not getattr(self, "wind_auto_storm", False):
            return

        self._tornado_vfx()

        # Strike every enemy in range
        struck = False
        for e in list(Enemy.enemies):
            if not e.sprite:
                continue
            pos = e.get_position()
            if not pos:
                continue
            if math.hypot(pos[0] - self.x, pos[1] - self.y) <= self.range:
                if not struck:
                    self._chain_lightning(e, getattr(self, "wind_lightning", 6))
                    struck = True
                else:
                    e.apply_damage(2)

        self.canvas.after(2000, self._start_auto_storm)

class BallTower(UpgradableMixin):
    def __init__(self, canvas, x, y, bullet_img):
        self.canvas       = canvas
        self.img          = bullet_img
        self.bullets      = []
        self.placement_radius = 5
        self.fire_rate    = 2300
        self.projectiles  = 4
        self.range        = 100
        self.damage       = 1
        self.sleeping     = False
        self.sleep_overlay = None
        self.invested     = 150
        self._init_upgrades()
        r = 20
        self.sprite = canvas.create_oval(x-r, y-r, x+r, y+r,
                                          fill="#ff9f1c", outline="black", width=2)
        self.canvas_id = self.sprite
        self.canvas.tag_bind(self.canvas_id, "<Enter>",    self.on_hover)
        self.canvas.tag_bind(self.canvas_id, "<Leave>",    self.on_leave)
        self.canvas.tag_bind(self.canvas_id, "<Button-3>", self.select)
        self._shoot_circle()
        self._update()

    def put_to_sleep(self, duration=2000):
        if self.sleeping: return
        self.sleeping = True
        x, y = self.get_center()
        self.sleep_overlay = self.canvas.create_text(x, y-25, text="💤", font=("Arial", 18))
        self.canvas.after(duration, self.wake_up)

    def wake_up(self):
        self.sleeping = False
        if self.sleep_overlay:
            self.canvas.delete(self.sleep_overlay)
            self.sleep_overlay = None

    def select(self, e): game.select_building(self)
    def get_range(self): return self.range

    def get_center(self):
        coords = self.canvas.coords(self.sprite)
        if not coords or len(coords) < 4: return (0, 0)
        x1, y1, x2, y2 = coords
        return (x1+x2)/2, (y1+y2)/2

    def on_hover(self, e):
        x, y = self.get_center()
        game.show_range(x, y, self.range, "#ffa502")

    def on_leave(self, e):
        if game.selected_building != self:
            game.hide_range()

    def has_enemy_in_range(self):
        cx, cy = self.get_center()
        for e in Enemy.enemies:
            if not self.can_target(e): continue
            pos = e.get_position()
            if pos and ((cx-pos[0])**2 + (cy-pos[1])**2)**0.5 <= self.range:
                return True
        return False

    def _shoot_circle(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if game.game_over or not self.alive: return
        if self.sleeping:
            self.canvas.after(200, self._shoot_circle)
            return
        if not self.has_enemy_in_range():
            self.canvas.after(200, self._shoot_circle)
            return
        x, y = self.get_center()
        step = 360 // self.projectiles
        for angle in range(0, 360, step):
            rad    = math.radians(angle)
            dx, dy = math.cos(rad)*6, math.sin(rad)*6
            self.bullets.append(Bullet(self.canvas, x, y, self.img, dx, dy,
                                        self.range, self.damage,
                                        aoe=self.aoe_shots, aoe_radius=self.aoe_radius))
        self.canvas.after(self.fire_rate, self._shoot_circle)

    def _update(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if game.game_over or not self.alive: return
        for b in list(self.bullets):
            if not b.move(Enemy.enemies):
                self.bullets.remove(b)
        self.canvas.after(50, self._update)

    def upgrade(self): pass


class AngryTower(UpgradableMixin):
    def __init__(self, canvas, x, y, imgs):
        self.canvas       = canvas
        self.imgs         = imgs
        self.direction    = "right"
        self.spread_shots = 1
        self.spread_angle = 30
        self.bullet_speed = 25
        self.sleeping     = False
        self.sleep_overlay = None
        self.range        = 260
        self.fire_rate    = 200
        self.damage       = 1
        self.placement_radius = 5
        self.invested     = 670
        self._init_upgrades()

        self.target_pos    = None
        self.fixed_target  = False
        self._target_marker_ids = []

        self.sprite    = canvas.create_image(x, y, image=self.imgs[self.direction])
        self.canvas_id = self.sprite
        self.bullets   = []
        self.canvas.tag_bind(self.sprite, "<Button-3>",       self.select)
        self.canvas.tag_bind(self.sprite, "<Shift-Button-1>", self.rotate)
        self.canvas.tag_bind(self.sprite, "<Enter>",          self.on_hover)
        self.canvas.tag_bind(self.sprite, "<Leave>",          self.on_leave)
        self._shoot()
        self._update()

    def put_to_sleep(self, duration=2000):
        if self.sleeping: return
        self.sleeping = True
        x, y = self.get_center()
        self.sleep_overlay = self.canvas.create_text(x, y-25, text="💤", font=("Arial", 18))
        self.canvas.after(duration, self.wake_up)

    def wake_up(self):
        self.sleeping = False
        if self.sleep_overlay:
            self.canvas.delete(self.sleep_overlay)
            self.sleep_overlay = None

    def select(self, e): game.select_building(self)

    def rotate(self, e):
        order = ["up", "right", "down", "left"]
        self.direction = order[(order.index(self.direction) + 1) % 4]
        self.canvas.itemconfig(self.sprite, image=self.imgs[self.direction])

    def get_center(self):
        coords = self.canvas.coords(self.sprite)
        if not coords: return (0, 0)
        return coords[0], coords[1]

    def get_range(self): return self.range

    def on_hover(self, e):
        x, y = self.get_center()
        game.show_range(x, y, self.range, "#ff3838")

    def on_leave(self, e):
        if game.selected_building != self:
            game.hide_range()

    def set_target(self, x, y):
        self.target_pos   = (x, y)
        self.fixed_target = True
        self._draw_target_marker(x, y)

    def clear_target(self):
        self.fixed_target = False
        self.target_pos   = None
        for item_id in self._target_marker_ids:
            self.canvas.delete(item_id)
        self._target_marker_ids.clear()

    def _draw_target_marker(self, x, y):
        for item_id in self._target_marker_ids:
            self.canvas.delete(item_id)
        self._target_marker_ids.clear()
        col = "#ff4757"
        r   = 14
        ids = [
            self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=col, width=2, state="hidden"),
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill=col, outline="", state="hidden"),
            self.canvas.create_line(x-r-4, y, x-r+4, y, fill=col, width=2, state="hidden"),
            self.canvas.create_line(x+r-4, y, x+r+4, y, fill=col, width=2, state="hidden"),
            self.canvas.create_line(x, y-r-4, x, y-r+4, fill=col, width=2, state="hidden"),
            self.canvas.create_line(x, y+r-4, x, y+r+4, fill=col, width=2, state="hidden"),
        ]
        cx, cy = self.get_center()
        ids.append(self.canvas.create_line(cx, cy, x, y,
                                            fill=col, dash=(4, 3), width=1, state="hidden"))
        self._target_marker_ids.extend(ids)

    def show_target_marker(self):
        for item_id in self._target_marker_ids:
            self.canvas.itemconfig(item_id, state="normal")

    def hide_target_marker(self):
        for item_id in self._target_marker_ids:
            self.canvas.itemconfig(item_id, state="hidden")

    def enemy_in_line(self):
        cx, cy = self.get_center()
        for e in Enemy.enemies:
            if not self.can_target(e): continue
            pos = e.get_position()
            if not pos: continue
            ex, ey = pos
            if self.direction == "right" and ex > cx and abs(ey-cy) < 25 and ex-cx <= self.range:
                return e
            if self.direction == "left"  and ex < cx and abs(ey-cy) < 25 and cx-ex <= self.range:
                return e
            if self.direction == "up"    and ey < cy and abs(ex-cx) < 25 and cy-ey <= self.range:
                return e
            if self.direction == "down"  and ey > cy and abs(ex-cx) < 25 and ey-cy <= self.range:
                return e
        return None

    def _shoot(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if game.game_over or not self.alive: return
        if self.sleeping:
            self.canvas.after(self.fire_rate, self._shoot)
            return

        if self.fixed_target and self.target_pos:
            cx, cy     = self.get_center()
            tx, ty     = self.target_pos
            dx, dy     = tx - cx, ty - cy
            dist_to_tgt = math.hypot(dx, dy)
            if dist_to_tgt > 0:
                base_angle = math.degrees(math.atan2(dy, dx))
                for _ in range(self.spread_shots):
                    angle  = base_angle + random.uniform(-self.spread_angle/2, self.spread_angle/2)
                    rad    = math.radians(angle)
                    vx, vy = math.cos(rad)*self.bullet_speed, math.sin(rad)*self.bullet_speed
                    self.bullets.append(
                        Bullet(self.canvas, cx, cy, game.bullet_img, vx, vy,
                               self.range, self.damage,
                               aoe=self.aoe_shots,
                               aoe_radius=getattr(self, "aoe_radius", 40),
                               pierce=self.pierce))
        else:
            target = self.enemy_in_line()
            if target:
                cx, cy = self.get_center()
                base   = {"right": 0, "down": 90, "left": 180, "up": 270}[self.direction]
                for _ in range(self.spread_shots):
                    angle  = base + random.uniform(-self.spread_angle/2, self.spread_angle/2)
                    rad    = math.radians(angle)
                    vx, vy = math.cos(rad)*self.bullet_speed, math.sin(rad)*self.bullet_speed
                    self.bullets.append(
                        Bullet(self.canvas, cx, cy, game.bullet_img, vx, vy,
                               self.range, self.damage,
                               aoe=self.aoe_shots,
                               aoe_radius=getattr(self, "aoe_radius", 40),
                               pierce=self.pierce))

        self.canvas.after(self.fire_rate, self._shoot)

    def _update(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if game.game_over or not self.alive: return
        for b in list(self.bullets):
            if not b.move(Enemy.enemies):
                self.bullets.remove(b)
        self.canvas.after(40, self._update)

    def upgrade(self): pass


class BombTower(UpgradableMixin):
    def __init__(self, canvas, x, y, tower_img, bomb_img):
        self.canvas       = canvas
        self.tower_img    = tower_img
        self.bomb_img     = bomb_img
        self.placement_radius = 5
        self.base_pil_img = Image.open("bomber.png")
        self.tk_img       = ImageTk.PhotoImage(self.base_pil_img)
        self.sleeping     = False
        self.sleep_overlay = None
        self.range        = 130
        self.fire_rate    = 4000
        self.bomb_radius  = 45
        self.damage       = 1
        self.invested     = 350
        self._init_upgrades()
        self.sprite    = canvas.create_image(x, y, image=tower_img)
        self.canvas_id = self.sprite
        self.canvas.tag_bind(self.sprite, "<Button-3>", self.select)
        self.canvas.tag_bind(self.canvas_id, "<Enter>",    self.on_hover)
        self.canvas.tag_bind(self.canvas_id, "<Leave>",    self.on_leave)
        self._throw_bomb()

    def put_to_sleep(self, duration=2000):
        if self.sleeping: return
        self.sleeping = True
        x, y = self.get_center()
        self.sleep_overlay = self.canvas.create_text(x, y-25, text="💤", font=("Arial", 18))
        self.canvas.after(duration, self.wake_up)

    def wake_up(self):
        self.sleeping = False
        if self.sleep_overlay:
            self.canvas.delete(self.sleep_overlay)
            self.sleep_overlay = None

    def select(self, e): game.select_building(self)

    def get_center(self):
        coords = self.canvas.coords(self.sprite)
        if not coords or len(coords) < 2: return (0, 0)
        return coords[0], coords[1]

    def get_range(self): return self.range

    def on_hover(self, e):
        x, y = self.get_center()
        game.show_range(x, y, self.range, "#ff6b6b")

    def on_leave(self, e):
        if game.selected_building != self:
            game.hide_range()

    def rotate_towards(self, target):
        center = self.get_center()
        pos    = target.get_position()
        if not center or not pos: return
        cx, cy = center; tx, ty = pos
        angle  = math.degrees(math.atan2(ty-cy, tx-cx)) + 90
        rotated = self.base_pil_img.rotate(-angle, expand=True)
        self.tk_img = ImageTk.PhotoImage(rotated)
        self.canvas.itemconfig(self.sprite, image=self.tk_img)

    def get_nearest_enemy(self):
        cx, cy = self.get_center()
        nearest, best_dist = None, float("inf")
        for e in Enemy.enemies:
            pos = e.get_position()
            if not pos: continue
            d = ((cx-pos[0])**2 + (cy-pos[1])**2)**0.5
            if d < best_dist and d <= self.range:
                best_dist, nearest = d, e
        return nearest

    def _throw_bomb(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if game.game_over or not self.alive: return
        if self.sleeping:
            self.canvas.after(self.fire_rate, self._throw_bomb)
            return
        target = self.get_nearest_enemy()
        if target:
            self.rotate_towards(target)
            pos = target.get_position()
            if pos:
                tx, ty = pos
                x, y   = self.get_center()
                Bomb(self.canvas, x, y, self.bomb_img, tx, ty,
                     radius=self.bomb_radius, damage=self.damage,
                     slow_on_hit=self.slow_on_hit, burn_on_hit=self.burn_on_hit,
                     cluster=self.cluster, shield_pierce=self.shield_pierce)
        self.canvas.after(self.fire_rate, self._throw_bomb)

    def upgrade(self): pass


class SniperTower(UpgradableMixin):
    def __init__(self, canvas, x, y):
        self.canvas       = canvas
        self.base_pil_img = Image.open("sniper.png")
        self.tk_img       = ImageTk.PhotoImage(self.base_pil_img)
        self.sprite       = canvas.create_image(x, y, image=self.tk_img)
        self.canvas_id    = self.sprite
        self.range        = 350
        self.damage       = 10
        self.reload_time  = 3200
        self.target       = None
        self.sleeping     = False
        self.sleep_overlay = None
        self.placement_radius = 5
        self.invested     = 850
        self._init_upgrades()
        self.canvas.tag_bind(self.sprite, "<Button-3>", self.select)
        self.canvas.tag_bind(self.sprite, "<Enter>",    self.on_hover)
        self.canvas.tag_bind(self.sprite, "<Leave>",    self.on_leave)
        self._reload()

    def select(self, e): game.select_building(self)

    def on_hover(self, e):
        x, y = self.get_center()
        game.show_range(x, y, self.range, "#1e90ff")

    def on_leave(self, e):
        if game.selected_building != self:
            game.hide_range()

    def get_center(self):
        coords = self.canvas.coords(self.sprite)
        if not coords or len(coords) < 2: return (0, 0)
        return coords[0], coords[1]

    def get_range(self): return self.range

    def put_to_sleep(self, duration=2000):
        if self.sleeping: return
        self.sleeping = True
        x, y = self.get_center()
        self.sleep_overlay = self.canvas.create_text(x, y-25, text="💤", font=("Arial", 18))
        self.canvas.after(duration, self.wake_up)

    def wake_up(self):
        self.sleeping = False
        if self.sleep_overlay:
            self.canvas.delete(self.sleep_overlay)
            self.sleep_overlay = None

    def rotate_towards(self, target):
        pos    = target.get_position()
        center = self.get_center()
        if not pos or not center: return
        cx, cy = center; tx, ty = pos
        angle  = math.degrees(math.atan2(ty-cy, tx-cx)) + 90
        rotated = self.base_pil_img.rotate(-angle, expand=True)
        self.tk_img = ImageTk.PhotoImage(rotated)
        self.canvas.itemconfig(self.sprite, image=self.tk_img)

    def find_target(self):
        cx, cy = self.get_center()
        best, best_dist = None, float("inf")
        for e in Enemy.enemies:
            if not self.can_target(e): continue
            pos = e.get_position()
            if not pos: continue
            d = ((cx-pos[0])**2 + (cy-pos[1])**2)**0.5
            if d <= self.range and d < best_dist:
                best_dist, best = d, e
        return best

    def _reload(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if game.game_over or not self.alive: return
        if self.sleeping:
            self.canvas.after(200, self._reload)
            return
        new_target = self.find_target()
        if new_target != self.target:
            if self.target:
                self.target.remove_sniper_mark(self.canvas)
            self.target = new_target
            if self.target:
                self.target.add_sniper_mark(self.canvas)
        if self.target:
            self.rotate_towards(self.target)
            self._shoot()
        self.canvas.after(self.reload_time, self._reload)

    def _shoot(self):
        if not self.target: return
        x, y = self.get_center()
        SniperBullet(self.canvas, x, y, game.sniper_bullet_img, self.target,
                     self.damage, pierce_all=self.pierce_all)
        self.target = None

    def upgrade(self): pass


class PulseTower(UpgradableMixin):
    def __init__(self, canvas, x, y):
        self.canvas       = canvas
        self.x, self.y   = x, y
        self.sleeping     = False
        self.sleep_overlay = None
        self.range        = 80
        self.damage       = 1
        self.pulse_rate   = 1800
        self.double_pulse = False
        self.triple_pulse = False
        self.placement_radius = 5
        self.invested     = 800
        self._init_upgrades()
        self.range_circle = canvas.create_oval(
            x-self.range, y-self.range, x+self.range, y+self.range,
            outline="#70a1ff", width=2, stipple="gray50")
        self.canvas.itemconfig(self.range_circle, state="hidden")
        r = 18
        self.sprite    = canvas.create_oval(x-r, y-r, x+r, y+r,
                                             fill="#70a1ff", outline="#1e90ff", width=3)
        self.canvas_id = self.sprite
        self.canvas.tag_bind(self.sprite, "<Button-3>", self.select)
        self._animate_range_opacity()
        self._pulse()

    def put_to_sleep(self, duration=2000):
        if self.sleeping: return
        self.canvas.itemconfig(self.canvas_id, state="disabled")
        self.sleeping = True
        x, y = self.get_center()
        self.sleep_overlay = self.canvas.create_text(x, y-25, text="💤", font=("Arial", 18))
        self.canvas.after(duration, self.wake_up)

    def wake_up(self):
        self.sleeping = False
        if self.sleep_overlay:
            self.canvas.delete(self.sleep_overlay)
            self.sleep_overlay = None
            self.canvas.itemconfig(self.canvas_id, state="normal")

    def select(self, e): game.select_building(self)
    def get_center(self): return self.x, self.y
    def get_range(self):  return self.range

    def _animate_range_opacity(self, toggle=True):
        if game.game_over or not self.alive: return
        self.canvas.itemconfig(self.range_circle, stipple="gray50" if toggle else "gray75")
        self.canvas.after(600, lambda: self._animate_range_opacity(not toggle))

    def _pulse(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if game.game_over or not self.alive: return
        if not self.sleeping:
            self._emit_pulse()
            if self.double_pulse:
                self.canvas.after(250, self._emit_pulse)
            if self.triple_pulse:
                self.canvas.after(500, self._emit_pulse)
        self.canvas.after(self.pulse_rate, self._pulse)

    def _emit_pulse(self):
        # ── FIX: guard if tower was sold between scheduling and firing ────
        if not self.alive: return
        ring  = self.canvas.create_oval(self.x, self.y, self.x, self.y,
                                         outline="#70a1ff", width=3)
        steps = 8
        step_size = self.range / steps
        def animate(step=0):
            if step > steps:
                self.canvas.delete(ring)
                return
            r = step * step_size
            self.canvas.coords(ring, self.x-r, self.y-r, self.x+r, self.y+r)
            self.canvas.after(25, lambda: animate(step+1))
        animate()
        for e in list(Enemy.enemies):
            pos = e.get_position()
            if not pos: continue
            ex, ey = pos
            if math.hypot(ex-self.x, ey-self.y) <= self.range:
                e.apply_damage(self.damage)
                if self.pulse_slow:
                    e.slow_effects["pulse"] = (self.pulse_slow, time.time() + 1.5)
                if self.stun_chance and random.random() < self.stun_chance:
                    e.slow_effects["stun"] = (0.01, time.time() + self.stun_duration/1000)

    def upgrade(self): pass


class Bank(UpgradableMixin):
    def __init__(self, canvas, x, y):
        self.canvas      = canvas
        self.base_income = 60
        self.interest    = 0.10
        self.cap         = 300
        self.invested    = 250
        self.sleeping    = False
        self.sleep_overlay = None
        self.stored_money = 0
        self._init_upgrades()
        self.sprite    = canvas.create_image(x, y, image=game.bank_img)
        self.canvas_id = self.sprite
        self.canvas.tag_bind(self.sprite, "<Button-3>", self.select)
        self.canvas.tag_bind(self.sprite, "<Button-1>", lambda e: self.collect())
        x0, y0 = self.canvas.coords(self.sprite)
        self.text = self.canvas.create_text(x0, y0-28, text="0c",
                                             fill="#2ed573", font=("Arial", 10, "bold"))

    def put_to_sleep(self, duration=2000):
        if self.sleeping: return
        self.sleeping = True
        x, y = self.get_center()
        self.sleep_overlay = self.canvas.create_text(x, y-25, text="💤", font=("Arial", 18))
        self.canvas.after(duration, self.wake_up)

    def wake_up(self):
        self.sleeping = False
        if self.sleep_overlay:
            self.canvas.delete(self.sleep_overlay)
            self.sleep_overlay = None

    def select(self, e): game.select_building(self)

    def get_center(self):
        coords = self.canvas.coords(self.sprite)
        if coords and len(coords) >= 2: return coords[0], coords[1]
        return (0, 0)

    def get_range(self): return 0

    def update_label(self):
        self.canvas.itemconfig(self.text, text=f"{self.stored_money}c")
        pos = self.canvas.coords(self.sprite)
        if pos and len(pos) >= 2:
            self.canvas.coords(self.text, pos[0], pos[1]-28)

    def on_new_wave(self):
        if getattr(self, "auto_collect", False) and self.stored_money > 0:
            Game.money += self.stored_money
            self.stored_money = 0
            game.update_money_label()
        profit = self.base_income + int(self.stored_money * self.interest)
        self.stored_money = min(self.cap, self.stored_money + profit)
        self.update_label()

    def collect(self):
        if self.stored_money > 0:
            Game.money += self.stored_money
            self.stored_money = 0
            self.update_label()
            game.update_money_label()

    def upgrade(self): pass


class Barricade(UpgradableMixin):
    barricades = []

    def __init__(self, canvas, x, y, img):
        self.canvas    = canvas
        self.sprite    = canvas.create_image(x, y, image=img)
        self.radius    = 60
        self.slow      = 0.7
        self.linger_time = 1.5
        self.invested  = 210
        self._init_upgrades()
        Barricade.barricades.append(self)
        self.canvas.tag_bind(self.sprite, "<Button-3>", self.select)
        self.canvas_id = self.sprite

    def select(self, e): game.select_building(self)
    def get_radius(self):  return self.radius
    def get_position(self): return self.canvas.coords(self.sprite)
    def get_center(self):   return self.canvas.coords(self.sprite)
    def get_range(self):    return self.radius

    def apply_slow(self, enemy):
        expire_at = time.time() + self.linger_time
        enemy.slow_effects[id(self)] = (self.slow, expire_at)
        if getattr(self, "spike_damage", 0) > 0:
            if not enemy.slow_effects.get(f"spike_{id(self)}_done"):
                enemy.apply_damage(self.spike_damage)
                enemy.slow_effects[f"spike_{id(self)}_done"] = (1.0, time.time() + 0.5)

    def upgrade(self): pass


# ─── MINE & MINE TOWER ───────────────────────────────────────────────────────

class Mine:
    DETECT_R = 18

    def __init__(self, canvas, x, y, damage, blast_r,
                 slow=None, burn=False, cluster=False, shield_pierce=False):
        self.canvas  = canvas
        self.x, self.y = x, y
        self.damage  = damage
        self.blast_r = blast_r
        self.slow    = slow
        self.burn    = burn
        self.cluster = cluster
        self.shield_pierce = shield_pierce
        self.alive   = True
        self._sprites = []
        self._draw()
        self._poll()

    def _draw(self):
        r = 7
        x, y = self.x, self.y
        body    = self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                          fill="#c0392b", outline="#e84393", width=2)
        cross_h = self.canvas.create_line(x-4, y, x+4, y, fill="#ff4757", width=2)
        cross_v = self.canvas.create_line(x, y-4, x, y+4, fill="#ff4757", width=2)
        self._sprites = [body, cross_h, cross_v]

    def delete_sprites(self):
        for s in self._sprites:
            self.canvas.delete(s)
        self._sprites.clear()

    def _poll(self):
        if not self.alive or game.game_over:
            return
        for e in list(Enemy.enemies):
            pos = e.get_position()
            if not pos:
                continue
            if math.hypot(pos[0]-self.x, pos[1]-self.y) < self.DETECT_R:
                self.explode()
                return
        self.canvas.after(40, self._poll)

    def explode(self):
        if not self.alive:
            return
        self.alive = False
        self.delete_sprites()
        x, y = self.x, self.y

        ring = self.canvas.create_oval(x-self.blast_r, y-self.blast_r,
                                        x+self.blast_r, y+self.blast_r,
                                        outline="#e84393", width=3)
        self.canvas.after(250, lambda r=ring: self.canvas.delete(r))

        for e in list(Enemy.enemies):
            pos = e.get_position()
            if not pos:
                continue
            if math.hypot(pos[0]-x, pos[1]-y) <= self.blast_r:
                if self.shield_pierce and hasattr(e, "shield_hp"):
                    e.shield_hp = 0
                    e.break_shield()
                e.apply_damage(self.damage)
                if self.slow:
                    e.slow_effects["mine_slow"] = (self.slow, time.time() + 2.5)
                if self.burn:
                    self.canvas.after(500,  lambda en=e: en.apply_damage(1) if en.sprite else None)
                    self.canvas.after(1000, lambda en=e: en.apply_damage(1) if en.sprite else None)
                    self.canvas.after(1500, lambda en=e: en.apply_damage(1) if en.sprite else None)

        if self.cluster:
            nearby = []
            for i in range(len(game.path) - 1):
                x1, y1 = game.path[i]
                x2, y2 = game.path[i + 1]
                seg_len = math.hypot(x2-x1, y2-y1)
                steps   = max(2, int(seg_len / 12))
                for s in range(steps + 1):
                    t  = s / steps
                    px = x1 + t*(x2-x1)
                    py = y1 + t*(y2-y1)
                    if math.hypot(px-x, py-y) < 70:
                        nearby.append((px, py))
            random.shuffle(nearby)
            placed = []
            for pt in nearby:
                if all(math.hypot(pt[0]-p[0], pt[1]-p[1]) > 20 for p in placed):
                    placed.append(pt)
                    if len(placed) >= 3:
                        break
            for pt in placed:
                Mine(self.canvas, pt[0], pt[1],
                     damage=max(1, self.damage // 2),
                     blast_r=max(18, self.blast_r // 2),
                     slow=self.slow, burn=False, cluster=False,
                     shield_pierce=self.shield_pierce)


class MineTower(UpgradableMixin):
    all_mine_towers = []

    def __init__(self, canvas, x, y):
        self.canvas  = canvas
        self.x, self.y = x, y
        self.range   = 90
        self.placement_radius = 5
        self.sleeping = False
        self.sleep_overlay = None
        self.invested = 300
        self._init_upgrades()

        self.mine_count   = 6
        self.mine_spacing = 35
        self.mine_damage  = 2
        self.mine_radius  = 40

        self._active_mines = []
        self._loop_active  = True

        r = 18
        self.range_oval = canvas.create_oval(x-self.range, y-self.range,
                                              x+self.range, y+self.range,
                                              outline="#e84393", width=1,
                                              dash=(3, 4), state="hidden")
        self.sprite = canvas.create_polygon(
            self._hex_pts(x, y, r),
            fill="#2d0a1e", outline="#e84393", width=3)
        self.canvas_id = self.sprite

        self.canvas.tag_bind(self.sprite, "<Button-3>", self.select)
        self.canvas.tag_bind(self.sprite, "<Enter>",    self.on_hover)
        self.canvas.tag_bind(self.sprite, "<Leave>",    self.on_leave)

        MineTower.all_mine_towers.append(self)
        self._schedule_throw()

    @staticmethod
    def _hex_pts(cx, cy, r):
        pts = []
        for i in range(6):
            a = math.radians(60 * i - 30)
            pts.extend([cx + r * math.cos(a), cy + r * math.sin(a)])
        return pts

    def put_to_sleep(self, duration=2000):
        if self.sleeping: return
        self.sleeping = True
        self.sleep_overlay = self.canvas.create_text(
            self.x, self.y - 25, text="💤", font=("Arial", 18))
        self.canvas.after(duration, self.wake_up)

    def wake_up(self):
        self.sleeping = False
        if self.sleep_overlay:
            self.canvas.delete(self.sleep_overlay)
            self.sleep_overlay = None

    def select(self, e): game.select_building(self)
    def get_center(self): return self.x, self.y
    def get_range(self):  return self.range

    def on_hover(self, e):
        game.show_range(self.x, self.y, self.range, "#e84393")

    def on_leave(self, e):
        if game.selected_building != self:
            game.hide_range()

    def clear_mines(self):
        for m in self._active_mines:
            if m.alive:
                m.alive = False
                m.delete_sprites()
        self._active_mines.clear()

    def _schedule_throw(self, delay=400):
        if self._loop_active:
            self.canvas.after(delay, self._throw_tick)

    def _throw_tick(self):
        # ── FIX: stop loop when tower has been sold ──────────────────────
        if not self._loop_active or game.game_over or not self.alive:
            return
        self._active_mines = [m for m in self._active_mines if m.alive]

        if len(self._active_mines) < self.mine_count:
            pt = self._pick_target_point()
            if pt:
                self._animate_throw(pt[0], pt[1])
                self._schedule_throw(delay=1300)
                return

        self._schedule_throw(delay=1200)

    def _pick_target_point(self):
        cx, cy = self.x, self.y
        candidates = []
        path = game.path
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            seg_len = math.hypot(x2 - x1, y2 - y1)
            steps   = max(2, int(seg_len / 12))
            for s in range(steps + 1):
                t  = s / steps
                px = x1 + t * (x2 - x1)
                py = y1 + t * (y2 - y1)
                if math.hypot(px - cx, py - cy) <= self.range:
                    candidates.append((px, py))

        random.shuffle(candidates)
        occupied = [(m.x, m.y) for m in self._active_mines if m.alive]
        min_d = self.mine_spacing
        for pt in candidates:
            if all(math.hypot(pt[0]-ox, pt[1]-oy) > min_d for ox, oy in occupied):
                return pt
        return None

    def _animate_throw(self, tx, ty):
        cx, cy = self.x, self.y
        dot = self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5,
                                       fill="#e84393", outline="#ff4757", width=1)
        steps = 14
        ddx = (tx - cx) / steps
        ddy = (ty - cy) / steps

        def fly(step=0):
            if step >= steps:
                self.canvas.delete(dot)
                if self._loop_active and self.alive and not game.game_over:
                    m = Mine(self.canvas, tx, ty,
                             damage=self.mine_damage,
                             blast_r=self.mine_radius,
                             slow=self.mine_slow,
                             burn=self.mine_burn,
                             cluster=self.mine_cluster,
                             shield_pierce=self.mine_shield_pierce)
                    self._active_mines.append(m)
                return
            self.canvas.move(dot, ddx, ddy)
            self.canvas.after(22, lambda: fly(step + 1))

        fly()

    def on_new_wave(self):
        self.clear_mines()

    def upgrade(self): pass

    def apply_path_upgrade(self, path):
        return super().apply_path_upgrade(path)


# ─── GAME ────────────────────────────────────────────────────────────────────

class Game:
    money     = 0
    game_over = False
    pygame.mixer.init()
    volume = 0.6
    paused = False

    def __init__(self):
        global game
        game = self
        self.towers   = []
        self.banks    = []
        self.root     = Tk()
        self.root.title("Bombastic Defense")
        self.root.configure(bg="#0f0f1a")
        self.root.geometry("1520x820")
        self.root.resizable(False, False)
        self.total_kills = 0
        self.selected_building    = None
        self._angry_target_mode   = False
        self._angry_target_tower  = None
        self._target_range_preview = None
        self._wave_label_id       = None
        self.blind_zones          = []   # populated per map
        self.all_paths            = []   # populated per map (multi-path support)
        self.show_main_menu()
        self.root.mainloop()

    # ── MENUS ───────────────────────────────────────────────────────────────

    def show_main_menu(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.menu = Frame(self.root, bg="#0f0f1a")
        self.menu.pack(fill="both", expand=True)

        # ── Scrollable container ─────────────────────────────────────────
        outer = Frame(self.menu, bg="#0f0f1a")
        outer.pack(fill="both", expand=True)

        scrollbar = Scrollbar(outer, orient="vertical", bg="#1a1a3a",
                              troughcolor="#0a0a1a", activebackground="#a29bfe",
                              highlightthickness=0, bd=0, width=12)
        scrollbar.pack(side=RIGHT, fill=Y)

        c = Canvas(outer, bg="#0f0f1a", highlightthickness=0,
                   yscrollcommand=scrollbar.set)
        c.pack(side=LEFT, fill="both", expand=True)
        scrollbar.config(command=c.yview)

        # Mouse-wheel scrolling (Windows / Linux / macOS)
        def _on_mousewheel(event):
            if event.delta:
                c.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif event.num == 4:
                c.yview_scroll(-1, "units")
            elif event.num == 5:
                c.yview_scroll(1, "units")

        c.bind("<MouseWheel>", _on_mousewheel)   # Windows / macOS
        c.bind("<Button-4>",   _on_mousewheel)   # Linux scroll up
        c.bind("<Button-5>",   _on_mousewheel)   # Linux scroll down
        self.menu.bind_all("<MouseWheel>", _on_mousewheel)

        # ── Content ──────────────────────────────────────────────────────
        CANVAS_W = 1188   # slightly narrower to account for scrollbar

        c.create_text(CANVAS_W // 2, 60, text="💣 BOMBASTIC DEFENSE",
                      fill="#a29bfe", font=("Courier", 30, "bold"))
        c.create_text(CANVAS_W // 2, 100, text="SELECT A MAP   ↕ scroll to see all",
                      fill="#6666aa", font=("Courier", 14))

        # Subtle scroll-hint arrow at bottom of header
        c.create_text(CANVAS_W // 2, 115, text="▼",
                      fill="#4444aa", font=("Courier", 9))

        map_keys = list(MAPS.keys())
        per_row  = 3
        card_w, card_h = 320, 520
        gap      = 24
        rows     = [map_keys[i:i+per_row] for i in range(0, len(map_keys), per_row)]
        start_y  = 130

        for row_idx, row_keys in enumerate(rows):
            total_w  = len(row_keys) * card_w + (len(row_keys) - 1) * gap
            start_x  = (CANVAS_W - total_w) // 2
            row_y    = start_y + row_idx * (card_h + 30)
            for col_idx, mk in enumerate(row_keys):
                cx = start_x + col_idx * (card_w + gap)
                self._draw_map_card(c, cx, row_y, card_w, card_h, mk)

        # Set scroll region to fit all content
        total_content_h = start_y + len(rows) * (card_h + 30) + 40
        c.config(scrollregion=(0, 0, CANVAS_W, total_content_h))

        c.bind("<Button-1>", lambda e: self._map_card_click(e.x, e.y + c.yview()[0] * total_content_h))

    def _draw_map_card(self, c, cx, cy, w, h, map_key):
        cfg = MAPS[map_key]
        x1, y1, x2, y2 = cx, cy, cx + w, cy + h
        border = cfg["color"]

        c.create_rectangle(x1, y1, x2, y2, fill="#1a1a2e", outline=border, width=3,
                           tags=f"mapcard_{map_key}")

        pw, ph = w - 20, 260
        px1, py1 = x1 + 10, y1 + 10
        px2, py2 = px1 + pw, py1 + ph
        c.create_rectangle(px1, py1, px2, py2,
                           fill=cfg["grass_color"], outline=border, width=1,
                           tags=f"mapcard_{map_key}")

        # Draw all paths for this map in the preview
        all_preview_paths = cfg.get("paths", [cfg["path"]])

        # ── Unified coordinate space across ALL paths so they align ──────
        all_pts = [p for path in all_preview_paths for p in path]
        min_x  = min(p[0] for p in all_pts)
        max_x  = max(p[0] for p in all_pts)
        min_y  = min(p[1] for p in all_pts)
        max_y  = max(p[1] for p in all_pts)
        span_x = max(max_x - min_x, 1)
        span_y = max(max_y - min_y, 1)
        pad    = 18

        def scale(px_, py_):
            sx = px1 + pad + (px_ - min_x) / span_x * (pw - 2 * pad)
            sy = py1 + pad + (py_ - min_y) / span_y * (ph - 2 * pad)
            return sx, sy

        drawn_start_pts = set()
        drawn_end_pts   = set()
        for path in all_preview_paths:
            road_pts = [scale(p[0], p[1]) for p in path]
            for i in range(len(road_pts) - 1):
                ax, ay = road_pts[i]
                bx, by = road_pts[i + 1]
                c.create_line(ax, ay, bx, by, fill=cfg["road_color"],
                              width=8, capstyle="round", joinstyle="round",
                              tags=f"mapcard_{map_key}")
            sx2, sy2 = road_pts[0]
            ex2, ey2 = road_pts[-1]
            sk = (round(sx2), round(sy2))
            ek = (round(ex2), round(ey2))
            if sk not in drawn_start_pts:
                c.create_oval(sx2-6, sy2-6, sx2+6, sy2+6, fill="#2ed573", outline="white", width=2,
                              tags=f"mapcard_{map_key}")
                drawn_start_pts.add(sk)
            if ek not in drawn_end_pts:
                c.create_oval(ex2-6, ey2-6, ex2+6, ey2+6, fill="#ff4757", outline="white", width=2,
                              tags=f"mapcard_{map_key}")
                drawn_end_pts.add(ek)

        # Draw blind zones in preview using the same unified scale
        for (bx1, by1, bx2, by2) in cfg.get("blind_zones", []):
            sxmin, symin = scale(bx1, by1)
            sxmax, symax = scale(bx2, by2)
            c.create_rectangle(max(px1, sxmin), max(py1, symin),
                               min(px2, sxmax), min(py2, symax),
                               fill="#2a1a0a", outline="#6b4e2a", width=1,
                               stipple="gray50", tags=f"mapcard_{map_key}")

        ty = py2 + 14
        c.create_text(cx + w // 2, ty, text=cfg["name"],
                      fill="white", font=("Courier", 13, "bold"),
                      tags=f"mapcard_{map_key}")
        c.create_text(cx + w // 2, ty + 24, text=cfg["desc"],
                      fill="#aaaacc", font=("Courier", 8), justify="center",
                      tags=f"mapcard_{map_key}")

        # Special badges
        badges = []
        if cfg.get("paths") and len(cfg["paths"]) > 1:
            badges.append(("⚠ DUAL SPAWN", "#00cec9"))
        if cfg.get("blind_zones"):
            badges.append(("🚧 BLIND ZONES", "#636e72"))
        badge_y = ty + 48
        for badge_txt, badge_col in badges:
            c.create_text(cx + w // 2, badge_y, text=badge_txt,
                          fill=badge_col, font=("Courier", 8, "bold"),
                          tags=f"mapcard_{map_key}")
            badge_y += 14

        by1_btn = ty + 72
        by2_btn = by1_btn + 36
        c.create_rectangle(cx + 24, by1_btn, cx + w - 24, by2_btn,
                           fill="#1e1e3a", outline=border, width=2,
                           tags=f"mapcard_{map_key}")
        c.create_text(cx + w // 2, (by1_btn + by2_btn) // 2, text="▶  PLAY THIS MAP",
                      fill=border, font=("Courier", 10, "bold"),
                      tags=f"mapcard_{map_key}")

        self._map_cards = getattr(self, "_map_cards", {})
        self._map_cards[map_key] = (x1, y1, x2, y2)

    def _map_card_click(self, mx, my):
        for map_key, (x1, y1, x2, y2) in getattr(self, "_map_cards", {}).items():
            if x1 <= mx <= x2 and y1 <= my <= y2:
                self.show_difficulty_menu(map_key)
                return

    def show_difficulty_menu(self, map_key):
        for w in self.root.winfo_children():
            w.destroy()
        self.menu = Frame(self.root, bg="#0f0f1a")
        self.menu.pack(fill="both", expand=True)
        c = Canvas(self.menu, width=1200, height=820, bg="#0f0f1a", highlightthickness=0)
        c.pack()

        map_cfg = MAPS[map_key]
        c.create_text(600, 80, text="💣 BOMBASTIC DEFENSE",
                      fill="#a29bfe", font=("Courier", 28, "bold"))
        c.create_text(600, 120, text=f"Map: {map_cfg['name']}  —  Choose Difficulty",
                      fill="#6666aa", font=("Courier", 13))

        c.create_rectangle(30, 30, 130, 60, fill="#1e1e2e", outline="#555577", width=1)
        c.create_text(80, 45, text="◀ BACK", fill="#aaaacc", font=("Courier", 10, "bold"))
        c.bind("<Button-1>", lambda e: self.show_main_menu()
               if 30 <= e.x <= 130 and 30 <= e.y <= 60 else
               self._diff_click(e.x, e.y, map_key))

        self._diff_cards = {}
        total  = len(DIFFICULTIES)
        card_w = 250
        gap    = 24
        total_w = total * card_w + (total - 1) * gap
        start_x = (1200 - total_w) // 2

        for col, (key, cfg) in enumerate(DIFFICULTIES.items()):
            cx = start_x + col * (card_w + gap)
            cy = 160
            ch = 440
            is_nightmare = (key == "nightmare")

            bg_fill = "#0d001a" if is_nightmare else "#1e1e2e"
            border_w = 4 if is_nightmare else 3
            c.create_rectangle(cx, cy, cx + card_w, cy + ch,
                               fill=bg_fill, outline=cfg["color"], width=border_w)

            if is_nightmare:
                for gi in range(3):
                    goff = (gi + 1) * 2
                    c.create_rectangle(cx - goff, cy - goff, cx + card_w + goff, cy + ch + goff,
                                      outline=cfg["color"], width=1,
                                      dash=(4 + gi * 2, 4 + gi * 2))

            c.create_text(cx + card_w // 2, cy + 35,
                          text=cfg["label"], fill=cfg["color"],
                          font=("Courier", 16, "bold"))

            if is_nightmare:
                c.create_text(cx + card_w // 2, cy + 58,
                              text="☠ ARE YOU SURE? ☠",
                              fill="#660033", font=("Courier", 8, "bold"))

            c.create_text(cx + card_w // 2, cy + 105,
                          text=cfg["desc"], fill="#dfe6e9",
                          font=("Courier", 9), justify="center", width=210)

            bcy = cy + ch - 60
            btn_fill = cfg["color"] if not is_nightmare else "#220033"
            btn_out  = cfg["color"]
            c.create_rectangle(cx + 20, bcy, cx + card_w - 20, bcy + 40,
                               fill=btn_fill, outline=btn_out, width=2)
            c.create_text(cx + card_w // 2, bcy + 20,
                          text="☠ I DARE" if is_nightmare else "PLAY",
                          fill=cfg["color"] if is_nightmare else ("black" if key == "normal" else "white"),
                          font=("Courier", 13, "bold"))
            self._diff_cards[key] = (cx, cy, cx + card_w, cy + ch)

    def _diff_click(self, mx, my, map_key):
        for diff_key, (x1, y1, x2, y2) in getattr(self, "_diff_cards", {}).items():
            if x1 <= mx <= x2 and y1 <= my <= y2:
                self.start_game(map_key, diff_key)
                return

    def _build_sidebar(self, cfg):
        """Vertical tower shop on the left sidebar."""
        cm = cfg.get("tower_cost_mult", 1.0)

        def mc(base): return int(base * cm)

        sb = self.sidebar
        # Title
        title_cv = Canvas(sb, width=160, height=54, bg="#0d0d1a", highlightthickness=0)
        title_cv.pack(fill=X)
        title_cv.create_rectangle(0, 0, 160, 54, fill="#0a0a18", outline="")
        title_cv.create_text(80, 18, text="💣 TOWER", fill="#a29bfe",
                             font=("Courier", 11, "bold"))
        title_cv.create_text(80, 36, text="SHOP", fill="#6666aa",
                             font=("Courier", 9))
        title_cv.create_line(10, 50, 150, 50, fill="#1a1a3a", width=1)

        TOWERS = [
            ("🔵 Trooper", mc(100), "#3498db", self.buy_tower),
            ("🟠 All-Round", mc(150), "#e67e22", self.buy_ball),
            ("💣 Bomber", mc(350), "#c0392b", self.buy_bombtower),
            ("🔴 Gunner", mc(670), "#ff4757", self.buy_angry),
            ("🎯 Sniper", mc(850), "#27ae60", self.buy_sniper),
            ("📡 Pulse", mc(800), "#70a1ff", self.buy_pulse),
            ("🛡 Slow", mc(210), "#95a5a6", self.buy_barricade),
            ("🏦 Bank", mc(250), "#feca57", self.buy_bank),
            ("🪤 Mine", mc(300), "#e84393", self.buy_minetower),
            ("⚗ Elemental", mc(180), "#9b59b6", self.buy_elemental),
        ]

        for name, cost, color, cmd in TOWERS:
            btn_frame = Frame(sb, bg="#0d0d1a", height=58)
            btn_frame.pack(fill=X, padx=6, pady=2)
            btn_frame.pack_propagate(False)

            cv = Canvas(btn_frame, width=148, height=54,
                        bg="#0f0f1e", highlightthickness=0)
            cv.pack(fill=BOTH, expand=True)

            cv.create_rectangle(0, 0, 148, 54,
                                fill="#0f0f1e", outline=color, width=1)
            cv.create_text(74, 18, text=name, fill="white",
                           font=("Courier", 9, "bold"))
            cv.create_rectangle(4, 32, 144, 50,
                                fill="#080810", outline=color, width=1)
            cv.create_text(74, 41, text=f"{cost}c",
                           fill=color, font=("Courier", 9, "bold"))

            def _enter(e, c=cv, col=color):
                c.configure(bg="#1a1a2e")
                c.create_rectangle(0, 0, 148, 54, fill="#1a1a2e",
                                   outline=col, width=2, tags="hover")
                c.tag_lower("hover")   # push the highlight behind the text

            def _leave(e, c=cv, col=color):
                c.delete("hover")
                c.configure(bg="#0f0f1e")

            cv.bind("<Enter>", _enter)
            cv.bind("<Leave>", _leave)
            cv.bind("<Button-1>", lambda e, fn=cmd: fn())

        # Separator + pause/auto at bottom
        sep = Frame(sb, bg="#1a1a3a", height=1)
        sep.pack(fill=X, padx=8, pady=4)

        ctrl_cv = Canvas(sb, width=160, height=80, bg="#0d0d1a", highlightthickness=0)
        ctrl_cv.pack(fill=X, pady=2)

        self.pause_btn = Button(sb, text="⏸ PAUSE", bg="#2f3542", fg="#a4b0be",
                                font=("Courier", 8, "bold"), relief="flat",
                                activebackground="#3d4452",
                                command=self.toggle_pause)
        self.pause_btn.pack(fill=X, padx=8, pady=2)

        self.auto_wave_btn = Button(sb, text="⏸ Auto Wave", bg="#57606f", fg="white",
                                    font=("Courier", 8, "bold"), relief="flat",
                                    command=self.toggle_auto_wave)
        self.auto_wave_btn.pack(fill=X, padx=8, pady=2)

        btn_wave = Button(sb, text="▶ Send Wave", bg="#6c3483", fg="white",
                          font=("Courier", 8, "bold"), relief="flat",
                          activebackground="#7d3c98",
                          command=self.spawn_wave)
        btn_wave.pack(fill=X, padx=8, pady=2)

    def _build_hud(self):
        """Bottom HUD bar with live stats."""
        hf = self.hud_frame
        cfg = self.difficulty

        diff_color = cfg.get("color", "#ffffff")
        diff_label = cfg.get("label", "")

        # Canvas-based HUD for full control
        self._hud_cv = Canvas(hf, width=1100, height=100,
                              bg="#080812", highlightthickness=0)
        self._hud_cv.pack(fill=BOTH, expand=True)

        # Divider line at top
        self._hud_cv.create_line(0, 0, 1100, 0, fill="#1a1a3a", width=2)

        # Difficulty badge
        self._hud_cv.create_rectangle(10, 12, 130, 38,
                                      fill="#0d0d1a", outline=diff_color, width=1)
        self._hud_cv.create_text(70, 25, text=diff_label,
                                 fill=diff_color, font=("Courier", 9, "bold"))

        # Stat labels — stored as canvas text ids for update_hud()
        stats = [
            ("❤️  HP", f"{Enemy.health}/{self._player_max_hp}", "#ff6b6b", 200),
            ("💰 Money", f"{Game.money}c", "#00ffcc", 370),
            ("🌊 Wave", f"{self.wave}/{FINAL_WAVE}", "#6bc5ff", 540),
            ("💀 Kills", "0", "#ff4757", 700),
        ]

        self._hud_ids = {}
        for label, value, color, x in stats:
            self._hud_cv.create_text(x, 22, text=label,
                                     fill="#444466", font=("Courier", 8))
            vid = self._hud_cv.create_text(x, 50, text=value,
                                           fill=color, font=("Courier", 16, "bold"))
            self._hud_ids[label] = vid

        # Wave progress bar
        self._hud_cv.create_rectangle(150, 68, 950, 82,
                                      fill="#0a0a18", outline="#1a1a3a", width=1)
        self._hud_bar = self._hud_cv.create_rectangle(150, 68, 150, 82,
                                                      fill="#6bc5ff", outline="")
        self._hud_cv.create_text(550, 92, text="WAVE PROGRESS",
                                 fill="#1a1a3a", font=("Courier", 7))

        # Real tkinter labels (hidden, kept for compatibility with existing code)
        self.label_money = Label(hf, text="", bg="#080812", fg="#00ffcc")
        self.label_hp = Label(hf, text="", bg="#080812", fg="#ff6b6b")
        self.label_wave = Label(hf, text="", bg="#080812", fg="#6bc5ff")

        self.update_hud()

    def update_hud(self):
        """Refresh all HUD stat values."""
        if not hasattr(self, "_hud_ids") or not self._hud_cv:
            return
        hp_text = f"{max(0, Enemy.health)}/{self._player_max_hp}"
        self._hud_cv.itemconfig(self._hud_ids["❤️  HP"], text=hp_text)
        self._hud_cv.itemconfig(self._hud_ids["💰 Money"], text=f"{Game.money}c")
        self._hud_cv.itemconfig(self._hud_ids["🌊 Wave"], text=f"{self.wave}/{FINAL_WAVE}")
        self._hud_cv.itemconfig(self._hud_ids["💀 Kills"], text=str(self.total_kills))

        # Update wave progress bar
        pct = min(1.0, (self.wave - 1) / FINAL_WAVE)
        barw = int(800 * pct)
        self._hud_cv.coords(self._hud_bar, 150, 68, 150 + barw, 82)

        # Also keep label refs up to date (used by enemy HP-damage code)
        self.label_money.config(text=f"💰 {Game.money}c")
        self.label_hp.config(text=f"❤️ {max(0, Enemy.health)} / {self._player_max_hp}")
        self.label_wave.config(text=f"🌊 Wave {self.wave}")

    def start_game(self, map_key, difficulty_key):
        map_cfg      = MAPS[map_key]
        self.map_key = map_key
        cfg          = DIFFICULTIES[difficulty_key]
        self.difficulty = cfg
        Enemy.base_hp   = cfg["enemy_hp"]
        Enemy.health    = cfg.get("player_hp", 50)
        Game.money      = cfg["start_money"]
        self.towers.clear()
        self.banks = []
        Enemy.enemies.clear()
        Barricade.barricades.clear()
        MineTower.all_mine_towers.clear()
        self.wave         = 1
        self.boss_spawned = False
        self.current_wave_type = "normal"
        self.menu.destroy()

        # ── Map-specific mechanics ────────────────────────────────────────
        self.blind_zones = map_cfg.get("blind_zones", [])
        self.all_paths   = map_cfg.get("paths", [map_cfg["path"]])

        # ── LEFT SIDEBAR (tower shop) ─────────────────────────────────────
        self.sidebar = Frame(self.root, bg="#0d0d1a", width=160)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)

        # ── RIGHT PANEL (upgrade panel — always visible) ──────────────────
        self.right_panel = Frame(self.root, bg="#0d0d1a", width=260)
        self.right_panel.pack(side=RIGHT, fill=Y)
        self.right_panel.pack_propagate(False)

        # ── CENTER: canvas + HUD ──────────────────────────────────────────
        self.game_frame = Frame(self.root, bg="#0f0f1a")
        self.game_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.canvas = Canvas(self.game_frame, width=1100, height=700,
                             bg="#1a1a2e", highlightthickness=0)
        self.canvas.pack(side=TOP)

        self.hud_frame = Frame(self.game_frame, bg="#080812", height=100)
        self.hud_frame.pack(side=TOP, fill=X)
        self.hud_frame.pack_propagate(False)

        self.map_img = PhotoImage(file="map.png")
        if map_cfg["use_png"]:
            self.canvas.create_image(500, 300, image=self.map_img)
        else:
            self._draw_procedural_map(map_cfg)

        self.path = map_cfg["path"]  # primary path (used for Mine targeting, boss, etc.)

        self.enemy_img        = PhotoImage(file="Baloon.png")
        self.tower_img        = PhotoImage(file="tower.png")
        self.bullet_img       = PhotoImage(file="Bullet.png")
        self.barricade_img    = PhotoImage(file="barrikade.png")
        self.star_img         = PhotoImage(file="stern.png")
        self.nuke_img         = PhotoImage(file="nuclear_baloon.png")
        self.blue_img         = PhotoImage(file="BlueBaloon.png")
        self.yellow_img       = PhotoImage(file="YellowBaloon.png")
        self.bombtower_img    = PhotoImage(file="bomber.png")
        self.bomb_img         = PhotoImage(file="bomb.png")
        self.angry_imgs       = {
            "left":  PhotoImage(file="angry1.png"),
            "right": PhotoImage(file="angry2.png"),
            "down":  PhotoImage(file="angry3.png"),
            "up":    PhotoImage(file="angry4.png"),
        }
        self.bank_img         = PhotoImage(file="money.png")
        self.armored_img      = PhotoImage(file="armored_baloon.png")
        self.shield_img       = PhotoImage(file="Shield.png")
        self.shield_break_img = PhotoImage(file="shield_breaks.png")
        self.boss_stage1      = PhotoImage(file="Boss1_stage1.png")
        self.boss_stage2      = PhotoImage(file="Boss1_stage2.png")
        self.boss_stage3      = PhotoImage(file="Boss1_stage3.png")
        self.sniper_img       = PhotoImage(file="sniper.png")
        self.sniper_bullet_img = PhotoImage(file="sniper_bullet.png")
        self.mark_img         = PhotoImage(file="mark.png")
        self.zeppelin_img     = {
            "L": PhotoImage(file="Zeppelin1_L.png"),
            "R": PhotoImage(file="Zeppelin1_R.png"),
            "U": PhotoImage(file="Zeppelin1_U.png"),
            "D": PhotoImage(file="Zeppelin1_D.png"),
        }
        self.juggernaut_img = PhotoImage(file="juggernaut.png")
        self.phase_runner_img = PhotoImage(file="phase_runner.png")
        self.regenerator_img = PhotoImage(file="regenerator.png")
        self.bomber_drone_img = PhotoImage(file="bomber_drone.png")
        self.shielded_brute_img = PhotoImage(file="shielded_brute.png")

        try:
            self.shadow_img = PhotoImage(file="Shadow.png")
        except Exception:
            self.shadow_img = self.blue_img

        self.balloon_pop_sounds   = [pygame.mixer.Sound(f"balloonPop{i}.mp3") for i in range(1,5)]
        for s in self.balloon_pop_sounds:
            s.set_volume(Game.volume)

        self.auto_wave     = False
        self.wave_running  = False
        self.placing_type  = None
        self.preview_sprite = None
        self.preview_range  = None

        self.upgrade_panel = UpgradePanel(
            self.right_panel,
            on_upgrade_cb=self._panel_upgrade,
            on_sell_cb=self._panel_sell,
            on_close_cb=self._panel_close,
            on_set_target_cb=self._panel_set_target,
        )

        # Temporary label refs — real ones built in _build_hud
        self.label_money = Label(self.hud_frame, text="", bg="#080812")
        self.label_hp = Label(self.hud_frame, text="", bg="#080812")
        self.label_wave = Label(self.hud_frame, text="", bg="#080812")
        self._player_max_hp = cfg.get("player_hp", 50)

        self._build_sidebar(cfg)
        self._build_hud()

        self.upgrade_panel.frame.pack(fill=BOTH, expand=True)
        self.upgrade_panel._draw_idle()

        self.pause_overlay = self.canvas.create_rectangle(0, 0, 1200, 820,
                                                          fill="black", stipple="gray50", state="hidden")
        self.pause_text = self.canvas.create_text(550, 350, text="⏸  PAUSED",
                                                  fill="white", font=("Courier", 32, "bold"),
                                                  state="hidden")

        # ── Path zones: computed from ALL paths (prevent tower placement on any road) ──
        self.path_width = 40
        self.path_zones = []
        for pth in self.all_paths:
            for i in range(len(pth) - 1):
                x1, y1 = pth[i]
                x2, y2 = pth[i+1]
                if x1 == x2:
                    self.path_zones.append((x1-self.path_width//2, min(y1,y2),
                                             x1+self.path_width//2, max(y1,y2)))
                else:
                    self.path_zones.append((min(x1,x2), y1-self.path_width//2,
                                             max(x1,x2), y1+self.path_width//2))

        self.canvas.bind("<Motion>",   self.move_preview)
        self.canvas.bind("<Button-1>", self.place_preview)
        self.canvas.bind("<Button-3>", self.cancel_preview)

    # ── PANEL CALLBACKS ──────────────────────────────────────────────────────

    def _panel_upgrade(self, building, path):
        ok = building.apply_path_upgrade(path)
        if ok:
            self.update_money_label()
            self.upgrade_panel.redraw()

    def _panel_sell(self):
        if not self.selected_building: return
        b = self.selected_building
        if isinstance(b, AngryTower):
            b.clear_target()
        # ── FIX: mark tower dead BEFORE removing from canvas so all
        # scheduled after() callbacks bail out immediately ─────────────────
        b.alive = False
        Game.money += b.get_refund_amount()
        self.update_money_label()
        if isinstance(b, ElementalTower):
            b.cleanup_sprites()
        else:
            self.canvas.delete(b.sprite)
        self.canvas.delete(UpgradeVisuals.tag(id(b)))
        if b in self.towers:
            self.towers.remove(b)
        if isinstance(b, Bank) and b in self.banks:
            self.banks.remove(b)
        if isinstance(b, Barricade) and b in Barricade.barricades:
            Barricade.barricades.remove(b)
        if isinstance(b, MineTower):
            b._loop_active = False
            b.clear_mines()
            self.canvas.delete(b.range_oval)
            if b in MineTower.all_mine_towers:
                MineTower.all_mine_towers.remove(b)
        self.selected_building = None
        self._panel_close()

    def _panel_close(self):
        self._cancel_angry_target_mode()
        if isinstance(self.selected_building, AngryTower):
            self.selected_building.hide_target_marker()
        self.selected_building = None
        self.upgrade_panel.hide()
        self.hide_range()

    # ── ANGRY TARGET MODE ────────────────────────────────────────────────────

    def _panel_set_target(self, tower):
        self._cancel_angry_target_mode()
        self._angry_target_mode  = True
        self._angry_target_tower = tower
        cx, cy = tower.get_center()
        r      = tower.range
        self._target_range_preview = self.canvas.create_oval(
            cx-r, cy-r, cx+r, cy+r,
            outline="#ff4757", width=2, dash=(5, 3))
        self._target_instruction = self.canvas.create_text(
            cx, cy - r - 18,
            text="Click to set target  |  Right-click to cancel",
            fill="#ff4757", font=("Courier", 9, "bold"))
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")
        self.canvas.bind("<Button-1>", self._angry_target_click)
        self.canvas.bind("<Button-3>", lambda e: self._cancel_angry_target_mode(restore=True))

    def _angry_target_click(self, event):
        if not self._angry_target_mode or not self._angry_target_tower:
            return
        tower  = self._angry_target_tower
        cx, cy = tower.get_center()
        ex, ey = event.x, event.y
        if math.hypot(ex - cx, ey - cy) <= tower.range:
            tower.set_target(ex, ey)
            self.upgrade_panel.redraw()
        self._cancel_angry_target_mode(restore=True)

    def _cancel_angry_target_mode(self, restore=False):
        if self._target_range_preview:
            self.canvas.delete(self._target_range_preview)
            self._target_range_preview = None
        if hasattr(self, "_target_instruction") and self._target_instruction:
            self.canvas.delete(self._target_instruction)
            self._target_instruction = None
        self._angry_target_mode  = False
        self._angry_target_tower = None
        if restore:
            self.canvas.bind("<Motion>",   self.move_preview)
            self.canvas.bind("<Button-1>", self.place_preview)
            self.canvas.bind("<Button-3>", self.cancel_preview)

    # ── BUILDING SELECTION ───────────────────────────────────────────────────

    def select_building(self, building):
        self._cancel_angry_target_mode()
        if isinstance(self.selected_building, AngryTower):
            self.selected_building.hide_target_marker()
        self.selected_building = building
        self.hide_range()
        if hasattr(building, "get_center") and hasattr(building, "get_range"):
            try:
                x, y = building.get_center()
                r    = building.get_range()
                if r > 0:
                    self.show_range(x, y, r)
            except Exception:
                pass
        if isinstance(building, AngryTower):
            building.show_target_marker()
        self.upgrade_panel.show(building)

    # ── SOUND ────────────────────────────────────────────────────────────────

    def play_balloon_pop(self):
        if self.balloon_pop_sounds:
            random.choice(self.balloon_pop_sounds).play()

    def toggle_pause(self):
        self.paused = not self.paused
        state = "normal" if self.paused else "hidden"
        self.canvas.itemconfig(self.pause_overlay, state=state)
        self.canvas.itemconfig(self.pause_text,    state=state)
        self.pause_btn.config(text="▶" if self.paused else "⏸")

    # ── AUTO WAVE ────────────────────────────────────────────────────────────

    def toggle_auto_wave(self):
        self.auto_wave = not self.auto_wave
        if self.auto_wave:
            self.auto_wave_btn.config(text="▶ Auto", bg="#2ed573")
            self._check_auto_wave()
        else:
            self.auto_wave_btn.config(text="⏸ Auto", bg="#57606f")

    def _check_auto_wave(self):
        if not self.auto_wave or self.game_over: return
        if not Enemy.enemies and not self.wave_running:
            self.spawn_wave()
        self.root.after(800, self._check_auto_wave)

    # ── PLACEMENT ────────────────────────────────────────────────────────────

    def can_place_tower(self, x, y, radius=30):
        for tower in self.towers:
            try:
                tx, ty = tower.get_center()
                if math.hypot(x-tx, y-ty) < radius + tower.placement_radius:
                    return False
            except Exception:
                pass
        return True

    def buy_tower(self):    self._buy(100,  "tower")
    def buy_ball(self):     self._buy(150,  "ball")
    def buy_barricade(self):self._buy(210,  "barricade")
    def buy_bombtower(self):self._buy(350,  "bomb")
    def buy_angry(self):    self._buy(670,  "angry")
    def buy_bank(self):     self._buy(250,  "bank")
    def buy_pulse(self):    self._buy(800,  "pulse")
    def buy_sniper(self):   self._buy(850,  "sniper")
    def buy_minetower(self):self._buy(300,  "mine")
    def buy_elemental(self):self._buy(180, "elemental")

    def _buy(self, cost, kind):
        cost = int(cost * getattr(self, "difficulty", {}).get("tower_cost_mult", 1.0))
        if Game.money >= cost and not self.placing_type:
            Game.money -= cost
            self.update_money_label()
            self.start_placement(kind)

    def start_placement(self, kind):
        self.placing_type = kind
        previews = {
            "tower":    (lambda: self.canvas.create_image(0, 0, image=self.tower_img), 150),
            "ball":     (lambda: self.canvas.create_oval(0,0,40,40,fill="#ff9f1c",outline="black",width=2), 100),
            "bomb":     (lambda: self.canvas.create_image(0, 0, image=self.bombtower_img), 130),
            "barricade":(lambda: self.canvas.create_image(0, 0, image=self.barricade_img), 0),
            "angry":    (lambda: self.canvas.create_image(0, 0, image=self.angry_imgs["right"]), 260),
            "bank":     (lambda: self.canvas.create_image(0, 0, image=self.bank_img), 0),
            "pulse":    (lambda: self.canvas.create_oval(0,0,36,36,fill="#70a1ff",outline="#1e90ff",width=3), 80),
            "sniper":   (lambda: self.canvas.create_image(0, 0, image=self.sniper_img), 300),
            "mine":     (lambda: self.canvas.create_polygon(0,0,0,0,0,0,0,0,0,0,0,0, fill="#2d0a1e", outline="#e84393", width=3), 90),
            "elemental": (lambda: self.canvas.create_oval(0, 0, 48, 48,fill="#1a1a3a", outline="#6666cc", width=3),170,),
        }
        fn, r = previews[kind]
        self.preview_sprite = fn()
        self.preview_radius = r
        self.preview_range  = self.canvas.create_oval(0, 0, 0, 0, dash=(4,2))

    def move_preview(self, event):
        if not self.placing_type: return
        x, y = event.x, event.y
        if self.placing_type in ("ball", "pulse", "elemental"):
            if self.placing_type == "ball":
                r = 20
            elif self.placing_type == "pulse":
                r = 18
            else:
                r = 24
            self.canvas.coords(self.preview_sprite, x - r, y - r, x + r, y + r)
        elif self.placing_type == "mine":
            pts = MineTower._hex_pts(x, y, 18)
            self.canvas.coords(self.preview_sprite, *pts)
        else:
            self.canvas.coords(self.preview_sprite, x, y)
        forbidden = (self.placing_type != "barricade" and
                     (self.is_on_path(x, y) or not self.can_place_tower(x, y)))
        color = "#ff4757" if forbidden else "#2ed573"
        if self.preview_radius > 0:
            self.canvas.coords(self.preview_range,
                               x-self.preview_radius, y-self.preview_radius,
                               x+self.preview_radius, y+self.preview_radius)
            self.canvas.itemconfig(self.preview_range, outline=color)

    def place_preview(self, event):
        if not self.placing_type: return
        x, y = event.x, event.y
        if self.placing_type != "barricade" and self.is_on_path(x, y): return
        if self.placing_type != "barricade" and not self.can_place_tower(x, y): return

        kind = self.placing_type
        cost_mult = getattr(self, "difficulty", {}).get("tower_cost_mult", 1.0)
        self.canvas.delete(self.preview_sprite)

        if kind == "tower":
            sprite = self.canvas.create_image(x, y, image=self.tower_img)
            t = Tower(self.canvas, sprite, self.bullet_img)
            t.invested = int(t.invested * cost_mult)
            self.towers.append(t)
        elif kind == "ball":
            t = BallTower(self.canvas, x, y, self.bullet_img)
            t.invested = int(t.invested * cost_mult)
            self.towers.append(t)
        elif kind == "bomb":
            t = BombTower(self.canvas, x, y, self.bombtower_img, self.bomb_img)
            t.invested = int(t.invested * cost_mult)
            self.towers.append(t)
        elif kind == "barricade":
            b2 = Barricade(self.canvas, x, y, self.barricade_img)
        elif kind == "angry":
            t = AngryTower(self.canvas, x, y, self.angry_imgs)
            t.invested = int(t.invested * cost_mult)
            self.towers.append(t)
        elif kind == "bank":
            b = Bank(self.canvas, x, y)
            b.invested = int(b.invested * cost_mult)
            self.banks.append(b)
        elif kind == "pulse":
            t = PulseTower(self.canvas, x, y)
            t.invested = int(t.invested * cost_mult)
            self.towers.append(t)
        elif kind == "sniper":
            t = SniperTower(self.canvas, x, y)
            t.invested = int(t.invested * cost_mult)
            self.towers.append(t)
        elif kind == "mine":
            t = MineTower(self.canvas, x, y)
            t.invested = int(t.invested * cost_mult)
            self.towers.append(t)
        elif kind == "elemental":
            t = ElementalTower(self.canvas, x, y)
            t.invested = int(t.invested * cost_mult)
            self.towers.append(t)

        self.cleanup_preview()

    def cancel_preview(self, event):
        if not self.placing_type: return
        base_costs = {
            "tower": 100, "ball": 150, "bomb": 350, "barricade": 210,
            "angry": 670, "bank": 250, "pulse": 800, "sniper": 850,
            "mine": 300,  "elemental": 180
        }
        cost_mult = getattr(self, "difficulty", {}).get("tower_cost_mult", 1.0)
        Game.money += int(base_costs.get(self.placing_type, 0) * cost_mult)
        self.update_money_label()
        self.cleanup_preview()

    def cleanup_preview(self):
        if self.preview_sprite:  self.canvas.delete(self.preview_sprite)
        if self.preview_range:   self.canvas.delete(self.preview_range)
        self.preview_sprite = None
        self.preview_range  = None
        self.placing_type   = None

    # ── WAVE SYSTEM ─────────────────────────────────────────────────────────

    def _determine_wave_type(self):
        w = self.wave

        Game.money += w*3 + 100

        if w < 8:
            if w % 5 == 0: return "swarm"
            return "normal"

        if 8 <= w < 20:
            if w % 6 == 0: return "armored"
            if w % 7 == 0: return "swarm"
            return "normal"

        if 20 <= w < 40:
            if w % 10 == 0: return "nuclear"
            if w % 8 == 0:  return "stealth"
            if w % 9 == 0:  return "air"
            return random.choice(["normal", "swarm", "armored"])

        if 40 <= w < BOSS_WAVE:
            if w % 5 == 0: return "chaos"
            if w % 7 == 0: return "tank"
            if w % 11 == 0: return "armored"
            return random.choice(["normal", "swarm", "armored", "stealth"])

        if w >= BOSS_WAVE:
            return "chaos"

    def _build_pool(self, wave_type_name):
        wt = WAVE_TYPES[wave_type_name]
        overrides = wt[2]

        base = {
            "normal": 60,
            "blue": 0 if self.wave < 4 else 25,
            "yellow": 0 if self.wave < 8 else 18,
            "armored": 0 if self.wave < 14 else 20,
            "star": 0 if self.wave < 21 else 12,
            "nuclear": 0 if self.wave < 28 else 5,
            "zeppelin1": 0 if self.wave < 34 else 2,
            "shadow": 0 if self.wave < 15 else 10,
        }

        if overrides:
            for k in base:
                base[k] = int(base[k] * 0.28)
            for k, v in overrides.items():
                if k in base:
                    base[k] = v

        if self.wave % 13 == 0 and self.wave >= 13:
            base["phase_runner"] = base.get("phase_runner", 0) + 8
        if self.wave % 17 == 0 and self.wave >= 17:
            base["regenerator"] = base.get("regenerator", 0) + 6
        if self.wave % 23 == 0 and self.wave >= 23:
            base["bomber_drone"] = base.get("bomber_drone", 0) + 5

        scale = 1 + (self.wave - 1) * 0.01
        for k in list(base.keys()):
            base[k] = max(0, int(base[k] * scale))

        return [(k, v) for k, v in base.items() if v > 0]

    def choose_enemy(self, pool):
        total = sum(w for _, w in pool)
        r     = random.uniform(0, total)
        upto  = 0
        for enemy_type, weight in pool:
            if upto + weight >= r:
                return enemy_type
            upto += weight
        return pool[-1][0]

    def _show_wave_banner(self, wave_type_name):
        if self._wave_label_id:
            for id_ in self._wave_label_id:
                try:
                    self.canvas.delete(id_)
                except:
                    pass
            self._wave_label_id = None

        wt = WAVE_TYPES[wave_type_name]
        label_text = wt[0]
        label_color = wt[1]
        if not label_text:
            return

        x2, y1 = 1080, 20
        x1 = x2 - 220
        y2 = y1 + 36

        bg  = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#0d0d1a", outline=label_color, width=1)
        txt = self.canvas.create_text(x1 + 12, (y1 + y2) // 2, text=label_text, anchor="w",
                                      fill=label_color, font=("Courier", 11, "bold"))
        self._wave_label_id = (bg, txt)

        def fade():
            try:
                self.canvas.delete(bg)
                self.canvas.delete(txt)
            except:
                pass
            if self._wave_label_id == (bg, txt):
                self._wave_label_id = None

        self.canvas.after(1500, fade)

    def spawn_wave(self):
        if self.wave_running: return
        self.wave_running = True

        for bank in self.banks:
            bank.on_new_wave()
        for mt in MineTower.all_mine_towers:
            mt.on_new_wave()

        # Boss always uses the primary path
        primary_path = self.path
        if self.wave >= BOSS_WAVE and not self.boss_spawned:
            boss = BossEnemy(self.canvas,
                             [self.boss_stage1, self.boss_stage2, self.boss_stage3],
                             primary_path, self.label_hp, self.label_money)
            boss.max_hp = int(boss.max_hp * self.difficulty["boss_hp_mult"])
            boss.hp     = boss.max_hp
            boss.spawn()
            self.boss_spawned = True

        wave_type_name = self._determine_wave_type()
        self.current_wave_type = wave_type_name
        self._show_wave_banner(wave_type_name)

        wt         = WAVE_TYPES[wave_type_name]
        count_mult = wt[3]
        delay_ms   = wt[4]

        base_count = int((8 + self.wave * 1.8) * self.difficulty["wave_size"] * count_mult)
        base_count = max(4, base_count)
        pool       = self._build_pool(wave_type_name)

        # ── Multi-path support: each enemy randomly picks a path ──────────
        all_paths = self.all_paths

        for i in range(base_count):
            def spawn_enemy(idx=i, p=pool, wtn=wave_type_name, ap=all_paths):
                if game.game_over: return
                etype        = self.choose_enemy(p)
                chosen_path  = random.choice(ap) if len(ap) > 1 else ap[0]
                self._spawn_single(etype, chosen_path, wtn)
            self.canvas.after(i * delay_ms, spawn_enemy)

        self.wave += 1
        self.update_hud()

    def _spawn_single(self, etype, path, wave_type_name="normal"):
        hp_mult    = self.difficulty["enemy_hp"]
        spd_mult   = self.difficulty.get("enemy_speed_mult", 1.0)
        wave_scale = 1 + (self.wave - 1) * 0.06

        def _apply_speed(enemy_obj):
            if spd_mult != 1.0:
                enemy_obj.speed *= spd_mult
            return enemy_obj

        if etype == "nuclear":
            _apply_speed(NuclearEnemy(self.canvas, self.nuke_img, path, self.label_hp, self.label_money)).spawn()
        elif etype == "star":
            _apply_speed(StarEnemy(self.canvas, self.star_img, path, self.label_hp, self.label_money, self.enemy_img)).spawn()
        elif etype == "yellow":
            _apply_speed(YellowEnemy(self.canvas, self.yellow_img, path, self.label_hp, self.label_money)).spawn()
        elif etype == "blue":
            _apply_speed(BlueEnemy(self.canvas, self.blue_img, path, self.label_hp, self.label_money)).spawn()
        elif etype == "armored":
            _apply_speed(ArmoredEnemy(self.canvas, self.armored_img, self.shield_img,
                         self.shield_break_img, path, self.label_hp, self.label_money)).spawn()
        elif etype == "zeppelin1":
            _apply_speed(ZeppelinEnemy(self.canvas, self.zeppelin_img, path,
                          self.label_hp, self.label_money, wave=self.wave)).spawn()
        elif etype == "shadow":
            _apply_speed(ShadowEnemy(self.canvas, self.shadow_img, path, self.label_hp, self.label_money)).spawn()
        elif etype == "juggernaut":
            _apply_speed(Juggernaut(self.canvas, self.juggernaut_img, path, self.label_hp, self.label_money)).spawn()
        elif etype == "phase_runner":
            _apply_speed(PhaseRunner(self.canvas, self.phase_runner_img, path, self.label_hp, self.label_money)).spawn()
        elif etype == "regenerator":
            _apply_speed(Regenerator(self.canvas, self.regenerator_img, path, self.label_hp, self.label_money)).spawn()
        elif etype == "bomber_drone":
            _apply_speed(BomberDrone(self.canvas, self.bomber_drone_img, path, self.label_hp, self.label_money)).spawn()
        elif etype == "shielded_brute":
            _apply_speed(ShieldedBrute(self.canvas, self.shielded_brute_img, self.shield_img, self.shield_break_img, path,
                          self.label_hp, self.label_money)).spawn()
        else:
            e = Enemy(self.canvas, self.enemy_img, path, 2 * spd_mult, self.label_hp, self.label_money)
            e.hp = max(1, int(Enemy.base_hp * wave_scale))
            e.spawn()

    # ── GAME OVER / RESTART ──────────────────────────────────────────────────

    def trigger_game_over(self):
        if self.game_over: return
        self.game_over = True
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 1100, 700, fill="#1e1e2e", outline="")
        self.canvas.create_text(550, 230, text="du wurdest penetriert",
                                fill="#ff4757", font=("Courier", 42, "bold"))
        self.canvas.create_text(550, 300, text=f"Wave reached: {self.wave - 1}",
                                fill="white", font=("Courier", 20))
        self.canvas.create_text(550, 360, text="Click to restart",
                                fill="#a4b0be", font=("Courier", 16))
        self.canvas.bind("<Button-1>", lambda e: self.restart_game())

    def trigger_victory(self):
        if getattr(self, "game_over", False): return
        self.game_over = True
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 1100, 700, fill="#0f2a1a", outline="")
        self.canvas.create_text(550, 220, text="VICTORY", fill="#2ed573", font=("Courier", 48, "bold"))
        self.canvas.create_text(550, 300, text=f"You defeated the boss on wave {self.wave - 1}", fill="white", font=("Courier", 18))
        self.canvas.create_text(550, 360, text="Click to return to menu", fill="#a4b0be", font=("Courier", 14))
        self.canvas.bind("<Button-1>", lambda e: self.restart_game())

    def _draw_procedural_map(self, map_cfg):
        c    = self.canvas
        W, H = 1100, 700
        grass = map_cfg["grass_color"]
        road  = map_cfg["road_color"]

        c.create_rectangle(0, 0, W, H, fill=grass, outline="")

        # Scattered foliage dots
        rng = random.Random(42)
        for _ in range(28):
            tx = rng.randint(20, W - 20)
            ty = rng.randint(20, H - 20)
            tr = rng.randint(7, 16)
            shade = rng.choice(["#1a4a1a", "#0e3a0e", "#2a5a2a", "#144014",
                                 "#0d2a2a", "#1a2a3a"])
            c.create_oval(tx-tr, ty-tr, tx+tr, ty+tr, fill=shade, outline="")

        # ── Draw blind zones FIRST (underneath roads) ────────────────────
        for (bx1, by1, bx2, by2) in map_cfg.get("blind_zones", []):
            c.create_rectangle(bx1, by1, bx2, by2,
                               fill="#2a1a0a", outline="#5a3a14", width=3)
            for tx in range(int(bx1) + 10, int(bx2), 16):
                c.create_line(tx, by1, tx - 10, by2, fill="#3a2510", width=1)
            for ty_ in range(int(by1) + 10, int(by2), 18):
                c.create_line(bx1, ty_, bx2, ty_, fill="#3a2510", width=1)
            mx = (bx1 + bx2) / 2
            my = (by1 + by2) / 2
            c.create_text(mx, my - 8, text="🚧", font=("Arial", 14))
            c.create_text(mx, my + 12, text="TUNNEL",
                          fill="#8B7355", font=("Courier", 9, "bold"))

        # ── Draw all paths (multi-path support for Twin Gates etc.) ──────
        all_paths_to_draw = map_cfg.get("paths", [map_cfg["path"]])
        road_w   = 38
        edge_col = "#3a2800"

        for pth in all_paths_to_draw:
            for i in range(len(pth) - 1):
                x1, y1 = pth[i]
                x2, y2 = pth[i + 1]
                c.create_line(x1, y1, x2, y2, fill=edge_col, width=road_w + 6,
                              capstyle="round", joinstyle="round")
                c.create_line(x1, y1, x2, y2, fill=road, width=road_w - 4,
                              capstyle="round", joinstyle="round")

        # Dashed center line on all paths
        for pth in all_paths_to_draw:
            for i in range(len(pth) - 1):
                x1, y1 = pth[i]
                x2, y2 = pth[i + 1]
                c.create_line(x1, y1, x2, y2, fill="#d4a800", width=2,
                              dash=(14, 10), capstyle="round")

        # ── Re-draw blind zone OVERLAY on top of roads (dark "roof") ─────
        for (bx1, by1, bx2, by2) in map_cfg.get("blind_zones", []):
            c.create_rectangle(bx1, by1, bx2, by2,
                               fill="#1a0e05", outline="#5a3a14", width=3,
                               stipple="gray50")
            c.create_rectangle(bx1 + 4, by1 + 4, bx2 - 4, by2 - 4,
                               outline="#7a5a20", fill="", width=1)

        # ── Spawn / exit markers ─────────────────────────────────────────
        drawn_exits = set()
        for pth in all_paths_to_draw:
            sx, sy = pth[0]
            ex, ey = pth[-1]
            c.create_oval(sx-12, sy-12, sx+12, sy+12, fill="#2ed573", outline="white", width=2)
            c.create_text(sx, sy, text="S", fill="white", font=("Courier", 11, "bold"))
            key = (ex, ey)
            if key not in drawn_exits:
                c.create_oval(ex-12, ey-12, ex+12, ey+12, fill="#ff4757", outline="white", width=2)
                c.create_text(ex, ey, text="E", fill="white", font=("Courier", 11, "bold"))
                drawn_exits.add(key)

        # ── Merge-point marker for twin gates ────────────────────────────
        if len(all_paths_to_draw) > 1:
            set_a = set(map(tuple, all_paths_to_draw[0]))
            for pth in all_paths_to_draw[1:]:
                for pt in pth:
                    if tuple(pt) in set_a and pt != all_paths_to_draw[0][0]:
                        mx, my = pt
                        c.create_oval(mx-10, my-10, mx+10, my+10,
                                      fill="#fdcb6e", outline="white", width=2)
                        c.create_text(mx, my, text="⚡", font=("Arial", 10))
                        break

    def restart_game(self):
        Enemy.enemies.clear()
        Barricade.barricades.clear()
        MineTower.all_mine_towers.clear()
        Game.game_over = False
        Game.paused    = False
        self.towers.clear()
        self.banks = []
        for w in self.root.winfo_children():
            w.destroy()
        self.show_main_menu()

    # ── HELPERS ──────────────────────────────────────────────────────────────

    def update_money_label(self):
        self.update_hud()

    def show_range(self, x, y, r, color="#00ffcc"):
        self.hide_range()
        self.range_circle = self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                                     outline=color, dash=(4,2), width=2)

    def hide_range(self):
        if hasattr(self, "range_circle"):
            self.canvas.delete(self.range_circle)
            del self.range_circle

    def is_on_path(self, x, y, radius=20):
        for x1, y1, x2, y2 in self.path_zones:
            if x+radius > x1 and x-radius < x2 and y+radius > y1 and y-radius < y2:
                return True
        return False


Game()