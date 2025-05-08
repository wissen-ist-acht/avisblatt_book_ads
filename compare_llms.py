import os

def read_tags(filename):
    """ reads a file containing key-value pairs for tags (BIBL, AUTHOR, etc) separated by ": " 
    and returns a dictionary where each key maps to a list of corresponding values. """
    tags_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            if ": " in line:
                key, value = line.split(": ", 1)
                if key in tags_dict:
                    tags_dict[key].append(value.strip())
                else:
                    tags_dict[key] = [value.strip()]
    return tags_dict

# check if a tag entry in the test file exists in the groundtruth, independent of position
# to make up for uneven number of entries, in case a test run did not identify every tag 
# as given in the groundtruth file
def compare_tags(ground_truth, predictions):
    """ compares two dictionaries of tags (ground truth and predictions) and calculates
    precision, recall, and F1 score based on their overlap. """
    total = correct = 0
    for key in ground_truth:
        if key in predictions:
            # count how many values are correctly matched, using intersections
            ground_set = set(ground_truth[key])
            pred_set = set(predictions[key])
            correct += len(ground_set.intersection(pred_set))
            total += len(ground_set)
        else:
            total += len(ground_truth[key])
    
    # account for any additional predictions that do not match
    for key in predictions:
        if key not in ground_truth:
            total += len(predictions[key])

    precision = correct / sum(len(v) for v in predictions.values()) if predictions else 0
    recall = correct / total if total else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0
    return precision, recall, f1

def main(ground_truth_file, prediction_files_dir):
    """ compares ground truth tags with prediction tags from multiple files and writes the results to a file."""
    ground_truth_tags = read_tags(ground_truth_file)
    
    with open(result_file, 'w') as f:
        for filename in os.listdir(prediction_files_dir):
            if filename.endswith('.txt'):
                prediction_tags = read_tags(os.path.join(prediction_files_dir, filename))
                precision, recall, f1 = compare_tags(ground_truth_tags, prediction_tags)
            
                result_str =  f"results for {filename}:\n" + \
                              f"precision: {precision:.4f}\n" + \
                              f"recall: {recall:.4f}\n" + \
                              f"f1 score: {f1:.4f}\n\n"
                
                print(result_str)
                
                f.write(result_str)


ground_truth_file = 'groundtruth/eval_set_small_standoff.txt'
prediction_files_dir = 'tests_standoff_tags'
result_file = 'model_comparison_results.txt'

if __name__ == "__main__":
    main(ground_truth_file, prediction_files_dir)


