import streamlit as st
import math

st.set_page_config(page_title="Geotech Calculator", layout="wide")
st.title("RMIT Geotechnical Engineering Calculator")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Earth Pressure", "Factor of Safety", "Bearing Capacity", "Consolidation"])

with tab1:
    st.header("Earth Pressure Calculations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rankine's Passive Earth Pressure")
        gamma2 = st.number_input("γ₂ (kN/m³)", value=18.0, key="gamma2")
        D = st.number_input("D (m)", value=2.0, key="D")
        c2_prime = st.number_input("c₂' (kPa)", value=10.0, key="c2")
        phi2_prime = st.number_input("φ₂' (degrees)", value=30.0, key="phi2")
        
        if st.button("Calculate Kp and Pp", key="calc_kp_pp"):
            kp = math.tan(math.radians(45 + phi2_prime/2))**2
            pp = 0.5 * kp * gamma2 * D**2 + 2 * c2_prime * D * math.sqrt(kp)
            st.success(f"Kp = {kp:.4f}")
            st.success(f"Pp = {pp:.2f} kN/m")
    
    with col2:
        st.subheader("Coulomb's Active Earth Pressure")
        alpha = st.number_input("α (degrees)", value=0.0, key="alpha")
        phi_prime = st.number_input("φ' (degrees)", value=30.0, key="phi")
        
        if st.button("Calculate Ka", key="calc_ka"):
            alpha_rad = math.radians(alpha)
            phi_rad = math.radians(phi_prime)
            
            numerator = math.cos(alpha_rad) - math.sqrt(math.cos(alpha_rad)**2 - math.cos(phi_rad)**2)
            denominator = math.cos(alpha_rad) + math.sqrt(math.cos(alpha_rad)**2 - math.cos(phi_rad)**2)
            ka = math.cos(alpha_rad) * (numerator / denominator)
            st.success(f"Ka = {ka:.4f}")

with tab2:
    st.header("Factor of Safety Against Sliding")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sigma_v = st.number_input("ΣV (kN/m)", value=100.0, key="sv")
        k1 = st.number_input("k₁", value=0.8, key="k1")
        phi2_prime_slide = st.number_input("φ₂' (degrees)", value=30.0, key="phi2_slide")
        B_slide = st.number_input("B (m)", value=1.5, key="B_slide")
    
    with col2:
        k2 = st.number_input("k₂", value=0.8, key="k2")
        c2_prime_slide = st.number_input("c₂' (kPa)", value=10.0, key="c2_slide")
        Pp_slide = st.number_input("Pp (kN/m)", value=50.0, key="Pp_slide")
        Pa_slide = st.number_input("Pₐ (kN/m)", value=30.0, key="Pa_slide")
        alpha_slide = st.number_input("α (degrees)", value=0.0, key="alpha_slide")
    
    if st.button("Calculate FS", key="calc_fs"):
        resisting_force = sigma_v * math.tan(math.radians(k1 * phi2_prime_slide)) + B_slide * k2 * c2_prime_slide + Pp_slide
        driving_force = Pa_slide * math.cos(math.radians(alpha_slide))
        
        if driving_force == 0:
            fs = float('inf')
        else:
            fs = resisting_force / driving_force
        
        st.success(f"Factor of Safety against Sliding = {fs:.3f}")
    
    st.header("Bearing Pressure Distribution")
    sigma_v_bp = st.number_input("ΣV (kN/m)", value=100.0, key="sv_bp")
    B_bp = st.number_input("B (m)", value=2.0, key="B_bp")
    e_bp = st.number_input("e (m)", value=0.2, key="e_bp")
    
    if st.button("Calculate Bearing Pressure", key="calc_bp"):
        q_max = (sigma_v_bp / B_bp) * (1 + (6 * e_bp) / B_bp)
        q_min = (sigma_v_bp / B_bp) * (1 - (6 * e_bp) / B_bp)
        st.success(f"q_max = {q_max:.2f} kPa")
        st.success(f"q_min = {q_min:.2f} kPa")

