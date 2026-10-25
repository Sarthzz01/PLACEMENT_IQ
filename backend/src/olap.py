import pandas as pd
import numpy as np
import time
from .database import log_olap_query

AGG_MAP = {
    "Average": "mean",
    "Mean": "mean",
    "mean": "mean",
    "Sum": "sum",
    "sum": "sum",
    "Count": "count",
    "count": "count",
    "Min": "min",
    "min": "min",
    "Max": "max",
    "max": "max",
    "Median": "median",
    "median": "median",
    "Count Distinct": "nunique",
    "nunique": "nunique"
}

HIERARCHIES = {
    "academic": {
        "id": "academic",
        "name": "Academic Performance Hierarchy",
        "description": "Detailed CGPA Range → CGPA Band → Overall Institution",
        "levels": ["cgpa_decile", "cgpa_band", "Overall"],
        "labels": {
            "cgpa_decile": "Detailed CGPA Range",
            "cgpa_band": "CGPA Band",
            "Overall": "Overall Institution"
        }
    },
    "demographic": {
        "id": "demographic",
        "name": "Demographic Age Hierarchy",
        "description": "Individual Age → Age Group → Overall Institution",
        "levels": ["age", "age_group", "Overall"],
        "labels": {
            "age": "Specific Age (Years)",
            "age_group": "Age Group",
            "Overall": "Overall Institution"
        }
    },
    "departmental": {
        "id": "departmental",
        "name": "Departmental Hierarchy",
        "description": "Engineering Branch → Overall Institution",
        "levels": ["branch", "Overall"],
        "labels": {
            "branch": "Engineering Branch",
            "Overall": "Overall Institution"
        }
    }
}

def sanitize_dim(dim):
    """Sanitize dimension string to prevent KeyError 'none' or null queries."""
    if not dim:
        return None
    s = str(dim).strip()
    if s.lower() in ["none", "null", "all", "overall", ""]:
        return None
    return s

def sanitize_dim_list(dims, valid_cols=None):
    """Clean list of dimension strings, stripping empty or invalid tokens."""
    if not dims:
        return []
    if isinstance(dims, str):
        dims = [dims]
    out = []
    for d in dims:
        sd = sanitize_dim(d)
        if sd:
            if valid_cols is None or sd in valid_cols:
                out.append(sd)
    return out

def apply_filters(df, filters):
    """
    Filter DataFrame by dictionary of conditions.
    Supports:
      - list/set of values
      - single scalar
      - tuple of (min, max)
      - dict of {'min': min_val, 'max': max_val}
    """
    if not filters or not isinstance(filters, dict):
        return df.copy()

    out = df.copy()
    for col, vals in filters.items():
        if col not in out.columns or vals is None or vals == "":
            continue

        # Range condition passed as tuple (min, max)
        if isinstance(vals, (tuple, list)) and len(vals) == 2 and (isinstance(vals[0], (int, float)) or isinstance(vals[1], (int, float))):
            min_v, max_v = vals
            if min_v is not None and min_v != "":
                out = out[out[col] >= float(min_v)]
            if max_v is not None and max_v != "":
                out = out[out[col] <= float(max_v)]
        # Range condition passed as dict {'min': ..., 'max': ...}
        elif isinstance(vals, dict):
            min_v = vals.get("min")
            max_v = vals.get("max")
            if min_v is not None and min_v != "":
                out = out[out[col] >= float(min_v)]
            if max_v is not None and max_v != "":
                out = out[out[col] <= float(max_v)]
        elif isinstance(vals, list):
            clean_vals = [str(v) for v in vals if str(v).lower() not in ["all", "none", ""]]
            if clean_vals:
                out = out[out[col].astype(str).isin(clean_vals)]
        else:
            s_val = str(vals).strip()
            if s_val.lower() not in ["all", "none", ""]:
                out = out[out[col].astype(str) == s_val]

    return out

