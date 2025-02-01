import streamlit as st

class IndiaTaxCalculator:
    def __init__(self, salary, regime):
        self.salary = salary
        self.regime = regime
        
        self.new_tax_slabs = [
            (1200000, 0.00),
            (1500000, 0.10),
            (1800000, 0.15),
            (2100000, 0.20),
            (2400000, 0.25),
            (float('inf'), 0.30)
        ]
        
        self.old_tax_slabs = [
            (250000, 0.00),
            (500000, 0.05),
            (750000, 0.10),
            (1000000, 0.15),
            (1250000, 0.20),
            (1500000, 0.25),
            (float('inf'), 0.30)
        ]
    
    def calculate_tax(self):
        taxable_income = self.salary
        tax = 0
        prev_limit = 0
        tax_slabs = self.new_tax_slabs if self.regime == "New" else self.old_tax_slabs
        
        for limit, rate in tax_slabs:
            if taxable_income > prev_limit:
                taxable_amount = min(taxable_income, limit) - prev_limit
                tax += taxable_amount * rate
                prev_limit = limit
            else:
                break
        
        return tax

def main():
    st.title("AI Research Centre, Woxsen University
    India Tax Calculator (2025 Updated)")
    salary = st.number_input("Enter your annual salary (CTC):", min_value=0.0, step=10000.0, format="%.2f")
    
    if st.button("Compare Tax Regimes"):
        new_tax = IndiaTaxCalculator(salary, "New").calculate_tax()
        old_tax = IndiaTaxCalculator(salary, "Old").calculate_tax()
        
        st.subheader("Tax Calculation Results")
        st.write(f"New Regime Tax: ₹{new_tax:,.2f}")
        st.write(f"Old Regime Tax: ₹{old_tax:,.2f}")
        st.write(f"Difference: ₹{abs(new_tax - old_tax):,.2f}")
        
        st.subheader("Tax Slabs")
        st.write("**New Tax Regime Slabs (2025):**")
        st.write("Up to ₹12,00,000: No tax")
        st.write("₹12,00,001 to ₹15,00,000: 10%")
        st.write("₹15,00,001 to ₹18,00,000: 15%")
        st.write("₹18,00,001 to ₹21,00,000: 20%")
        st.write("₹21,00,001 to ₹24,00,000: 25%")
        st.write("Above ₹24,00,000: 30%")
        
        st.write("**Old Tax Regime Slabs:**")
        st.write("Up to ₹2,50,000: No tax")
        st.write("₹2,50,001 to ₹5,00,000: 5%")
        st.write("₹5,00,001 to ₹7,50,000: 10%")
        st.write("₹7,50,001 to ₹10,00,000: 15%")
        st.write("₹10,00,001 to ₹12,50,000: 20%")
        st.write("₹12,50,001 to ₹15,00,000: 25%")
        st.write("Above ₹15,00,000: 30%")

if __name__ == "__main__":
    main()
