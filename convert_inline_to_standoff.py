import re
import os

def clean_inner_tags(content):
    """ removes all inner tags for BIBL tag. """
    return re.sub(r"<[^>]+>", "", content)

def extract_bibl_tags(text):
    """ extracts <BIBL> blocks without inner tags from the given text. """
    bibl_re = re.compile(r"(<BIBL>(.*?)</BIBL>)", re.DOTALL)
    results = []

    for bibl_match in bibl_re.finditer(text):
        bibl_content = bibl_match.group(2)

        # clean the BIBL content from inner tags for standalone BIBL entry
        clean_content = clean_inner_tags(bibl_content).strip()

        results.append(('BIBL', clean_content))

        # extract and append data for inner tags
        inner_tags = extract_inner_tags(bibl_content)
        results.extend(inner_tags)

    return results

def extract_inner_tags(content):
    """ extracts inner tags and their content within BIBL block. """
    tag_re = re.compile(r"<(\w+)>(.*?)</\1>", re.DOTALL)
    tag_data = []

    for match in tag_re.finditer(content):
        tag_name = match.group(1)
        tag_content = match.group(2).strip()
        tag_data.append((tag_name, tag_content))

    return tag_data

def process_file(input_path, output_path):
    """ processes a single file to extract <BIBL> tags and their inner tags, 
    writes the results in a standoff format to output file. """
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()

    tags_data = extract_bibl_tags(text)

    # write results to output file in specific standoff format
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(f"{entry[0]}: {entry[1]}\n" for entry in tags_data)

# process all .txt files in input directory, write outputs to output directory
def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        os.makedirs(output_dir, exist_ok=True)
    try:
        for filename in os.listdir(input_dir):
            if filename.endswith('.txt'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                process_file(input_path, output_path)
                print(f"Processed {filename}")
    except FileNotFoundError:
        print(f"Error: The directory '{input_dir}' does not exist.")
        return
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            process_file(input_path, output_path)
            print(f"Processed {filename}")

def main():
    input_dir = 'tests'
    output_dir = 'tests_standoff_tags'
    process_directory(input_dir, output_dir)

if __name__ == "__main__":
    main()


 