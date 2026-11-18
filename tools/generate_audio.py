"""Generate original, dependency-free chiptune music and sound effects."""
from __future__ import annotations

import math
import random
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "assets" / "audio"
RATE = 22050
random.seed(84)


def write_wav(name: str, samples: list[float], loop: bool = False) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    peak = max((abs(x) for x in samples), default=1.0) or 1.0
    with wave.open(str(ROOT / f"{name}.wav"), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x / peak * 0.82)) * 32767)) for x in samples))


def note(freq: float, dur: float, shape: str = "square", volume: float = 0.2) -> list[float]:
    count = int(RATE * dur)
    out = []
    for i in range(count):
        t = i / RATE
        phase = (t * freq) % 1.0
        if shape == "square":
            v = 1.0 if phase < 0.5 else -1.0
        elif shape == "triangle":
            v = 1.0 - 4.0 * abs(phase - 0.5)
        else:
            v = math.sin(2 * math.pi * freq * t)
        env = min(1.0, i / max(1, int(RATE * 0.012))) * min(1.0, (count - i) / max(1, int(RATE * 0.04)))
        out.append(v * volume * env)
    return out


def music(name: str, bpm: int, melody: list[int], bass: list[int], bright: bool = True) -> None:
    step = 60.0 / bpm / 2
    bars = 4
    total = int(RATE * step * len(melody) * bars)
    out = [0.0] * total
    for bar in range(bars):
        for i, midi in enumerate(melody):
            start = int((bar * len(melody) + i) * step * RATE)
            f = 440.0 * 2 ** ((midi - 69) / 12)
            for j, sample in enumerate(note(f, step * 0.88, "square" if bright else "triangle", 0.13)):
                if start + j < total:
                    out[start + j] += sample
        for i, midi in enumerate(bass):
            start = int((bar * len(bass) + i) * step * 2 * RATE)
            f = 440.0 * 2 ** ((midi - 69) / 12)
            for j, sample in enumerate(note(f, step * 1.72, "triangle", 0.13)):
                if start + j < total:
                    out[start + j] += sample
        # A quiet kick/snare pulse keeps the rhythm without masking gameplay.
        for beat in range(8):
            if beat % 2 == 1:
                start = int((bar * len(melody) + beat) * step * RATE)
                length = int(RATE * 0.055)
                for j in range(length):
                    env = (1 - j / length) ** 2
                    out[start + j] += random.uniform(-0.12, 0.12) * env
    write_wav(name, out, True)


def effect(name: str, freqs: list[float], durations: list[float], noise: float = 0.0) -> None:
    samples: list[float] = []
    for freq, dur in zip(freqs, durations):
        samples.extend(note(freq, dur, "square", 0.26))
    if noise:
        for i in range(len(samples)):
            samples[i] += random.uniform(-noise, noise) * (1 - i / max(1, len(samples)))
    write_wav(name, samples)


def main() -> None:
    # Original melodies in a warm, arcade football palette.
    music("menu", 104, [72, 76, 79, 84, 79, 76, 74, 76], [48, 55, 53, 60], False)
    music("level", 144, [72, 72, 79, 76, 74, 74, 81, 79], [48, 48, 55, 55], True)
    music("gameover", 86, [71, 69, 67, 62, 64, 62, 59, 55], [43, 47, 50, 43], False)
    music("victory", 126, [72, 79, 84, 79, 76, 83, 88, 84], [48, 55, 60, 55], True)
    effect("jump", [380, 520, 700], [0.045, 0.045, 0.06])
    effect("attack", [620, 450, 330], [0.025, 0.03, 0.045], 0.04)
    effect("kick", [230, 390, 560], [0.035, 0.06, 0.04], 0.12)
    effect("hit", [270, 190, 130], [0.04, 0.04, 0.07], 0.06)
    effect("hurt", [350, 260, 180, 120], [0.05, 0.07, 0.08, 0.1], 0.1)
    effect("pickup", [660, 830, 990], [0.045, 0.045, 0.1])


if __name__ == "__main__":
    main()
