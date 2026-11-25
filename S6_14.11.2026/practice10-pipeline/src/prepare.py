# -*- coding: utf-8 -*-
'''Слой 2: типы и новые столбцы, метрики тут не считаются'''
import pandas as pd


def prepare_trips(raw, cost_bins, cost_labels):
    '''Готовит таблицу к анализу. Возвращает (df, отчет о качестве)'''
    report = {"строк получено": len(raw)}
    df = raw.copy()

    df = df.drop_duplicates(subset=["trip_id"])
    report["удалено дублей"] = report["строк получено"] - len(df)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    report["дат не распознано"] = int(df["date"].isna().sum())
    report["пропусков всего"] = int(df.isna().sum().sum())

    # данные в практике 10 чистые, по этому тут только новые столбцы
    df["is_delayed"] = df["delay_h"] > 0
    df["cost_group"] = pd.cut(df["cost_rub"], bins=cost_bins, labels=cost_labels)

    report["строк осталось"] = len(df)
    return df.reset_index(drop=True), report