with tab3:
    st.header("General Bearing Capacity Equation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        c2_prime_bc = st.number_input("c₂' (kPa)", value=10.0, key="c2_bc")
        phi2_prime_bc = st.number_input("φ₂' (degrees)", value=30.0, key="phi2_bc")
        gamma2_bc = st.number_input("γ₂ (kN/m³)", value=18.0, key="gamma2_bc")
        B_prime_bc = st.number_input("B' (m)", value=1.5, key="B_prime_bc")
    
    with col2:
        q_bc = st.number_input("q (kPa)", value=20.0, key="q_bc")
        D_bc = st.number_input("D (m)", value=1.0, key="D_bc")
        psi_bc = st.number_input("ψ (degrees)", value=5.0, key="psi_bc")
    
    if st.button("Calculate Bearing Capacity", key="calc_bc"):
        # Bearing capacity factors
        Nq = math.exp(math.pi * math.tan(math.radians(phi2_prime_bc))) * (math.tan(math.radians(45 + phi2_prime_bc/2))**2)
        Nc = (Nq - 1) * (1 / math.tan(math.radians(phi2_prime_bc))) if phi2_prime_bc > 0 else 5.14
        Ng = 2 * (Nq + 1) * math.tan(math.radians(phi2_prime_bc))
        
        # Depth factors
        Fqd = 1 + 2 * math.tan(math.radians(phi2_prime_bc)) * (1 - math.sin(math.radians(phi2_prime_bc)))**2 * (D_bc / B_prime_bc)
        Fcd = Fqd - (1 - Fqd) / (Nc * math.tan(math.radians(phi2_prime_bc))) if phi2_prime_bc > 0 else 1
        Fyd = 1  # Common simplification
        
        # Inclination factors
        Fci = Fqi = (1 - psi_bc / 90)**2
        Fyi = (1 - psi_bc / phi2_prime_bc)**2 if phi2_prime_bc > 0 else 1
        
        # Ultimate bearing capacity
        qu = (c2_prime_bc * Nc * Fcd * Fci + 
              q_bc * Nq * Fqd * Fqi + 
              0.5 * gamma2_bc * B_prime_bc * Ng * Fyd * Fyi)
        
        st.success(f"q_u = {qu:.2f} kPa")
        st.info(f"Nc = {Nc:.2f}, Nq = {Nq:.2f}, Nγ = {Ng:.2f}")
        st.info(f"Fcd = {Fcd:.3f}, Fqd = {Fqd:.3f}, Fci = Fqi = {Fci:.3f}, Fyi = {Fyi:.3f}")
    
    st.header("Resultant Force Inclination")
    Pa_psi = st.number_input("Pₐ (kN/m)", value=30.0, key="Pa_psi")
    alpha_psi = st.number_input("α (degrees)", value=0.0, key="alpha_psi")
    sigma_v_psi = st.number_input("ΣV (kN/m)", value=100.0, key="sv_psi")
    
    if st.button("Calculate ψ", key="calc_psi"):
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
        Cc = st.number_input("C_c", value=0.3, key="Cc")
        Hc = st.number_input("H_c (m)", value=5.0, key="Hc")
        e0 = st.number_input("e₀", value=0.8, key="e0")
        sigma0_prime = st.number_input("σ₀' (kPa)", value=100.0, key="sigma0")
    
    with col2:
        dsigma_p_prime = st.number_input("Δσ₍ₚ₎' (kPa)", value=50.0, key="dsigma_p")
        dsigma_f_prime = st.number_input("Δσ₍f₎' (kPa)", value=20.0, key="dsigma_f")
    
    if st.button("Calculate Settlement", key="calc_settlement"):
        settlement = (Cc * Hc / (1 + e0)) * math.log10((sigma0_prime + dsigma_p_prime + dsigma_f_prime) / sigma0_prime)
        st.success(f"S_c(p+f) = {settlement:.4f} m")
    
    st.header("Time Factor Calculation")
    Tv = st.number_input("T_v", value=0.2, key="Tv")
    H_tv = st.number_input("H (m)", value=4.0, key="H_tv")
    Cv = st.number_input("C_v (m²/year)", value=10.0, key="Cv")
    
    if st.button("Calculate Time", key="calc_time"):
        H_drainage = H_tv / 2
        time = (Tv * H_drainage**2) / Cv
        st.success(f"t = {time:.2f} years")

st.sidebar.info("""
**Geotech Calculator**  
Created for RMIT Geotechnical Engineering 3  
All calculations based on standard geotechnical formulas
""")