"""
This module reformats the input and corrected data to one consolidated dataset in json.
This module has the possibility of creating CSV output from the consolidated data.

Ground data is in "all_bib_items_annotated" which is a TSV file
A subset of values from this file is in "incorrect_tags.txt". They refer to a certain line in the ground data.
For each line in the subset, a LLM-generated correction was saved in the form "line_X.json"
"""

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Any


def load_ground_data(tsv_path: str) -> List[Dict[str, Any]]:
    """
    Load ground data from TSV file.

    Args:
        tsv_path: Path to the all_bib_items_annotated.tsv file

    Returns:
        List of dictionaries containing the ground data
    """
    ground_data = []
    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            ground_data.append(row)
    return ground_data


def normalize_xml(xml_string: str) -> str:
    """
    Normalize XML string for comparison by removing extra whitespace.

    Args:
        xml_string: XML string to normalize

    Returns:
        Normalized XML string
    """
    # Strip leading/trailing whitespace and normalize internal whitespace
    return ' '.join(xml_string.split())


def load_faulty_lines(faulty_lines_path: str) -> List[str]:
    """
    Load faulty XML lines from the subset file.

    Args:
        faulty_lines_path: Path to the incorrect_tags.txt file

    Returns:
        List of faulty XML strings
    """
    with open(faulty_lines_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def load_correction(correction_file: str) -> Optional[Dict[str, Any]]:
    """
    Load correction data from a line_X.json file.

    Args:
        correction_file: Path to the correction JSON file

    Returns:
        Dictionary containing fixed_xml, number_of_fixes, and explanation
    """
    try:
        with open(correction_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return None
            return json.loads(content)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON in {correction_file}: {e}")
        return None
    except Exception as e:
        print(f"Warning: Error reading {correction_file}: {e}")
        return None


def xml_to_json_lowercase(xml_string: str) -> Optional[Dict[str, Any]]:
    """
    Parse XML string and convert to JSON with lowercase keys.

    Args:
        xml_string: XML string to parse

    Returns:
        Dictionary representation of XML with lowercase keys
    """
    try:
        root = ET.fromstring(xml_string)
        return _element_to_dict_lowercase(root)
    except ET.ParseError as e:
        return {"error": f"Failed to parse XML: {str(e)}"}


def _element_to_dict_lowercase(element: ET.Element) -> Dict[str, Any]:
    """
    Convert XML element to dictionary with lowercase keys (recursive helper).

    Args:
        element: XML Element to convert

    Returns:
        Nested dictionary with tag: value/nested_dict structure
    """
    tag = element.tag.lower()

    # If element has children, create nested structure
    if len(element) > 0:
        children_dict = {}
        for child in element:
            child_tag = child.tag.lower()
            child_data = _element_to_dict_lowercase(child)

            # If tag already exists, convert to list or append to list
            if child_tag in children_dict:
                if not isinstance(children_dict[child_tag], list):
                    children_dict[child_tag] = [children_dict[child_tag]]
                children_dict[child_tag].append(child_data[child_tag])
            else:
                children_dict[child_tag] = child_data[child_tag]

        return {tag: children_dict}
    else:
        # Leaf element - just return tag: text
        text = element.text.strip() if element.text else ""
        return {tag: text}



def create_consolidated_dataset(
    tsv_path: str,
    faulty_lines_path: str,
    corrections_dir: str
) -> List[Dict[str, Any]]:
    """
    Create consolidated dataset combining ground data with corrections.

    Args:
        tsv_path: Path to the all_bib_items_annotated.tsv file
        faulty_lines_path: Path to the incorrect_tags.txt file
        corrections_dir: Directory containing line_X.json correction files

    Returns:
        List of consolidated data records
    """
    # Load all data
    ground_data = load_ground_data(tsv_path)
    faulty_lines = load_faulty_lines(faulty_lines_path)

    # Get XML column name
    columns = list(ground_data[0].keys()) if ground_data else []
    xml_column = columns[1] if len(columns) > 1 else None

    if not xml_column:
        raise ValueError("Could not determine XML column in ground data")

    # Extract faulty records from ground data (in order)
    faulty_ground_records = []
    for record in ground_data:
        if record.get("quality_xml_well_formed", "").upper() == "FALSE":
            faulty_ground_records.append(record)

    print(f"Found {len(faulty_ground_records)} faulty records in ground data")
    print(f"Found {len(faulty_lines)} lines in incorrect_tags.txt")

    # Create position-based mapping: Nth faulty record -> line N in incorrect_tags.txt
    faulty_record_to_line = {}
    for idx, record in enumerate(faulty_ground_records):
        record_id = record.get("id", "")
        faulty_record_to_line[record_id] = idx + 1  # Line numbers start at 1

    consolidated = []

    for record in ground_data:
        original_xml = record[xml_column]

        # Check if line is faulty based on quality_xml_well_formed column
        is_faulty = record.get("quality_xml_well_formed", "").upper() == "FALSE"

        # Create base entry
        entry = {
            "id": record.get("id", ""),
            "original_xml": original_xml,
            "is_faulty": is_faulty,
            "has_correction": False,
            "corrected_xml": None,
            "number_of_fixes": 0,
            "fix_explanation": None,
            "json_representation": None,
            "metadata": {k: v for k, v in record.items() if k not in ['id', xml_column]}
        }

        # If faulty, look up the correction by position
        if is_faulty:
            record_id = record.get("id", "")
            if record_id in faulty_record_to_line:
                line_number = faulty_record_to_line[record_id]
                correction_file = Path(corrections_dir) / f"line_{line_number}.json"

                correction = load_correction(str(correction_file))
                if correction:
                    entry["has_correction"] = True
                    entry["corrected_xml"] = correction.get("fixed_xml")
                    entry["number_of_fixes"] = correction.get("number_of_fixes", 0)
                    entry["fix_explanation"] = correction.get("explanation")

                    # Create JSON representation of corrected XML
                    if entry["corrected_xml"]:
                        entry["json_representation"] = xml_to_json_lowercase(entry["corrected_xml"])

        # For non-faulty lines or faulty lines without corrections,
        # try to create JSON representation from original (may fail for faulty ones)
        if entry["json_representation"] is None:
            entry["json_representation"] = xml_to_json_lowercase(original_xml)

        consolidated.append(entry)

    return consolidated


def save_consolidated_json(consolidated_data: List[Dict[str, Any]], output_path: str):
    """
    Save consolidated dataset to JSON file.

    Args:
        consolidated_data: List of consolidated records
        output_path: Path to output JSON file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(consolidated_data, f, indent=2, ensure_ascii=False)


def save_consolidated_csv(consolidated_data: List[Dict[str, Any]], output_path: str):
    """
    Save consolidated dataset to CSV file (flattened).

    Args:
        consolidated_data: List of consolidated records
        output_path: Path to output CSV file
    """
    if not consolidated_data:
        return

    # Flatten the data for CSV
    flattened = []
    for record in consolidated_data:
        flat_record = {
            "id": record["id"],
            "original_xml": record["original_xml"],
            "is_faulty": record["is_faulty"],
            "has_correction": record.get("has_correction", False),
            "corrected_xml": record["corrected_xml"] or "",
            "number_of_fixes": record["number_of_fixes"],
            "fix_explanation": record["fix_explanation"] or "",
        }
        flattened.append(flat_record)

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ["id", "original_xml", "is_faulty", "has_correction", "corrected_xml", "number_of_fixes", "fix_explanation"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened)


def main():
    """
    Main function to run the consolidation process.
    """
    # Define paths
    tsv_path = "data/all_bib_items_annotated.tsv"
    faulty_lines_path = "data/incorrect_tags.txt"
    corrections_dir = "output/content"
    output_json_path = "output/consolidated_data.json"
    output_csv_path = "output/consolidated_data.csv"

    print("Starting data consolidation...")

    # Load faulty lines to report stats
    with open(faulty_lines_path, 'r', encoding='utf-8') as f:
        faulty_lines_count = len([line for line in f if line.strip()])

    print(f"Found {faulty_lines_count} lines in {faulty_lines_path}")

    # Create consolidated dataset
    consolidated = create_consolidated_dataset(tsv_path, faulty_lines_path, corrections_dir)

    print(f"\n=== Summary ===")
    print(f"Total records processed: {len(consolidated)}")
    faulty_count = sum(1 for r in consolidated if r["is_faulty"])
    corrected_count = sum(1 for r in consolidated if r.get("has_correction", False))
    print(f"Faulty records (quality_xml_well_formed=FALSE): {faulty_count}")
    print(f"Faulty records with valid LLM corrections: {corrected_count}")
    print(f"Faulty records without corrections: {faulty_count - corrected_count}")

    if corrected_count < faulty_lines_count:
        missing = faulty_lines_count - corrected_count
        print(f"Note: {missing} correction files were missing or had invalid JSON")

    # Save outputs
    save_consolidated_json(consolidated, output_json_path)
    print(f"Saved JSON output to: {output_json_path}")

    save_consolidated_csv(consolidated, output_csv_path)
    print(f"Saved CSV output to: {output_csv_path}")

    print("Consolidation complete!")


if __name__ == "__main__":
    main()