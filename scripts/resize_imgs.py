import xml.etree.ElementTree as ET
import json
import argparse
import os

def process_xml(library_file, max_width, max_height):
    # Parse the XML file
    tree = ET.parse(library_file)
    root = tree.getroot()

    # Extract and parse the JSON content
    json_data = json.loads(root.text)

    # Process each item
    for item in json_data:
        original_width = item["w"]
        original_height = item["h"]

        # First, attempt to resize based on max height
        height_scale_factor = max_height / original_height
        new_width = original_width * height_scale_factor

        if new_width <= max_width:
            # If resized width is within limits, finalize this resizing
            new_height = max_height
            item["w"] = format(round(new_width, 2), '.2f').rstrip('0').rstrip('.')
            item["h"] = format(round(new_height, 2), '.2f').rstrip('0').rstrip('.')
        else:
            # Otherwise, scale based on max width
            width_scale_factor = max_width / original_width
            new_width = max_width
            new_height = original_height * width_scale_factor
            item["w"] = format(round(new_width, 2), '.2f').rstrip('0').rstrip('.')
            item["h"] = format(round(new_height, 2), '.2f').rstrip('0').rstrip('.')

    # Convert the modified JSON back to a string with 2-space indentation
    root.text = json.dumps(json_data, indent=2)

    # Generate the output file name
    base, ext = os.path.splitext(library_file)
    output_file = f"{base}_resized{ext}"

    # Save the results to a new XML file without XML declaration
    tree.write(output_file, encoding='utf-8', xml_declaration=False)

    print(f"Processed XML saved to {output_file}")

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Process and resize XML data.')
    parser.add_argument('library_file', help='Path to the library XML file')
    parser.add_argument('--max_width', type=int, default=150, help='Max width')
    parser.add_argument('--max_height', type=int, default=50, help='Max height')

    # Parse command-line arguments
    args = parser.parse_args()

    # Process the XML file with specified max width and height
    process_xml(args.library_file, args.max_width, args.max_height)

if __name__ == "__main__":
    main()
