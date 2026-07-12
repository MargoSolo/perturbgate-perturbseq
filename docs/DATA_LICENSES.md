# Data licenses

This project uses a permissive license (**MIT**) for its original code. It does
**not** relicense upstream data. Source datasets retain their upstream licenses;
derived-data redistribution follows the source terms; literature and database
content are cited, not republished.

## Code

- **Original code** in this repository: **MIT** (see [`../LICENSE`](../LICENSE)).
  Chosen because it is permissive and matches the license of the primary dataset's
  analysis code, minimising friction for reuse.

## Data

### Primary Human CD4+ T Cell Perturb-seq — MIT

- **License:** MIT (copyright Emma Dann, 2025), as stated on the CZI Virtual Cell
  Models dataset page and in the analysis repository's `LICENSE` file
  (https://github.com/emdann/GWT_perturbseq_analysis_2025).
- **Verification source:** the repository `LICENSE` file + the Virtual Cell Models
  dataset page.
- **Redistribution:** permitted with retention of the copyright notice and license
  text, and subject additionally to the CZI Virtual Cell Models Acceptable Use
  Policy. MIT is a software license applied here to a dataset; treat redistribution as
  governed jointly by MIT and that Acceptable Use Policy.
- **What we redistribute:** derived per-gene aggregate knockdown log2FC vectors only.

### JIA synovial single-cell atlas — CC-BY-4.0

- **License:** CC-BY-4.0, the CZ CELLxGENE Discover platform-wide license: published
  datasets can be downloaded, shared, and used "without restriction beyond providing
  attribution to the original data contributor(s)."
- **Verification source:** CELLxGENE documentation on contributing and publishing
  data (platform-wide CC-BY-4.0). **Caveat:** the per-dataset `license` field returned
  by the CELLxGENE curation API for this collection was null, so we rely on the
  platform-wide policy rather than a dataset-specific string.
- **Redistribution:** permitted, including derivative works (our disease vectors),
  with attribution to the original contributors (Knight et al.; and Bolton/Mahony et
  al. for the synovial-tissue layer).
- **What we redistribute:** derived per-gene aggregate disease-direction log2FC only.

## Attribution

Attribution for both datasets is given in [`../NOTICE`](../NOTICE),
[`../CITATION.cff`](../CITATION.cff), and this documentation. When reusing the derived
JIA vectors, cite both Knight et al. (global atlas) and Bolton/Mahony et al. (synovial
tissue). When reusing the derived Perturb-seq vectors, cite Zhu, Dann, … Pritchard &
Marson.

## Principle

"Publicly downloadable" is not assumed to mean "redistributable": both licenses above
were checked for redistribution terms, and only **derived aggregate** (non-cell-level)
data is committed. Where redistribution terms were unclear (the JIA per-dataset field),
the uncertainty is stated and the download-and-derive route is provided so that no user
depends on our committed copy.
