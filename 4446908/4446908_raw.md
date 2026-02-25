# An Exploration of Scientific Press Releases in the Context of Altmetrics

Oliver Hahn¹, Steffen Lemke¹

¹ZBW — Leibniz Information Centre for Economics  
Address: Düsternbrooker Weg 120, 24105 Kiel, Germany  
Email: o.hahn@zbw.eu | s.lemke@zbw.eu

DOI: 10.5281/zenodo.4446908  
Presented at altmetrics20 – The 2020 Altmetrics Workshop

## Introduction

Press releases are published by organizations to bring attention to achievements they have reached. In the scientific domain, research institutions, funders, and academic publishers use press releases to advertise newly published papers and particularly promising scientific results.

For altmetrics research, which analyzes the presence of scientific objects in various public domains like social media, news, or policy documents, press releases have been an almost unregarded albeit promising source of data (Bowman & Hassan, 2019). Previous studies have shown a strong association between a journal article receiving promotion in a press release and its later citations and altmetrics (Lemke, 2020).

Study goal: explore two large samples of science press releases to gain further insights on their contents, creators, and role in the communication of research.

## Dataset & Methods

Two samples of press releases published over one year between April 2016 and March 2017:
- 26,358 press releases from EurekAlert!  (average length: 755 words)
- 1,856 press releases from IDW-Online (average length: 724 words)

Two randomly chosen subsamples of 100 press releases each were used for content analysis by two independent raters. Inter-rater reliability: Cohen's kappa κ = 0.89.

## EurekAlert! & IDW-Online

EurekAlert!: Founded 1996 by the American Association for the Advancement of Sciences; 14,000+ registered journalists from 90+ countries.

IDW-Online: Founded 1995 by a coalition of press officers from German universities; 8,000+ registered journalists (predominantly German-speaking).

## Subjects / Disciplines

EurekAlert! disciplines (based on Scopus subjects of 10,483 journal articles promoted):
Life Sciences (13.95%), Health Sciences (12.79%), Medicine (12.59%), Biochemistry (9.27%), Genetics and Molecular Biology (9.27%), Physical Sciences (7.55%), Agricultural and Biological Sciences (5.20%).

IDW-Online disciplines (assigned by IDW):
Biology (13.67%), Medicine (11.13%), Environment and Ecology (7.76%), Chemistry (6.57%), Physics incl. Astronomy (6.35%).

## Topics

Most frequent word stems in press release titles (Porter Stemming Algorithm). EurekAlert! dominated by: research, cancer, patient, studi, brain, drug, cell, develop, scientist. IDW-Online dominated by: productprocess, treatment, grant, network, diseas, quantumatom, cell, climat, studi.

## Content Analysis — Press Release Texts

From each dataset, 100 random press releases were examined for mentions of:
- Methods (EurekAlert!: 67; IDW-Online: 62)
- Limitations (EurekAlert!: 18; IDW-Online: 18)
- Implications (EurekAlert!: 39; IDW-Online: 30)
- References (EurekAlert!: 3; IDW-Online: 6)
- No Research (EurekAlert!: 6; IDW-Online: 15)

## Content Analysis — Releasing Institutions

EurekAlert!: University (public) largest share; significant contribution from Publisher/Journal.
IDW-Online: University (public) largest share; significant contribution from Non-University Research Institutes.

## Conclusion & Future Work

- Press releases on both EurekAlert! and IDW-Online are dominated by life sciences, followed by physical sciences.
- They frequently describe featured studies' methodologies and practical implications; descriptions of limitations or references are less typical.
- Structurally, press releases are a comparatively homogeneous format of external science communication.
- EurekAlert! is shaped more by publishers and journals; IDW-Online features many contributions from non-university research institutes.
- Future work: apply machine learning to automatically classify larger samples; combine datasets with other formats of external science communication.

## Acknowledgements

Funded by the German Federal Ministry of Education and Research for project MeWiKo (grant number 01PU17018A). Data access provided by EurekAlert! and IDW-Online.

## References

Bowman, T. D., & Hassan, S.-U. (2019). Science News and Altmetrics: Looking at EurekAlert!. altmetrics19 Workshop, Stirling, Scotland.

Lemke, S. (2020). The Effect of Press Releases on Promoted Articles' Citations and Altmetrics. Metrics 2020: ASIS&T Virtual Workshop, Pittsburgh.

de Vrieze, J. (2018). EurekAlert! has spoiled science news. Here's how we can fix it. VWN.
