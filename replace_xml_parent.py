import xml.etree.ElementTree as ET


def replace_element_from_source(input_file, output_file, xpath_to_replace, source_file, xpath_to_source):
    """
    Replaces an element in a target XML file with a specific element
    found in a source XML file that shares a similar structure.

    Args:
        input_file (str): Path to the target XML file to be modified.
        output_file (str): Path to save the modified XML file.
        xpath_to_replace (str): XPath to find the element to replace in the input_file.
        source_file (str): Path to the source XML file containing the new data.
        xpath_to_source (str): XPath to find the element to use as the replacement in the source_file.
    """
    try:
        # 1. Parse both the target and source XML files
        target_tree = ET.parse(input_file)
        target_root = target_tree.getroot()
        
        source_tree = ET.parse(source_file)
        source_root = source_tree.getroot()

        # 2. Find the new element from the source file using its specific XPath
        new_element = source_root.find(xpath_to_replace)
        if new_element is None:
            print(f"❌ Error: Source element not found in '{source_file}' with XPath '{xpath_to_source}'")
            return

        # 3. Find the old element in the target file that will be replaced
        element_to_replace = target_root.find(xpath_to_replace)
        if element_to_replace is None:
            print(f"❌ Error: Target element not found in '{input_file}' with XPath '{xpath_to_replace}'")
            return

        # 4. Find the parent of the element to be replaced to perform the swap
        parent_map = {c: p for p in target_root.iter() for c in p}
        parent = parent_map.get(element_to_replace)

        # Determine the tree to write later (handles root replacement)
        if parent is None:
            tree_to_write = ET.ElementTree(new_element)
            print("ℹ️ Note: The root element was replaced.")
        else:
            # Replace a child element
            children = list(parent)
            index = children.index(element_to_replace)
            parent.remove(element_to_replace)
            parent.insert(index, new_element)
            tree_to_write = target_tree

        # 5. Format and write the modified tree to the output file
        try:
            ET.indent(tree_to_write, space="  ", level=0)
        except AttributeError:
            pass

        tree_to_write.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"✅ Successfully updated '{xpath_to_replace}' from source and saved to '{output_file}'")

    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e.filename}")
    except ET.ParseError as e:
        print(f"❌ Error parsing XML file: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    import os
    from tkinter.filedialog import askopenfilename
    un = os.getlogin()
    print(un)
    initial_dir = f"C:/Users/{un}/AppData/Roaming/Bluebeam Software/Revu/21"
    target_filename = askopenfilename(
        initialdir=initial_dir,
        title="Select the target Bluebeam profile",
        filetypes=[("BPX files", "*.bpx")]
    )
    output_filename = target_filename[:target_filename.rfind(".")] + "-BurnsQAQC.bpx"

    source_filename = askopenfilename(
        title="Select the template profile for status",
        filetypes=[("BPX files", "*.bpx")]
    )
    print("--- Running status replacement ---")
    
    # Define the XPath selector.
    # In this common use case, we use the same XPath to find the desired
    # element in both the target file and the source file.
    xpath_selector = "./Record[@Key='StateModels']"
    
    # 4. Call the function
    replace_element_from_source(
        input_file=target_filename,
        output_file=output_filename,
        xpath_to_replace=xpath_selector,
        source_file=source_filename,
        xpath_to_source=xpath_selector 
    )