def aggregate(df, rows, cols, measure="cgpa", agg="Average"):
    """
    Compute multi-dimensional OLAP aggregation over selected rows, columns, and measure.
    Handles empty row/column selections gracefully.
    Calculates binary placement_prediction as percentage when averaged.
    """
    clean_rows = sanitize_dim_list(rows, valid_cols=df.columns)
    clean_cols = sanitize_dim_list(cols, valid_cols=df.columns)

    if measure not in df.columns:
        measure = "cgpa" if "cgpa" in df.columns else df.columns[0]

    fn = AGG_MAP.get(agg, "mean")
    is_placement_rate = (measure == "placement_prediction" and fn == "mean")

    # If no grouping axes, aggregate across entire cohort
    if not clean_rows and not clean_cols:
        series = df[measure]
        if fn == "mean":
            val = series.mean()
        elif fn == "sum":
            val = series.sum()
        elif fn == "count":
            val = series.count()
        elif fn == "min":
            val = series.min()
        elif fn == "max":
            val = series.max()
        elif fn == "median":
            val = series.median()
        elif fn == "nunique":
            val = series.nunique()
        else:
            val = series.mean()

        if is_placement_rate:
            val = val * 100.0

        label = "Predicted Placement Rate (%)" if is_placement_rate else f"{agg} of {measure}"
        return pd.DataFrame({label: [round(float(val), 2)]})

    piv = df.pivot_table(
        index=clean_rows if clean_rows else None,
        columns=clean_cols if clean_cols else None,
        values=measure,
        aggfunc=fn,
        fill_value=0
    )

    if is_placement_rate:
        piv = piv * 100.0

    if isinstance(piv.columns, pd.MultiIndex):
        piv.columns = ['_'.join(str(c) for c in col).strip() for col in piv.columns.values]
    elif clean_cols:
        piv.columns = [f"{c}" for c in piv.columns]

    res = piv.reset_index()

    # Round numeric columns to 2 decimal places
    num_cols = res.select_dtypes(include=[np.number]).columns
    res[num_cols] = res[num_cols].round(2)

    return res

def slice_op(df, dimension, value, measure="placement_prediction", agg="Average", display_dim=None):
    """
    OLAP Slice: Filter single dimension by a single value.
    Computes aggregated sub-cube, plus overall slice KPIs.
    """
    san_dim = sanitize_dim(dimension)
    if not san_dim or san_dim not in df.columns:
        san_dim = "branch"

    filtered = df[df[dimension].astype(str) == str(value)].copy()
    if len(filtered) == 0:
        return pd.DataFrame()

    san_display = sanitize_dim(display_dim)
    if san_display and san_display != san_dim and san_display in df.columns:
        rows = [san_display]
    else:
        rows = [san_dim]

    return aggregate(filtered, rows, [], measure, agg)

def dice_op(df, conditions, rows, cols, measure="placement_prediction", agg="Average"):
    """
    OLAP Dice: Multi-dimensional sub-cube filtering across multiple conditions.
    """
    filtered = apply_filters(df, conditions)
    clean_rows = sanitize_dim_list(rows, valid_cols=df.columns) or ["branch"]
    clean_cols = sanitize_dim_list(cols, valid_cols=df.columns)
    return aggregate(filtered, clean_rows, clean_cols, measure, agg)

