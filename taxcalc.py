import streamlit as st
import pandas as pd

class IndiaTaxCalculator:
    def __init__(self, salary, investments, tds, regime):
        self.salary = salary
        self.investments = investments
        self.tds = tds
        self.regime = regime
        self.standard_deduction = 50000
        
        self.new_tax_slabs = [
            (300000, 0.00),
            (600000, 0.05),
            (900000, 0.10),
            (1200000, 0.15),
            (float('inf'), 0.20)
        ]
        
        self.old_tax_slabs = [
            (250000, 0.00),
            (500000, 0.05),
            (1000000, 0.20),
            (float('inf'), 0.30)
        ]
    
    def calculate_tax(self):
        taxable_income = max(self.salary - self.standard_deduction - self.investments, 0)
        tax = 0
        prev_limit = 0
        tax_slabs = self.new_tax_slabs if self.regime == "New" else self.old_tax_slabs
        
        tax_breakdown = []
        for limit, rate in tax_slabs:
            if taxable_income > prev_limit:
                taxable_amount = min(taxable_income, limit) - prev_limit
                tax_amount = taxable_amount * rate
                tax += tax_amount
                tax_breakdown.append([f"{prev_limit} - {limit}", f"{rate*100}%", f"₹{taxable_amount:,.2f}", f"₹{tax_amount:,.2f}"])
                prev_limit = limit
            else:
                break
        
        tax -= self.tds  # Adjust for TDS paid
        tax = max(tax, 0)  # Ensure tax is not negative
        return tax, tax_breakdown


def main():
    st.title("🇮🇳 India Tax Calculator (2025)")
    
    salary = st.number_input("Enter your annual salary (CTC):", min_value=0.0, step=10000.0, format="%.2f")
    investments = st.number_input("Enter total eligible investments (80C, etc.):", min_value=0.0, step=10000.0, format="%.2f")
    tds = st.number_input("Enter TDS deducted:", min_value=0.0, step=1000.0, format="%.2f")
    regime = st.radio("Choose a tax regime:", ["New", "Old"])
    
    if st.button("Calculate Tax"):
        tax, breakdown = IndiaTaxCalculator(salary, investments, tds, regime).calculate_tax()
        
        st.subheader(f"Total Tax under {regime} Regime: ₹{tax:,.2f}")
        
        st.write("### Tax Calculation Breakdown")
        df = pd.DataFrame(breakdown, columns=["Income Slab", "Rate", "Taxable Amount", "Tax Paid"])
        st.table(df)
    
    if st.button("Compare Tax Regimes"):
        new_tax, _ = IndiaTaxCalculator(salary, investments, tds, "New").calculate_tax()
        old_tax, _ = IndiaTaxCalculator(salary, investments, tds, "Old").calculate_tax()
        
        st.subheader("Tax Comparison")
        st.write(f"New Regime Tax: ₹{new_tax:,.2f}")
        st.write(f"Old Regime Tax: ₹{old_tax:,.2f}")
        st.write(f"Difference: ₹{abs(new_tax - old_tax):,.2f}")
        
        st.bar_chart({"New Regime": new_tax, "Old Regime": old_tax})

if __name__ == "__main__":
    main()
