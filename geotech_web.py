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
                kp = math.tan(math.radians(45 + phi2_prime/2))**2
                st.success(f"Kp = {kp:.4f}")
                
                # Check if we have enough for Pp calculation
                pp_missing = []
                if gamma2 is None: pp_missing.append("γ₂")
                if D is None: pp_missing.append("D")
                if c2_prime is None: pp_missing.append("c₂'")
                
                if pp_missing:
                    st.warning(f"Cannot calculate Pp: Missing {', '.join(pp_missing)}")
                else:
                    pp = 0.5 * kp * gamma2 * D**2 + 2 * c2_prime * D * math.sqrt(kp)
                    st.success(f"Pp = {pp:.2f} kN/m")
    
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
                alpha_rad = math.radians(alpha)
                phi_rad = math.radians(phi_prime)
                
                # Check for valid input range
                if math.cos(alpha_rad)**2 - math.cos(phi_rad)**2 < 0:
                    st.error("Invalid input: cos²α must be greater than cos²φ'")
                else:
                    numerator = math.cos(alpha_rad) - math.sqrt(math.cos(alpha_rad)**2 - math.cos(phi_rad)**2)
                    denominator = math.cos(alpha_rad) + math.sqrt(math.cos(alpha_rad)**2 - math.cos(phi_rad)**2)
                    ka = math.cos(alpha_rad) * (numerator / denominator)
                    st.success(f"Ka = {ka:.4f}")

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
            resisting_force = sigma_v * math.tan(math.radians(k1 * phi2_prime_slide)) + B_slide * k2 * c2_prime_slide + Pp_slide
            driving_force = Pa_slide * math.cos(math.radians(alpha_slide))
            
            if driving_force == 0:
                fs = float('inf')
            else:
                fs = resisting_force / driving_force
            
            st.success(f"Factor of Safety against Sliding = {fs:.3f}")
    
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
            # Check for eccentricity limit
            if e_bp > B_bp/6:
                st.error("Eccentricity (e) cannot exceed B/6")
            else:
                q_max = (sigma_v_bp / B_bp) * (1 + (6 * e_bp) / B_bp)
                q_min = (sigma_v_bp / B_bp) * (1 - (6 * e_bp) / B_bp)
                st.success(f"q_max = {q_max:.2f} kPa")
                st.success(f"q_min = {q_min:.2f} kPa")

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
            # Bearing capacity factors
            Nq = math.exp(math.pi * math.tan(math.radians(phi2_prime_bc))) * (math.tan(math.radians(45 + phi2_prime_bc/2))**2)
            Nc = (Nq - 1) * (1 / math.tan(math.radians(phi2_prime_bc))) if phi2_prime_bc > 0 else 5.14
            Ng = 2 * (Nq + 1) * math.tan(math.radians(phi2_prime_bc))
            
            # Depth factors
            Fqd = 1 + 2 * math.tan(math.radians(phi2_prime_bc)) * (1 - math.sin(math.radians(phi2_prime_bc)))**2 * (D_bc/B_prime_bc if D_bc is not None else 0)
            Fcd = Fqd - (1 - Fqd) / (Nc * math.tan(math.radians(phi2_prime_bc))) if phi2_prime_bc > 0 else 1
            Fyd = 1  # Common simplification
            
            # Inclination factors
            Fci = Fqi = (1 - (psi_bc/90 if psi_bc is not None else 0))**2
            Fyi = (1 - (psi_bc/phi2_prime_bc if psi_bc is not None and phi2_prime_bc > 0 else 0))**2 if phi2_prime_bc > 0 else 1
            
            # Calculate each component separately
            component1 = (c2_prime_bc * Nc * Fcd * Fci) if c2_prime_bc is not None else 0
            component2 = (q_bc * Nq * Fqd * Fqi) if q_bc is not None else 0
            component3 = (0.5 * gamma2_bc * B_prime_bc * Ng * Fyd * Fyi) if gamma2_bc is not None else 0
            
            # Ultimate bearing capacity
            qu = component1 + component2 + component3
            
            st.success(f"q_u = {qu:.2f} kPa")
            
            # Show which components were included
            components_used = []
            if c2_prime_bc is not None: components_used.append("cohesion")
            if q_bc is not None: components_used.append("surcharge")
            if gamma2_bc is not None: components_used.append("soil weight")
            
            st.info(f"Calculation includes: {', '.join(components_used) if components_used else 'no components (all inputs missing)'}")
            st.info(f"Nc = {Nc:.2f}, Nq = {Nq:.2f}, Nγ = {Ng:.2f}")
    
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
            if sigma_v_psi == 0:
                psi = 90
            else:
                psi_rad = math.atan((Pa_psi * math.cos(math.radians(alpha_psi))) / sigma_v_psi)
                psi = math.degrees(psi_rad)
            
            st.success(f"ψ = {psi:.2f} degrees")

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
            settlement = (Cc * Hc / (1 + e0)) * math.log10((sigma0_prime + dsigma_p_prime + dsigma_f_prime) / sigma0_prime)
            st.success(f"S_c(p+f) = {settlement:.4f} m")
    
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
            H_drainage = H_tv / 2
            time = (Tv * H_drainage**2) / Cv
            st.success(f"t = {time:.2f} years")

# Clear all button
if st.sidebar.button("Clear All Data"):
    clear_all_inputs()
    st.rerun()

st.sidebar.info("""
**Geotech Calculator**  
Created for RMIT Geotechnical Engineering 3  
All calculations based on standard geotechnical formulas
""")
