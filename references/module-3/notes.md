# Module 3: Why Interactivity Accelerates AI Discovery

This module is about showing why interactivity matters for AI and ML work.

The main message:

> In a reactive notebook, data exploration, feature choices, model training, plots, and error analysis are connected. When one input changes, the rest of the workflow updates with it.

We are using one notebook:

```bash
marimo edit --sandbox 3_1_interactive_ml_workflow.py
```

This notebook uses the Adult Income dataset. The prediction task is binary classification: predict whether a person earns more than `$50K` per year.

---

### 3.1 Let's Start With the Dataset

Let's first open the notebook and look at the raw dataframe.

The dataset has a mix of:

- numeric columns, like `age`, `hours-per-week`, `capital-gain`, and `education-num`
- categorical columns, like `occupation`, `education`, `marital-status`, and `sex`
- a target column called `income`

The target is:

- `0` for income `<=50K`
- `1` for income `>50K`

I would say:

> Before we model anything, we need to understand the data. In marimo, a dataframe is not just printed text. It becomes an interactive table where we can page, search, sort, and filter.

The notebook first shows:

```python
df[:1000]
```

marimo renders that as an interactive dataframe viewer.

If someone asks how to show a plain static dataframe instead, point to:

```python
mo.plain(df.head())
```

That opts out of the rich dataframe display.

---

### 3.2 Let's Look at Editable Data

Next, we show:

```python
mo.ui.data_editor(df)
```

This creates an editable table.

I would explain it like this:

> `mo.ui.data_editor` is useful for small what-if experiments. We can edit a few values directly in the table and then access the edited data from another cell.

The important concept is `.value`.

```python
data_editor.value
```

That gives us the edited data back.

If someone asks why we read `.value` in another cell:

> In marimo, UI elements are reactive objects. We usually define the widget in one cell, then read `.value` in another cell so downstream cells can react when the value changes.

The notebook also shows:

```python
mo.ui.data_editor(df, editable_columns=["age", "education"])
```

This is useful because sometimes we only want specific columns to be editable.

A good teaching line:

> Editing data directly is not for bulk data cleaning here. It is for quick what-if checks while we are exploring.

---

### 3.3 Let's Explore the Data Visually

Now we move from rows and columns into visual exploration.

The first tool is:

```python
mo.ui.data_explorer(df)
```

I would explain:

> `data_explorer` is chart-first. Use it when you do not yet know exactly what plot you want. You can drag columns into visual encodings and quickly explore relationships.

During the demo, try something simple:

- put `occupation` or `education` on the x-axis
- use count as the y-axis
- color by `sex` or `income`

The goal is not to make the final perfect chart. The goal is to show fast visual discovery.

The second tool is:

```python
mo.ui.dataframe(df)
```

I would explain:

> `mo.ui.dataframe` is useful when we want to inspect, sort, filter, group, or transform the table interactively.

The difference:

- `data_explorer` helps us discover charts.
- `dataframe` helps us inspect and transform table views.
- `data_editor` lets us edit values.

That distinction is useful if someone asks why there are multiple dataframe-related widgets.

---

### 3.4 Let's Add Modeling Controls

Now we move into modeling, but the important part is that the model is controlled by UI widgets.

The notebook creates:

```python
selected_features_ui = mo.ui.multiselect(...)
sample_size_ui = mo.ui.slider(...)
preview_rows = mo.ui.slider(...)
```

The feature selector controls which columns go into the model.

The sample-size slider controls how many rows we train on.

The preview-rows slider controls how many error-analysis rows we show later.

I would say:

> These controls are not cosmetic. They drive the actual pipeline. If we remove a feature or change the sample size, the preprocessing, model fitting, metrics, and plots downstream update from the new inputs.

The key marimo idea:

> We do not write callbacks. Downstream cells read `.value`, and marimo figures out what needs to rerun.

For example:

```python
selected_features = selected_features_ui.value
sample_size = sample_size_ui.value
```

If TabICL is slow during the live demo, lower the sample size. That is also a nice moment to show why interactivity matters: we can trade speed and fidelity live.

---

### 3.5 Let's Prepare the Data for Modeling

Now the notebook samples rows, selects features, encodes categorical columns, and splits the data.

The high-level flow is:

1. Read selected features from the multiselect.
2. Read sample size from the slider.
3. Sample the dataframe while preserving the class balance with `stratify=df["income"]`.
4. Encode categorical columns with `LabelEncoder`.
5. Split into train and test sets.

If someone asks why we encode categorical columns:

> Most scikit-learn style models expect numeric input. Columns like occupation or education are text categories, so we convert them into numeric codes before modeling.

If someone asks why we use train/test split:

