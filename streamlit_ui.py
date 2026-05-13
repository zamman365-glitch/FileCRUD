
import streamlit as st
from pathlib import Path
import os

st.set_page_config(page_title="File Manager", page_icon="🗂️", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #0f1117; }
        .block-container { padding-top: 2rem; }
        h1 { color: #00d4aa; font-family: 'Courier New', monospace; }
        .stButton > button {
            width: 100%;
            background-color: #1e2130;
            color: #00d4aa;
            border: 1px solid #00d4aa;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
        .stButton > button:hover {
            background-color: #00d4aa;
            color: #0f1117;
        }
        .file-list {
            background-color: #1e2130;
            border: 1px solid #2e3250;
            border-radius: 6px;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            color: #cdd6f4;
            min-height: 100px;
            max-height: 300px;
            overflow-y: auto;
        }
        .success-box {
            background-color: #1a2f2a;
            border-left: 4px solid #00d4aa;
            padding: 0.75rem 1rem;
            border-radius: 4px;
            color: #00d4aa;
            font-family: 'Courier New', monospace;
        }
        .error-box {
            background-color: #2f1a1a;
            border-left: 4px solid #f38ba8;
            padding: 0.75rem 1rem;
            border-radius: 4px;
            color: #f38ba8;
            font-family: 'Courier New', monospace;
        }
    </style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_all_items():
    return list(Path('').rglob('*'))


def show_items():
    items = get_all_items()
    if items:
        lines = [f"{'📁' if i.is_dir() else '📄'} {i}" for i in items]
        return "\n".join(lines)
    return "(no files or folders found)"


def msg(text, kind="success"):
    tag = "success-box" if kind == "success" else "error-box"
    st.markdown(f'<div class="{tag}">{text}</div>', unsafe_allow_html=True)


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("🗂️ File Manager")
st.markdown("---")

col_sidebar, col_main = st.columns([1, 2])

with col_sidebar:
    st.subheader("Operations")
    operation = st.radio(
        "Choose an action:",
        [
            "📋 View Files & Folders",
            "➕ Create File",
            "📖 Read File",
            "✏️ Update File",
            "🗑️ Delete File",
            "🔤 Rename File",
            "📁 Create Folder",
            "❌ Delete Folder",
            "📁➕ Create Folder + File",
        ],
        label_visibility="collapsed",
    )

with col_main:
    # ── View ──
    if operation == "📋 View Files & Folders":
        st.subheader("Current Files & Folders")
        st.markdown(
            f'<div class="file-list"><pre>{show_items()}</pre></div>',
            unsafe_allow_html=True,
        )

    # ── Create File ──
    elif operation == "➕ Create File":
        st.subheader("Create a New File")
        st.markdown(
            f'<div class="file-list"><pre>{show_items()}</pre></div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        file_name = st.text_input("File name (e.g. notes.txt)")
        content = st.text_area("File content")
        if st.button("Create File"):
            if file_name:
                p = Path(file_name)
                if p.exists():
                    msg("⚠️ File already exists!", "error")
                else:
                    try:
                        p.write_text(content)
                        msg(f"✅ File '{file_name}' created!")
                    except Exception as e:
                        msg(str(e), "error")
            else:
                msg("Please enter a file name.", "error")

    # ── Read File ──
    elif operation == "📖 Read File":
        st.subheader("Read a File")
        st.markdown(
            f'<div class="file-list"><pre>{show_items()}</pre></div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        file_name = st.text_input("File name to read")
        if st.button("Read File"):
            if file_name:
                p = Path(file_name)
                if p.exists():
                    try:
                        st.code(p.read_text(), language="text")
                    except Exception as e:
                        msg(str(e), "error")
                else:
                    msg("⚠️ File not found!", "error")
            else:
                msg("Please enter a file name.", "error")

    # ── Update File ──
    elif operation == "✏️ Update File":
        st.subheader("Update a File")
        st.markdown(
            f'<div class="file-list"><pre>{show_items()}</pre></div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        file_name = st.text_input("File name to update")
        update_mode = st.radio("Update mode", ["Overwrite", "Append"])
        new_content = st.text_area("New content")
        if st.button("Update File"):
            if file_name:
                p = Path(file_name)
                if p.exists():
                    try:
                        mode = 'w' if update_mode == "Overwrite" else 'a'
                        with open(file_name, mode) as f:
                            f.write(new_content)
                        msg(f"✅ File '{file_name}' updated ({update_mode.lower()})!")
                    except Exception as e:
                        msg(str(e), "error")
                else:
                    msg("⚠️ File does not exist!", "error")
            else:
                msg("Please enter a file name.", "error")

    # ── Delete File ──
    elif operation == "🗑️ Delete File":
        st.subheader("Delete a File")
        st.markdown(
            f'<div class="file-list"><pre>{show_items()}</pre></div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        file_name = st.text_input("File name to delete")
        if st.button("Delete File", type="primary"):
            if file_name:
                p = Path(file_name)
                if p.exists():
                    try:
                        os.remove(p)
                        msg(f"✅ File '{file_name}' deleted!")
                    except Exception as e:
                        msg(str(e), "error")
                else:
                    msg("⚠️ File not found!", "error")
            else:
                msg("Please enter a file name.", "error")

    # ── Rename File ──
    elif operation == "🔤 Rename File":
        st.subheader("Rename a File")
        st.markdown(
            f'<div class="file-list"><pre>{show_items()}</pre></div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        file_name = st.text_input("Current file name")
        new_name = st.text_input("New file name")
        if st.button("Rename File"):
            if file_name and new_name:
                p = Path(file_name)
                if p.exists():
                    try:
                        p.rename(new_name)
                        msg(f"✅ Renamed '{file_name}' → '{new_name}'!")
                    except Exception as e:
                        msg(str(e), "error")
                else:
                    msg("⚠️ File not found!", "error")
            else:
                msg("Please fill in both fields.", "error")

    # ── Create Folder ──
    elif operation == "📁 Create Folder":
        st.subheader("Create a Folder")
        st.markdown(
            f'<div class="file-list"><pre>{show_items()}</pre></div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        folder_name = st.text_input("Folder name")
        if st.button("Create Folder"):
            if folder_name:
                p = Path(folder_name)
                if p.exists():
                    msg("⚠️ Folder already exists!", "error")
                else:
                    try:
                        p.mkdir()
                        msg(f"✅ Folder '{folder_name}' created!")
                    except Exception as e:
                        msg(str(e), "error")
            else:
                msg("Please enter a folder name.", "error")

    # ── Delete Folder ──
    elif operation == "❌ Delete Folder":
        st.subheader("Delete a Folder")
        st.markdown(
            f'<div class="file-list"><pre>{show_items()}</pre></div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        folder_name = st.text_input("Folder name to delete")
        if st.button("Delete Folder", type="primary"):
            if folder_name:
                p = Path(folder_name)
                if p.exists():
                    try:
                        p.rmdir()
                        msg(f"✅ Folder '{folder_name}' deleted!")
                    except Exception as e:
                        msg(str(e), "error")
                else:
                    msg("⚠️ Folder not found!", "error")
            else:
                msg("Please enter a folder name.", "error")

    # ── Create Folder + File ──
    elif operation == "📁➕ Create Folder + File":
        st.subheader("Create Folder and File Inside It")
        st.markdown(
            f'<div class="file-list"><pre>{show_items()}</pre></div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        folder_name = st.text_input("Folder name")
        file_name = st.text_input("File name inside folder")
        content = st.text_area("File content")
        if st.button("Create Folder + File"):
            if folder_name and file_name:
                try:
                    p = Path(folder_name)
                    if not p.exists():
                        p.mkdir()
                        msg(f"📁 Folder '{folder_name}' created!")
                    else:
                        msg(f"📁 Folder '{folder_name}' already exists, using it.")
                    file_path = p / file_name
                    file_path.write_text(content)
                    msg(f"✅ File '{file_name}' created inside '{folder_name}'!")
                except Exception as e:
                    msg(str(e), "error")
            else:
                msg("Please fill in both folder and file names.", "error")
