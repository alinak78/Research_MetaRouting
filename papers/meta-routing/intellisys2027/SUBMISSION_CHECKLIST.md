# IntelliSys revision and submission checks

Checked against the official CFP and conference-supplied LaTeX template on 2026-10-30:
https://saiconference.com/IntelliSys/CallforPapers

## Completed technical and editorial checks

- [x] Introduced the LLM-agent motivation and the deliberate isolation of controller decision logic. Qualified “lower-bound” as a simplified engineering test, not a mathematical guarantee or measured agent-transfer claim.
- [x] Split Section 6 into prospective main and exploratory boundary-condition analyses. Retained the original frozen experiment record, policies, and results.
- [x] Distinguished main (M) and exploratory (E) rows in Table 3 and groups in Figure 3. Connected the shared-fault main result to its analytical expectation without reclassifying the later extension as prospective.
- [x] Added actionable semantic/invariant checks and fault-diversity considerations as untested design proposals, with invocation costs requiring explicit accounting.
- [x] Used the official, unmodified `svproc.cls`, its accompanying styles, and the Springer bibliography style. Body text uses embedded Times New Roman fonts. No page-margin or type-size reductions were introduced.
- [x] Exported a PDF with blank author metadata and no author identities, author-affiliation strings, emails, owner paths, or identifying repository URLs detected in extracted text, metadata, or links. Names in ordinary cited literature are retained. The related submission is cited anonymously.
- [x] Verified a 201-word abstract; 15 pages total; references begin on page 15. The entire PDF is below the 18-page main-text allowance, with one page containing references and no appendices.
- [x] Verified all 11 references are cited and all three figures and three tables are uniquely numbered and referenced in the text.
- [x] Enlarged figure text and legends at approximately final text width, kept vector output, and moved Figure 2 before the next results subsection. Charts distinguish series by line style/markers as well as color.
- [x] Checked the latest rendered pages for overlap, clipping, table overflow, caption length, and figure readability. The LaTeX build reports no warnings, unresolved references, or overfull boxes.
- [x] Verified the saved summaries against both main and exploratory execution traces and checked paired fault schedules, budget compliance, and frozen source/data hashes. All seven standalone study tests pass.
- [x] Retained an accurate GenAI disclosure covering design, code, analysis, drafting, and figure assistance. This is a disclosure check, not certification of policy eligibility.

## Human-author and venue review still required

- [ ] Human authors must critically review and edit the entire manuscript and substantively develop and take responsibility for the scientific ideas, arguments, results, and conclusions. IntelliSys restricts the permitted role of GenAI; the disclosed assistance goes beyond language refinement, so disclosure and a final read alone cannot certify eligibility. Resolve this with the organizers as needed; do not narrow the declaration inaccurately.
- [ ] Assess originality against the authors' relevant published work and disclose the related manuscript under review through the venue's permitted anonymous procedure. Textual difference and new experiments alone do not settle publication-overlap rules.
- [ ] Confirm that the anonymized companion reference and any confidential accompanying manuscript satisfy the submission portal/chairs' instructions.
- [ ] Complete final author proofreading and submit only the anonymous PDF for initial review. Add complete author information only to the camera-ready version if accepted.

The editorial revision does not guarantee acceptance. The exact main and exploratory numerical outcomes remain those in the archived experiments; no new experiment was conducted to support the positioning changes.
