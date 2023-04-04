import json
import pandas as pd


def load_data(reference_path, tasks_path):

    with open(reference_path, 'r') as f:
        references = json.load(f)

    with open(tasks_path, 'r') as f:
        tasks = json.load(f)

    references_frames, tasks_frames = create_frames(references, tasks)

    return references_frames, tasks_frames


def create_frames(references, tasks):
    references_frames = pd.DataFrame(references)
    tasks_frames = pd.DataFrame(tasks['results']['root_node']['results'])


    return references_frames.T, tasks_frames.T


def cleanup_tasks(tasks):

    tasks_frame = tasks.copy()

    tasks_list = []

    for i, row in tasks_frame.iterrows():
        for j in range(len(row['results'])):
            task_row = {
                'task_id': i,
                'annotator_id': row['results'][j]['user']['vendor_user_id'],
                'answer': row['results'][j]['task_output']['answer'],
                'cant_solve': row['results'][j]['task_output']['cant_solve'],
                'corrupt_data': row['results'][j]['task_output']['corrupt_data'],
                'image_id': row['results'][j]['task_input']['image_url'].split("/")[-1].split(".")[0]
            }
            tasks_list.append(task_row)

    tasks_frame = pd.DataFrame(tasks_list)

    return tasks_frame
