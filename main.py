#!/usr/bin/env python3
# Run: python main.py

import random
import time
import os


# ---------------------------- Utility Helpers ----------------------------

def random_choice(options):
    """Return a random option from a non-empty list."""
    return random.choice(options)


def input_with_default(prompt, default_value):
    """Prompt the user. If ENTER, return default_value."""
    value = input(prompt).strip()
    if value == "":
        return default_value
    return value


def ask_menu(prompt, options, default_index=None):
    """
    Show a numbered menu and return the chosen option.
    If ENTER, pick a random option (or default_index if provided).
    """
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"  {i}) {opt}")

    while True:
        raw = input("Choose a number (ENTER = random/default): ").strip()
        if raw == "":
            if default_index is not None and 0 <= default_index < len(options):
                return options[default_index]
            return random_choice(options)
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        print("Invalid choice. Please enter a valid number.")


def ask_multi_menu(prompt, options, allow_none=True):
    """
    Multiple selections. User enters comma-separated numbers.
    ENTER picks random 1-2 options (or 'none' if present and chosen randomly).
    """
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"  {i}) {opt}")

    while True:
        raw = input("Choose numbers (e.g., 1,3). ENTER = random: ").strip()
        if raw == "":
            if allow_none and "none" in options and random.random() < 0.25:
                return ["none"]
            count = 1 if len(options) == 1 else random.choice([1, 2])
            return random.sample(options, k=min(count, len(options)))

        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if not parts:
            print("Invalid input. Try again.")
            continue

        chosen = []
        valid = True
        for p in parts:
            if not p.isdigit():
                valid = False
                break
            idx = int(p) - 1
            if 0 <= idx < len(options):
                chosen.append(options[idx])
            else:
                valid = False
                break

        if valid and chosen:
            # Deduplicate while preserving order
            seen = set()
            result = []
            for c in chosen:
                if c not in seen:
                    seen.add(c)
                    result.append(c)
            return result

        print("Invalid selection. Please choose valid numbers.")


def ask_yes_no(prompt, default_random=True):
    """
    Return True/False based on y/n. ENTER = random (or True if default_random).
    """
    while True:
        raw = input(prompt).strip().lower()
        if raw == "":
            if default_random:
                return random.choice([True, False])
            return True
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please enter y or n (or ENTER for default).")


def enforce_adult_age(age_str):
    """
    Accepts user input for age and enforces 21-30.
    If invalid or <21, set to 25 and warn.
    """
    if not age_str.isdigit():
        print("Age invalid. Using 25.")
        return 25
    age = int(age_str)
    if age < 21:
        print("Age under 21 is not allowed. Using 25.")
        return 25
    if age > 30:
        print("Age over 30 not allowed for this pack. Using 25.")
        return 25
    return age


def clean_prompt_parts(parts):
    """Remove empty parts and return comma-separated single line."""
    clean = [p for p in parts if p and p.strip()]
    return ", ".join(clean)


# ---------------------------- Data Lists ----------------------------

EXAMPLE_SUBJECTS = [
    "beauty influencer holding a skincare bottle",
    "female model showcasing a luxury perfume",
    "fashion blogger holding a branded tote bag",
    "lifestyle influencer holding a coffee cup",
    "athletic influencer holding a sports drink",
    "tech reviewer holding a sleek smartphone",
]

BODY_TYPES = [
    "slim athletic",
    "sporty fit",
    "curvy",
    "average",
    "runway model (tall slim)",
    "gym physique (toned)",
]

SKIN_TONES = [
    "porcelain pale white",
    "fair",
    "light tan",
    "olive",
    "brown",
    "dark",
]

FACE_DETAILS = [
    "beauty mark above upper lip",
    "freckles (subtle)",
    "dimples",
    "sharp jawline",
    "soft jawline",
    "high cheekbones",
]

EYE_COLORS = ["green", "brown", "blue", "hazel", "gray"]
EYEBROW_STYLES = ["thick natural", "thin", "arched", "straight"]

HAIR_COLORS = ["black", "dark brown", "brown", "blonde", "red"]
HAIR_STYLES = ["extremely curly tight ringlets", "curly", "wavy", "straight"]
HAIR_LENGTHS = ["short bob", "shoulder length", "long", "very long"]
HAIR_PARTING = ["middle part", "side part"]

MAKEUP = ["natural makeup", "soft glam", "bold lipstick", "smoky eyes", "no makeup look"]

ACCESSORIES = [
    "none",
    "small hoop earrings",
    "pearl earrings",
    "minimal necklace",
    "rings",
    "sunglasses",
    "watch",
]

TOPS = [
    "black turtleneck",
    "white blouse",
    "elegant blazer",
    "simple dress",
    "hoodie (street)",
    "crop jacket",
]

BOTTOMS = [
    "jeans",
    "black trousers",
    "skirt",
    "shorts",
    "dress",
    "leggings (sporty)",
]

FOOTWEAR = ["sneakers", "heels", "boots", "none (not visible)"]

