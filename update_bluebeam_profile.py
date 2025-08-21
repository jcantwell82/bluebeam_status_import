import os
from tkinter.filedialog import askopenfilename
from replace_xml_parent import replace_element_from_source
import yaml

# open the settings file to get the template file and update suffix
with open("settings.yaml", "r") as file:
    settings = yaml.safe_load(file)

# get the current user's login name for the initial directory
un = os.getlogin()

initial_dir = f"C:/Users/{un}/AppData/Roaming/Bluebeam Software/Revu/21"

# Prompt the user to select the target Bluebeam profile file
target_filename = askopenfilename(
    initialdir=initial_dir,
    title="Select the target Bluebeam profile",
    filetypes=[("BPX files", "*.bpx")]
)

output_filename = target_filename[:target_filename.rfind(".")] + settings['update_suffix'] + ".bpx"
source_filename = settings['template_file']
print("--- Running status replacement ---")

# Define the XPath selector.
xpath_selector = "./Record[@Key='StateModels']"

replace_element_from_source(
    input_file=target_filename,
    output_file=output_filename,
    xpath_to_replace=xpath_selector,
    source_file=source_filename,
    xpath_to_source=xpath_selector 
)