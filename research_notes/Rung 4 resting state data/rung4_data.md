# Rung 4 data survey: resting-state targets for the MaleCNS brain

Compiled 26 Sep 2026 by a research agent for brainfly's rung 4. "Verified" means it opened the files or the API listing itself. PP = preprint. The files were downloaded to a temporary folder; get them again from the sources cited.

**Bottom line**
- Only one public dataset is a true resting state with per-fly region time series: **Turner, Mann & Clandinin 2021**. It has 20 immobilized female flies, stimulus-free, in an Ito-atlas parcellation, with a precomputed FC matrix. Wang et al. 2026 trained its FlyWire LIF model on this same data.
- **Brezovec 2024 (DANDI 000727)** is whole-brain voxel data from flies walking on a ball. It has no region series and no FC. It would make a good second, out-of-condition test set.
- **MaleCNS has public neuron-by-ROI synapse tables that need no token.** Its ROI names are the hemibrain/Ito 2014 abbreviations, so the Ito-atlas regions map across by name.
- Calcium FC carries no absolute rate. The ≤4 Hz mean has to come from electrophysiology targets (§3).
- No whole-brain resting-state dataset indexed to connectome neuron IDs or types exists (§4).

---

## 1. Resting-state and whole-brain datasets

### 1a. Turner, Mann & Clandinin 2021 (the one to fit)
- **Paper:** Curr Biol 31:2386–2394, [doi:10.1016/j.cub.2021.03.004](https://doi.org/10.1016/j.cub.2021.03.004) ([PMC8519013](https://pmc.ncbi.nlm.nih.gov/articles/PMC8519013/)). Preprint: [bioRxiv 10.1101/2020.12.11.422105](https://doi.org/10.1101/2020.12.11.422105).
- **Data:** public on figshare, [doi:10.6084/m9.figshare.13349282](https://doi.org/10.6084/m9.figshare.13349282) (v3, 23 Feb 2021, MIT licence). Code: [github.com/mhturner/SC-FC](https://github.com/mhturner/SC-FC).
- **Flies:** 20 females, 5 days old. Genotype R57C10 (nSyb)-GAL4 > GCaMP6s + myr::tdTomato, pan-neuronal.
- **Preparation:** immobilized, central brain exposed from the anterior. The imaging protocol is cited to Mann 2017: darkness, no stimuli.
- **Imaging:** 2-photon, 3 µm isotropic, **1.2 Hz**. Each fly has 2,000 frames (≈28 min; the paper says "~25 min"); flies 2017-11-08_1 and _2 have 4,000.
- **Atlas:** the Ito et al. 2014 neuropil atlas from Virtual Fly Brain, on the JFRC2 template, warped into each fly with CMTK.
  - The label file has 86 indices, 75 of them named.
  - The paper analyses 37 regions that lie inside the hemibrain, and a finer Branson/Panser atlas cut to 295 segments.
- **Files** (tarball `data_TurnerMannClandinin.tar.gz`: 245.7 MB compressed, 4.45 GB unpacked; paths below are inside it unless noted):

| File | What it is |
|---|---|
| `data/subsample/subsample_CorrelationMatrix_Full.pkl` | **Processed FC.** pandas 37×37 matrix: mean Fisher-z FC over 20 flies, diagonal NaN, values −0.04 to 1.07. I recomputed it from the raw series with SC-FC's `getCmat` recipe (1st-order Butterworth high-pass at 0.01 Hz, fs = 1.2 Hz, drop the first 100 frames, plus 3 fly-specific trims); the result matches to 4e-15. |
| `data/subsample/subsample_cmats_full.npy` | (20, 37, 37) per-fly z-FC. Its mean equals the .pkl. The fly order is not recorded. |
| `CorrelationMatrix_branson.csv` (figshare top level, 1.7 MB) | 295×295 mean FC on Branson segments. The headers give only the parent region name, repeated. `StructuralMatrix_branson.csv` (0.4 MB) is the matching SC. |
| `data/ito_responses/ito_<date>_<n>.pkl` (20 files, 26 MB) | **Raw region time series.** Rows are atlas label numbers (0 = outside the atlas; 72–75 rows per fly); columns are frames of raw mean fluorescence, not ΔF/F. |
| `data/branson_responses/branson_<fly>.pkl` (20 files, 244 MB) | The same series for the 999 Branson segments. |
| `data/ito_68_atlas/Original_Index_panda_full.csv` | Label number → name. WED_L is called **IVLP_L** in this file. |
| `data/ito_68_atlas/vfb_68_<fly>.nii.gz` | Each fly's registered atlas mask. |
| `data/template_brains/ito_2018.nii.gz` | The Ito atlas on the JRC2018F 0.38 µm grid (1652×768×479). `2018_999_atlas.nii.gz` is the Branson atlas on the same grid. |
| `registration.xform.zip` (figshare top level) | CMTK transform from JFRC2 to JRC2018F. |
| `data/connectome_connectivity/*_computed_20210114.pkl` | Hemibrain v1.2 SC, 36×36 (the two IB regions merged): cell count, T-bars, weighted synapses. |

- **Region coverage in the series:** 74 named regions across both hemispheres; LOP_L is absent.
  - All **67 non-optic regions are present in every fly.** The 4 optic regions LOP_R, ME_R, AME_L and ME_L are missing in some flies.
  - The paper used only 37 regions because the hemibrain covers one hemisphere. MaleCNS removes that restriction.

### 1b. Brezovec et al. 2024 (DANDI 000727)
- **Paper:** Curr Biol 34:710–726, [doi:10.1016/j.cub.2023.12.063](https://doi.org/10.1016/j.cub.2023.12.063). Preprint: [bioRxiv 10.1101/2022.03.20.485047](https://doi.org/10.1101/2022.03.20.485047).
- **Data:** public on DANDI, [dandiset 000727 v0.240106.0043](https://dandiarchive.org/dandiset/000727/0.240106.0043) ([doi:10.48324/dandi.000727/0.240106.0043](https://doi.org/10.48324/dandi.000727/0.240106.0043)), CC-BY-4.0.
  - 609.6 GB in total: **9 NWB files of 66.6–69.0 GB each**, plus 9 FicTrac .avi videos of 0.15–0.23 GB.
- **Flies:** 9 females, 3–4 days old. Genotype w+; UAS-myr::tdTomato/UAS-GCaMP6f; nSyb-Gal4/+.
  - They were head-fixed in darkness on an air-supported ball, walking or resting spontaneously. They were **not immobilized**.
- **Imaging:** GCaMP6f at **1.88 Hz**, 3,384 volumes (30 min) per fly.
  - Voxels are 128×256×49 at 2.55×2.67×5 µm (the paper says 2.6×2.6×5 µm). The field covers the whole brain, including most of the optic lobes.
- **Inside each NWB** (verified via the Neurosift LINDI index):
  - `acquisition/TwoPhotonSeriesFunctionalGreen` and `…Red`: raw uint16.
  - `TwoPhotonSeriesAnatomical*`: 100 repeats of 1024×512×241 at about 0.65×0.67×1 µm.
  - `processing/ophys/TwoPhotonSeriesFunctionalGreenProcessed`: float32, 3384×314×146×91, described as "motion corrected high-pass temporal filtered z-scored and registered into … the Functional Drosophila Atlas". From the grid sizes, I infer this is the FDA extent (628×292×182 µm) at 2 µm.
  - `processing/behavior/FicTrac`: 90,000 samples (50 Hz).
  - **There are no ROI or region time series and no FC matrices.** The paper's 98,000 supervoxels (2,000 per z-slice) were not deposited.
- **Getting regions:**
  - The FDA template and its transforms to and from JRC2018F are in BIFROST (Brezovec et al., PNAS 2024, [doi:10.1073/pnas.2322687121](https://doi.org/10.1073/pnas.2322687121), [PMC11588091](https://pmc.ncbi.nlm.nih.gov/articles/PMC11588091/)), deposited at [Dryad doi:10.5061/dryad.8pk0p2nx1](https://doi.org/10.5061/dryad.8pk0p2nx1) (40.9 GB). That deposit holds three FDA volumes of 2.43 GB each (thresholded, unthresholded, NIfTI-1-compliant), `thresholded_FDA_to_JRC2018_female.h5` (13.8 GB), and ANTs "recapitulated" transforms in both directions (6.7 GB each).
  - **Ready-made FDA-space atlases** are in Okuno et al.'s [flywalk](https://github.com/takuto-okuno-riken/flywalk) repository:
    - `atlas/jrc2018f_2010roiCal_invFDACal.nii.gz`: the same 75-label Ito index as Turner, on a 256×128×49 grid covering the same extent.
    - `atlas/hemiFlyem52atlasCal.nii.gz`: 52 hemibrain primary ROIs.
    - `atlas/hemiroi/roi1–114.nii.gz` with `data/hemiroi.xlsx`: 114 hemibrain ROIs.
  - Okuno et al. computed FC for 8 of the flies in their paper ([bioRxiv 10.1101/2025.07.01.662601](https://doi.org/10.1101/2025.07.01.662601), **PP**; now an eLife reviewed preprint). Their 9.8 GB demo zip is on Zenodo ([10.5281/zenodo.15532271](https://doi.org/10.5281/zenodo.15532271)); the download returned 403, so I did not verify its contents.

### 1c. Mann, Gallen & Clandinin 2017
- **Paper:** Curr Biol 27:2389–2396, [doi:10.1016/j.cub.2017.06.076](https://doi.org/10.1016/j.cub.2017.06.076) ([PMC5967399](https://pmc.ncbi.nlm.nih.gov/articles/PMC5967399/)).
- **Flies:** 18 females, 5 days old, nSyb-GAL4 > GCaMP6m + tdTomato.
- **Imaging:** 128×128×25 voxels of 2.6×2.6×7.5 µm at **1.91 Hz**, 2,000 frames (17.4 min) per session; 10 flies had two sessions.
- **Conditions:** darkness, antennae and proboscis removed, legs glued.
- **Regions:** the same VFB Ito/JFRC2 atlas, with **61 regions** analysed. Of the 75, 14 were dropped: the optic lobes, BU, CAN, IPS_L and GA_L.
- **Public data:** mostly not. [Mendeley Data 10.17632/8b6nw2xxhn.1](https://doi.org/10.17632/8b6nw2xxhn.1) holds only:
  - `anatomical.zip` (324 MB): template, atlas and alignments.
  - `roi_timeseries_data.zip` (2.34 GB): the atlas plus **a single fly's** functional scan (`brain03gc6m.nii.gz`).
  - `sample_video.tif.zip` (1.19 GB).
  - There are no per-fly series and no FC matrices. Code: [cgallen/MannGallen_2017_CurrentBiology](https://github.com/cgallen/MannGallen_2017_CurrentBiology).

### 1d. Wang et al. 2026 (PMC12913608)
- **Paper:** "Model-agnostic linear-memory online learning in spiking neural networks", Nat Commun 2026, [doi:10.1038/s41467-026-68453-w](https://doi.org/10.1038/s41467-026-68453-w).
- **Data:** the Turner figshare above; their data statement cites 10.6084/m9.figshare.13349282.
- **Their description** says GCaMP6s, 1.2 Hz, "approximately 17 minutes per recording", **68 regions** and an 80/20 train/test split in time. The 17 minutes looks borrowed from Mann 2017, since Turner's 2,000 frames at 1.2 Hz last about 28 min. I did not work out which 68 regions they kept.
- **Code:** [chaobrain/fitting_drosophila_whole_brain_spiking_model](https://github.com/chaobrain/fitting_drosophila_whole_brain_spiking_model).
  - It fits one Turner fly at a time (default `2017-10-26_1`).
  - Its inputs are preprocessed files on a Google Drive: `spike_rates/ito_<fly>_spike_rate.npz`, and `783_connections_processed.csv`, which has a per-connection `neuropil` column.
  - A neuropil's rate is the synapse-weighted mean of the rates of presynaptic neurons connecting in that neuropil.
  - Deconvolved rates are scaled to a 120 Hz maximum, so they are arbitrary units.
- **Follow-up:** Li, Ping, Zhang & Wang, [bioRxiv 10.64898/2026.08.21.745055](https://doi.org/10.64898/2026.08.21.745055) (**PP**). It fits the same kind of spontaneous recordings; I did not check which dataset.

### 1e. Other public whole-brain sets with rest epochs (none of them immobilized resting state)

| Dataset | Scope | Where |
|---|---|---|
| Schaffer et al. 2023, Nat Commun ([PMC10495430](https://pmc.ncbi.nlm.nih.gov/articles/PMC10495430/)) | SCAPE, dorsal third of the central brain; nuclear GCaMP6s; females; 8–12 vol/s; single-cell ROIs with no cell types; flies quiescent ~50% of the time | [figshare 10.6084/m9.figshare.23749074](https://doi.org/10.6084/m9.figshare.23749074), 48 NWB files, 4.1 GB |
| Aimon et al. 2023, eLife ([PMC10168698](https://pmc.ncbi.nlm.nih.gov/articles/PMC10168698/)) | Light-field whole brain, pan-neuronal plus neuron-class GAL4 lines; spontaneous walk, forced walk and rest | [Dryad 10.5061/dryad.3bk3j9kpb](https://doi.org/10.5061/dryad.3bk3j9kpb): regional time series, 0.96 GB |
| Gauthey et al. 2026, Nat Commun ([PMC13328740](https://pmc.ncbi.nlm.nih.gov/articles/PMC13328740/)) | Light-beads microscopy, 28 vol/s whole brain; females walking, with auditory stimuli | [Zenodo 10.5281/zenodo.17618684](https://doi.org/10.5281/zenodo.17618684), 48.8 GB preprocessed |
| Mann, Deny, Ganguli & Clandinin 2021, Nature ([PMC10544789](https://pmc.ncbi.nlm.nih.gov/articles/PMC10544789/)) | Whole-brain activity and metabolism | **On request only** |

---

## 2. Mapping MaleCNS neurons onto the imaging regions

**Public files with neuron-by-ROI synapse counts, no token needed** (all verified):

| File (`gs://flyem-male-cns/v1.0/…`) | Size | Contents |
|---|---|---|
| `database/neuprint-inputs/roi_elements.feather` | 3.68 GB | **The table to use.** Columns `body, roi, pre, post, downstream, upstream, synweight`; 353.7 M rows. Every ROI level is included. The `<unspecified>` row is the whole-body total, and the primary-ROI rows sum to it. |
| `database/neuprint-inputs/Neuprint_Neurons.feather` | 4.65 GB | One row per body (88.4 M): the `roiInfo` JSON (the same field neuPrint serves), plus all annotations and transmitters. |
| `database/neuprint-inputs/Neuprint_Neuron_Connections.feather` | 3.53 GB | **Per-ROI connectivity.** 151.9 M body pairs with `weight, weightHP, weightHR` and a per-connection `roiInfo`, e.g. `{"SAD(-AMMC)":{"post":1},…}`. Also available as a 16.9 GB CSV. |
| `database/neuprint-inputs/Neuprint_Meta.csv` | 1.2 MB | The primary ROI list, the ROI hierarchy and dataset-wide totals per ROI. |
| `connectome-data/flat-connectome/syn-points-…-minconf-0.5.feather` | 13.1 GB | One row per pre- or post-synaptic site, with body, xyz, `primary`/`subprimary`/`superprimary` ROI and optic-lobe column/layer. Use it for spatial splits. |
| `connectome-data/flat-connectome/syn-partners-…-minconf-0.5.feather` | 6.8 GB | 311.8 M synapse pairs with the `primary_post` ROI. |

- `body-stats` and `connectome-weights` carry **no** ROI information.
- The whole neo4j database is at `v1.0/database/neo4j`, and ROI volumes are at `gs://flyem-male-cns/rois/fullbrain-roi-v4` (also v4.1 and v5).
- **Filter** `roi_elements` to the primary ROIs and to annotated bodies (the 211,577 bodies in `body-annotations`); otherwise the hierarchy levels are double counted.
- **neuPrint `male-cns:v1.0`** gives the same data but needs a free token. `roiInfo` is on every Neuron node; `neuprint-python`'s `fetch_neurons` returns a `roi_counts_df`, and `fetch_adjacencies(rois=…)` returns per-ROI connection weights.

**MaleCNS ROI names:**
- There are 144 primary ROIs:
  - **80 brain neuropils**;
  - `CentralBrain-unspecified` (6.05 M postsynapses), `Optic-unspecified(L/R)` and `CV-unspecified`;
  - 23 VNC neuropils plus `VNC-unspecified`;
  - 36 nerves.
- Brain names are the hemibrain/Ito abbreviations with an `(L)`/`(R)` suffix, e.g. `SMP(R)`. Midline ROIs have no suffix: `EB, FB, PB, NO, IB, GNG, PRW, SAD`.
- The mushroom body is split into `CA, PED, a'L, aL, b'L, bL, gL`.
- Sub-ROIs include:
  - AL glomeruli (`AL-DA1(R)` etc.);
  - `EBr*`, `FBl1–9`, `PB(L1)–(R9)`, `NO1–3`;
  - `GA(R)` inside LAL, `AMMC(L/R)` inside SAD, `ROB/RUB` inside CRE;
  - optic-lobe columns and layers.
- The brain ROI volume was "initialized via transfer from ROIs in JRC2018M and refined manually" ([bucket README](https://storage.googleapis.com/flyem-male-cns/README_RELEASE_BUCKET.md)). It therefore uses the same Ito 2014 nomenclature as the JFRC2/JRC2018 atlases, but its boundaries are not identical to the Ito atlas warped into each fly.

**Ito label (Turner/VFB) → MaleCNS ROI.** Most labels are a direct rename (`AL_R` → `AL(R)`, `SMP_L` → `SMP(L)`, `EB` → `EB`, `GNG` → `GNG`). The exceptions:
```python
ITO_TO_MCNS_EXCEPTIONS = {
  'MB_CA_R': ['CA(R)'], 'MB_PED_R': ['PED(R)'],
  'MB_VL_R': ["a'L(R)", 'aL(R)'], 'MB_ML_R': ["b'L(R)", 'bL(R)', 'gL(R)'],  # same for _L
  'FB': ['FB', 'AB(L)', 'AB(R)'],            # AB has no Ito label; Turner folded it into FB
  'LAL_R': ['LAL(-GA)(R)'], 'GA_R': ['GA(R)'],  # GA is its own Ito label
  'SAD': ['SAD(-AMMC)'], 'AMMC_R': ['AMMC(R)'],
  'IB_R': ['IB'], 'IB_L': ['IB'],            # MaleCNS IB is one ROI: split by syn-points x, or merge (Turner merged)
  'IVLP_L': ['WED(L)'],                      # old name in the VFB label file
}
```
- MaleCNS ROIs with no Ito counterpart: `LA(L/R)`, the `*-unspecified` ROIs, and the VNC.
- For the hemibrain, Turner's own mapping is `bridge.getRoiMapping()` in SC-FC; it applies to MaleCNS names unchanged.

**Spatial route** (for the Branson segments, or to cross-check the names; I have not run it):
1. Transform MaleCNS synapse coordinates to JRC2018F with navis-flybrains (`JRCFIB2022M` → JRC2018M → JRC2018U → JRC2018F). The bucket also has MaleCNS skeletons already in JRC2018U.
2. Look up the label in Turner's `ito_2018.nii.gz` or `2018_999_atlas.nii.gz`.
3. For the DANDI data, continue from JRC2018F to the FDA with BIFROST's ANTs transform, or use Okuno's FDA-space atlases.

**Forward model to compare with the data:**
- For each region r, the predicted signal is F_r(t) = Σ_i w_ir·(k∗s_i)(t) / Σ_i w_ir. Here w_ir is neuron i's pre + post synapse count in r (from `roi_elements`), s_i is its spike train, and k is a GCaMP6s kernel.
- Then downsample to 1.2 Hz, high-pass at 0.01 Hz, drop the first 100 frames, take Pearson correlations and Fisher-z them.

---

## 3. Measured spontaneous rates for per-type targets

| MaleCNS type | Rate at rest | Condition | Source |
|---|---|---|---|
| DM4 ORNs (Or59b) | 3.44 ± 0.16 Hz (n = 11) | in vivo | [Kazama & Wilson 2009, PMC2751859](https://pmc.ncbi.nlm.nih.gov/articles/PMC2751859/) |
| AL projection neurons | "typically 1–5 spikes/s" with no odour | in vivo cell-attached/whole-cell | same |
| Kenyon cells | ≈0: "most cells had a baseline rate of zero" | in vivo whole-cell | [Gruntman & Turner 2013, PMC3908930](https://pmc.ncbi.nlm.nih.gov/articles/PMC3908930/) |
| **MBON11** (γ1pedc>α/β) | **37.2 ± 2.0 Hz** | 1 kHz pAce voltage imaging; head-fixed on a trackball, able to walk; females 3–8 d; n = 20 flies per type (mean ± s.e.m.) | [Huang et al. 2024 Nature, PMC11525173](https://pmc.ncbi.nlm.nih.gov/articles/PMC11525173/), Source Data for Fig. 1d,e |
| MBON12 (γ2α′1) / MBON13 (α′2) / MBON14 (α3) / MBON17 (α′3m) / MBON18 (α2sc)* | 21.5 ± 0.7 / 16.5 ± 1.0 / 15.5 ± 0.8 / 13.4 ± 0.6 / 10.9 ± 1.0 Hz | same | same |
| **PPL101** (PPL1-γ1pedc) | **20.1 ± 1.0 Hz** | same | same |
| PPL1-γ2α′1 / -α′2α2 / -α3 / -α′3* | 11.8 ± 0.6 / 9.3 ± 0.4 / 14.8 ± 0.9 / 9.8 ± 1.3 Hz | same | same |
| PEN_a (P-EN) | 3.9 ± 2.6 Hz while standing; rises by 5.6 ± 3.7 Hz in fast preferred-direction turns (N = 12) | in vivo loose patch, fly on a ball | [Turner-Evans et al. 2017, PMC5440168](https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/) |
| EPG | No spike rate in any text I could read. **Bump:** a single bump, ~100° FWHM in calcium imaging, that persists without visual or self-motion cues | calcium imaging, fly on a ball | Turner-Evans 2017; [Seelig & Jayaraman 2015, PMC4704792](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/) |
| DNa02, DNg13 | "typically very low" when not walking. DNa02's stride-locked modulation of ~15 Hz is ≈10% of its dynamic range (so ~150 Hz); it hyperpolarizes when the fly stops | in vivo whole-cell, walking | [Yang et al. 2024 Cell, PMC12778575](https://pmc.ncbi.nlm.nih.gov/articles/PMC12778575/); [Rayshubskiy et al. 2025 eLife, PMC12279373](https://pmc.ncbi.nlm.nih.gov/articles/PMC12279373/) |
| DNp07 / DNp10 | 0.017 ± 0.06 / 0.003 ± 0.017 Hz when not flying | tethered patch; grooming, air-walking or quiescent | [Ache et al. 2019 Nat Neurosci, PMC7444277](https://pmc.ncbi.nlm.nih.gov/articles/PMC7444277/) |
| DNp01 (giant fiber) | ≈0: it depolarized to looming but did not spike | head-fixed whole-cell | [Dombrovski et al. 2023, PMC9849133](https://pmc.ncbi.nlm.nih.gov/articles/PMC9849133/) |
| Leg MNs (tibia flexor) | Fast and intermediate MNs silent. Slow MN **≈30 Hz**. Resting potentials −68 / −60 / −48 mV | in vivo whole-cell, fly at rest | [Azevedo et al. 2020 eLife, PMC7347388](https://pmc.ncbi.nlm.nih.gov/articles/PMC7347388/) |
| Neck MNs | **None found.** Gorko et al. 2024 (Nature) characterize them by activation only | — | — |

\* The paper names MBONs and DANs by compartment. I assigned the MBON12–18 numbers from the hemibrain naming (Li et al. 2020), and the counts per side in MaleCNS are consistent. The PPL1 numbering is not verified; check it against MaleCNS `roiInfo`.

- **DNa02 raw data:** [Harvard Dataverse 10.7910/DVN/0NCLP1](https://doi.org/10.7910/DVN/0NCLP1) has recordings at 4 kHz with ball velocity. A quick, unvalidated re-detection on 2 cells gave a median of 0 spikes/s in still 1-s bins (means 0.8 and 7.1 Hz).
- **Not found:** PAM DAN rates from electrophysiology.

---

## 4. Whole-brain resting state at cell-type resolution

**None exists that is indexed to connectome IDs or types**, as far as I could find (Sept 2026). The closest options:
- **BIFROST + DANDI 000727.** Transforms bring hemibrain or FlyWire synapses into the imaging space with ~5–10 µm precision, which gives candidate types per supervoxel, not IDs. Brezovec 2024 did this for the hemibrain (neuron × supervoxel synapse counts), but those intermediate files are not public.
- **Schaffer 2023.** Single-cell ROIs, but no cell types.
- **Aimon 2023.** Neuron classes defined by GAL4 lines, not connectome types.
- **Randel et al. 2025** ([bioRxiv 10.1101/2025.09.25.678485](https://doi.org/10.1101/2025.09.25.678485), **PP**). Whole-brain activity followed by EM of the same brain, with neurons identified, but in the **larva** and stimulus-evoked.
- **Targeted populations** outside whole-brain imaging: EPG/PEN, descending-neuron populations (Aymanns 2022), and flyvis's visual types.

---

## Recommendation

**Fit first to Turner 2021.**
- Target: the mean z-FC over the **67 non-optic Ito regions** in both hemispheres, recomputed from `data/ito_responses/*.pkl` with the SC-FC recipe.
- Hold out whole flies, e.g. train on 15 and test on 5.
- Also report the 37-region subset, to compare against Turner (SC–FC r = 0.74) and Wang 2026.

**Map regions by name** using `roi_elements.feather`, with the exceptions above for the MB lobes, AB, GA, AMMC and IB. Spot-check with the spatial route.

**Why this dataset:**
- It is the only public, stimulus-free, immobilized, multi-fly whole-central-brain dataset.
- The region series are already extracted, and the FC pipeline reproduces the published matrix exactly.
- Its atlas names match MaleCNS ROIs one to one.
- The recipe has already been run on a FlyWire LIF model.

**Set absolute rates separately**, because FC is scale-free:
- impose a mean ≤4 Hz;
- use the §3 targets: KCs and descending neurons ≈0, PNs 1–5 Hz, P-EN ≈4 Hz, MBONs and PPL1 10–37 Hz, slow MNs ≈30 Hz;
- use the EPG bump as a separate check.

**Then test out of condition on DANDI 000727.** Use still epochs selected from FicTrac, and Okuno's FDA-space Ito atlas. That data differs from the fitting set in indicator (GCaMP6f), state (awake) and coverage (includes the optic lobes).

**Caveats:**
- All imaging flies are female; MaleCNS is male.
- Mann's protocol removed the antennae, so decide whether ORNs should be silent or at their spontaneous rate.
- Calcium sampled at 1.2 Hz constrains slow correlations only, not spike timing.
