import import_data as data
import analysis
import report


def main():
    references, tasks = data.load_data("data_input/references.json", "data_input/anonymized_project.json")

    missing_ref, missing_tasks = analysis.check_data(references, tasks)
    cleanedup_tasks = data.cleanup_tasks(tasks)

    if not missing_ref:
        print("\n!!! Missing values found in the reference JSON file. Please check the data.!!!")
        exit()

    if not missing_tasks:
        print("\n!!! Missing values found in the anonymized_project JSON file. Please check the data.!!!")
        exit()

    analysis.get_no_annonators(tasks)

    analysis.calculate_annotation_durations(tasks)

    analysis.compare_annotator_results(tasks)

    analysis.analyze_extra_outputs(tasks)

    analysis.analyze_ref(references)

    analysis.check_annotator_accuracy(cleanedup_tasks, references)

    analysis.calculate_kappa_coefficient(tasks)

    report.generate_report('analysis_results.json')


if __name__ == "__main__":

    main()

