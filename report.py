import matplotlib.pyplot as plt
import import_data


def visualize_annotation_durations(mean_time, min_time, max_time, output_file):
    fig, ax = plt.subplots()
    ax.bar(['Mean Time', 'Minimum Time', 'Maximum Time'], [mean_time, min_time, max_time])
    ax.set_xlabel('Time')
    ax.set_ylabel('Duration (seconds)')
    ax.set_title('Annotation Durations')
    plt.savefig('annotation_durations.png')


def visualize_annotator_results(annotator_results, output_file):
    fig, ax = plt.subplots()
    ax.bar(annotator_results.keys(), annotator_results.values())
    ax.set_xlabel('Annotator IDs')
    ax.set_ylabel('Number of Annotations')
    ax.set_title('Annotator Results')
    plt.savefig('annotator_results.png')


def visualize_kappa_coefficient(iaa, output_file):
    fig, ax = plt.subplots()
    ax.bar(iaa.keys(), iaa.values())
    ax.set_xlabel('Question IDs')
    ax.set_ylabel('Probability of Agreement')
    ax.set_title('Kappa Coefficient')
    plt.savefig('kappa_coefficient.png')
    plt.close()


def visualize_extra_outputs(cant_solve_overall_count, corrupt_data_overall_count, annotator_frequency, output_file):
    fig, ax = plt.subplots()
    ax.bar(['Cannot Solve', 'Corrupt Data'], [cant_solve_overall_count, corrupt_data_overall_count])
    ax.set_xlabel('Type of Issue')
    ax.set_ylabel('Number of Annotations')
    ax.set_title('Frequency of "Cannot Solve" and "Corrupt Data"')
    plt.savefig('extra_outputs.png')


def visualize_ref(n_positive, n_negative, output_file):
    fig, ax = plt.subplots()
    ax.bar(['Bicycles', 'Non-bicycles'], [n_positive, n_negative])
    ax.set_xlabel('Labels')
    ax.set_ylabel('Number of Images')
    ax.set_title('Reference Set Balance')
    plt.savefig('ref_balance.png')


def visualize_annotator_accuracy(annotator_accuracy, overall_accuracy, good_annotators, bad_annotators, output_file):
    fig, ax = plt.subplots()
    x = list(annotator_accuracy.keys())
    y = list(annotator_accuracy.values())
    ax.scatter(x, y)
    ax.set_xlabel('Annotator IDs')
    ax.set_ylabel('Accuracy')
    ax.set_title('Annotator Accuracy')
    plt.show()


def generate_report(filepath):
    data = import_data.get_analysis_data(filepath)

    visualize_annotation_durations(data['mean_time'], data['min_time'], data['max_time'], 'annotation_durations.png')
    visualize_annotator_results(data['annotator_results'], 'annotator_results.png')
    visualize_kappa_coefficient(data['iaa'], 'kappa_coefficient.png')
    visualize_extra_outputs(data['cant_solve_count'], data['corrupt_data_count'], data['annotator_frequency'],
                            'extra_outputs.png')
    visualize_ref(data['n_positive'], data['n_negative'], 'reference_set.png')
    visualize_annotator_accuracy(data['annotator_accuracy'], data['overall_accuracy'], data['good_annotators'],
                                 data['bad_annotators'], 'annotator_accuracy.png')

    print("\nReport generated successfully! Please find the graphs in the output file.\n")