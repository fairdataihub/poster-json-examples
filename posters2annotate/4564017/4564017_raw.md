# Modeling of 3D Atmospheres of Cool Stars with the MANCHA Code

A. Perdomo*,**,¹; N. Vitas*,**; E. Khomenko*,**; M. Collados*,**

*Instituto de Astrofísica de Canarias, 38205 La Laguna, Tenerife, Spain  
**Departamento de Astrofísica, Universidad de La Laguna, 38205 La Laguna, Tenerife, Spain  
¹aperdomo@iac.es

DOI: 10.5281/zenodo.4564017

## Abstract

The first results of the application of the MANCHA code to the case of stars beyond the solar case are presented: hydrodynamical simulations of stars of spectral type K0V and M0V compared with the solar case. Hydrodynamical models of the photosphere in 3D are the first step towards more realistic models including magnetic fields and non-ideal effects, and extending to the higher atmosphere.

## Introduction

Although 1D models have been proved useful to study stellar atmospheres, 3D simulations are required to fully understand their structure and dynamics — for magnetic and velocity fields or more accurate abundances. The 3D-convection had been extensively simulated for the sun, but only recently for other stars (Beeck et al., 2013; Magic et al., 2013).

## MANCHA Code

MANCHA is a numerical code originally written for 3D "box-in-a-star" simulations of the solar atmosphere and near-surface convection (Khomenko et al., 2017). It simultaneously solves, on a regular Cartesian grid, the system of MHD equations, including non-ideal terms (Ohmic, ambipolar, Biermann's battery), realistic radiative transfer equation, and equation of state accounting for partial ionization. The code is highly modular and has been used in various setups.

## Initial Models

1D models created by modifying the structure of a gray atmosphere using mixing length theory. Models then replicated into the 3D domain; small perturbation in density and internal energy added as a seed to initiate convection.

## Developed Convection

Results after 6 hours of stellar time:

Stellar parameters:
- Sun: T_eff = 5780 K, g = 274 m/s², domain = 5760×5760 km (H), 1568 km (height)
- K0V: T_eff = 4855 K, g = 406 m/s², domain = 2880×2880 km (H), 784 km (height)
- M0V: T_eff = 3900 K, g = 670 m/s², domain = 1440×1440 km (H), 448 km (height)

Horizontal cuts at mean geometrical height around τ=1 showing temperature (K) and vertical velocity (m/s). For earlier spectral types, granule cell size is larger and vertical velocities are higher.

Properties of convection of K0V and M0V stars in general agreement with Beeck et al. (2013).

Plots include: mean temperature per iso-τ surface vs log(optical depth); mean density per geometrical height vs mean pressure; mean pressure per iso-τ surface vs log(optical depth); RMS vertical velocity vs mean pressure.

## Future Work

MANCHA code can be adapted to simulate photospheres of other stars cooler than the sun. Ongoing effort to make opacities at low temperatures more realistic using 1D SYNSPEC code (Hubeny & Lanz, 2017). Models will be used as initial 3D models for setups including magnetic fields, non-ideal effects due to partial ionization, and extension to chromosphere.

## References

[1] Beeck et al, 2013. A&A, 558  
[2] Magic et al, 2013. A&A, 557  
[3] Khomenko et al, 2017. A&A, 604  
[4] I. Hubeny and T. Lanz, 2017. arXiv:1706.01859
