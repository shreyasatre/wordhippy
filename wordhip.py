import requests
import dearpygui.dearpygui as dpg
from bs4 import BeautifulSoup

def search_word(word):

    word = word.replace(" ", "_")

    page = requests.get(f"https://www.wordhippo.com/what-is/another-word-for/{word}.html")
    soup = BeautifulSoup(page.content, 'html.parser')

    synonyms = [
        a.getText() for a in soup.select_one('div.relatedwords').find_all("a")
    ]

    page = requests.get(f"https://www.wordhippo.com/what-is/the-opposite-of/{word}.html")
    soup = BeautifulSoup(page.content, 'html.parser')

    antonyms = [
        a.getText() for a in soup.select_one('div.relatedwords').find_all("a")
    ]

    return synonyms, antonyms

# Callback function for searching.
def search_callback():
    dpg.set_value("SynonymsValues", "")
    dpg.set_value("AntonymsValues", "")

    dpg.configure_item(item="SynonymsLoading", show=True)
    dpg.configure_item(item="AntonymsLoading", show=True)
    
    synonyms, antonyms = search_word(dpg.get_value("InputWord"))

    dpg.set_value("SynonymsValues", ", ".join(synonyms))
    dpg.set_value("AntonymsValues", ", ".join(antonyms))

    dpg.configure_item(item="SynonymsLoading", show=False)
    dpg.configure_item(item="AntonymsLoading", show=False)
    dpg.focus_item("InputWord")


# Sets up DearPyGUI layout.
def setup():
    dpg.create_context()
    dpg.create_viewport(title='WordHippy', min_height=600, min_width=500, max_height=600, max_width=500, resizable=False)
    dpg.setup_dearpygui()

    with dpg.window(label="WordHippy", tag="WordHippyPrimaryWindow"):
        dpg.add_text("WordHippo Clone")
        dpg.add_separator()
        dpg.add_spacer(height=3)

        with dpg.handler_registry(tag="__demo_keyboard_handler"):  
            dpg.add_key_press_handler(tag="EnterKeyHandler", key=dpg.mvKey_Return, callback=search_callback)

        with dpg.group(horizontal=True):
            dpg.add_input_text(tag="InputWord", width=410)
            dpg.focus_item("InputWord")
            dpg.add_button(label="Search", callback=search_callback)

        dpg.add_spacer(height=3)
        dpg.add_text("Synonyms")
        synonyms_window = dpg.generate_uuid()
        with dpg.child_window(tag=synonyms_window, autosize_x=True, height=200):
            dpg.add_text(tag="SynonymsValues", default_value="", wrap=400)
            dpg.add_loading_indicator(tag="SynonymsLoading", style=1, indent=200, radius=5, pos=[100, 75], show=False)
        
        dpg.add_spacer(height=3)
        dpg.add_text("Antonyms")
        antonyms_window = dpg.generate_uuid()
        with dpg.child_window(tag=antonyms_window, autosize_x=True, height=200):
            dpg.add_text(tag="AntonymsValues", default_value="", wrap=400)
            dpg.add_loading_indicator(tag="AntonymsLoading", style=1, indent=200, radius=5, pos=[100, 75], show=False)

    dpg.show_viewport()
    dpg.set_primary_window("WordHippyPrimaryWindow", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
# ---

# Main.
def main():
    setup()
# ---

# Main program starts.
if __name__ == "__main__":
    main()
# ===