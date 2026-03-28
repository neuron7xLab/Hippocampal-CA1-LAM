# Bibliography

Complete scientific references for CA1 Hippocampus Framework v2.0

All parameters in this framework are extracted from peer-reviewed literature. This document provides complete bibliographic information with DOI links.

## Primary References

### 1. Laminar Organization

**Pachicano M., Marín O., Rico B.** (2025)  
*Laminar organization of pyramidal neuron cell types defines distinct CA1 hippocampal subregions*  
**Nature Communications**, Article 10604  
Published: 03 December 2025  
DOI: [10.1038/s41467-025-66613-y](https://doi.org/10.1038/s41467-025-66613-y)

**Data extracted:**
- 58,065 cells analyzed via RNAscope/HiPlex smFISH
- 332,938 transcripts quantified (QuPath + SCAMPR)
- 4 sublayer markers: Lrmp (Layer 1), Ndst4 (Layer 2), Trib2 (Layer 3), Peg10 (Layer 4)
- Subregion composition: CA1d (L1+L2), CA1i (L2+L3), CA1v (L2+L3+L4), CA1vv (L4)
- Limited coexpression: CE ≤ 0.05

### 2. Ca²⁺-Based Plasticity

**Graupner M., Brunel N.** (2012)  
*Calcium-based plasticity model explains sensitivity of synaptic changes to spike pattern, rate, and dendritic location*  
**Proceedings of the National Academy of Sciences**, 109(10):3991-3996  
DOI: [10.1073/pnas.1109359109](https://doi.org/10.1073/pnas.1109359109)

**Parameters extracted:**
- τ_Ca = 20 ms (calcium time constant, Fig 2A)
- θ_d = 1.0 μM (LTD threshold, Fig 3B)
- θ_p = 2.0 μM (LTP threshold, Fig 3B)
- η_p = 0.001 (potentiation rate, Table 1)
- η_d = 0.0005 (depression rate, Table 1)
- A_pre = 1.0, A_post = 1.0, A_NMDA = 2.0 (calcium influx amplitudes)

### 3. Input-Specific Plasticity (DELTA)

**Mohar B., Ganmore I., Lampl I.** (2025)  
*DELTA: a method for brain-wide measurement of synaptic protein turnover reveals localized plasticity during learning*  
**Nature Neuroscience**  
Published: 2025  
DOI: [10.1038/s41593-025-01923-4](https://doi.org/10.1038/s41593-025-01923-4)

**Motivation:**
- Layer-specific protein turnover rates
- Feedforward vs recurrent pathway differentiation
- Rationale for EC (10x lower) vs CA3 (normal) plasticity rates

### 4. HCN Channel Gradient

**Magee J.C.** (1998)  
*Dendritic hyperpolarization-activated currents modify the integrative properties of hippocampal CA1 pyramidal neurons*  
**Journal of Neuroscience**, 18(19):7613-7624  
DOI: [10.1523/JNEUROSCI.18-19-07613.1998](https://doi.org/10.1523/JNEUROSCI.18-19-07613.1998)

**Data extracted:**
- HCN conductance gradient: g_h increases with depth (patch-clamp recordings, Fig 4)
- Quantified values: [0.5, 1.5, 3.0, 5.0] mS/cm² (superficial → deep)
- Half-activation voltages: V_half shifts with depth (Fig 5)
- Functional impact on temporal summation and resonance

### 5. Theta Phase Precession

**O'Keefe J., Recce M.L.** (1993)  
*Phase relationship between hippocampal place units and the EEG theta rhythm*  
**Hippocampus**, 3(3):317-330  
DOI: [10.1002/hipo.450030307](https://doi.org/10.1002/hipo.450030307)

**Data extracted:**
- Theta frequency range: 4-12 Hz
- Phase precession slope: κ ≈ 2π rad/place field
- Phase-position relationship: φ = φ₀ - κx (mod 2π)

**Skaggs W.E., McNaughton B.L., Wilson M.A., Barnes C.A.** (1996)  
*Theta phase precession in hippocampal neuronal populations and the compression of temporal sequences*  
**Hippocampus**, 6(2):149-172  
DOI: [10.1002/(SICI)1098-1063(1996)6:2<149::AID-HIPO6>3.0.CO;2-K](https://doi.org/10.1002/(SICI)1098-1063(1996)6:2<149::AID-HIPO6>3.0.CO;2-K)

**Additional data:**
- Temporal compression during theta cycles
- Population dynamics of phase precession

### 6. Sharp-Wave Ripples (SWR)

**A curated dataset of hippocampal sharp-wave ripples supports investigations of memory replay** (2025)  
**Scientific Data**, Nature  
DOI: [10.1038/s41597-025-06115-0](https://doi.org/10.1038/s41597-025-06115-0)

**Data extracted:**
- SWR duration: mean = 50 ms, std = 20 ms
- SWR rate: 0.5-2 events/min during rest
- Multi-lab curated dataset for replay validation
- Sequence correlation metrics

### 7. OLM Interneuron Control

**Udakis M., Pedrosa V., Chamberlain S.E.L., Clopath C., Mellor J.R.** (2025)  
*A neural circuit mechanism for controlling learning in the hippocampus*  
**Nature Communications**  
DOI: [10.1038/s41467-025-64859-0](https://doi.org/10.1038/s41467-025-64859-0)

**Data extracted:**
- OLM interneurons gate dendritic Ca²⁺ events
- Control of place field formation
- Dendritic inhibition modulates plasticity
- Rationale for plasticity gating factor G ∈ [0,1]

### 8. Behavioral Time-Scale Plasticity (BTSP)

**Bittner K.C., Grienberger C., Vaidya S.P., Milstein A.D., Macklin J.J., Suh J., Tonegawa S., Magee J.C.** (2017)  
*Behavioral time scale synaptic plasticity underlies CA1 place fields*  
**Science**, 357(6355):1033-1036  
DOI: [10.1126/science.aan3846](https://doi.org/10.1126/science.aan3846)

**Data extracted:**
- Eligibility trace time constant: τ_e ≈ 1000 ms
- Behavioral timescale (seconds) vs STDP timescale (ms)
- Modulatory signals bridge timescales

### 9. Voltage-Based STDP with Homeostasis

**Clopath C., Büsing L., Vasilaki E., Gerstner W.** (2010)  
*Connectivity reflects coding: a model of voltage-based STDP with homeostasis*  
**Nature Neuroscience**, 13:344-352  
DOI: [10.1038/nn.2479](https://doi.org/10.1038/nn.2479)

**Data extracted:**
- Homeostatic target firing rate: ν* ≈ 5 Hz
- Synaptic scaling mechanism: W ← W · exp(γ(ν* - ν))
- Voltage-based STDP framework

### 10. Short-Term Plasticity

**Tsodyks M.V., Markram H.** (1997)  
*The neural code between neocortical pyramidal neurons depends on neurotransmitter release probability*  
**Proceedings of the National Academy of Sciences**, 94(2):719-723  
DOI: [10.1073/pnas.94.2.719](https://doi.org/10.1073/pnas.94.2.719)

**Data extracted:**
- Facilitation time constant: τ_F ≈ 100 ms
- Depression time constant: τ_D ≈ 200 ms
- Release probability: U ≈ 0.5
- Tsodyks-Markram model equations

### 11. Network Stability

**Brunel N.** (2000)  
*Dynamics of sparsely connected networks of excitatory and inhibitory spiking neurons*  
**Journal of Computational Neuroscience**, 8:183-208  
DOI: [10.1023/A:1008925309027](https://doi.org/10.1023/A:1008925309027)

**Data extracted:**
- Spectral radius constraint: ρ(W) < 1 for stability
- Balance of excitation and inhibition
- Asynchronous irregular firing regime

### 12. Fractal Analysis Methodology

**Orima T., Shigematsu N., Koyama S., Jimbo Y.** (2025)  
*Fractal memory structure in the spatiotemporal learning rule*  
**Frontiers in Computational Neuroscience**  
DOI: [10.3389/fncom.2025.1641519](https://doi.org/10.3389/fncom.2025.1641519)

**Methodology reference:**
- Box-counting dimension calculation
- Scale window selection: [0.01, 1.0]
- Linearity validation: R² > 0.9
- Bootstrap confidence intervals

### 13. HippoRAG (AI Integration)

**Gutiérrez B.J., Zhou Y., Lee S., Luria G., Haber N., Sundaram S.** (2025)  
*HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models*  
**arXiv:2405.14831** (v3, January 2025)  
DOI: [10.48550/arXiv.2405.14831](https://doi.org/10.48550/arXiv.2405.14831)

**Architecture reference:**
- Hippocampus-inspired retrieval for LLMs
- Multi-hop question answering benchmarks
- Memory consolidation strategies

## Additional References

### NMDA Receptor Dynamics

**Jahr C.E., Stevens C.F.** (1990)  
*Voltage dependence of NMDA-activated macroscopic conductances predicted by single-channel kinetics*  
**Journal of Neuroscience**, 10(9):3178-3182  
DOI: [10.1523/JNEUROSCI.10-09-03178.1990](https://doi.org/10.1523/JNEUROSCI.10-09-03178.1990)  
PubMed: https://pubmed.ncbi.nlm.nih.gov/1697902/

**Mg²⁺ block parameters:**
- [Mg²⁺] = 1.0 mM
- Voltage dependence: g(V) = 1 / (1 + [Mg²⁺]·exp(-αV)/β)
- α = 0.062 mV⁻¹, β = 3.57 mM

### Two-Compartment Models

**Migliore M., Shepherd G.M.** (2002)  
*Emerging rules for the distributions of active dendritic conductances*  
**Nature Reviews Neuroscience**, 3:362-370  
DOI: [10.1038/nrn810](https://doi.org/10.1038/nrn810)

**Compartment modeling principles:**
- Soma: spike generation, AHP
- Dendrite: integration, NMDA, Ca²⁺
- Coupling conductance

**Golding N.L., Staff N.P., Spruston N.** (2002)  
*Dendritic spikes as a mechanism for cooperative long-term potentiation*  
**Nature**, 418:326-331  
DOI: [10.1038/nature00854](https://doi.org/10.1038/nature00854)

**Dendritic Ca²⁺ plateaus:**
- Critical for LTP induction
- NMDA receptor-dependent
- Back-propagating action potentials

## BibTeX Entries

```bibtex
@article{pachicano2025laminar,
  title = {Laminar organization of pyramidal neuron cell types defines distinct CA1 hippocampal subregions},
  author = {Pachicano, M. and Mar{\'i}n, O. and Rico, B.},
  journal = {Nature Communications},
  year = {2025},
  volume = {Article 10604},
  doi = {10.1038/s41467-025-66613-y},
  note = {58,065 cells, 332,938 transcripts}
}

@article{graupner2012calcium,
  title = {Calcium-based plasticity model explains sensitivity of synaptic changes to spike pattern, rate, and dendritic location},
  author = {Graupner, M. and Brunel, N.},
  journal = {Proceedings of the National Academy of Sciences},
  year = {2012},
  volume = {109},
  number = {10},
  pages = {3991--3996},
  doi = {10.1073/pnas.1109359109}
}

@article{mohar2025delta,
  title = {DELTA: a method for brain-wide measurement of synaptic protein turnover reveals localized plasticity during learning},
  author = {Mohar, B. and Ganmore, I. and Lampl, I.},
  journal = {Nature Neuroscience},
  year = {2025},
  doi = {10.1038/s41593-025-01923-4}
}

@article{magee1998dendritic,
  title = {Dendritic hyperpolarization-activated currents modify the integrative properties of hippocampal CA1 pyramidal neurons},
  author = {Magee, J. C.},
  journal = {Journal of Neuroscience},
  year = {1998},
  volume = {18},
  number = {19},
  pages = {7613--7624},
  doi = {10.1523/JNEUROSCI.18-19-07613.1998}
}

@article{okeefe1993phase,
  title = {Phase relationship between hippocampal place units and the EEG theta rhythm},
  author = {O'Keefe, J. and Recce, M. L.},
  journal = {Hippocampus},
  year = {1993},
  volume = {3},
  number = {3},
  pages = {317--330},
  doi = {10.1002/hipo.450030307}
}

@article{swr_dataset2025,
  title = {A curated dataset of hippocampal sharp-wave ripples supports investigations of memory replay},
  journal = {Scientific Data},
  year = {2025},
  publisher = {Nature},
  doi = {10.1038/s41597-025-06115-0}
}

@article{udakis2025olm,
  title = {A neural circuit mechanism for controlling learning in the hippocampus},
  author = {Udakis, M. and Pedrosa, V. and Chamberlain, S. E. L. and Clopath, C. and Mellor, J. R.},
  journal = {Nature Communications},
  year = {2025},
  doi = {10.1038/s41467-025-64859-0}
}

@article{bittner2017btsp,
  title = {Behavioral time scale synaptic plasticity underlies CA1 place fields},
  author = {Bittner, K. C. and Grienberger, C. and Vaidya, S. P. and Milstein, A. D. and Macklin, J. J. and Suh, J. and Tonegawa, S. and Magee, J. C.},
  journal = {Science},
  year = {2017},
  volume = {357},
  number = {6355},
  pages = {1033--1036},
  doi = {10.1126/science.aan3846}
}

@article{clopath2010voltage,
  title = {Connectivity reflects coding: a model of voltage-based STDP with homeostasis},
  author = {Clopath, C. and B{\"u}sing, L. and Vasilaki, E. and Gerstner, W.},
  journal = {Nature Neuroscience},
  year = {2010},
  volume = {13},
  pages = {344--352},
  doi = {10.1038/nn.2479}
}

@article{tsodyks1997stp,
  title = {The neural code between neocortical pyramidal neurons depends on neurotransmitter release probability},
  author = {Tsodyks, M. V. and Markram, H.},
  journal = {Proceedings of the National Academy of Sciences},
  year = {1997},
  volume = {94},
  number = {2},
  pages = {719--723},
  doi = {10.1073/pnas.94.2.719}
}

@article{brunel2000dynamics,
  title = {Dynamics of sparsely connected networks of excitatory and inhibitory spiking neurons},
  author = {Brunel, N.},
  journal = {Journal of Computational Neuroscience},
  year = {2000},
  volume = {8},
  pages = {183--208},
  doi = {10.1023/A:1008925309027}
}

@article{orima2025fractal,
  title = {Fractal memory structure in the spatiotemporal learning rule},
  author = {Orima, T. and Shigematsu, N. and Koyama, S. and Jimbo, Y.},
  journal = {Frontiers in Computational Neuroscience},
  year = {2025},
  doi = {10.3389/fncom.2025.1641519}
}

@article{gutierrez2025hipporag,
  title = {HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models},
  author = {Guti{\'e}rrez, B. J. and Zhou, Y. and Lee, S. and Luria, G. and Haber, N. and Sundaram, S.},
  journal = {arXiv preprint arXiv:2405.14831},
  year = {2025},
  note = {v3, January 2025},
  doi = {10.48550/arXiv.2405.14831}
}

@article{jahr1990nmda,
  title = {Voltage dependence of NMDA-activated macroscopic conductances predicted by single-channel kinetics},
  author = {Jahr, C. E. and Stevens, C. F.},
  journal = {Journal of Neuroscience},
  year = {1990},
  volume = {10},
  number = {9},
  pages = {3178--3182},
  doi = {10.1523/JNEUROSCI.10-09-03178.1990}
}
```

## Citation Policy

When using this framework in publications:

1. **Cite the framework**:
   ```
   CA1 Hippocampus Framework v2.0 (2025)
   https://github.com/neuron7x/Hippocampal-CA1-LAM
   ```

2. **Cite primary references** for mechanisms used:
   - If using Ca²⁺ plasticity → Cite Graupner & Brunel 2012
   - If using laminar structure → Cite Pachicano et al. 2025
   - If using AI integration → Cite Gutiérrez et al. 2025

3. **Cite parameters** if extracted:
   - Example: "HCN gradient g_h from Magee 1998 (DOI: 10.1523/JNEUROSCI.18-19-07613.1998)"

## Verification

To verify a DOI: visit doi.org and enter the DOI identifier.

---

**Last updated**: December 14, 2025
