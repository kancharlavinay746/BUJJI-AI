import os
import subprocess
import glob
import shutil
import re


# =========================================================
# NAME NORMALIZATION
# =========================================================

def normalize_name(name):
    """
    Normalize an application name for comparison.
    """

    name = name.lower().strip()

    # Remove common words
    name = re.sub(
        r"\b(application|app|program)\b",
        "",
        name
    )

    # Remove punctuation
    name = re.sub(
        r"[^a-z0-9 ]",
        "",
        name
    )

    # Normalize spaces
    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name.strip()


# =========================================================
# SEARCH START MENU + DESKTOP SHORTCUTS
# =========================================================

def search_shortcuts(app_name):
    """
    Search Windows Start Menu and Desktop shortcuts.
    """

    locations = [

        # Current user's Start Menu
        os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
        ),

        # All users Start Menu
        os.path.expandvars(
            r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"
        ),

        # Current user's Desktop
        os.path.expandvars(
            r"%USERPROFILE%\Desktop"
        ),

        # Public Desktop
        os.path.expandvars(
            r"%PUBLIC%\Desktop"
        ),
    ]

    target = normalize_name(app_name)

    best_match = None
    best_score = 0

    for location in locations:

        if not os.path.exists(location):
            continue

        try:

            files = glob.glob(
                location + r"\**\*.lnk",
                recursive=True
            )

        except Exception as e:

            print(
                f"⚠️ Shortcut search error: {e}"
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

            # Exact match
            if normalized == target:

                return shortcut

            # Target is inside shortcut name
            if target in normalized:

                score = len(target)

                if score > best_score:

                    best_match = shortcut
                    best_score = score

            # Shortcut name is inside target
            elif normalized in target:

                score = len(normalized)

                if score > best_score:

                    best_match = shortcut
                    best_score = score

    return best_match


# =========================================================
# SEARCH WINDOWS PATH
# =========================================================

def search_windows_path(app_name):
    """
    Search applications available through Windows PATH.
    """

    target = normalize_name(app_name)

    # Try original name
    try:

        result = shutil.which(
            app_name
        )

        if result:
            return result

    except Exception:
        pass

    # Try normalized name without spaces
    try:

        result = shutil.which(
            target.replace(" ", "")
        )

        if result:
            return result

    except Exception:
        pass

    return None


# =========================================================
# SEARCH PROGRAM FILES
# =========================================================

def search_program_files(app_name):
    """
    Search common Windows application directories.

    The search is intentionally limited in depth so that
    BUJJI does not scan the entire hard drive.
    """

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

    target = normalize_name(
        app_name
    )

    if len(target) < 2:
        return None

    for location in locations:

        if not location:
            continue

        if not os.path.exists(location):
            continue

        try:

            for root, dirs, files in os.walk(
                location
            ):

                # Limit search depth
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

                    # Exact executable match
                    if normalized == target:

                        return os.path.join(
                            root,
                            file
                        )

                    # Partial match
                    if (
                        target in normalized
                        and len(target) >= 3
                    ):

                        return os.path.join(
                            root,
                            file
                        )

        except PermissionError:

            continue

        except Exception as e:

            print(
                f"⚠️ Program search error: {e}"
            )

    return None


# =========================================================
# UNIVERSAL APPLICATION LAUNCHER
# =========================================================

def open_app(app_name):
    """
    Search for and launch a Windows application.

    Returns:
        True  -> application found and launch attempted
        False -> application could not be found
    """

    app_name = app_name.strip()

    if not app_name:

        print(
            "❌ Empty application name."
        )

        return False

    print()
    print(
        "=" * 55
    )
    print(
        f"🔎 Searching Windows for: {app_name}"
    )
    print(
        "=" * 55
    )

    # =====================================================
    # METHOD 1
    # START MENU / DESKTOP
    # =====================================================

    print(
        "1️⃣ Searching Start Menu/Desktop..."
    )

    shortcut = search_shortcuts(
        app_name
    )

    if shortcut:

        print(
            f"✅ Shortcut found:"
        )

        print(
            f"   {shortcut}"
        )

        try:

            os.startfile(
                shortcut
            )

            print(
                f"🚀 {app_name} launched."
            )

            return True

        except Exception as e:

            print(
                f"⚠️ Shortcut launch failed: {e}"
            )

    # =====================================================
    # METHOD 2
    # WINDOWS PATH
    # =====================================================

    print(
        "2️⃣ Searching Windows PATH..."
    )

    executable = search_windows_path(
        app_name
    )

    if executable:

        print(
            f"✅ Executable found:"
        )

        print(
            f"   {executable}"
        )

        try:

            subprocess.Popen(
                [executable]
            )

            print(
                f"🚀 {app_name} launched."
            )

            return True

        except Exception as e:

            print(
                f"⚠️ Executable launch failed: {e}"
            )

    # =====================================================
    # METHOD 3
    # PROGRAM FILES
    # =====================================================

    print(
        "3️⃣ Searching Program Files..."
    )

    executable = search_program_files(
        app_name
    )

    if executable:

        print(
            f"✅ Program found:"
        )

        print(
            f"   {executable}"
        )

        try:

            subprocess.Popen(
                [executable]
            )

            print(
                f"🚀 {app_name} launched."
            )

            return True

        except Exception as e:

            print(
                f"⚠️ Program launch failed: {e}"
            )

    # =====================================================
    # NOT FOUND
    # =====================================================

    print()
    print(
        f"❌ Application not found: {app_name}"
    )

    return False


# =========================================================
# WINDOWS SYSTEM APPLICATIONS
# =========================================================

def open_file_explorer():

    try:

        subprocess.Popen(
            ["explorer.exe"]
        )

        return True

    except Exception as e:

        print(
            f"❌ File Explorer error: {e}"
        )

        return False


def open_cmd():

    try:

        subprocess.Popen(
            ["cmd.exe"]
        )

        return True

    except Exception as e:

        print(
            f"❌ CMD error: {e}"
        )

        return False


def open_powershell():

    try:

        subprocess.Popen(
            ["powershell.exe"]
        )

        return True

    except Exception as e:

        print(
            f"❌ PowerShell error: {e}"
        )

        return False


def open_task_manager():

    try:

        subprocess.Popen(
            ["taskmgr.exe"]
        )

        return True

    except Exception as e:

        print(
            f"❌ Task Manager error: {e}"
        )

        return False