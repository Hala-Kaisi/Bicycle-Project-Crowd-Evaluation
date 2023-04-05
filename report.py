import matplotlib.pyplot as plt
import import_data
import pandas as pd
from plotnine import ggplot, aes, geom_bar, geom_errorbar, theme, element_text
import numpy as np
import seaborn as sns



def visualize_annotation_durations(mean_time, min_time, max_time, durations, output_file):

    print("\nVisualizing annotation durations...\n")
    # Convert the durations dictionary to a pandas DataFrame
    durations_list = []
    for annotator_id, annotator_durations in durations.items():
        for duration in annotator_durations:
            durations_list.append({'annotator_id': annotator_id, 'duration': duration})
    durations_df = pd.DataFrame(durations_list)

    # Calculate mean and standard deviation for each annotator
    summary_df = durations_df.groupby('annotator_id')['duration'].agg(['mean', 'std']).reset_index()

    # Set the lower limit of the error bars to zero
    summary_df['ymin'] = np.maximum(0, summary_df['mean'] - summary_df['std'])

    # Create the bar chart with error bars using ggplot
    plot = (
            ggplot(summary_df, aes(x='annotator_id', y='mean', fill='annotator_id'))
            + geom_bar(stat='identity', position='dodge', width=0.7)
            + geom_errorbar(aes(ymin='ymin', ymax='mean+std'), position='dodge', width=0.5)
            + theme(axis_text_x=element_text(rotation=45, hjust=1))
            + theme(figure_size=(12, 6))
    )

    plot.save(output_file)

    print("Mean annotation duration: " + str(mean_time) + " seconds")
    print("Minimum annotation duration: " + str(min_time) + " seconds")
    print("Maximum annotation duration: " + str(max_time) + " seconds")


def visualize_annotator_results(annotator_results, output_file):
    fig, ax = plt.subplots()
    ax.bar(annotator_results.keys(), annotator_results.values())
    ax.set_xlabel('Annotator IDs')
    ax.set_ylabel('Number of Annotations')
    ax.set_title('Annotator Results')
    plt.xticks(rotation=90)
    plt.savefig(output_file)


def visualize_kappa_coefficient(iaa, output_file):

    print("\nVisualizing kappa coefficient...\n")

    iaa_scores = list(iaa.values())
    question_ids = list(iaa.keys())
    low_iaa_question_ids = []

    for i in range(len(iaa_scores)):
        if iaa_scores[i] <= 0.4:
            low_iaa_question_ids.append(question_ids[i])

    fig, ax = plt.subplots(figsize=(20, 10))
    ax.scatter(question_ids, iaa_scores, c='#b2df8a', alpha=0.8)
    ax.set_xlabel('Question ID')
    ax.set_ylabel('IAA Score')
    ax.set_title('Inter-Annotator Agreement Scores')
    ax.grid(axis='y')
    plt.xticks(rotation=90)

    plt.savefig(output_file)

    print("Lowest IAA score: ", min(iaa_scores))
    print("Highest IAA score: ", max(iaa_scores))

    if len(low_iaa_question_ids) > 0:
        print(f"Found {len(low_iaa_question_ids)} questions with IAA score equal to or lower than 0.4.")


def visualize_extra_outputs(cant_solve_overall_count, corrupt_data_overall_count, annotator_frequency, output_file):

    print("\nVisualizing extra outputs...\n")
    annotator_df = pd.DataFrame(annotator_frequency).T

    # Add a column for the total count of tasks for each annotator
    annotator_df['total_tasks'] = annotator_df['cant_solve_count'] + annotator_df['corrupt_data_count']

    # Sort the DataFrame by total task count in descending order
    annotator_df.sort_values('total_tasks', ascending=False, inplace=True)

    # Create a stacked bar chart
    ax = annotator_df[['cant_solve_count', 'corrupt_data_count']].plot(kind='bar', stacked=True, figsize=(12, 8))
    ax.set_xlabel('Annotator ID')
    ax.set_ylabel('Task Count')
    ax.set_title('Frequency of "cant_solve" and "corrupt_data" by annotator')
    plt.savefig(output_file)

    print("cant_solve_overall_count: ", cant_solve_overall_count)
    print("corrupt_data_overall_count: ", corrupt_data_overall_count)



def visualize_ref(n_positive, n_negative, output_file):

    print("\nVisualizing reference labels...\n")

    labels = ['Positive', 'Negative']
    sizes = [n_positive, n_negative]
    colors = ['#4b86b4', '#b44b4b']  # blue pastel colors
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Add title
    plt.title('Reference Labels Distribution')

    # Show the chart
    plt.axis('equal')
    plt.savefig(output_file)

    print("n_positive: ", n_positive)
    print("n_negative: ", n_negative)


def visualize_annotator_accuracy(annotator_accuracy, overall_accuracy, good_annotators, bad_annotators, output_file):


    print("\nVisualizing annotator accuracy...\n")

    # Calculate mean accuracy score for all annotators
    mean_accuracy = sum(annotator_accuracy.values()) / len(annotator_accuracy)

    fig, ax = plt.subplots()
    x = list(annotator_accuracy.keys())
    y = list(annotator_accuracy.values())
    ax.scatter(x, y)
    ax.axhline(y=mean_accuracy, color='b', linestyle='--', label='Mean Accuracy')
    ax.set_xlabel('Annotator IDs')
    ax.set_ylabel('Accuracy')
    ax.set_title('Annotator Accuracy')
    plt.xticks(rotation=90)
    plt.legend()
    plt.savefig(output_file)

    print("mean_accuracy: ", mean_accuracy)
    print("good_annotators: ", good_annotators)
    print("bad_annotators: ", bad_annotators)



def generate_report(filepath):
    data = import_data.get_analysis_data(filepath)

    print("\nGenerating report...\n")

    visualize_annotation_durations(data['mean_time'], data['min_time'], data['max_time'], data['durations'], 'annotation_durations.png')
    visualize_annotator_results(data['annotator_results'], 'annotator_results.png')
    visualize_kappa_coefficient(data['iaa'], 'kappa_coefficient.png')
    visualize_extra_outputs(data['cant_solve_count'], data['corrupt_data_count'], data['annotator_frequency'],
                            'extra_outputs.png')
    visualize_ref(data['n_positive'], data['n_negative'], 'reference_set.png')
    visualize_annotator_accuracy(data['annotator_accuracy'], data['overall_accuracy'], data['good_annotators'],
                                 data['bad_annotators'], 'annotator_accuracy.png')

    print("\nReport generated successfully! Please find the graphs in the output file.\n")