POSES = [
    "standing, confident",
    "sitting, relaxed",
    "walking candid",
    "over-the-shoulder look",
    "holding product with one hand",
    "holding product with both hands",
    "selfie pose (mirror)",
    "arms crossed (editorial)",
]

HEAD_GAZE = [
    "neutral expression",
    "soft smile",
    "serious editorial",
    "laughing candid",
    "head tilted down, eyes downward (clear)",
    "head tilted up, looking upward (clear)",
    "looking left",
    "looking right",
]

CAMERA_ANGLES = [
    "eye level",
    "low angle (shot from below)",
    "high angle (shot from above)",
    "three-quarter angle (45 degrees right)",
    "three-quarter angle (45 degrees left)",
    "side profile right (90 degrees)",
    "side profile left (90 degrees)",
]

SHOT_TYPES = [
    "close-up face portrait",
    "headshot",
    "half body",
    "full body",
    "product close-up (hands + object)",
]

CAMERAS = [
    "iPhone 17 Pro Max (smartphone photo, computational photography, crisp detail)",
    "iPhone 15/16 Pro (smart HDR, natural)",
    "Canon EOS R5",
    "Sony A7 IV",
    "Nikon Z6 II",
    "Fujifilm X-T5 (film-like colors)",
    "cheap phone camera (amateur noise, imperfect)",
]

LENSES = ["24mm", "35mm", "50mm", "85mm", "105mm macro"]
APERTURES = ["f/1.4 strong bokeh", "f/2.8 balanced", "f/5.6 sharper background"]

LIGHTING = [
    "professional studio beauty lighting (softbox)",
    "cinematic low key lighting",
    "natural window daylight",
    "overcast outdoor daylight",
    "golden hour sunlight",
    "neon night city",
    "harsh flash",
    "office fluorescent",
    "warm indoor bulb light",
]

BACKGROUNDS = [
    "plain white wall",
    "plain gray wall",
    "plain black backdrop (luxury)",
    "studio seamless paper",
    "minimal modern apartment",
    "city street bokeh",
    "cafe interior",
    "bedroom realistic",
    "product table setup",
]

QUALITY_STYLE = [
    "ultra realistic commercial advertisement",
    "natural realistic (visible skin texture)",
    "amateur candid (slight blur/noise)",
    "fashion editorial magazine look",
    "cinematic still frame",
    "product advertisement (sharp product focus)",
]

COMPOSITION = [
    "centered composition",
    "rule of thirds",
    "shallow depth of field",
    "sharp focus on eyes",
    "sharp focus on product",
    "subtle film grain",
]


DEFAULT_NEGATIVE = (
    "blurry, low quality, jpeg artifacts, watermark, text, logo, misspelled words, "
    "random letters, bad anatomy, deformed, extra fingers, missing fingers, bad hands, "
    "distorted face, cross-eye, poorly drawn, oversaturated"
)


PRESETS = {
    "Luxury Product Ad": {
        "lighting": "professional studio beauty lighting (softbox)",
        "lens": "85mm",
        "background": "plain black backdrop (luxury)",
        "quality": "ultra realistic commercial advertisement",
        "shot_type": "product close-up (hands + object)",
    },
    "Social Media iPhone": {
        "camera": "iPhone 17 Pro Max (smartphone photo, computational photography, crisp detail)",
        "lighting": "natural window daylight",
        "background": "minimal modern apartment",
        "quality": "natural realistic (visible skin texture)",
        "shot_type": "half body",
    },
    "Street Candid": {
        "camera": "Sony A7 IV",
        "lens": "35mm",
        "lighting": "overcast outdoor daylight",
        "background": "city street bokeh",
        "quality": "amateur candid (slight blur/noise)",
        "pose": "walking candid",
    },
    "Studio Headshot": {
        "lighting": "professional studio beauty lighting (softbox)",
        "background": "plain gray wall",
        "quality": "fashion editorial magazine look",
        "shot_type": "headshot",
    },
}


# ---------------------------- Prompt Builder ----------------------------

def apply_preset(preset_name, current):
    """Apply preset values into current settings."""
    preset = PRESETS.get(preset_name, {})
    for key, value in preset.items():
        current[key] = value


