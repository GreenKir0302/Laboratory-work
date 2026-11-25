# -*- coding: utf-8 -*-
'''Точка входа: от сырого файла до отчета по практике 10'''
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

import config
from src.load import load_trips
from src.prepare import prepare_trips
from src.analyze import overall_kpi, cost_stats, top_share, cost_groups, kpi_by


def build_report(kpi, stats, top, groups, by_carrier, by_month, quality):
    '''Собирает отчет в markdown'''
    lines = ["# Отчет по рейсам: описательная статистика и KPI", ""]
    lines.append("Сформирован: " + datetime.now().strftime("%d.%m.%Y %H:%M"))

    lines += ["", "## KPI компании", ""]
    for k, v in kpi.items():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Стоимость рейса", ""]
    for k, v in stats.items():
        lines.append(f"- {k}: {v}")
    lines.append(f"- топ {round((1 - config.TOP_QUANTILE) * 100)}% самых дорогих рейсов "
                 f"({top['рейсов в топе']} шт.) дают {top['доля выручки, %']}% выручки")

    # таблицы как текст в блоке кода, что бы не ставить лишних библиотек
    lines += ["", "## Распределение по стоимости", "", "```", groups.to_string(index=False), "```"]
    lines += ["", "## По перевозчикам", "", "```", by_carrier.to_string(index=False), "```"]
    lines += ["", "## По месяцам", "", "```", by_month.to_string(index=False), "```"]

    lines += ["", "## Качество данных", ""]
    for k, v in quality.items():
        lines.append(f"- {k}: {v}")
    return "\n".join(lines) + "\n"


def main():
    started = datetime.now()
    print("ЗАПУСК PIPELINE", started.strftime("%Y-%m-%d %H:%M:%S"))
    Path(config.PROCESSED_DIR).mkdir(parents=True, exist_ok=True)
    Path(config.REPORTS_DIR).mkdir(parents=True, exist_ok=True)

    print("[1/4] загрузка")
    raw = load_trips(config.RAW_DIR, config.RAW_FILE)

    print("[2/4] подготовка")
    df, quality = prepare_trips(raw, config.COST_BINS, config.COST_LABELS)

    print("[3/4] расчет")
    kpi = overall_kpi(df)
    stats = cost_stats(df)
    top = top_share(df, config.TOP_QUANTILE)
    groups = cost_groups(df)
    by_carrier = kpi_by(df, "carrier").sort_values("revenue", ascending=False)
    by_month = kpi_by(df, "month")
    by_carrier.to_csv(Path(config.PROCESSED_DIR) / "kpi_by_carrier.csv", index=False, encoding="utf-8")
    by_month.to_csv(Path(config.PROCESSED_DIR) / "kpi_by_month.csv", index=False, encoding="utf-8")

    print("[4/4] отчет")
    report_path = Path(config.REPORTS_DIR) / "report.md"
    report_path.write_text(build_report(kpi, stats, top, groups, by_carrier, by_month, quality),
                           encoding="utf-8")

    raw_path = Path(config.RAW_DIR) / config.RAW_FILE
    manifest = {
        "запуск": started.isoformat(timespec="seconds"),
        "параметры": {"RAW_FILE": config.RAW_FILE, "COST_BINS": config.COST_BINS,
                      "TOP_QUANTILE": config.TOP_QUANTILE},
        "файлы": [{"файл": raw_path.name, "размер, байт": raw_path.stat().st_size}],
        "версии": {"pandas": pd.__version__, "python": sys.version},
        "качество данных": quality,
        "итоговые метрики": kpi,
    }
    manifest_path = Path(config.PROCESSED_DIR) / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print("    " + str(report_path))
    print("    " + str(manifest_path))
    print("ГОТОВО")


if __name__ == "__main__":
    main()
