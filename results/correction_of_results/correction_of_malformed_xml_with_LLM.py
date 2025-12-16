import json
import os

from ai_client import create_ai_client
from decouple import config

INPUT_DIR = "data"
OUTPUT_DIR = "output"

client = create_ai_client(provider="openai", api_key=config("OPENAI_API_KEY"))

prompt = "Fix this xml. Add xml-tags if faulty where it makes sense. Format your response as JSON. Use the keys 'fixed_xml', 'number_of_fixes', 'explanation'."

with(open(os.path.join(INPUT_DIR, "incorrect_tags.txt"), "r", encoding="utf-8")) as f:
    xmls = f.readlines()
lines = len(xmls)
print("Opened input file with", lines, "lines.")

os.makedirs(os.path.join(OUTPUT_DIR, "raw"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "content"), exist_ok=True)

line = 1
print("Starting processing...")
for xml in xmls:
    filename = f"line_{line}.json"
    if os.path.exists(os.path.join(OUTPUT_DIR, "raw", filename)) and\
            os.path.exists(os.path.join(OUTPUT_DIR, "content", filename)):
        print(f"Skipping line {line} of {lines}, already processed.")
        line += 1
        continue

    print("Processing", xml)
    response, duration = client.prompt("gpt-4", f"{prompt}\n{xml}")
    with(open(os.path.join(OUTPUT_DIR, "raw", filename), "w", encoding="utf-8")) as f_out:
        json.dump(response.to_dict(), f_out,
                  indent=4, ensure_ascii=False)

    with(open(os.path.join(OUTPUT_DIR, "content", filename), "w", encoding="utf-8")) as f_out:
        json_text_response = response.text
        json.dump(json.loads(json_text_response), f_out,
                  indent=4, ensure_ascii=False)

    print(f"Processed line {line} of {lines}")
    line += 1