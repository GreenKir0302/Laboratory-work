# Практика 10 в виде pipeline

Описательная статистика и KPI по журналу рейсов (февраль-май 2025, 910 рейсов).
Исходные данные лежат в `data/raw/trips_q.csv` и не меняются.

## Как запустить

```
pip install -r requirements.txt
python run.py
```

После запуска появятся:
- `reports/report.md` - отчет (KPI, стоимость рейса, распределение, перевозчики, месяцы)
- `data/processed/kpi_by_carrier.csv`, `kpi_by_month.csv` - таблицы KPI
- `data/processed/run_manifest.json` - когда запускали, с какими параметрами и что получилось

Параметры (пути, интервалы стоимости, порог для топа дорогих рейсов) меняются в `config.py`.

## Структура

- `src/load.py` - читает csv
- `src/prepare.py` - даты, дубли, новые столбцы `is_delayed` и `cost_group`
- `src/analyze.py` - KPI, статистика стоимости, распределение, разрезы
- `run.py` - запускает все по порядку
