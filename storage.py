import json

def save_data(data):

    with open('analysis_results.json', 'r') as f:
        file_data = json.load(f)

    file_data.update(data)

    with open('analysis_results.json', 'w') as f:
        json.dump(file_data, f)

def save_annotator_count(num_annotators):

    data = {'num_annotators': num_annotators}
    save_data(data)

def save_annotation_durations(mean_time, min_time, max_time, durations):

    data = {'mean_time': mean_time, 'min_time': min_time, 'max_time': max_time, 'durations': durations}
    save_data(data)

def save_annotator_results(annotator_results):

    data = {'annotator_results': annotator_results}
    save_data(data)

def save_kappa_coefficient(iaa):

    data = {'iaa': iaa}
    save_data(data)

def save_extra_outputs(cant_solve_count, corrupt_data_count, annotator_frequency):

    data = {'cant_solve_count': cant_solve_count, 'corrupt_data_count': corrupt_data_count, 'annotator_frequency': annotator_frequency}
    save_data(data)

def save_ref_data(n_positive, n_negative):

    data = {'n_positive': n_positive, 'n_negative': n_negative}
    save_data(data)

def save_annotator_accuracy(annotator_accuracy, overall_accuracy, good_annotators, bad_annotators):

    data = {'annotator_accuracy': annotator_accuracy, 'overall_accuracy': overall_accuracy, 'good_annotators': good_annotators, 'bad_annotators': bad_annotators}
    save_data(data)