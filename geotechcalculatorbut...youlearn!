import streamlit as st
import math

st.set_page_config(page_title="Geotech Calculator", layout="wide")
st.title("RMIT Geotechnical Engineering Calculator")

# Initialize session state for input fields
if 'clear_all' not in st.session_state:
    st.session_state.clear_all = False

# Function to clear all inputs
def clear_all_inputs():
    for key in st.session_state.keys():
        if key not in ['clear_all']:
            del st.session_state[key]
    st.session_state.clear_all = True

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Earth Pressure", "Factor of Safety", "Bearing Capacity", "Consolidation"])

with tab1:
    st.header("Earth Pressure Calculations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rankine's Passive Earth Pressure")
        gamma2 = st.number_input("γ₂ (kN/m³)", value=None, placeholder="Enter value", key="gamma2", format="%.4f")
        D = st.number_input("D (m)", value=None, placeholder="Enter value", key="D", format="%.4f")
        c2_prime = st.number_input("c₂' (kPa)", value=None, placeholder="Enter value", key="c2", format="%.4f")
        phi2_prime = st.number_input("φ₂' (degrees)", value=None, placeholder="Enter value", key="phi2", format="%.4f")
        
        if st.button("Calculate Kp and Pp", key="calc_kp_pp"):
            # Check if we have enough for Kp calculation
            if phi2_prime is None:
                st.error("Cannot calculate Kp: Missing φ₂' value")
            else:
                with st.expander("Calculation Breakdown for Kp", expanded=True):
                    st.write("**Formula:** Kp = tan²(45° + φ₂'/2)")
                    st.write(f"Kp = tan²(45° + {phi2_prime}/2)")
                    st.write(f"Kp = tan²(45° + {phi2_prime/2:.1f}°)")
                    st.write(f"Kp = tan²({45 + phi2_prime/2:.1f}°)")
                    kp = math.tan(math.radians(45 + phi2_prime/2))**2
                    st.write(f"Kp = {math.tan(math.radians(45 + phi2_prime/2)):.4f}²")
                    st.write(f"**Kp = {kp:.4f}**")
                
                # Check if we have enough for Pp calculation
                pp_missing = []
                if gamma2 is None: pp_missing.append("γ₂")
                if D is None: pp_missing.append("D")
                if c2_prime is None: pp_missing.append("c₂'")
                
                if pp_missing:
                    st.warning(f"Cannot calculate Pp: Missing {', '.join(pp_missing)}")
                else:
                    with st.expander("Calculation Breakdown for Pp", expanded=True):
                        st.write("**Formula:** Pp = ½ × Kp × γ₂ × D² + 2 × c₂' × D × √Kp")
                        st.write(f"Pp = ½ × {kp:.4f} × {gamma2} × {D}² + 2 × {c2_prime} × {D} × √{kp:.4f}")
                        st.write(f"Pp = ½ × {kp:.4f} × {gamma2} × {D**2:.2f} + 2 × {c2_prime} × {D} × {math.sqrt(kp):.4f}")
                        term1 = 0.5 * kp * gamma2 * D**2
                        term2 = 2 * c2_prime * D * math.sqrt(kp)
                        st.write(f"Pp = {term1:.2f} + {term2:.2f}")
                        pp = term1 + term2
                        st.write(f"**Pp = {pp:.2f} kN/m**")
    
    with col2:
        st.subheader("Coulomb's Active Earth Pressure")
        alpha = st.number_input("α (degrees)", value=None, placeholder="Enter value", key="alpha", format="%.4f")
        phi_prime = st.number_input("φ' (degrees)", value=None, placeholder="Enter value", key="phi", format="%.4f")
        
        if st.button("Calculate Ka", key="calc_ka"):
            missing_fields = []
            if alpha is None: missing_fields.append("α")
            if phi_prime is None: missing_fields.append("φ'")
            
            if missing_fields:
                st.error(f"Cannot calculate Ka: Missing {', '.join(missing_fields)}")
            else:
                with st.expander("Calculation Breakdown for Ka", expanded=True):
                    st.write("**Formula:** Ka = cosα × [cosα - √(cos²α - cos²φ')] / [cosα + √(cos²α - cos²φ')]")
                    
                    alpha_rad = math.radians(alpha)
                    phi_rad = math.radians(phi_prime)
                    
                    cos_alpha = math.cos(alpha_rad)
                    cos_phi = math.cos(phi_rad)
                    cos_alpha_sq = cos_alpha**2
                    cos_phi_sq = cos_phi**2
                    
                    st.write(f"cosα = cos({alpha}°) = {cos_alpha:.4f}")
                    st.write(f"cosφ' = cos({phi_prime}°) = {cos_phi:.4f}")
                    st.write(f"cos²α = {cos_alpha_sq:.4f}")
                    st.write(f"cos²φ' = {cos_phi_sq:.4f}")
                    
                    # Check for valid input range
                    if cos_alpha_sq - cos_phi_sq < 0:
                        st.error("Invalid input: cos²α must be greater than cos²φ'")
                    else:
                        sqrt_term = math.sqrt(cos_alpha_sq - cos_phi_sq)
                        st.write(f"√(cos²α - cos²φ') = √({cos_alpha_sq:.4f} - {cos_phi_sq:.4f}) = √{cos_alpha_sq - cos_phi_sq:.4f} = {sqrt_term:.4f}")
                        
                        numerator = cos_alpha - sqrt_term
                        denominator = cos_alpha + sqrt_term
                        st.write(f"Numerator = {cos_alpha:.4f} - {sqrt_term:.4f} = {numerator:.4f}")
                        st.write(f"Denominator = {cos_alpha:.4f} + {sqrt_term:.4f} = {denominator:.4f}")
                        
                        ka = cos_alpha * (numerator / denominator)
                        st.write(f"Ka = {cos_alpha:.4f} × ({numerator:.4f} / {denominator:.4f})")
                        st.write(f"Ka = {cos_alpha:.4f} × {numerator/denominator:.4f}")
                        st.write(f"**Ka = {ka:.4f}**")