def rollup_hierarchy(df, hierarchy_id, current_level, target_level, comparison_dim=None, measure="cgpa", agg="Average"):
    """
    Genuine hierarchical OLAP Roll-Up.
    Generalizes from a granular level to a summarized target level within a defined hierarchy.
    Example: Academic hierarchy: cgpa_decile -> cgpa_band -> Overall.
    Returns: (before_df, after_df, totals_dict)
    """
    hier = HIERARCHIES.get(hierarchy_id, HIERARCHIES["academic"])
    levels = hier["levels"]

    c_lvl = current_level if current_level in levels else levels[0]
    t_lvl = target_level if target_level in levels else levels[-1]

    comp = sanitize_dim(comparison_dim)
    comp_cols = [comp] if comp and comp in df.columns else []

    # Before state (at current granular level)
    before_rows = [c_lvl] if c_lvl != "Overall" and c_lvl in df.columns else []
    before_df = aggregate(df, before_rows, comp_cols, measure, agg)

    # After state (at target generalized level)
    after_rows = [t_lvl] if t_lvl != "Overall" and t_lvl in df.columns else []
    after_df = aggregate(df, after_rows, comp_cols, measure, agg)

    # Compute totals
    totals_df = aggregate(df, [], comp_cols, measure, agg)
    totals_dict = totals_df.to_dict(orient="records")[0] if len(totals_df) > 0 else {}

    return before_df, after_df, totals_dict

def drilldown_hierarchy(df, hierarchy_id, current_level, target_level, filter_value=None, comparison_dim=None, measure="cgpa", agg="Average"):
    """
    Genuine hierarchical OLAP Drill-Down.
    De-aggregates from a high-level summary to a more granular breakdown.
    If filter_value is specified, isolates that specific cohort before drilling down.
    Returns: (before_df, after_df, totals_dict)
    """
    hier = HIERARCHIES.get(hierarchy_id, HIERARCHIES["academic"])
    levels = hier["levels"]

    c_lvl = current_level if current_level in levels else levels[-1]
    t_lvl = target_level if target_level in levels else levels[0]

    comp = sanitize_dim(comparison_dim)
    comp_cols = [comp] if comp and comp in df.columns else []

    target_df = df.copy()
    if filter_value is not None and str(filter_value).strip().lower() not in ["all", "overall", "none", ""]:
        if c_lvl in df.columns:
            target_df = target_df[target_df[c_lvl].astype(str) == str(filter_value)]

    before_rows = [c_lvl] if c_lvl != "Overall" and c_lvl in df.columns else []
    before_df = aggregate(target_df, before_rows, comp_cols, measure, agg)

    after_rows = [t_lvl] if t_lvl != "Overall" and t_lvl in target_df.columns else []
    after_df = aggregate(target_df, after_rows, comp_cols, measure, agg)

    totals_df = aggregate(target_df, [], comp_cols, measure, agg)
    totals_dict = totals_df.to_dict(orient="records")[0] if len(totals_df) > 0 else {}

    return before_df, after_df, totals_dict

def rollup_2d(df, current_rows, target_rows, current_cols, target_cols, measure="cgpa", agg="Average"):
    """
    2-Dimensional OLAP Roll-Up.
    Preserved for backwards compatibility with test suites and custom multi-axis roll-ups.
    """
    clean_curr_rows = sanitize_dim_list(current_rows, valid_cols=df.columns)
    clean_targ_rows = sanitize_dim_list(target_rows, valid_cols=df.columns)
    clean_curr_cols = sanitize_dim_list(current_cols, valid_cols=df.columns)
    clean_targ_cols = sanitize_dim_list(target_cols, valid_cols=df.columns)

    before_df = aggregate(df, clean_curr_rows, clean_curr_cols, measure, agg)
    after_df = aggregate(df, clean_targ_rows, clean_targ_cols, measure, agg)
    return before_df, after_df

def drilldown_2d(df, current_rows, target_rows, current_cols, target_cols, measure="cgpa", agg="Average"):
    """
    2-Dimensional OLAP Drill-Down.
    Preserved for backwards compatibility with test suites and custom multi-axis drill-downs.
    """
    clean_curr_rows = sanitize_dim_list(current_rows, valid_cols=df.columns)
    clean_targ_rows = sanitize_dim_list(target_rows, valid_cols=df.columns)
    clean_curr_cols = sanitize_dim_list(current_cols, valid_cols=df.columns)
    clean_targ_cols = sanitize_dim_list(target_cols, valid_cols=df.columns)

    before_df = aggregate(df, clean_curr_rows, clean_curr_cols, measure, agg)
    after_df = aggregate(df, clean_targ_rows, clean_targ_cols, measure, agg)
    return before_df, after_df

