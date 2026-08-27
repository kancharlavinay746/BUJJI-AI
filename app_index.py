import os
import json
import glob
import re


# =========================================================
# CONFIGURATION
# =========================================================

CACHE_FILE = os.path.join(
    os.path.dirname(__file__),
    "applications.json"
)


# =========================================================
# NAME NORMALIZATION
# =========================================================

def normalize_name(name):
    """
    Normalize application names for searching.
    """

    name = name.lower().strip()

    name = re.sub(
        r"\.(exe|lnk)$",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"[^a-z0-9 ]",
        "",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name.strip()


# =========================================================
# APPLICATION SCAN LOCATIONS
# =========================================================

def get_scan_locations():

    locations = [

        # User Start Menu
        os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
        ),

        # System Start Menu
        os.path.expandvars(
            r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"
        ),

        # User Desktop
        os.path.expandvars(
            r"%USERPROFILE%\Desktop"
        ),

        # Public Desktop
        os.path.expandvars(
            r"%PUBLIC%\Desktop"
        ),

    ]

    return [
        path
        for path in locations
        if path and os.path.exists(path)
    ]


# =========================================================
# SCAN SHORTCUTS
# =========================================================

def scan_shortcuts():

    applications = {}

    locations = get_scan_locations()

    print()
    print("🔎 Scanning Windows application shortcuts...")

    for location in locations:

        print(
            f"📁 Scanning: {location}"
        )

        try:

            files = glob.glob(
                location + r"\**\*.lnk",
                recursive=True
            )

        except Exception as e:

            print(
                f"⚠️ Scan error: {e}"
            )

            continue

        for shortcut in files:

            filename = os.path.splitext(
                os.path.basename(shortcut)
            )[0]

            normalized = normalize_name(
                filename
            )

            if not normalized:
                continue

            applications[normalized] = {
                "name": filename,
                "path": shortcut,
                "type": "shortcut"
            }

    return applications


# =========================================================
# SCAN EXECUTABLES
# =========================================================

def scan_executables():

    applications = {}

    locations = [

        os.environ.get(
            "PROGRAMFILES",
            r"C:\Program Files"
        ),

        os.environ.get(
            "PROGRAMFILES(X86)",
            r"C:\Program Files (x86)"
        ),

        os.environ.get(
            "LOCALAPPDATA",
            ""
        ),

    ]

    print()
    print("🔎 Scanning installed applications...")

    for location in locations:

        if not location:
            continue

        if not os.path.exists(location):
            continue

        print(
            f"📁 Scanning: {location}"
        )

        try:

            for root, dirs, files in os.walk(
                location
            ):

                # Limit scan depth
                relative = os.path.relpath(
                    root,
                    location
                )

                if relative == ".":
                    depth = 0
                else:
                    depth = relative.count(
                        os.sep
                    ) + 1

                if depth > 3:

                    dirs[:] = []

                    continue

                for file in files:

                    if not file.lower().endswith(
                        ".exe"
                    ):
                        continue

                    filename = os.path.splitext(
                        file
                    )[0]

                    normalized = normalize_name(
                        filename
                    )

                    if not normalized:
                        continue

                    # Don't overwrite shortcut
                    # entries with executables
                    if normalized not in applications:

                        applications[normalized] = {
                            "name": filename,
                            "path": os.path.join(
                                root,
                                file
                            ),
                            "type": "executable"
                        }

        except PermissionError:

            continue

        except Exception as e:

            print(
                f"⚠️ Scan error: {e}"
            )

    return applications


# =========================================================
# BUILD APPLICATION INDEX
# =========================================================

def build_index():

    print()
    print("=" * 60)
    print("🧠 BUJJI APPLICATION INDEX")
    print("=" * 60)

    applications = {}

    # Start Menu + Desktop
    shortcuts = scan_shortcuts()

    applications.update(
        shortcuts
    )

    # Program Files
    executables = scan_executables()

    for name, data in executables.items():

        if name not in applications:

            applications[name] = data

    # Save index
    try:

        with open(
            CACHE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                applications,
                file,
                indent=2,
                ensure_ascii=False
            )

        print()
        print(
            f"💾 Application index saved:"
        )

        print(
            f"   {CACHE_FILE}"
        )

    except Exception as e:

        print(
            f"❌ Failed to save index: {e}"
        )

    print()
    print(
        f"✅ Applications indexed: {len(applications)}"
    )

    print("=" * 60)

    return applications


# =========================================================
# LOAD INDEX
# =========================================================

def load_index():

    if not os.path.exists(
        CACHE_FILE
    ):

        print(
            "⚠️ Application index does not exist."
        )

        return build_index()

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            applications = json.load(
                file
            )

        print(
            f"📚 Loaded {len(applications)} applications."
        )

        return applications

    except Exception as e:

        print(
            f"⚠️ Could not load application index: {e}"
        )

        return build_index()


# =========================================================
# SEARCH INDEX
# =========================================================

def find_application(
    app_name,
    applications=None
):

    if applications is None:

        applications = load_index()

    target = normalize_name(
        app_name
    )

    if not target:
        return None

    # -----------------------------------------------------
    # Exact match
    # -----------------------------------------------------

    if target in applications:

        return applications[target]

    # -----------------------------------------------------
    # Partial match
    # -----------------------------------------------------

    best_match = None
    best_score = 0

    for name, data in applications.items():

        # Target contained in application name
        if target in name:

            score = len(target)

            if score > best_score:

                best_match = data
                best_score = score

        # Application name contained in target
        elif name in target:

            score = len(name)

            if score > best_score:

                best_match = data
                best_score = score

    return best_match


# =========================================================
# LAUNCH APPLICATION
# =========================================================

def launch_application(app_name):

    application = find_application(
        app_name
    )

    if not application:

        print(
            f"❌ Application not found: {app_name}"
        )

        return False

    path = application["path"]

    print()
    print(
        f"✅ Found: {application['name']}"
    )

    print(
        f"📍 Path: {path}"
    )

    try:

        if application["type"] == "shortcut":

            os.startfile(path)

        else:

            os.startfile(path)

        print(
            f"🚀 Launching {application['name']}..."
        )

        return True

    except Exception as e:

        print(
            f"❌ Launch failed: {e}"
        )

        return False