with tab2:
    st.header("Factor of Safety Against Sliding")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sigma_v = st.number_input("ΣV (kN/m)", value=None, placeholder="Enter value", key="sv", format="%.4f")
        k1 = st.number_input("k₁", value=None, placeholder="Enter value", key="k1", format="%.4f")
        phi2_prime_slide = st.number_input("φ₂' (degrees)", value=None, placeholder="Enter value", key="phi2_slide", format="%.4f")
        B_slide = st.number_input("B (m)", value=None, placeholder="Enter value", key="B_slide", format="%.4f")
    
    with col2:
        k2 = st.number_input("k₂", value=None, placeholder="Enter value", key="k2", format="%.4f")
        c2_prime_slide = st.number_input("c₂' (kPa)", value=None, placeholder="Enter value", key="c2_slide", format="%.4f")
        Pp_slide = st.number_input("Pp (kN/m)", value=None, placeholder="Enter value", key="Pp_slide", format="%.4f")
        Pa_slide = st.number_input("Pₐ (kN/m)", value=None, placeholder="Enter value", key="Pa_slide", format="%.4f")
        alpha_slide = st.number_input("α (degrees)", value=None, placeholder="Enter value", key="alpha_slide", format="%.4f")
    
    if st.button("Calculate FS", key="calc_fs"):
        missing_fields = []
        if sigma_v is None: missing_fields.append("ΣV")
        if k1 is None: missing_fields.append("k₁")
        if phi2_prime_slide is None: missing_fields.append("φ₂'")
        if B_slide is None: missing_fields.append("B")
        if k2 is None: missing_fields.append("k₂")
        if c2_prime_slide is None: missing_fields.append("c₂'")
        if Pp_slide is None: missing_fields.append("Pp")
        if Pa_slide is None: missing_fields.append("Pₐ")
        if alpha_slide is None: missing_fields.append("α")
        
        if missing_fields:
            st.error(f"Cannot calculate FS: Missing {', '.join(missing_fields)}")
        else:
            with st.expander("Calculation Breakdown for FS", expanded=True):
                st.write("**Formula:** FS = [ΣV × tan(k₁ × φ₂') + B × k₂ × c₂' + Pp] / [Pₐ × cosα]")
                
                # Calculate resisting force components
                tan_component = sigma_v * math.tan(math.radians(k1 * phi2_prime_slide))
                cohesion_component = B_slide * k2 * c2_prime_slide
                resisting_force = tan_component + cohesion_component + Pp_slide
                
                st.write("**Resisting Force Components:**")
                st.write(f"ΣV × tan(k₁ × φ₂') = {sigma_v} × tan({k1} × {phi2_prime_slide}°)")
                st.write(f"= {sigma_v} × tan({k1 * phi2_prime_slide:.1f}°)")
                st.write(f"= {sigma_v} × {math.tan(math.radians(k1 * phi2_prime_slide)):.4f} = {tan_component:.2f} kN/m")
                
                st.write(f"B × k₂ × c₂' = {B_slide} × {k2} × {c2_prime_slide} = {cohesion_component:.2f} kN/m")
                st.write(f"Pp = {Pp_slide} kN/m")
                st.write(f"**Total Resisting Force = {tan_component:.2f} + {cohesion_component:.2f} + {Pp_slide} = {resisting_force:.2f} kN/m**")
                
                # Calculate driving force
                driving_force = Pa_slide * math.cos(math.radians(alpha_slide))
                st.write("**Driving Force:**")
                st.write(f"Pₐ × cosα = {Pa_slide} × cos({alpha_slide}°)")
                st.write(f"= {Pa_slide} × {math.cos(math.radians(alpha_slide)):.4f} = {driving_force:.2f} kN/m")
                
                if driving_force == 0:
                    fs = float('inf')
                    st.write("**FS = ∞ (driving force is zero)**")
                else:
                    fs = resisting_force / driving_force
                    st.write(f"**FS = {resisting_force:.2f} / {driving_force:.2f} = {fs:.3f}**")
    
    st.header("Bearing Pressure Distribution")
    sigma_v_bp = st.number_input("ΣV (kN/m)", value=None, placeholder="Enter value", key="sv_bp", format="%.4f")
    B_bp = st.number_input("B (m)", value=None, placeholder="Enter value", key="B_bp", format="%.4f")
    e_bp = st.number_input("e (m)", value=None, placeholder="Enter value", key="e_bp", format="%.4f")
    
    if st.button("Calculate Bearing Pressure", key="calc_bp"):
        missing_fields = []
        if sigma_v_bp is None: missing_fields.append("ΣV")
        if B_bp is None: missing_fields.append("B")
        if e_bp is None: missing_fields.append("e")
        
        if missing_fields:
            st.error(f"Cannot calculate bearing pressure: Missing {', '.join(missing_fields)}")
        else:
            with st.expander("Calculation Breakdown", expanded=True):
                # Check for eccentricity limit
                if e_bp > B_bp/6:
                    st.error("Eccentricity (e) cannot exceed B/6")
                else:
                    st.write("**Formulas:**")
                    st.write("q_max = (ΣV/B) × (1 + 6e/B)")
                    st.write("q_min = (ΣV/B) × (1 - 6e/B)")
                    
                    base_pressure = sigma_v_bp / B_bp
                    st.write(f"ΣV/B = {sigma_v_bp} / {B_bp} = {base_pressure:.2f} kPa")
                    
                    eccentricity_factor_max = 1 + (6 * e_bp) / B_bp
                    eccentricity_factor_min = 1 - (6 * e_bp) / B_bp
                    st.write(f"1 + 6e/B = 1 + 6×{e_bp}/{B_bp} = 1 + {6*e_bp/B_bp:.2f} = {eccentricity_factor_max:.2f}")
                    st.write(f"1 - 6e/B = 1 - 6×{e_bp}/{B_bp} = 1 - {6*e_bp/B_bp:.2f} = {eccentricity_factor_min:.2f}")
                    
                    q_max = base_pressure * eccentricity_factor_max
                    q_min = base_pressure * eccentricity_factor_min
                    
                    st.write(f"**q_max = {base_pressure:.2f} × {eccentricity_factor_max:.2f} = {q_max:.2f} kPa**")
                    st.write(f"**q_min = {base_pressure:.2f} × {eccentricity_factor_min:.2f} = {q_min:.2f} kPa**")

