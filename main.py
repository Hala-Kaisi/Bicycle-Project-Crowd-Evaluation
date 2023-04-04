import data
import analysis
import report


def main():
    print("running main")


if __name__ == "__main__":

    references, tasks = data.load_data("data_input/references.json", "data_input/anonymized_project.json")

    missing_ref, missing_tasks = analysis.check_data(references, tasks)

    if not missing_ref:
        print("\n!!! Missing values found in the reference JSON file. Please check the data.!!!")
        exit()

    if not missing_tasks:
        print("\n!!! Missing values found in the anonymized_project JSON file. Please check the data.!!!")
        exit()

    annotators_no = analysis.get_no_annonators(tasks)

    print("\nNumber of annotators: ", annotators_no)

    mean_time, min_time, max_time = analysis.calculate_annotation_durations(tasks)

    print("\nAnnotation durations:\n")
    print("Mean time: ", mean_time)
    print("Min time: ", min_time)
    print("Max time: ", max_time)

    annotators_results = analysis.compare_annotator_results(tasks)

    print("\nAnnotators results:\n")
    print(annotators_results)

    cant_solve_count, corrupt_data_count, annotator_frequency = analysis.analyze_extra_outputs(tasks)

    print("\nExtra outputs:\n")
    print("Number of tasks that could not be solved: ", cant_solve_count)
    print("Number of tasks with corrupt data: ", corrupt_data_count)
    for annotator in annotator_frequency:
        print(
            f"Annotator {annotator} used 'cant_solve' {annotator_frequency[annotator]['cant_solve_count']} times and 'corrupt_data' {annotator_frequency[annotator]['corrupt_data_count']} times")

    positive_labels, negative_labels = analysis.analyze_ref(references)

    cleanedup_tasks = data.cleanup_tasks(tasks)

    annotator_accuracy, overall_accuracy, good_annotators, bad_annotators = analysis.check_annotator_accuracy(cleanedup_tasks, references)

    print("\nAnnotator accuracy:\n")

    print("Overall accuracy: ", overall_accuracy)
    for annotator in annotator_accuracy:
        print(f"Annotator {annotator} accuracy: {annotator_accuracy[annotator]}")

    print("\nGood annotators:\n")
    for annotator in good_annotators:
        print(f"Annotator {annotator} accuracy: {annotator_accuracy[annotator]}")

    print("\nBad annotators:\n")
    for annotator in bad_annotators:
        print(f"Annotator {annotator} accuracy: {annotator_accuracy[annotator]}")


    iaa = analysis.calculate_kappa_coefficient(tasks)

    print("\nKappa coefficient:\n")
    for i, poa in iaa.items():
        print("Question " + str(i) + " has a probability of agreement of " + str(poa))