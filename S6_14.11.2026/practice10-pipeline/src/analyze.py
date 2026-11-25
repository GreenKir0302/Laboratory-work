# -*- coding: utf-8 -*-
'''Слой 3: описательная статистика и KPI. Файлы не читает'''


def overall_kpi(df):
    '''KPI по всей компании как в части 5 практики 10'''
    revenue = df["cost_rub"].sum()
    return {
        "рейсов": len(df),
        "выручка": int(revenue),
        "средний чек": round(df["cost_rub"].mean()),
        "выручка на км": round(revenue / df["distance_km"].sum(), 1),
        "выручка на тонно-км": round(revenue / (df["weight_t"] * df["distance_km"]).sum(), 2),
        "средняя загрузка, т": round(df["weight_t"].mean(), 1),
        "OTD, %": round((~df["is_delayed"]).mean() * 100, 1),
        "средняя задержка, ч": round(df["delay_h"].mean(), 2),
    }


def cost_stats(df):
    '''Центр и разброс стоимости рейса'''
    cost = df["cost_rub"]
    q1 = cost.quantile(0.25)
    q3 = cost.quantile(0.75)
    return {
        "среднее": round(cost.mean(), 1),
        "медиана": round(cost.median(), 1),
        "стандартное отклонение": round(cost.std(), 1),
        "Q1": round(q1, 1),
        "Q3": round(q3, 1),
        "IQR": round(q3 - q1, 1),
        "коэффициент вариации, %": round(cost.std() / cost.mean() * 100, 1),
    }


def top_share(df, q):
    '''Какую долю выручки дают самые дорогие рейсы (выше перцентиля q)'''
    gr = df["cost_rub"].quantile(q)
    top = df[df["cost_rub"] >= gr]
    return {"рейсов в топе": len(top),
            "доля выручки, %": round(top["cost_rub"].sum() / df["cost_rub"].sum() * 100, 1)}


def cost_groups(df):
    '''Таблица распределения: рейсы и выручка по интервалам стоимости'''
    freq = df["cost_group"].value_counts().sort_index().to_frame("рейсов")
    freq["доля рейсов, %"] = (freq["рейсов"] / len(df) * 100).round(1)
    freq["выручка"] = df.groupby("cost_group", observed=False)["cost_rub"].sum()
    freq["доля выручки, %"] = (freq["выручка"] / freq["выручка"].sum() * 100).round(1)
    return freq.reset_index()


def kpi_by(df, column):
    '''KPI в разрезе столбца: перевозчик или месяц'''
    kpi = df.groupby(column).agg(
        trips=("trip_id", "count"),
        revenue=("cost_rub", "sum"),
        avg_ticket=("cost_rub", "mean"),
        otd=("is_delayed", lambda s: (~s).mean() * 100),
    ).round(1)
    rev = df.groupby(column)["cost_rub"].sum()
    km = df.groupby(column)["distance_km"].sum()
    kpi["rev_per_km"] = (rev / km).round(1)
    return kpi.reset_index()