def build_prompt():
    print("\n=== Ultra Realistic Prompt Builder ===\n")

    subject = input_with_default(
        "Subject (free text) (ENTER = random example): ",
        random_choice(EXAMPLE_SUBJECTS),
    )

    # Preset selection (optional)
    preset_names = list(PRESETS.keys())
    preset_choice = ask_menu("Choose a preset (optional):", preset_names + ["none"], default_index=len(preset_names))

    # Person pack
    age_raw = input_with_default("Age (21-30, ENTER = random): ", str(random.randint(21, 30)))
    age = enforce_adult_age(age_raw)

    body_type = ask_menu("Body type:", BODY_TYPES)
    skin_tone = ask_menu("Skin tone:", SKIN_TONES)
    face_details = ask_multi_menu("Face details (multiple allowed):", FACE_DETAILS, allow_none=False)

    eye_color = ask_menu("Eye color:", EYE_COLORS)
    brow_style = ask_menu("Eyebrow style:", EYEBROW_STYLES)

    hair_color = ask_menu("Hair color:", HAIR_COLORS)
    hair_style = ask_menu("Hair style:", HAIR_STYLES)
    hair_length = ask_menu("Hair length:", HAIR_LENGTHS)
    hair_parting = ask_menu("Hair parting:", HAIR_PARTING)
    hair_visible = ask_yes_no("Hair clearly visible? (ENTER = random, y/n): ", default_random=True)

    makeup = ask_menu("Makeup:", MAKEUP)
    accessories = ask_multi_menu("Accessories (multiple allowed):", ACCESSORIES, allow_none=True)

    top = ask_menu("Clothing top:", TOPS)
    bottom_options = BOTTOMS
    if top == "simple dress":
        bottom_options = ["n/a (dress)"]
    bottom = ask_menu("Clothing bottom:", bottom_options)

    footwear = ask_menu("Footwear:", FOOTWEAR)

    # Pose / camera angles
    pose = ask_menu("Pose:", POSES)
    head_gaze = ask_menu("Head + gaze:", HEAD_GAZE)
    camera_angle = ask_menu("Camera angle:", CAMERA_ANGLES)
    shot_type = ask_menu("Shot type:", SHOT_TYPES)

    # Camera / quality
    camera = ask_menu("Camera device:", CAMERAS)
    lens = ask_menu("Lens:", LENSES)
    aperture = ask_menu("Aperture:", APERTURES)
    lighting = ask_menu("Lighting:", LIGHTING)
    background = ask_menu("Background:", BACKGROUNDS)
    quality = ask_menu("Quality style:", QUALITY_STYLE)
    composition = ask_menu("Composition:", COMPOSITION)

    # Text on product
    force_text = ask_yes_no('Try to force brand text on label? (ENTER=random, y=yes, n=no): ', default_random=True)

    # Current selections as dict for preset overrides
    current = {
        "pose": pose,
        "shot_type": shot_type,
        "camera": camera,
        "lens": lens,
        "lighting": lighting,
        "background": background,
        "quality": quality,
    }
    if preset_choice != "none":
        apply_preset(preset_choice, current)

    # Apply any preset updates back to variables
    pose = current["pose"]
    shot_type = current["shot_type"]
    camera = current["camera"]
    lens = current["lens"]
    lighting = current["lighting"]
    background = current["background"]
    quality = current["quality"]

    # Build positive prompt parts
    prompt_parts = [
        subject,
        f"adult female influencer, age {age}",
        body_type,
        skin_tone,
        ", ".join(face_details),
        f"{eye_color} eyes",
        f"{brow_style} eyebrows",
        f"{hair_color} hair",
        hair_style,
        hair_length,
        hair_parting,
        "hair clearly visible" if hair_visible else "",
        makeup,
        ", ".join(accessories) if accessories else "",
        f"wearing {top}",
        f"bottom: {bottom}",
        f"footwear: {footwear}",
        pose,
        head_gaze,
        camera_angle,
        shot_type,
        camera,
        lens,
        aperture,
        lighting,
        background,
        quality,
        composition,
    ]

    if force_text:
        prompt_parts.append('the label clearly says "NoctAmor"')
    else:
        prompt_parts.append("label text added later in design software")

    final_prompt = clean_prompt_parts(prompt_parts)

    # Build negative prompt
    negative_parts = [DEFAULT_NEGATIVE]
    # Conditional negatives
    if hair_style == "extremely curly tight ringlets":
        negative_parts.append("straight hair")
    if hair_style == "straight":
        negative_parts.append("curly hair")
    if hair_visible:
        negative_parts.append("hair covering face")
    if top == "simple dress":
        negative_parts.append("separate top and bottom")
    if force_text:
        negative_parts.append("misspelled brand name, garbled label text, broken typography")

    negative_prompt = clean_prompt_parts(negative_parts)

    # Settings suggestion block
    settings_block = (
        "SETTINGS SUGGESTION\n"
        "Sampler: DPM++ 2M Karras\n"
        "Steps: 25\n"
        "CFG: 6.5-7\n"
        "Resolution: 512x768 portrait\n"
        "Notes: Text can be misspelled; consider adding text in post."
    )

    # Output
    print("\n--- FINAL PROMPT ---")
    print(final_prompt)
    print("\n--- NEGATIVE PROMPT ---")
    print(negative_prompt)
    print("\n--- SETTINGS ---")
    print(settings_block)

    # Save to file?
    save = input("Save output to timestamped .txt? (ENTER = don't save, y = save): ").strip().lower()
    if save == "y":
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"prompts_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("FINAL PROMPT\n")
            f.write(final_prompt + "\n\n")
            f.write("NEGATIVE PROMPT\n")
            f.write(negative_prompt + "\n\n")
            f.write(settings_block + "\n")
        print(f"Saved to {os.path.abspath(filename)}")


def main():
    while True:
        build_prompt()
        again = input("\nGenerate another? (ENTER = yes, q = quit): ").strip().lower()
        if again == "q":
            break


if __name__ == "__main__":
    main()
