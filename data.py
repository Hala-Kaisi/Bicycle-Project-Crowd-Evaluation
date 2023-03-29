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
    references_frames = pd.DataFrame.from_dict(references)
    tasks_frames = pd.DataFrame.from_dict(tasks)

    return references_frames, tasks_frames
