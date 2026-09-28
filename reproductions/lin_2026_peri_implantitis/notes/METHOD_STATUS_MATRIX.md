# Method and Status Matrix

This matrix is updated after each executed module. `planned` means no scientific output has yet been generated.

| Module | Paper figure/conclusion | Paper-reported method | Missing information | Initial reconstruction choice | Classification | Status |
|---|---|---|---|---|---|---|
| PI count generation | foundational | Cell Ranger 7.0.0; GRCh38-2020-A | FASTQ and exact command unavailable | consume released filtered 10x H5 matrices without regenerating counts | PAPER-REPORTED METHOD | planned |
| PI archive integrity | foundational | Zenodo dataset | none for published archive checksum | verify published MD5 and record file inventory | USER/CODEX ANALYTICAL CHOICE | planned |
| Cell QC | Fig. 1 / Suppl. Fig. 1 | remove cells with mitochondrial fraction >25% | lower gene/count thresholds and gene counting convention | preserve 25% cutoff; derive conservative lower thresholds from sample QC and record them before filtering | METHOD-BASED RECONSTRUCTION | planned |
| Doublet removal | Fig. 1 / Suppl. Fig. 1 | doublets excluded | tool, expected rate and threshold | Scrublet per capture with expected rate based on recovered-cell loading; retain scores and thresholds | MODERNIZED IMPLEMENTATION | planned |
| Healthy reference | Fig. 1 / Suppl. Fig. 1 | integrate healthy gingiva; GSE164241 | exact samples and upstream object state | use gingival samples only; build from public raw/filtered counts and explicit metadata | METHOD-BASED RECONSTRUCTION | planned |
| Batch integration | Fig. 1a | scVI; Seurat/Scanpy; schard | scVI version, covariates, latent size, epochs, HVGs | current scvi-tools; sample/capture batch; 2,000 HVGs; latent dimension 30; seeded training; revise only with diagnostics | MODERNIZED IMPLEMENTATION | planned |
| Major-cell annotation | Fig. 1a | marker-based annotations shown | marker list/rules and source labels | combine canonical markers, source labels when defensible, and differential markers; retain uncertainty | METHOD-BASED RECONSTRUCTION | planned |
| Differential abundance | Fig. 1b–d | MiloR and edgeR | neighborhood parameters, design matrix and contrasts | donor-aware design; sample as observation only after donor relationship is encoded | METHOD-BASED RECONSTRUCTION | planned |
| Functional enrichment | paper-wide | GO and GSEA | gene-set release, ranking statistic, cutoffs | pin gene-set release and retain full ranked lists; no cell-level pseudoreplication | METHOD-BASED RECONSTRUCTION | planned |
| Spatial preprocessing | Fig. 2 | Space Ranger 1.3.1; GRCh38-2020-A | exact command and image parameters | consume released Space Ranger outputs; preserve coordinates/images/counts | PAPER-REPORTED METHOD | not started |
| Cell-type spatial mapping | Fig. 2 | cell2location | model settings and reference signature construction | current cell2location after 4A label validation; document priors and fit diagnostics | MODERNIZED IMPLEMENTATION | not started |
| Spatial programs | Fig. 2 | NMF/co-location | rank selection and initialization | evaluate ranks with seeded repeated fits and stability; select before biological interpretation | METHOD-BASED RECONSTRUCTION | not started |
| Neutrophil states | Fig. 3 | reclustering/markers and abundance comparisons | clustering and annotation parameters | subset from validated integrated object; state labels require marker evidence | METHOD-BASED RECONSTRUCTION | not started |
| CellChat | Fig. 4 | CellChat | database/version, filters and probability settings | reconstruct in an isolated R environment only after cell labels stabilize | METHOD-BASED RECONSTRUCTION | not started |
| COMMOT | Fig. 4 | COMMOT | database/version and spatial settings | run on validated spatial object; pin database and distance kernel | METHOD-BASED RECONSTRUCTION | not started |
| Trajectory | Fig. 5 | Slingshot | root, lineage and reduced-space choices | root and topology justified by marker/state evidence; sensitivity analysis | METHOD-BASED RECONSTRUCTION | not started |
| SCENIC | Fig. 5 | SCENIC | implementation/version, motif database and thresholds | choose pySCENIC or R SCENIC only after database availability audit | UNRESOLVED / UNAVAILABLE INFORMATION | not started |
| CellOracle | Fig. 5 | CellOracle | base GRN, promoter window and perturbation settings | audit compatible motif/base-GRN resources after trajectory validation | UNRESOLVED / UNAVAILABLE INFORMATION | not started |
| Figure reconstruction | Figs. 1–5 computational panels | plotted results | exact aesthetics and intermediate values | compare biological patterns and available quantities; do not equate visual similarity with exact reproduction | USER/CODEX ANALYTICAL CHOICE | not started |