with tab3:
    st.header("General Bearing Capacity Equation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        c2_prime_bc = st.number_input("c₂' (kPa)", value=None, placeholder="Enter value", key="c2_bc", format="%.4f")
        phi2_prime_bc = st.number_input("φ₂' (degrees)", value=None, placeholder="Enter value", key="phi2_bc", format="%.4f")
        gamma2_bc = st.number_input("γ₂ (kN/m³)", value=None, placeholder="Enter value", key="gamma2_bc", format="%.4f")
        B_prime_bc = st.number_input("B' (m)", value=None, placeholder="Enter value", key="B_prime_bc", format="%.4f")
    
    with col2:
        q_bc = st.number_input("q (kPa)", value=None, placeholder="Enter value", key="q_bc", format="%.4f")
        D_bc = st.number_input("D (m)", value=None, placeholder="Enter value", key="D_bc", format="%.4f")
        psi_bc = st.number_input("ψ (degrees)", value=None, placeholder="Enter value", key="psi_bc", format="%.4f")
    
    if st.button("Calculate Bearing Capacity", key="calc_bc"):
        missing_fields = []
        if phi2_prime_bc is None: missing_fields.append("φ₂'")
        if B_prime_bc is None: missing_fields.append("B'")
        
        if missing_fields:
            st.error(f"Cannot calculate bearing capacity: Missing {', '.join(missing_fields)}")
        else:
            with st.expander("Calculation Breakdown", expanded=True):
                st.write("**Formula:** q_u = c₂' × Nc × Fcd × Fci + q × Nq × Fqd × Fqi + ½ × γ₂ × B' × Nγ × Fγd × Fγi")
                
                # Bearing capacity factors
                st.write("**Bearing Capacity Factors:**")
                Nq = math.exp(math.pi * math.tan(math.radians(phi2_prime_bc))) * (math.tan(math.radians(45 + phi2_prime_bc/2))**2)
                st.write(f"Nq = exp(π × tanφ₂') × tan²(45° + φ₂'/2)")
                st.write(f"Nq = exp({math.pi:.3f} × tan{phi2_prime_bc}°) × tan²(45° + {phi2_prime_bc/2:.1f}°)")
                st.write(f"Nq = exp({math.pi:.3f} × {math.tan(math.radians(phi2_prime_bc)):.4f}) × tan²({45 + phi2_prime_bc/2:.1f}°)")
                st.write(f"Nq = {math.exp(math.pi * math.tan(math.radians(phi2_prime_bc))):.3f} × {math.tan(math.radians(45 + phi2_prime_bc/2))**2:.3f} = {Nq:.3f}")
                
                if phi2_prime_bc > 0:
                    Nc = (Nq - 1) * (1 / math.tan(math.radians(phi2_prime_bc)))
                    st.write(f"Nc = (Nq - 1) × cotφ₂' = ({Nq:.3f} - 1) × cot{phi2_prime_bc}° = {Nc:.3f}")
                else:
                    Nc = 5.14
                    st.write(f"Nc = 5.14 (for φ₂' = 0°)")
                
                Ng = 2 * (Nq + 1) * math.tan(math.radians(phi2_prime_bc))
                st.write(f"Nγ = 2 × (Nq + 1) × tanφ₂' = 2 × ({Nq:.3f} + 1) × tan{phi2_prime_bc}° = {Ng:.3f}")
                
                # Depth factors
                st.write("**Depth Factors:**")
                if D_bc is not None:
                    Fqd = 1 + 2 * math.tan(math.radians(phi2_prime_bc)) * (1 - math.sin(math.radians(phi2_prime_bc)))**2 * (D_bc / B_prime_bc)
                    st.write(f"Fqd = 1 + 2 × tanφ₂' × (1 - sinφ₂')² × (D/B')")
                    st.write(f"Fqd = 1 + 2 × tan{phi2_prime_bc}° × (1 - sin{phi2_prime_bc}°)² × ({D_bc}/{B_prime_bc})")
                    st.write(f"Fqd = 1 + 2 × {math.tan(math.radians(phi2_prime_bc)):.4f} × {((1 - math.sin(math.radians(phi2_prime_bc)))**2):.4f} × {D_bc/B_prime_bc:.3f} = {Fqd:.3f}")
                else:
                    Fqd = 1
                    st.write("Fqd = 1 (D not provided)")
                
                if phi2_prime_bc > 0:
                    Fcd = Fqd - (1 - Fqd) / (Nc * math.tan(math.radians(phi2_prime_bc)))
                    st.write(f"Fcd = Fqd - (1 - Fqd)/(Nc × tanφ₂') = {Fqd:.3f} - (1 - {Fqd:.3f})/({Nc:.3f} × tan{phi2_prime_bc}°) = {Fcd:.3f}")
                else:
                    Fcd = 1
                
                Fyd = 1
                st.write("Fγd = 1 (common simplification)")
                
                # Inclination factors
                st.write("**Inclination Factors:**")
                if psi_bc is not None:
                    Fci = Fqi = (1 - psi_bc / 90)**2
                    st.write(f"Fci = Fqi = (1 - ψ/90)² = (1 - {psi_bc}/90)² = {Fci:.3f}")
                    
                    if phi2_prime_bc > 0:
                        Fyi = (1 - psi_bc / phi2_prime_bc)**2
                        st.write(f"Fγi = (1 - ψ/φ₂')² = (1 - {psi_bc}/{phi2_prime_bc})² = {Fyi:.3f}")
                    else:
                        Fyi = 1
                        st.write("Fγi = 1 (φ₂' = 0°)")
                else:
                    Fci = Fqi = Fyi = 1
                    st.write("Fci = Fqi = Fγi = 1 (ψ not provided)")
                
                # Ultimate bearing capacity
                st.write("**Ultimate Bearing Capacity:**")
                components = []
                
                if c2_prime_bc is not None:
                    component1 = c2_prime_bc * Nc * Fcd * Fci
                    st.write(f"Cohesion term = c₂' × Nc × Fcd × Fci = {c2_prime_bc} × {Nc:.3f} × {Fcd:.3f} × {Fci:.3f} = {component1:.2f} kPa")
                    components.append(component1)
                else:
                    component1 = 0
                    st.write("Cohesion term = 0 (c₂' not provided)")
                
                if q_bc is not None:
                    component2 = q_bc * Nq * Fqd * Fqi
                    st.write(f"Surcharge term = q × Nq × Fqd × Fqi = {q_bc} × {Nq:.3f} × {Fqd:.3f} × {Fqi:.3f} = {component2:.2f} kPa")
                    components.append(component2)
                else:
                    component2 = 0
                    st.write("Surcharge term = 0 (q not provided)")
                
                if gamma2_bc is not None:
                    component3 = 0.5 * gamma2_bc * B_prime_bc * Ng * Fyd * Fyi
                    st.write(f"Soil weight term = ½ × γ₂ × B' × Nγ × Fγd × Fγi = 0.5 × {gamma2_bc} × {B_prime_bc} × {Ng:.3f} × {Fyd} × {Fyi:.3f} = {component3:.2f} kPa")
                    components.append(component3)
                else:
                    component3 = 0
                    st.write("Soil weight term = 0 (γ₂ not provided)")
                
                qu = sum(components)
                st.write(f"**q_u = {component1:.2f} + {component2:.2f} + {component3:.2f} = {qu:.2f} kPa**")
    
    st.header("Resultant Force Inclination")
    Pa_psi = st.number_input("Pₐ (kN/m)", value=None, placeholder="Enter value", key="Pa_psi", format="%.4f")
    alpha_psi = st.number_input("α (degrees)", value=None, placeholder="Enter value", key="alpha_psi", format="%.4f")
    sigma_v_psi = st.number_input("ΣV (kN/m)", value=None, placeholder="Enter value", key="sv_psi", format="%.4f")
    
    if st.button("Calculate ψ", key="calc_psi"):
        missing_fields = []
        if Pa_psi is None: missing_fields.append("Pₐ")
        if alpha_psi is None: missing_fields.append("α")
        if sigma_v_psi is None: missing_fields.append("ΣV")
        
        if missing_fields:
            st.error(f"Cannot calculate ψ: Missing {', '.join(missing_fields)}")
        else:
            with st.expander("Calculation Breakdown", expanded=True):
                st.write("**Formula:** ψ = arctan[(Pₐ × cosα) / ΣV]")
                st.write(f"ψ = arctan[({Pa_psi} × cos{alpha_psi}°) / {sigma_v_psi}]")
                
                horizontal_component = Pa_psi * math.cos(math.radians(alpha_psi))
                st.write(f"Horizontal component = Pₐ × cosα = {Pa_psi} × cos{alpha_psi}°")
                st.write(f"= {Pa_psi} × {math.cos(math.radians(alpha_psi)):.4f} = {horizontal_component:.2f} kN/m")
                
                if sigma_v_psi == 0:
                    psi = 90
                    st.write("**ψ = 90° (ΣV = 0, resultant is purely horizontal)**")
                else:
                    tan_psi = horizontal_component / sigma_v_psi
                    st.write(f"tanψ = {horizontal_component:.2f} / {sigma_v_psi} = {tan_psi:.4f}")
                    psi_rad = math.atan(tan_psi)
                    psi = math.degrees(psi_rad)
                    st.write(f"ψ = arctan({tan_psi:.4f}) = {psi:.2f}°")
                    st.write(f"**ψ = {psi:.2f} degrees**")

with tab4:
    st.header("Consolidation Settlement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        Cc = st.number_input("C_c", value=None, placeholder="Enter value", key="Cc", format="%.4f")
        Hc = st.number_input("H_c (m)", value=None, placeholder="Enter value", key="Hc", format="%.4f")
        e0 = st.number_input("e₀", value=None, placeholder="Enter value", key="e0", format="%.4f")
        sigma0_prime = st.number_input("σ₀' (kPa)", value=None, placeholder="Enter value", key="sigma0", format="%.4f")
    
    with col2:
        dsigma_p_prime = st.number_input("Δσ₍ₚ₎' (kPa)", value=None, placeholder="Enter value", key="dsigma_p", format="%.4f")
        dsigma_f_prime = st.number_input("Δσ₍f₎' (kPa)", value=None, placeholder="Enter value", key="dsigma_f", format="%.4f")
    
    if st.button("Calculate Settlement", key="calc_settlement"):
        missing_fields = []
        if Cc is None: missing_fields.append("C_c")
        if Hc is None: missing_fields.append("H_c")
        if e0 is None: missing_fields.append("e₀")
        if sigma0_prime is None: missing_fields.append("σ₀'")
        if dsigma_p_prime is None: missing_fields.append("Δσ₍ₚ₎'")
        if dsigma_f_prime is None: missing_fields.append("Δσ₍f₎'")
        
        if missing_fields:
            st.error(f"Cannot calculate settlement: Missing {', '.join(missing_fields)}")
        else:
            with st.expander("Calculation Breakdown", expanded=True):
                st.write("**Formula:** S_c(p+f) = [C_c × H_c / (1 + e₀)] × log₁₀[(σ₀' + Δσ₍ₚ₎' + Δσ₍f₎') / σ₀']")
                
                st.write(f"S_c(p+f) = [{Cc} × {Hc} / (1 + {e0})] × log₁₀[({sigma0_prime} + {dsigma_p_prime} + {dsigma_f_prime}) / {sigma0_prime}]")
                
                term1 = Cc * Hc / (1 + e0)
                st.write(f"Term 1 = C_c × H_c / (1 + e₀) = {Cc} × {Hc} / {1 + e0} = {term1:.4f} m")
                
                total_sigma = sigma0_prime + dsigma_p_prime + dsigma_f_prime
                st.write(f"Total stress = σ₀' + Δσ₍ₚ₎' + Δσ₍f₎' = {sigma0_prime} + {dsigma_p_prime} + {dsigma_f_prime} = {total_sigma} kPa")
                
                stress_ratio = total_sigma / sigma0_prime
                st.write(f"Stress ratio = {total_sigma} / {sigma0_prime} = {stress_ratio:.4f}")
                
                log_term = math.log10(stress_ratio)
                st.write(f"log₁₀({stress_ratio:.4f}) = {log_term:.4f}")
                
                settlement = term1 * log_term
                st.write(f"**S_c(p+f) = {term1:.4f} × {log_term:.4f} = {settlement:.4f} m**")
    
    st.header("Time Factor Calculation")
    Tv = st.number_input("T_v", value=None, placeholder="Enter value", key="Tv", format="%.4f")
    H_tv = st.number_input("H (m)", value=None, placeholder="Enter value", key="H_tv", format="%.4f")
    Cv = st.number_input("C_v (m²/year)", value=None, placeholder="Enter value", key="Cv", format="%.4f")
    
    if st.button("Calculate Time", key="calc_time"):
        missing_fields = []
        if Tv is None: missing_fields.append("T_v")
        if H_tv is None: missing_fields.append("H")
        if Cv is None: missing_fields.append("C_v")
        
        if missing_fields:
            st.error(f"Cannot calculate time: Missing {', '.join(missing_fields)}")
        else:
            with st.expander("Calculation Breakdown", expanded=True):
                st.write("**Formula:** t = (T_v × H_drainage²) / C_v")
                st.write("Where H_drainage = H/2 (for two-way drainage)")
                
                H_drainage = H_tv / 2
                st.write(f"H_drainage = {H_tv} / 2 = {H_drainage} m")
                
                time = (Tv * H_drainage**2) / Cv
                st.write(f"t = ({Tv} × {H_drainage}²) / {Cv}")
                st.write(f"t = ({Tv} × {H_drainage**2:.4f}) / {Cv}")
                st.write(f"**t = {time:.2f} years**")

# Clear all button
if st.sidebar.button("Clear All Data"):
    clear_all_inputs()
    st.rerun()

st.sidebar.info("""
**Geotech Calculator**  
Created for RMIT Geotechnical Engineering 3  
All calculations based on standard geotechnical formulas
""")
