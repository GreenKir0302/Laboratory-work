# -*- coding: utf-8 -*-
'''Слой 1: загрузка журнала рейсов, ничего не исправляет'''
from pathlib import Path

import pandas as pd


def load_trips(raw_dir, filename):
    '''Читает файл с рейсами из raw_dir'''
    path = Path(raw_dir) / filename
    if not path.exists():
        raise FileNotFoundError(f"нет файла {path}")
    df = pd.read_csv(path)
    print(f"    {path.name}: {len(df)} строк")
    return df
