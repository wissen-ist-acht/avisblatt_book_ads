## Extraction of bibliographic entries from early modern newspaper advertisements

We are interested in the early modern book market in the Swiss city of Basel and would like to analyze book advertisements from a local newspaper, the [*Avisblatt*](https://avisblatt.philhist.unibas.ch/), which ran from 1729 to 1844. 
These ads often contain more than one bibliographic entry, with an entry usually (but not necessarily) consisting of author, book title, format, date and place of publication, price, and sometimes even more information:

![Avisblatt_1746-10-13](https://github.com/user-attachments/assets/9984b5a2-1c8f-43d6-bf54-b14f7d000381)

<sup> Wöchentliche Nachrichten aus dem Baslerischen Bericht-Haus (1746), issue 41, p. 1, 1746-10-13, ad id d7feab55-01a0-5dde-b35b-2cc1f65614bc/t7</sup>



To extract the bibliographic information, we want to identify both the entire bibliographic string as well as the containing information, such as:
```7. Bey Herrn Daniel Haag dem Buchbinder sind folgende Bücher zu verkauffen: 
<BIBL><AUTHOR>Moreri</AUTHOR> <TITLE>Dictionaire</TITLE>, <FORMAT>fol.</FORMAT> <VOLUME>6. Tom.</VOLUME> gantz neu in Frantzös. schem Band.</BIBL> 
<BIBL>Ein gantz neuer in roht Leder gebundener <TITLE>Atlas</TITLE> von 20. Homännischen Carten</BIBL> 
<BIBL><AUTHOR>Simlers</AUTHOR> <TITLE>Regiment Löbl. Eydgnoßschafft</TITLE>, in <FORMAT>4tò</FORMAT>.</BIBL> 
<BIBL><AUTHOR>Menantes</AUTHOR> <TITLE>Brieffsteller</TITLE>, <VOLUME>2. Tom</VOLUME>, <FORMAT>8vò</FORMAT>.</BIBL> 
<BIBL><AUTHOR>Kyburtzens</AUTHOR> abgekürtzte Kinder-Bibel, in <FORMAT>8vò</FORMAT>.</BIBL> 
<BIBL><TITLE>Alt und Nen Testament</TITLE>, mit und ohne Kupfer.</BIBL>
```

We are using LLMs to perform this task and compare the results.
For comparison, the output of the LLM is first converted from inline into standoff tagging, using [convert_inline_to_standoff.py](convert_inline_to_standoff.py). 
Then the comparison is performed in [compare_llms.py](compare_llms.py) by measuring the amount of matches between prediction and groundtruth, independent of the position in the text, to make up for uneven number of entries.
The results are stored in [model_comparison_results.txt](model_comparison_results.txt).

The prompt used for the LLM requests can be found in [LLM_NER_annotation_prompt.md](LLM_NER_annotation_prompt.md).

After evaluation, we chose Llama3.3:70b as model for the XML annotation of the whole data set. The results of the tagging are stored in results/data/all_bib_items_annotated.tsv.
We used a script to evaluate the correctness of the XML annotations, evaluate_tsv.py, and of the ~22 000 ads, around 2000 were recognized as malformed. These entries were again sent to a LLM, using the script [correction_of_malformed_xml_with_LLM.py](results/correction_of_results/correction_of_malformed_xml_with_LLM.py). The results are stored in [results/output/content](results/output/output) and [results/output/raw](results/output/raw). The corrected entries were then consolidated with the original data set, which can be found in [results/output](results/output) as csv and json file. 
