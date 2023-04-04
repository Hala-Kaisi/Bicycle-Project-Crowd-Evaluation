import pandas as pd
import storage
import statistics
from collections import Counter

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

num = 0
def check_data(references_frames, tasks_frames):
    ref = references_frames
    tasks = tasks_frames

    ref_missing_values = ref.isna().sum()
    tasks_missing_values = tasks.isna().sum()
    ref_missing_columns = ref_missing_values[ref_missing_values > 0]
    tasks_missing_columns = tasks_missing_values[tasks_missing_values > 0]

    print("\nMissing values in the JSON files:\n")
    if ref_missing_columns.empty:
        print("No missing values found in reference.json")
    else:
        print("Missing values found in the following columns:")
        #print(ref_missing_columns)

    if tasks_missing_columns.empty:
        print("No missing values found in anonymized_project.json")
    else:
        print("Missing values found in the following columns:")
        #print(tasks_missing_columns)

    return ref_missing_columns.empty, tasks_missing_columns.empty


def get_no_annonators(tasks_frames):
    tasks = tasks_frames
    annotators_no = set()

    for index, row in tasks.iterrows():
        for i in range(len(row['results'])):
            annotators_no.add(row['results'][i]['user']["vendor_user_id"])

    return len(annotators_no)


def calculate_annotation_durations(tasks_frames):
    tasks = tasks_frames
    durations = []

    for index, row in tasks.iterrows():
        for i in range(len(row['results'])):
            time = row['results'][i]['task_output']['duration_ms']/1000
            if time > 0:
                durations.append(time)

    mean_time = statistics.mean(durations)
    durations.sort()
    min_time = durations[0]
    max_time = durations[-1]

    storage.save_annotation_durations(mean_time, min_time, max_time)

def compare_annotator_results(tasks_frames):

    num_annotations = 0
    tasks = tasks_frames
    annotataros_results = {}

    for index, row in tasks.iterrows():
        for i in range(len(row['results'])):
            id = row['results'][i]['user']["vendor_user_id"]
            if id not in annotataros_results:
                annotataros_results[id] = 0
            annotataros_results[id] += 1
            num_annotations += 1

    storage.save_annotator_results(annotataros_results)


def calculate_kappa_coefficient(tasks_frames):

    tasks = tasks_frames
    question_counts = {}
    question_responses = []
    iaa = {}

    for index, row in tasks.iterrows():
        for i in range(len(row['results'])):
            task_id = i
            annotator_id = row['results'][i]['user']['vendor_user_id']
            answer = row['results'][i]['task_output']['answer']
            question_responses.append(
                {'question_id': task_id, 'annotator_id': annotator_id, 'answer': answer})

    question_responses_df = pd.DataFrame(question_responses, columns=['question_id', 'annotator_id', 'answer'])

    for question_id, responses in question_responses_df.groupby('question_id'):
        counts = Counter(responses['answer'])
        question_counts[question_id] = {'yes': counts.get('yes', 0) / len(responses),
                                        'no': counts.get('no', 0) / len(responses)}

    for question_id, counts in question_counts.items():
        poa = counts.get('yes', 0) * counts.get('no', 0) + (1 - counts.get('yes', 0)) * (1 - counts.get('no', 0))
        iaa[question_id] = poa

    storage.save_kappa_coefficient(iaa)


def analyze_extra_outputs(tasks_frames):

    tasks = tasks_frames

    cant_solve_overall_count = 0
    corrupt_data_overall_count = 0
    annotator_frequency = {}


    for i, row in tasks.iterrows():
        for j in range(len(row['results'])):
            annotator_id = row['results'][j]['user']['vendor_user_id']
            cant_solve_count = 0
            corrupt_data_count = 0
            task_output = row['results'][j]['task_output']
            if task_output['cant_solve']:
                cant_solve_count += 1
                cant_solve_overall_count += 1
            elif task_output['corrupt_data']:
                corrupt_data_count += 1
                corrupt_data_overall_count += 1
            if annotator_id in annotator_frequency:
                annotator_frequency[annotator_id]['cant_solve_count'] += cant_solve_count
                annotator_frequency[annotator_id]['corrupt_data_count'] += corrupt_data_count
            else:
                annotator_frequency[annotator_id] = {'cant_solve_count': cant_solve_count,
                                                     'corrupt_data_count': corrupt_data_count}

    storage.save_extra_outputs(cant_solve_overall_count, corrupt_data_overall_count, annotator_frequency)

def analyze_ref(reference_frames):

    ref = reference_frames

    labels = []

    for i, row in ref.iterrows():
        labels.append(row['is_bicycle'])

    n_positive = labels.count(True)
    n_negative = labels.count(False)

    storage.save_ref_data(n_positive, n_negative)

def check_annotator_accuracy(tasks_frames, reference_frames):

    tasks = tasks_frames
    ref = reference_frames

    annotator_accuracy = {}
    overall_correct_answers = 0

    for annotator_id, annotator_data in tasks.groupby('annotator_id'):
        correct_answers = 0
        total_answers = 0
        for i, row in annotator_data.iterrows():
            image_id = row['image_id']
            answer = row['answer']
            if answer == "no":
                answer = False
            elif answer == "yes":
                answer = True
            else:
                total_answers += 1
                continue
            if ref.loc[image_id]['is_bicycle'] == answer:
                correct_answers += 1
                overall_correct_answers += 1
            total_answers += 1
        accuracy = correct_answers / total_answers
        annotator_accuracy[annotator_id] = accuracy

    overall_accuracy = overall_correct_answers / len(tasks)

    good_annotators = []
    bad_annotators = []
    for annotator_id, accuracy in annotator_accuracy.items():
        if accuracy >= overall_accuracy:
            good_annotators.append(annotator_id)
        else:
            bad_annotators.append(annotator_id)


    storage.save_annotator_accuracy(annotator_accuracy, overall_accuracy, good_annotators, bad_annotators)