> We train on one part of the data and evaluate on held-out rows so we can estimate how well the model generalizes.

If someone asks what stratify means:

> Stratify keeps the class balance similar in the sample or split. Since most rows are `<=50K`, this prevents us from accidentally creating a sample with a very different target distribution.

---

### 3.6 Let's Compare Two Models

Now we fit two models on the same selected features and the same train/test split:

- TabICL
- Random Forest

I would explain TabICL like this:

> TabICL is a tabular foundation model. The idea is similar to in-context learning for language models, but for tables. It has seen many tabular tasks during pretraining and can make predictions on a new table.

I would explain Random Forest like this:

> Random Forest is our classic baseline. It trains many decision trees and averages their predictions.

The important teaching point:

> We are not comparing these models in isolation. They are connected to the same live inputs. If I change the features or sample size, both models rerun under the same conditions.

The notebook computes predicted probabilities:

```python
tabicl_proba = tabicl.predict_proba(X_test)
rf_proba = rf.predict_proba(X_test)
```

`proba[:, 1]` means the predicted probability of the positive class, which is income `>50K`.

---

### 3.7 Let's Explain ROC AUC

Now we compare the models using ROC AUC.

I would say:

> ROC AUC measures how well the model ranks positive examples above negative examples across all possible thresholds.

The rough interpretation:

- `1.0` means perfect ranking
- `0.5` means random guessing

Why not just use accuracy?

> Accuracy depends on one fixed threshold, usually 0.5. ROC AUC looks across thresholds, which is useful when the classes are imbalanced.

This dataset is imbalanced because most people in the dataset earn `<=50K`.

The bar chart gives us a quick model comparison, but the point is not only the score. The point is that the score updates when the feature selection or sample size changes.

---

### 3.8 Let's Look at Predicted Probability Histograms

Next, the notebook shows probability histograms for both models.

I would explain:

> The histograms show how confident each model is. For each row, the model outputs a probability of income `>50K`.

What we want to see:

- rows that are truly `>50K` should be pushed toward higher probabilities
- rows that are truly `<=50K` should be pushed toward lower probabilities

If the two groups overlap a lot, the model is less confident or the task is harder.

This is useful because two models can have similar ROC AUC but different probability behavior.

---

### 3.9 Let's Do Interactive Error Analysis

Now we close the loop from model scores back to the actual rows.

The notebook gives us three controls:

```python
model_source = mo.ui.radio(...)
threshold_slider = mo.ui.slider(...)
model_view = mo.ui.radio(...)
```

The model radio chooses which model to inspect:

- TabICL
- Random Forest

The threshold slider controls how probabilities become hard predictions.

For example:

- if the threshold is `0.5`, a probability of `0.73` becomes predicted `>50K`
- if the threshold is `0.8`, that same row still has high probability, but it may not be high enough for a positive prediction

The error-type radio lets us inspect:

- all errors
- false positives
- false negatives

I would define them clearly:

> A false positive means the model predicted `>50K`, but the true label was `<=50K`.

> A false negative means the model predicted `<=50K`, but the true label was `>50K`.

The summary table updates with:

- correct predictions
- all errors
- false positives
- false negatives

Then the row table shows actual misclassified examples.

The teaching point:

> This is where interactivity becomes practical. We are not just asking, "what is the score?" We are asking, "which rows did the model get wrong, and how does that change when I move the threshold?"

---

### 3.10 Wrap-Up

I would close Module 3 like this:

> In this module, we saw one reactive ML workflow. We started with raw data, explored it visually, used widgets to choose features and sample size, trained two models, compared ROC AUC and probability behavior, and then inspected errors by changing the threshold. The key idea is that all of these steps are connected.

The key takeaways:

- marimo renders dataframes as useful interactive tables.
- UI widgets can drive real modeling pipelines.
- Downstream cells update automatically from `.value`.
- Interactivity makes model comparison faster and more explainable.
- Error analysis becomes easier when the threshold, model choice, and table are connected.

Now we will end with a few quiz questions.

## Quick Reference

| Goal | Command |
|------|---------|
| Edit notebook | `marimo edit --sandbox 3_1_interactive_ml_workflow.py` |
| Show dataframe viewer | put `df` as the last expression in a cell |
| Show plain dataframe | `mo.plain(df.head())` |
| Editable table | `mo.ui.data_editor(df)` |
| Visual exploration | `mo.ui.data_explorer(df)` |
| Interactive dataframe | `mo.ui.dataframe(df)` |
| Feature selector | `mo.ui.multiselect(...)` |
| Slider control | `mo.ui.slider(...)` |
| Radio control | `mo.ui.radio(...)` |
