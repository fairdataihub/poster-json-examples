# A Workflow for Protein Function Discovery

Alisa Surkis, PhD, MLS¹; Aileen M. McCrillis, MSLIS¹; Richard McGowan, MLS¹; Brian L. Schmidt, DDS, MD, PhD²

¹NYU Health Sciences Libraries, New York University School of Medicine, New York, NY  
²Bluestone Center for Clinical Research, New York University College of Dentistry, New York, NY

Contact: Alisa.surkis@med.nyu.edu | 212-263-2953

DOI: 10.5281/zenodo.4519718  
Presented at AMIA Joint Summits on Translational Science 2013

## Abstract

A workflow is presented for identifying from within a large set of proteins, those that have been identified in the literature as being associated with one of a set of concepts related to cancer pain. The workflow uses the programming utilities available through NCBI for accessing their linked databases from within a Matlab programming environment to replace a formerly time-intensive manual process with a much more efficient automated process.

## Introduction

In a study undertaken to define the repertoire of peptides and proteases that produce pain in the cancer microenvironment of oral cancer patients, a protein chemist identifies proteins by a discovery approach producing several hundreds of candidate molecules. Likely candidates for involvement in the pain process are selected based on published studies of these proteins. The search for literature on protein function had been done manually — a cumbersome and time-intensive approach. A team of librarians was brought in to collaborate to overcome this information management challenge.

## Methods

The method being used was keyword searching in PubMed and Google Scholar — too time consuming and not making use of advanced searching features.

An automated search methodology was introduced that programmatically accessed the linked NCBI databases through the Entrez programming utilities (NCBI 2010). Databases could then be automatically queried and linkages between databases exploited.

## Results

An automated workflow was established to discover which identified proteins were associated with terms related to cancer pain, or to pain more generally, and to identify those proteins with no published literature regarding their function.

Workflow from protein name (P_N) through protein identifier (P_UID) to relevant papers (PMID) that were then searched for each relevant search term (S) to establish a measure of known associations (∑S).

The final output was an Excel table of size N × (2×M), where N = number of proteins and M = number of concepts. For each protein: total number of papers containing the concept, plus a column with the PubMed IDs.

## Conclusions

This technique provides a practical means of doing a more comprehensive survey of literature on known functions of a large list of identified proteins.

## Next Steps

- Filtering results by impact factor (as proxy for reproducibility)
- Finding proteins with concepts joined through common peptide/protease

## Acknowledgements

Supported by National Library of Medicine grant R01DE019796-03S1.

## References

Hardt M, Lam DK, Dolan JC, Schmidt BL. (2011). Surveying Proteolytic Processes in Human Cancer Microenvironments by Microdialysis and Activity-based Mass Spectrometry. Proteomics Clinical Applications 5(11-12):636–43.

NCBI. (2010). Entrez Programming Utilities Help. Bethesda (MD): NCBI. http://www.ncbi.nlm.nih.gov/books/NBK25501/.
