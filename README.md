# Research_MetaRouting

Standalone research on budgeted tool recovery and verification in intelligent workflows.

The study asks when a controller should retry, switch numerical engines, or seek agreement under a hard invocation budget, and how silent errors and shared corruptions affect answer acceptance. It uses UCI Iris, Wine, and Banknote Authentication data with executed SQLite, Python, and NumPy computations.

## Paper and artifacts

- [Research draft PDF](output/pdf/IntelliSys2027_Tool_Recovery_Draft.pdf)
- [Manuscript source and build instructions](papers/meta-routing/intellisys2027/README.md)
- [Research protocol](papers/meta-routing/intellisys2027/STUDY_PROTOCOL.md)
- [Study scope and related-submission disclosure](papers/meta-routing/intellisys2027/OVERLAP_AND_FEEDBACK.md)
- [Anonymous LaTeX source bundle](output/intellisys2027/IntelliSys2027_Anonymous_Source.zip)
- [Reproducibility bundle](output/intellisys2027/IntelliSys2027_Recovery_Reproducibility.zip)
- [Results and frozen development configuration](results/meta-routing/intellisys2027/)

## Verify the supplied run

```bash
pip install -e '.[dev]'
python -m pytest -q
PYTHONPATH=src python experiments/meta-routing/intellisys2027/prepare_paper.py
```

The supplied run contains 72 development and 72 test queries, with repeated fault schedules. The main evaluation and later exploratory collision sensitivity are identified separately. Runners refuse to silently overwrite existing evaluated traces; preserve the supplied run when conducting a fresh replication.

The manuscript remains a research draft requiring human-author review and appropriate related-submission disclosure. Dataset attribution and bundled third-party template notices are retained. No affiliation or endorsement is asserted by this repository.
