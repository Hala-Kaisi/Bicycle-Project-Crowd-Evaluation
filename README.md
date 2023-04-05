# Bicycle Project Crowd Evaluation v1.3

This project is an analysis of an anonymized dataset containing annotations on images of bicycles. The dataset was collected from multiple annotators, and includes information such as the time it took to annotate each image, the annotator IDs, and the results of each annotation.

The goal of this project is to gather insights about the annotators and the quality of their annotations, as well as to evaluate the reference set used to train the annotators. This analysis can be used to identify good and bad annotators, and to improve the quality of future annotations.

This project is part of the Quality Match GmbH recruitment process for a data scientist position. The task presented to the annotators was to identify whether an image contained a bicycle or not. The annotators were allowed to choose between "yes," "no," "can't solve," or "corrupt data."

## How to Run

1- Download the JSON files named anonymized_project.json and references.json.

2- Move these files to a folder named data_input.

3- Clone this repository to your local machine and add data_input to the same directory.

4- Make sure you have Python 3.6 or higher installed, along with the following modules:

    - pandas
    - numpy
    - matplotlib
    - plotnine

5- Run the code from the terminal:

    python3 main.py


## Data Analysis

The analysis of the dataset involves four main tasks:


1- Gather insights about the annotators

- Determine the number of annotators who contributed to the dataset

- Calculate the average, minimum, and maximum annotation times of the annotators

- Identify whether all annotators produced the same amount of results or if there were differences

- Determine if there were any questions for which annotators highly disagree

2- Analyze the usage of "cant_solve" and "corrupt_data" options

- Determine how often each option occurred in the project

- Identify if there is a trend within the annotators who used these options

3- Evaluate the balance of the reference set

- Demonstrate the balance via numbers and visualizations

4- Identify good and bad annotators using the reference set

- Use statistics and visualizations to distinguish between good and bad annotators


## Results

**Missing Values**
No missing values were found in the reference.json and anonymized_project.json files.

**Annotator Insights**
- **Number of Annotators:** There were 22 annotators that contributed to the dataset.
- **Annotation Durations:** The mean annotation time was 1.29 seconds, with the minimum time being 0.01 seconds and the maximum time being 42.398 seconds.
- **Annotator Results:** There were differences in the number of results produced by each annotator. Annotator_02 produced the highest number of results at 7596, while annotator_10 produced the lowest number of results at 315.

**Highly Disagreed Questions:** There were no questions for which annotators highly disagreed.

**Usage of "cant_solve" and "corrupt_data" Options** 
- **Occurrence:** In the project, 'cant_solve' occurred 17 times and 'corrupt_data' occurred 4 times.
- **Trends:** Annotator_22 used 'cant_solve' 4 times, while annotators_02 and 04 used 'cant_solve' 2 and 4 times, respectively. Only annotator_18 used 'corrupt_data' twice.

**Reference Set Balance**
The reference set was balanced, with an equal number of positive and negative examples.

**Identifying Good and Bad Annotators**
- **Annotator Accuracy:** The overall accuracy of the annotators was 0.93. The accuracy of each annotator ranged from 0.9 to 0.95.
- **Good annotators:** The good annotators were annotators_01, 02, 05, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, and 22, based on their high accuracy scores.
- **Bad annotators:** The bad annotators were annotators_03, 04, 06, 07, 08, 09, 10, and 12, based on their low accuracy scores.

**Kappa coefficient:** The kappa coefficient was calculated for each question, with the probability of agreement ranging from 0.4997 to 0.4999.

## Limitations

There are some limitations to this analysis that should be considered. First, the dataset only includes annotations for images of bicycles, so the findings may not be applicable to other types of images or tasks. Second, the analysis only considers the results of the annotators, and does not take into account their individual backgrounds or experience.

## Future Work

Future work could include expanding the dataset to include annotations for other types of images or tasks, as well as collecting more information about the annotators themselves, such as their backgrounds and experience. Additionally, further analysis could be conducted to investigate the reasons behind the lower accuracy scores for some annotators, and to develop strategies for improving their performance.

## References

The "anonymized_project.json" and "references.json" files were provided by Quality Match GmbH.
