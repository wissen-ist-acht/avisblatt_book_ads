import csv
from xml.etree import ElementTree as ET
from collections import Counter
import io
import os
import re

def escape_xml_text(text: str) -> str:
    """
    escape reserved XML characters (&, <, >) found in text content,
    while trying to preserve the actual XML tags.
    """
    # Escape ampersands
    text = text.replace('&', '&amp;')
    # Add more if necessary
    return text


def check_overlapping_tags(xml_string):
    """
    Checks for overlapping tags in an XML string.
    """
    tags = []
    last_pos = 0
    for i, char in enumerate(xml_string):
        if char == '<':
            if i + 1 < len(xml_string) and xml_string[i+1] != '/':
                end = xml_string.find('>', i)
                if end != -1:
                    tag = xml_string[i+1:end].split()[0]
                    tags.append((tag, i))
            elif i + 1 < len(xml_string) and xml_string[i+1] == '/':
                end = xml_string.find('>', i)
                if end != -1:
                    closing_tag = xml_string[i+2:end]
                    if not tags or tags[-1][0] != closing_tag:
                        return True
                    tags.pop()
    return not not tags # Returns True if there are unclosed tags at the end

def analyze_annotations(xml_string: str):
    """
    Performs an analysis of the inline XML annotations.

    Args:
        xml_string: The string containing the annotated text.

    Returns:
        A dictionary with the analysis results.
    """
    analysis = {
        "xml_well_formed": False,
        "error_message": None,
        "has_overlapping_tags": True,
        "tags_used": [],
        "tag_counts": {},
    }

    safe_xml_string = escape_xml_text(xml_string)
    wrapped_xml = f"<root>{safe_xml_string}</root>"

    try:
        root = ET.fromstring(wrapped_xml)
        analysis["xml_well_formed"] = True
        
        analysis["has_overlapping_tags"] = check_overlapping_tags(xml_string)

        all_tags = [elem.tag for elem in root.iter() if elem.tag != 'root']
        analysis["tags_used"] = sorted(list(set(all_tags)))
        analysis["tag_counts"] = dict(Counter(all_tags))

    except ET.ParseError as e:
        analysis["error_message"] = str(e)

    return analysis

def process_tsv(input_filepath, output_filepath):
    """
    Reads TSV file, analyzes the annotations in one column,
    and writes the results to a new TSV file with additional columns.
    """
    print(f"Starting analysis of {input_filepath}...")

    with open(input_filepath, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter='\t')
            
        try:
            header = next(reader)
        except StopIteration:
            print("ERROR: The input file is empty.")
            return

        # Assuming the annotation string is in the second column
        annotation_col_index = 1 

        new_header = header + [
            "quality_xml_well_formed",
            "quality_error_message",
            "quality_has_overlapping_tags",
            "quality_tags_used",
            "quality_tag_counts",
            "quality_summary"
        ]

        processed_rows = []
        for i, row in enumerate(reader):
            if len(row) > annotation_col_index:
                doc_id = row[0]
                annotation_string = row[annotation_col_index]
                
                print(f"  Processing row {i+1} (ID: {doc_id})...")

                analysis_results = analyze_annotations(annotation_string)

                summary = "OK"
                if not analysis_results["xml_well_formed"]:
                    summary = f"XML_ERROR: {analysis_results['error_message']}"
                elif analysis_results["has_overlapping_tags"]:
                    summary = "Overlapping tags detected"
                
                new_row = row + [
                    analysis_results["xml_well_formed"],
                    analysis_results["error_message"],
                    analysis_results["has_overlapping_tags"],
                    ", ".join(analysis_results["tags_used"]),
                    str(analysis_results["tag_counts"]),
                    summary
                ]
                processed_rows.append(new_row)

    with open(output_filepath, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerow(new_header)
        writer.writerows(processed_rows)

    print(f"\nAnalysis complete. Results saved to {output_filepath}")


if __name__ == '__main__':
    INPUT_TSV_FILE = os.path.join("output", "annotated_output_llama3.tsv")
    OUTPUT_TSV_FILE = os.path.join("output", "annotated_output_llama3_evaluated.tsv")
    
    try:
        process_tsv(INPUT_TSV_FILE, OUTPUT_TSV_FILE)
    except FileNotFoundError:
        print(f"\nERROR: The input file was not found at '{INPUT_TSV_FILE}'")
        print("Please update the INPUT_TSV_FILE variable in the script.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")