def rollup_op(df, hierarchy, measure="cgpa", agg="Average"):
    """Traditional 1D hierarchy roll-up."""
    outs = []
    for i in range(len(hierarchy), 0, -1):
        levels = hierarchy[:i]
        level_name = " → ".join(levels)
        res = aggregate(df, levels, [], measure, agg)
        outs.append((level_name, res))
    return outs

def drilldown_op(df, hierarchy, measure="cgpa", agg="Average"):
    """Traditional 1D hierarchy drill-down."""
    outs = []
    for i in range(1, len(hierarchy) + 1):
        levels = hierarchy[:i]
        level_name = " → ".join(levels)
        res = aggregate(df, levels, [], measure, agg)
        outs.append((level_name, res))
    return outs

def pivot_op(df, rows, cols, measure="cgpa", agg="Average"):
    """
    OLAP Pivot: Rotate dimensional axes for cross-tabulation.
    Calculates cross-tabulation table with row and column marginal totals.
    """
    clean_rows = sanitize_dim_list(rows, valid_cols=df.columns) or ["branch"]
    clean_cols = sanitize_dim_list(cols, valid_cols=df.columns) or ["gender"]
    return aggregate(df, clean_rows, clean_cols, measure, agg)

def multi_measure_op(df, group_dim, measures, agg="Average"):
    """
    Multi-Measure Analysis (Cross-Fact Synthesis).
    Aggregates multiple numeric measures across a shared grouping dimension.
    Provides raw metric values AND min-max normalized (0-100 scale) values for direct comparison.
    """
    dim = sanitize_dim(group_dim)
    if not dim or dim not in df.columns:
        dim = "branch"

    valid_measures = [m for m in measures if m in df.columns]
    if not valid_measures:
        valid_measures = ["cgpa", "aptitude_score", "coding_skill_score"]

    fn = AGG_MAP.get(agg, "mean")

    piv = df.pivot_table(
        index=dim,
        values=valid_measures,
        aggfunc=fn,
        fill_value=0
    )

    # For placement_prediction, express as percentage if mean
    if "placement_prediction" in valid_measures and fn == "mean":
        piv["placement_prediction"] = piv["placement_prediction"] * 100.0

    raw_df = piv.reset_index().round(2)

    # Compute Min-Max Normalized (0-100 scale) for fair small-multiple / radar comparison
    norm_df = raw_df.copy()
    for m in valid_measures:
        min_v = norm_df[m].min()
        max_v = norm_df[m].max()
        if max_v > min_v:
            norm_df[f"{m}_normalized"] = ((norm_df[m] - min_v) / (max_v - min_v) * 100.0).round(1)
        else:
            norm_df[f"{m}_normalized"] = 100.0

    return raw_df, norm_df

def drill_across(df, row, col, measures, agg="Average"):
    """
    OLAP Drill-Across / Multi-Measure Synthesis.
    Combines multiple facts/measures across warehouse dimensions.
    Preserved for backwards compatibility with validate_project.py.
    """
    clean_row = sanitize_dim(row) or "branch"
    clean_col = sanitize_dim(col)
    valid_measures = [m for m in measures if m in df.columns] if measures else ["cgpa", "aptitude_score"]

    fn = AGG_MAP.get(agg, "mean")
    piv = df.pivot_table(
        index=clean_row,
        columns=clean_col if clean_col and clean_col in df.columns else None,
        values=valid_measures,
        aggfunc=fn,
        fill_value=0
    )
    if isinstance(piv.columns, pd.MultiIndex):
        piv.columns = ['_'.join(str(c) for c in c_val).strip() for c_val in piv.columns.values]
    return piv.reset_index().round(2)
