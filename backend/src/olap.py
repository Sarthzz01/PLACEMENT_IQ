import pandas as pd
import numpy as np
from .database import log_olap_query

AGG_MAP = {
    "Average": "mean",
    "Mean": "mean",
    "Sum": "sum",
    "Count": "count",
    "Min": "min",
    "Max": "max",
    "Median": "median"
}

def apply_filters(df, filters):
    """
    Filter DataFrame by dictionary of conditions.
    Supports list of values or numeric tuples (min, max).
    """
    out = df.copy()
    for col, vals in filters.items():
        if col not in out.columns or not vals:
            continue
        if isinstance(vals, tuple) and len(vals) == 2:
            min_v, max_v = vals
            if min_v is not None:
                out = out[out[col] >= min_v]
            if max_v is not None:
                out = out[out[col] <= max_v]
        elif isinstance(vals, list):
            out = out[out[col].astype(str).isin([str(v) for v in vals])]
        else:
            out = out[out[col].astype(str) == str(vals)]
    return out

def aggregate(df, rows, cols, measure, agg="Average"):
    """
    Compute multi-dimensional OLAP aggregation over selected rows, columns, and measure.
    Handles empty row/column selections gracefully.
    """
    fn = AGG_MAP.get(agg, "mean")
    if not rows and not cols:
        val = getattr(df[measure], fn)() if hasattr(df[measure], fn) else (df[measure].median() if fn == "median" else df[measure].mean())
        return pd.DataFrame({f"{agg} of {measure}": [round(val, 3)]})

    piv = df.pivot_table(
        index=rows if rows else None,
        columns=cols if cols else None,
        values=measure,
        aggfunc=fn,
        fill_value=0
    )

    if isinstance(piv.columns, pd.MultiIndex):
        piv.columns = ['_'.join(str(c) for c in col).strip() for col in piv.columns.values]
    elif cols:
        piv.columns = [f"{c}" for c in piv.columns]

    return piv.reset_index()

def slice_op(df, dimension, value, measure="placement_prediction", agg="Average", display_dim=None):
    """OLAP Slice: Filter single dimension by a single value."""
    filtered = df[df[dimension].astype(str) == str(value)]
    if len(filtered) == 0:
        return pd.DataFrame()
    rows = [display_dim] if display_dim and display_dim != dimension and display_dim in df.columns else [dimension]
    return aggregate(filtered, rows, [], measure, agg)

def dice_op(df, conditions, rows, cols, measure="placement_prediction", agg="Average"):
    """OLAP Dice: Multi-dimensional sub-cube filtering across multiple conditions."""
    filtered = apply_filters(df, conditions)
    return aggregate(filtered, rows, cols, measure, agg)

def rollup_2d(df, current_rows, target_rows, current_cols, target_cols, measure="cgpa", agg="Average"):
    """
    Independent 2-Dimensional OLAP Roll-Up.
    Allows user to select which row dimensions and which column dimensions to drill up at once.
    Example:
        current_rows = ['branch', 'gender'] -> target_rows = ['branch'] or [] (Overall)
        current_cols = ['placement_status', 'placement_training'] -> target_cols = ['placement_status'] or [] (Overall)
    Returns:
        (before_df, after_df)
    """
    clean_curr_rows = [r for r in current_rows if r != "Overall" and r]
    clean_targ_rows = [r for r in target_rows if r != "Overall" and r]
    clean_curr_cols = [c for c in current_cols if c != "Overall" and c]
    clean_targ_cols = [c for c in target_cols if c != "Overall" and c]

    before_df = aggregate(df, clean_curr_rows, clean_curr_cols, measure, agg)
    after_df = aggregate(df, clean_targ_rows, clean_targ_cols, measure, agg)
    return before_df, after_df

def drilldown_2d(df, current_rows, target_rows, current_cols, target_cols, measure="cgpa", agg="Average"):
    """
    Independent 2-Dimensional OLAP Drill-Down.
    De-aggregates along row and/or column axes simultaneously.
    Example:
        current_rows = ['branch'] -> target_rows = ['branch', 'gender']
        current_cols = ['placement_status'] -> target_cols = ['placement_status', 'placement_training']
    Returns:
        (before_df, after_df)
    """
    clean_curr_rows = [r for r in current_rows if r != "Overall" and r]
    clean_targ_rows = [r for r in target_rows if r != "Overall" and r]
    clean_curr_cols = [c for c in current_cols if c != "Overall" and c]
    clean_targ_cols = [c for c in target_cols if c != "Overall" and c]

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
    """OLAP Pivot: Rotate dimensional axes for cross-tabulation."""
    return aggregate(df, rows, cols, measure, agg)

def drill_across(df, row, col, measures, agg="Average"):
    """
    OLAP Drill-Across: Combine multiple facts/measures across different warehouse dimensions.
    """
    fn = AGG_MAP.get(agg, "mean")
    piv = df.pivot_table(
        index=row,
        columns=col,
        values=measures,
        aggfunc=fn,
        fill_value=0
    )
    if isinstance(piv.columns, pd.MultiIndex):
        piv.columns = ['_'.join(str(c) for c in c_val).strip() for c_val in piv.columns.values]
    return piv.reset_index()
